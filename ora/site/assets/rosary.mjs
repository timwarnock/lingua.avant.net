/*
 * rosary.mjs
 * Shared module for Rosary landing pages across languages.
 * - Computes recommended mystery set based on weekday + liturgical rules
 *   (Sorrowful daily during Lent; Joyful on Advent/Christmas Sundays; etc.)
 * - Auto-initializes .mystery-chooser UI (pills + dynamic decade titles)
 *
 * Each language index.md that uses the chooser provides:
 *   <script type="application/json" id="rosary-mysteries"> { titles, mysteries } </script>
 * If absent, English defaults are used as fallback.
 */

function getEaster(year) {
  // Anonymous Gregorian algorithm (Meeus/Jones/Butcher)
  const a = year % 19;
  const b = Math.floor(year / 100);
  const c = year % 100;
  const d = Math.floor(b / 4);
  const e = b % 4;
  const f = Math.floor((b + 8) / 25);
  const g = Math.floor((b - f + 1) / 3);
  const h = (19 * a + b - d - g + 15) % 30;
  const i = Math.floor(c / 4);
  const k = c % 4;
  const l = (32 + 2 * e + 2 * i - h - k) % 7;
  const m = Math.floor((a + 11 * h + 22 * l) / 451);
  const month = Math.floor((h + l - 7 * m + 114) / 31); // 3 or 4
  const day = ((h + l - 7 * m + 114) % 31) + 1;
  return new Date(year, month - 1, day);
}

function getFirstSundayOfAdvent(year) {
  // Walk backwards from Dec 24 to find the 4th Sunday before Christmas (first of Advent)
  const christmas = new Date(year, 11, 25);
  let d = new Date(christmas.getTime());
  d.setDate(d.getDate() - 1);
  let count = 0;
  while (count < 4) {
    if (d.getDay() === 0) {
      count++;
      if (count === 4) return new Date(d.getTime());
    }
    d.setDate(d.getDate() - 1);
  }
  return new Date(d.getTime());
}

function getSundayAfter(d0) {
  const d = new Date(d0.getTime());
  const dow = d.getDay();
  const add = dow === 0 ? 7 : (7 - dow);
  d.setDate(d.getDate() + add);
  return d;
}

function toDateOnly(d) {
  // Normalize to a clean date object (noon local) for reliable comparisons
  if (!(d instanceof Date)) d = new Date(d);
  return new Date(d.getFullYear(), d.getMonth(), d.getDate(), 12, 0, 0, 0);
}

function isInAdvent(date) {
  const d = toDateOnly(date);
  const y = d.getFullYear();
  const start = toDateOnly(getFirstSundayOfAdvent(y));
  const end = new Date(y, 11, 24, 12, 0, 0, 0);
  return d >= start && d <= end;
}

function isInChristmasSeason(date) {
  const d = toDateOnly(date);
  const y = d.getFullYear();
  const mo = d.getMonth();
  const da = d.getDate();
  if (mo === 11 && da >= 25) {
    const start = new Date(y, 11, 25, 12, 0, 0, 0);
    const end = getSundayAfter(new Date(y + 1, 0, 6));
    return d >= start && d <= toDateOnly(end);
  }
  if (mo < 2) {
    const py = y - 1;
    const start = new Date(py, 11, 25, 12, 0, 0, 0);
    const end = getSundayAfter(new Date(y, 0, 6));
    return d >= start && d <= toDateOnly(end);
  }
  return false;
}

function isDuringLent(date) {
  const d = toDateOnly(date);
  const year = d.getFullYear();
  const easter = getEaster(year);
  const ashWed = toDateOnly(new Date(easter.getFullYear(), easter.getMonth(), easter.getDate() - 46));
  const holySat = toDateOnly(new Date(easter.getFullYear(), easter.getMonth(), easter.getDate() - 1));
  return d >= ashWed && d <= holySat;
}

/**
 * Return the recommended mystery set for the given date.
 *
 * Rules:
 * - During Lent (Ash Wednesday through Holy Saturday): Sorrowful Mysteries daily.
 * - Base weekly cycle outside Lent:
 *     Joyful on Mon/Sat
 *     Sorrowful on Tue/Fri
 *     Glorious on Wed + (most) Sun
 *     Luminous on Thu
 * - Additional Sunday overrides (outside Lent):
 *     Advent Sundays and Christmas season Sundays → Joyful
 *     Other Sundays (Eastertide, Ordinary Time, etc.) → Glorious
 */
