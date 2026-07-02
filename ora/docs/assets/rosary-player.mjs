/*
 * rosary-player.mjs
 * English-only Rosary player on the landing page.
 * 7 rows of indicator dots (simple linear tracking).
 * 3-button controls (prev / play-pause / next) above viewer.
 * Auto mode: play full current then auto-advance.
 * Reuses prayer.mjs view (embedded; secondary/phonetic optional via hideSecondary) for prayers and mysteries.
 * Mysteries use dedicated JSONs under english/mysteries/.
 * Direct sequence, manual nav or auto.
 */

const GOLD = '#d4af37'; // golden yellow for done (unused in js, for reference)

// Build flat steps list. Mysteries resolved at runtime via active set.
function buildSteps() {
  const steps = [];

  // Row 0: Intro (8 steps)
  steps.push({ row: 0, kind: 'prayer', prayerId: 'sign-of-the-cross' });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'apostles-creed' });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'our-father' });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'hail-mary' });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'hail-mary' });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'hail-mary' });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'glory-be' });
  steps.push({ row: 0, kind: 'prayer', prayerId: 'fatima-prayer' });

  // Rows 1-5: 5 decades, 14 each
  for (let d = 0; d < 5; d++) {
    steps.push({ row: d + 1, kind: 'mystery', decade: d });
    steps.push({ row: d + 1, kind: 'prayer', prayerId: 'our-father' });
    for (let h = 0; h < 10; h++) {
      steps.push({ row: d + 1, kind: 'prayer', prayerId: 'hail-mary' });
    }
    steps.push({ row: d + 1, kind: 'prayer', prayerId: 'glory-be' });
    steps.push({ row: d + 1, kind: 'prayer', prayerId: 'fatima-prayer' });
  }

  // Row 6: Conclusion (2)
  steps.push({ row: 6, kind: 'prayer', prayerId: 'hail-holy-queen' });
  steps.push({ row: 6, kind: 'prayer', prayerId: 'rosary-prayer', specialJson: 'hail-holy-queen/rosary-prayer.json' });

  return steps;
}

let steps = buildSteps();
let current = 0;
let progress = 0; // progress up to (and including) current position (0-based)
let autoPlaying = false;
let autoTimeout = null;
let viewerApp = null;
let activeSet = 'joyful';
let showPhonetic; // default from data-show-phonetic on #rosary-player div (no language hardcode in js)

let titlesCache = {};

function getCurrentDir() {
  let url = window.location.href.split('#')[0].split('?')[0];
  if (!url.endsWith('/')) {
    url = url.substring(0, url.lastIndexOf('/') + 1);
  }
  return url;
}

async function preloadRosaryTitles() {
  const set = getActiveSet();

  // Fixed prayers used in the rosary
  const fixed = ['sign-of-the-cross', 'apostles-creed', 'our-father', 'hail-mary', 'glory-be', 'fatima-prayer', 'hail-holy-queen'];
  const base = getCurrentDir();
  for (const id of fixed) {
    const p = `${id}/${id}.json`;
    if (!titlesCache[p]) {
      try {
        const r = await fetch(new URL(p, base).href);
        const d = await r.json();
        titlesCache[p] = d.title || id;
      } catch (e) {
        titlesCache[p] = id;
      }
    }
  }

  // Special rosary-prayer
  const rp = 'hail-holy-queen/rosary-prayer.json';
  if (!titlesCache[rp]) {
    try {
      const r = await fetch(new URL(rp, base).href);
      const d = await r.json();
      titlesCache[rp] = d.title || 'Rosary Prayer';
    } catch (e) {
      titlesCache[rp] = 'Rosary Prayer';
    }
  }

  // Current set's 5 mysteries
  for (let d = 0; d < 5; d++) {
    const mid = `${set}${d + 1}`;
    const p = `mysteries/${mid}.json`;
    if (!titlesCache[p]) {
      try {
        const r = await fetch(new URL(p, base).href);
        const d = await r.json();
        titlesCache[p] = d.title || `Mystery ${d + 1}`;
      } catch (e) {
        titlesCache[p] = `Mystery ${d + 1}`;
      }
    }
  }
}

