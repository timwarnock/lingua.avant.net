/*
 * rosary-player.mjs
 * English-only Rosary player on the landing page.
 * 7 rows of indicator dots (simple linear tracking).
 * 3-button controls (prev / play-pause / next) above viewer.
 * Auto mode: play full current then auto-advance.
 * Reuses prayer.mjs view (embedded, text+phonetic) for prayers and mysteries.
 * Mysteries use dedicated JSONs under english/mysteries/.
 * Direct sequence, manual nav or auto.
 */

const GOLD = '#d4af37'; // golden yellow for done (unused in js, for reference)

// Build flat steps list. Mysteries resolved at runtime via active set.
function buildSteps() {
  const steps = [];

  // Row 0: Intro (8 steps)
  steps.push({ row: 0, kind: 'prayer', prayerId: 'sign-of-the-cross', label: 'Sign of the Cross' });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'apostles-creed', label: "Apostles' Creed" });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'our-father', label: 'Our Father' });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'hail-mary', label: 'Hail Mary' });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'hail-mary', label: 'Hail Mary' });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'hail-mary', label: 'Hail Mary' });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'glory-be', label: 'Glory Be' });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'fatima-prayer', label: 'Fatima Prayer' });

  // Rows 1-5: 5 decades, 14 each
  for (let d = 0; d < 5; d++) {
    steps.push({ row: d + 1, kind: 'mystery', decade: d });
    steps.push({ row: d + 1, kind: 'prayer', prayerId: 'our-father', label: 'Our Father' });
    for (let h = 0; h < 10; h++) {
      steps.push({ row: d + 1, kind: 'prayer', prayerId: 'hail-mary', label: 'Hail Mary' });
    }
    steps.push({ row: d + 1, kind: 'prayer', prayerId: 'glory-be', label: 'Glory Be' });
    steps.push({ row: d + 1, kind: 'prayer', prayerId: 'fatima-prayer', label: 'Fatima Prayer' });
  }

  // Row 6: Conclusion (2)
  steps.push({ row: 6, kind: 'prayer', prayerId: 'hail-holy-queen', label: 'Hail, Holy Queen' });
  steps.push({ row: 6, kind: 'prayer', prayerId: 'rosary-prayer', label: 'Rosary Prayer', specialJson: 'hail-holy-queen/rosary-prayer.json' });

  return steps;
}

let steps = buildSteps();
let current = 0;
let progress = 0; // progress up to (and including) current position (0-based)
let autoPlaying = false;
let autoTimeout = null;
let viewerApp = null;
let activeSet = 'joyful';