export function getRecommendedMysterySet(date = new Date()) {
  // Normalize input to a clean "civil date" (local noon) so that:
  // - new Date() works (browser "today")
  // - explicit Date objects work
  // - "YYYY-MM-DD" strings are interpreted as that local calendar date (not UTC)
  let base;
  if (date instanceof Date) {
    base = date;
  } else if (typeof date === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(date)) {
    const [y, m, da] = date.split('-').map(Number);
    base = new Date(y, m - 1, da);
  } else {
    base = new Date(date);
  }
  const d = new Date(base.getFullYear(), base.getMonth(), base.getDate(), 12, 0, 0, 0);

  // Lent takes precedence: Sorrowful every day during the season
  if (isDuringLent(d)) {
    return 'sorrowful';
  }

  const day = d.getDay(); // 0=Sun ... 6=Sat

  let set;
  switch (day) {
    case 0: set = 'glorious'; break;   // Sunday (may be overridden below)
    case 1:
    case 6: set = 'joyful'; break;     // Mon, Sat
    case 2:
    case 5: set = 'sorrowful'; break;  // Tue, Fri
    case 3: set = 'glorious'; break;   // Wed
    case 4: set = 'luminous'; break;   // Thu
    default: set = 'glorious';
  }

  if (day === 0) {
    if (isInAdvent(d) || isInChristmasSeason(d)) {
      set = 'joyful';
    } else {
      set = 'glorious';
    }
  }

  return set;
}

const DEFAULT_DATA = {
  titles: {
    joyful: "Joyful Mysteries",
    sorrowful: "Sorrowful Mysteries",
    glorious: "Glorious Mysteries",
    luminous: "Luminous Mysteries"
  },
  mysteries: {
    joyful: [
      "The First Joyful Mystery, the Annunciation",
      "The Second Joyful Mystery, the Visitation",
      "The Third Joyful Mystery, the Nativity",
      "The Fourth Joyful Mystery, the Presentation",
      "The Fifth Joyful Mystery, the Finding of Jesus in the Temple"
    ],
    sorrowful: [
      "The First Sorrowful Mystery, the Agony in the Garden",
      "The Second Sorrowful Mystery, the Scourging at the Pillar",
      "The Third Sorrowful Mystery, the Crowning with Thorns",
      "The Fourth Sorrowful Mystery, the Carrying of the Cross",
      "The Fifth Sorrowful Mystery, the Crucifixion"
    ],
    glorious: [
      "The First Glorious Mystery, the Resurrection",
      "The Second Glorious Mystery, the Ascension",
      "The Third Glorious Mystery, the Descent of the Holy Spirit",
      "The Fourth Glorious Mystery, the Assumption",
      "The Fifth Glorious Mystery, the Coronation of Mary"
    ],
    luminous: [
      "The First Luminous Mystery, the Baptism of Jesus",
      "The Second Luminous Mystery, the Wedding at Cana",
      "The Third Luminous Mystery, the Proclamation of the Kingdom",
      "The Fourth Luminous Mystery, the Transfiguration",
      "The Fifth Luminous Mystery, the Institution of the Eucharist"
    ]
  }
};

function getRosaryData() {
  const el = document.getElementById('rosary-mysteries');
  if (el && el.textContent && el.textContent.trim()) {
    try {
      const parsed = JSON.parse(el.textContent);
      // shallow merge with defaults so partial data still works
      return {
        titles: { ...DEFAULT_DATA.titles, ...(parsed.titles || {}) },
        mysteries: { ...DEFAULT_DATA.mysteries, ...(parsed.mysteries || {}) }
      };
    } catch (err) {
      console.warn('[rosary] invalid #rosary-mysteries JSON, using defaults', err);
    }
  }
  return DEFAULT_DATA;
}

function activate(set, data) {
  document.querySelectorAll('.mystery-set').forEach(el => {
    el.classList.toggle('active', el.dataset.set === set);
  });

  const titleEl = document.querySelector('.mystery-set-title');
  if (titleEl) {
    titleEl.textContent = (data.titles && data.titles[set]) || data.titles.joyful;
  }

  const names = (data.mysteries && data.mysteries[set]) || data.mysteries.joyful;
  document.querySelectorAll('.decade-label').forEach((el, i) => {
    if (names[i]) el.textContent = names[i];
  });
}

function init() {
  const chooser = document.querySelector('.mystery-chooser');
  if (!chooser) return;

  const data = getRosaryData();
  const recommended = getRecommendedMysterySet();

  activate(recommended, data);

  chooser.querySelectorAll('.mystery-set').forEach(el => {
    el.addEventListener('click', () => activate(el.dataset.set, data));
  });
}

// Auto-init when DOM is ready (works whether script is loaded sync or as module)
if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    // DOM already parsed (common when extra_javascript runs at end of body)
    init();
  }
}

// Also expose for manual use or debugging
export { activate, init, DEFAULT_DATA };