function getActiveSet() {
  const activeEl = document.querySelector('.mystery-set.active');
  return (activeEl && activeEl.dataset.set) || 'joyful';
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
    const mid = `${set}${s.decade + 1}`;
    const p = `mysteries/${mid}.json`;
    return {
      label: titlesCache[p] || `Mystery ${s.decade + 1}`,
      jsonPath: p,
      kind: 'mystery',
      mysteryId: mid
    };
  } else if (s.specialJson) {
    const p = s.specialJson;
    return { label: titlesCache[p] || 'Rosary Prayer', jsonPath: p, kind: 'prayer' };
  } else {
    const id = s.prayerId;
    const p = `${id}/${id}.json`;
    const fallback = id.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    return { label: titlesCache[p] || fallback, jsonPath: p, kind: 'prayer' };
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
      const info = getStepInfo(idx);
      dot.title = info.label;
      dot.dataset.idx = idx;

      // Use the step to identify repeats for styling (more reliable than label)
      const stepForClass = steps[idx];
      if (stepForClass && stepForClass.prayerId === 'hail-mary') {
        dot.classList.add('hail-mary');
      }

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

  // Resolve jsonPath relative to current dir to ensure correct path even without trailing /
  const baseDir = getCurrentDir();
  const jsonPath = info.jsonPath ? new URL(info.jsonPath, baseDir).href : null;

  // Use the exposed createPrayerApp (embedded: no internal header)
  const create = window.createPrayerApp || (window.createApp); // fallback if any
  if (typeof create === 'function' && jsonPath) {
    try {
      create(v, { jsonPath: jsonPath, embedded: true, hideSecondary: !showPhonetic });
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

  // Compute the audio file url relative to current dir (robust even without trailing / on page url)
  const baseDir = getCurrentDir();
  let relPath = '';
  if (info.kind === 'mystery') {
    const audioId = info.mysteryId || info.jsonPath.split('/').pop().replace('.json','');
    relPath = `mysteries/${audioId}.mp3`;
  } else if (info.jsonPath.includes('/rosary-prayer.json')) {
    relPath = `hail-holy-queen/rosary-prayer.mp3`;
  } else {
    const id = info.jsonPath.split('/')[0];
    relPath = `${id}/${id}.mp3`;
  }

  const audioUrl = new URL(relPath, baseDir).href;

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
  btn.innerHTML = '';
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  svg.setAttribute('fill', 'currentColor');
  svg.setAttribute('stroke', 'none');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('width', '1em');
  svg.setAttribute('height', '1em');
  if (autoPlaying) {
    // pause: two bars
    svg.innerHTML = '<rect x="6" y="4" width="4" height="16" fill="currentColor" stroke="none"/><rect x="14" y="4" width="4" height="16" fill="currentColor" stroke="none"/>';
  } else {
    // play: triangle (centered, nudged for optical alignment)
    svg.innerHTML = '<path d="M8 5l12 8-12 8V5z" fill="currentColor" stroke="none"/>';
  }
  btn.appendChild(svg);
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
  const phonetic = document.getElementById('rosary-phonetic');
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

  if (phonetic) {
    // use lucide languages icon (same as language landing pages)
    phonetic.innerHTML = '';
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svg.setAttribute('fill', 'none');
    svg.setAttribute('stroke', 'currentColor');
    svg.setAttribute('stroke-linecap', 'round');
    svg.setAttribute('stroke-linejoin', 'round');
    svg.setAttribute('stroke-width', '2');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.style.width = '0.95em';
    svg.style.height = '0.95em';
    svg.setAttribute('class', 'lucide lucide-languages');
    svg.innerHTML = '<path d="m5 8 6 6M4 14l6-6 2-3M2 5h12M7 2h1M22 22l-5-10-5 10M14 18h6"/>';
    phonetic.appendChild(svg);

    phonetic.addEventListener('click', () => {
      showPhonetic = !showPhonetic;
      phonetic.classList.toggle('active', showPhonetic);
      phonetic.title = showPhonetic ? 'Hide phonetic' : 'Show phonetic';
      loadCurrentViewer();
    });
    // initial state from data attr
    phonetic.classList.toggle('active', showPhonetic);
    phonetic.title = showPhonetic ? 'Hide phonetic' : 'Show phonetic';
  }
}

function setupChooserSync(indicatorsContainer) {
  const chooser = document.querySelector('.mystery-chooser');
  if (!chooser) return;

  // Update on set click (after rosary.mjs handled its activate)
  chooser.querySelectorAll('.mystery-set').forEach(el => {
    el.addEventListener('click', async () => {
      // let rosary.mjs finish
      setTimeout(async () => {
        activeSet = getActiveSet();
        await preloadRosaryTitles();
        const ind = document.getElementById('rosary-indicators');
        if (ind) {
          renderIndicators(ind);  // refresh dots with titles from JSONs
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

  const playerEl = document.getElementById('rosary-player');
  showPhonetic = playerEl && playerEl.dataset.showPhonetic === 'true';

  steps = buildSteps();
  current = 0;
  progress = 0;
  activeSet = getActiveSet();

  preloadRosaryTitles().then(() => {
    renderIndicators(indContainer);
    setupControls();
    setupChooserSync(indContainer);
    loadCurrentViewer();

    // Initial sync with current mystery active
    setTimeout(() => {
      const ind = document.getElementById('rosary-indicators');
      if (ind) updateIndicators(ind);
    }, 50);
  });

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