// Mystery helpers (reuse page data if present)
function getRosaryData() {
  const el = document.getElementById('rosary-mysteries');
  if (el && el.textContent && el.textContent.trim()) {
    try {
      const parsed = JSON.parse(el.textContent);
      return {
        titles: { joyful: 'Joyful Mysteries', sorrowful: 'Sorrowful Mysteries', glorious: 'Glorious Mysteries', luminous: 'Luminous Mysteries', ...(parsed.titles || {}) },
        mysteries: {
          joyful: ["The First Joyful Mystery, the Annunciation", "The Second Joyful Mystery, the Visitation", "The Third Joyful Mystery, the Nativity", "The Fourth Joyful Mystery, the Presentation", "The Fifth Joyful Mystery, the Finding of Jesus in the Temple"],
          sorrowful: ["The First Sorrowful Mystery, the Agony in the Garden", "The Second Sorrowful Mystery, the Scourging at the Pillar", "The Third Sorrowful Mystery, the Crowning with Thorns", "The Fourth Sorrowful Mystery, the Carrying of the Cross", "The Fifth Sorrowful Mystery, the Crucifixion"],
          glorious: ["The First Glorious Mystery, the Resurrection", "The Second Glorious Mystery, the Ascension", "The Third Glorious Mystery, the Descent of the Holy Spirit", "The Fourth Glorious Mystery, the Assumption", "The Fifth Glorious Mystery, the Coronation of Mary"],
          luminous: ["The First Luminous Mystery, the Baptism of Jesus", "The Second Luminous Mystery, the Wedding at Cana", "The Third Luminous Mystery, the Proclamation of the Kingdom", "The Fourth Luminous Mystery, the Transfiguration", "The Fifth Luminous Mystery, the Institution of the Eucharist"],
          ...(parsed.mysteries || {})
        }
      };
    } catch (e) {}
  }
  // fallback
  return {
    titles: { joyful: 'Joyful Mysteries', sorrowful: 'Sorrowful Mysteries', glorious: 'Glorious Mysteries', luminous: 'Luminous Mysteries' },
    mysteries: {
      joyful: ["The First Joyful Mystery, the Annunciation", "The Second Joyful Mystery, the Visitation", "The Third Joyful Mystery, the Nativity", "The Fourth Joyful Mystery, the Presentation", "The Fifth Joyful Mystery, the Finding of Jesus in the Temple"],
      sorrowful: ["The First Sorrowful Mystery, the Agony in the Garden", "The Second Sorrowful Mystery, the Scourging at the Pillar", "The Third Sorrowful Mystery, the Crowning with Thorns", "The Fourth Sorrowful Mystery, the Carrying of the Cross", "The Fifth Sorrowful Mystery, the Crucifixion"],
      glorious: ["The First Glorious Mystery, the Resurrection", "The Second Glorious Mystery, the Ascension", "The Third Glorious Mystery, the Descent of the Holy Spirit", "The Fourth Glorious Mystery, the Assumption", "The Fifth Glorious Mystery, the Coronation of Mary"],
      luminous: ["The First Luminous Mystery, the Baptism of Jesus", "The Second Luminous Mystery, the Wedding at Cana", "The Third Luminous Mystery, the Proclamation of the Kingdom", "The Fourth Luminous Mystery, the Transfiguration", "The Fifth Luminous Mystery, the Institution of the Eucharist"]
    }
  };
}

function getActiveSet() {
  const activeEl = document.querySelector('.mystery-set.active');
  return (activeEl && activeEl.dataset.set) || 'joyful';
}

function getMysteryLabel(set, decade) {
  const data = getRosaryData();
  const names = data.mysteries[set] || data.mysteries.joyful;
  return names[decade] || `Mystery ${decade + 1}`;
}

function getMysteryJson(set, decade) {
  const prefix = set; // joyful, sorrowful etc
  return `mysteries/${prefix}${decade + 1}.json`;
}

// Get jsonPath and display label for a flat step index
function getStepInfo(idx) {
  const s = steps[idx];
  if (!s) return { label: '', jsonPath: null, kind: 'prayer' };

  if (s.kind === 'mystery') {
    const set = getActiveSet();
    return {
      label: getMysteryLabel(set, s.decade),
      jsonPath: getMysteryJson(set, s.decade),
      kind: 'mystery',
      mysteryId: `${set}${s.decade + 1}`
    };
  } else if (s.specialJson) {
    return { label: s.label, jsonPath: s.specialJson, kind: 'prayer' };
  } else {
    const dir = s.prayerId;
    return { label: s.label, jsonPath: `${dir}/${dir}.json`, kind: 'prayer' };
  }
}

function getTotal() {
  return steps.length;
}

// Render the 7 rows of dots into container
function renderIndicators(container) {
  container.innerHTML = '';

  // Group steps by row (7 rows of dots, no labels)
  const rows = [];
  for (let r = 0; r < 7; r++) rows[r] = [];
  steps.forEach((s, i) => {
    rows[s.row].push({ idx: i, step: s });
  });

  rows.forEach((rowSteps) => {
    const rowEl = document.createElement('div');
    rowEl.className = 'rosary-row';

    const dotsWrap = document.createElement('div');
    dotsWrap.className = 'rosary-dots';

    rowSteps.forEach(({ idx }) => {
      const dot = document.createElement('button');
      dot.className = 'rosary-dot';
      dot.type = 'button';
      dot.title = getStepInfo(idx).label;
      dot.dataset.idx = idx;

      if (idx <= progress) dot.classList.add('done');
      if (idx === current) dot.classList.add('current');

      dot.addEventListener('click', () => {
        jumpTo(idx);
      });

      dotsWrap.appendChild(dot);
    });

    rowEl.appendChild(dotsWrap);
    container.appendChild(rowEl);
  });
}

function updateIndicators(container) {
  const dots = container.querySelectorAll('.rosary-dot');
  dots.forEach(dot => {
    const idx = parseInt(dot.dataset.idx, 10);
    dot.classList.toggle('done', idx <= progress);
    dot.classList.toggle('current', idx === current);
  });
}

function jumpTo(idx) {
  if (idx < 0 || idx >= getTotal()) return;
  stopAuto();
  current = idx;
  progress = current;
  updateIndicators(document.getElementById('rosary-indicators'));
  loadCurrentViewer();
}

// Load the viewer for current step using prayer view (embedded)
function loadCurrentViewer() {
  const viewer = document.getElementById('rosary-viewer');
  if (!viewer) return;

  viewer.innerHTML = '';
  const info = getStepInfo(current);

  // Create a container for the prayer view
  const v = document.createElement('div');
  v.className = 'rosary-prayer-view';
  viewer.appendChild(v);

  // Use the exposed createPrayerApp (embedded: no internal header)
  const create = window.createPrayerApp || (window.createApp); // fallback if any
  if (typeof create === 'function' && info.jsonPath) {
    try {
      create(v, { jsonPath: info.jsonPath, embedded: true });
    } catch (e) {
      v.innerHTML = `<em>Unable to load view for ${info.label}.</em>`;
    }
  } else {
    v.innerHTML = `<em>Unable to load ${info.label}.</em>`;
  }

  // When autoplay is active, any manual play click (passage/segment) in the viewer
  // must stop/pause autoplay. Resuming auto always restarts current from start.
  v.addEventListener('click', (e) => {
    const el = e.target.closest('.dual-play, .dual-seg, .play-btn');
    if (el && autoPlaying) {
      stopAuto();
    }
  }, true);
}

// Also stop autoplay full audio if a manual play starts inside the viewer
// (defensive: prayer's internal play() will run after our capture)
if (typeof window !== 'undefined') {
  window.stopRosaryAuto = stopAuto;
  // flag for prayer side if needed
  window.rosaryAutoActive = () => autoPlaying;
}

// Setup independent full audio for a step (for auto and main play)
let currentFullAudio = null;

function playFullForCurrent(onEnded) {
  stopFullAudio();

  const info = getStepInfo(current);
  if (!info.jsonPath) return;

  // Compute the audio file url same way as player does: base + id + .mp3
  // For mysteries: mysteries/joyful1.mp3
  // For normal: e.g. hail-mary/hail-mary.mp3
  // For special rosary-prayer: hail-holy-queen/rosary-prayer.mp3
  let base = '';
  let audioId = '';
  if (info.kind === 'mystery') {
    audioId = info.mysteryId || info.jsonPath.split('/').pop().replace('.json','');
    base = `mysteries/`;
  } else if (info.jsonPath.includes('/rosary-prayer.json')) {
    audioId = 'rosary-prayer';
    base = `hail-holy-queen/`;
  } else {
    const id = info.jsonPath.split('/')[0];
    audioId = id;
    base = `${id}/`;
  }

  const audioUrl = `${base}${audioId}.mp3`;

  currentFullAudio = new Audio(audioUrl);
  currentFullAudio.preload = 'auto';

  currentFullAudio.addEventListener('ended', () => {
    if (onEnded) onEnded();
  }, { once: true });

  currentFullAudio.play().catch(() => {});
}

function stopFullAudio() {
  if (currentFullAudio) {
    currentFullAudio.pause();
    currentFullAudio.currentTime = 0;
    currentFullAudio = null;
  }
  if (autoTimeout) {
    clearTimeout(autoTimeout);
    autoTimeout = null;
  }
}

function updatePlayBtn(btn) {
  if (!btn) return;
  btn.textContent = autoPlaying ? '⏸' : '▶';
  btn.title = autoPlaying ? 'Pause auto' : 'Auto play from here';
}

function startAuto() {
  if (autoPlaying) return;
  autoPlaying = true;
  const playBtn = document.getElementById('rosary-play');
  updatePlayBtn(playBtn);
  function continueAuto() {
    if (!autoPlaying) return;
    if (current + 1 < getTotal()) {
      current++;
      progress = current;
      const ind = document.getElementById('rosary-indicators');
      updateIndicators(ind);
      loadCurrentViewer();
      autoTimeout = setTimeout(() => {
        if (autoPlaying) playFullForCurrent(continueAuto);
      }, 350);
    } else {
      stopAuto();
    }
  }
  playFullForCurrent(continueAuto);
}

function stopAuto() {
  autoPlaying = false;
  stopFullAudio();
  const playBtn = document.getElementById('rosary-play');
  updatePlayBtn(playBtn);
}

function advance() {
  if (current + 1 < getTotal()) {
    jumpTo(current + 1);
  }
}

function setupControls() {
  const prev = document.getElementById('rosary-prev');
  const play = document.getElementById('rosary-play');
  const next = document.getElementById('rosary-next');

  if (prev) prev.addEventListener('click', () => {
    stopAuto();
    if (current > 0) jumpTo(current - 1);
  });

  if (next) next.addEventListener('click', () => {
    stopAuto();
    advance();
  });

  if (play) {
    play.addEventListener('click', () => {
      if (autoPlaying) {
        stopAuto();
      } else {
        startAuto();
      }
    });
    updatePlayBtn(play);
  }
}

function setupChooserSync(indicatorsContainer) {
  const chooser = document.querySelector('.mystery-chooser');
  if (!chooser) return;

  // Update on set click (after rosary.mjs handled its activate)
  chooser.querySelectorAll('.mystery-set').forEach(el => {
    el.addEventListener('click', () => {
      // let rosary.mjs finish
      setTimeout(() => {
        activeSet = getActiveSet();
        const ind = document.getElementById('rosary-indicators');
        if (ind) {
          renderIndicators(ind);  // refresh dots (titles for mysteries will be current set)
          updateIndicators(ind);
        }
        const curInfo = getStepInfo(current);
        if (curInfo.kind === 'mystery') {
          loadCurrentViewer();
        }
      }, 10);
    });
  });
}

function init() {
  const indContainer = document.getElementById('rosary-indicators');
  const viewer = document.getElementById('rosary-viewer');
  if (!indContainer || !viewer) return;

  steps = buildSteps();
  current = 0;
  progress = 0;
  activeSet = getActiveSet();

  renderIndicators(indContainer);
  setupControls();
  setupChooserSync(indContainer);
  loadCurrentViewer();

  // Initial sync with current mystery active
  setTimeout(() => {
    const ind = document.getElementById('rosary-indicators');
    if (ind) updateIndicators(ind);
  }, 50);

  // Keyboard support (simple)
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      const p = document.getElementById('rosary-prev');
      if (p) p.click();
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      const n = document.getElementById('rosary-next');
      if (n) n.click();
    } else if (e.key.toLowerCase() === ' ' || e.key === 'p') {
      e.preventDefault();
      const pl = document.getElementById('rosary-play');
      if (pl) pl.click();
    }
  });
}

// Auto init
if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
}

export { init };