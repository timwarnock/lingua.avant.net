/*
 * flashcards.mjs
 * Faithful port of the original flashcards.js behavior for Zensical.
 * Core mechanics unchanged: latency-based scoring, EPSILON, prompt/answer audio,
 * pause modal with stats + resets, etc.
 */

const BASE = new URL('.', import.meta.url).href.replace(/\/$/, '');

// GLOBALS (kept similar to original for fidelity)
let MAX_WAIT = 20;
let INIT_SCORE = 3;
let EPSILON = 0.3;

let FC_DATA = [];
let FC_AUDIO = [];
let FC_AUDIO_PROMPT = [];
let CURR_FC = 0;
let HOW_MANY = 10;
let HOW_MANY_E = Math.floor(HOW_MANY * EPSILON);
HOW_MANY = HOW_MANY - HOW_MANY_E;

let NEXT_UP = [];
let FC_HIST = [];
let FC_STATUS = 'front';
let FIRST_FLIP = true;

let START_TS = 0;
let FC_SCORE = [];
let FC_NAME = '';

let templates = {
  modal: '',
  card: '',
  pause: ''
};

let currentOverrides = {};

// Helper
function $(id) {
  return document.getElementById(id);
}

function startwatch() {
  START_TS = new Date().getTime();
}

function stopwatch() {
  return (new Date().getTime() - START_TS) / 1000;
}

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

async function loadTemplates() {
  const [modal, card, pause] = await Promise.all([
    fetch(`${BASE}/templates/modal.html`).then(r => r.text()),
    fetch(`${BASE}/templates/card.html`).then(r => r.text()),
    fetch(`${BASE}/templates/pause.html`).then(r => r.text())
  ]);
  templates.modal = modal;
  templates.card = card;
  templates.pause = pause;
}

async function loadOverrides(deck) {
  const [lang] = (deck || '').split('/');
  if (!lang || lang === 'en') return {};
  try {
    const url = `${BASE}/languages/${lang}/lang.json`;
    const res = await fetch(url);
    if (res.ok) {
      const data = await res.json();
      return data || {};
    }
  } catch (e) {}
  return {};
}

function label(key, enDefault) {
  if (currentOverrides && key in currentOverrides) {
    return currentOverrides[key];
  }
  return enDefault;
}

function initScores(fcname) {
  FC_NAME = fcname;
  FC_SCORE = localStorage.getObj ? localStorage.getObj(fcname) : null;
  if (!(FC_SCORE && FC_SCORE.length === FC_DATA.length)) {
    clearScores();
  }
}

function clearScores(base_score) {
  if (typeof base_score === 'undefined') base_score = INIT_SCORE;
  NEXT_UP = [];
  FC_SCORE = Array(FC_DATA.length).fill(base_score);
}

function getScore(index) {
  return FC_SCORE[index];
}

function setScore(index, score) {
  FC_SCORE[index] = score;
  if (localStorage.setObj) localStorage.setObj(FC_NAME, FC_SCORE);
}

function _currFlashcard() {
  return FC_DATA[CURR_FC];
}

function _nextFlashcard() {
  let cand = NEXT_UP.shift();
  if (cand == null) {
    const score_index = reverse_scores_index();
    const how_many = HOW_MANY < score_index.length ? HOW_MANY : score_index.length;
    NEXT_UP = score_index.slice(0, how_many);
    const remaining = score_index.slice(how_many);
    if (remaining.length > 0) {
      shuffle(remaining);
      NEXT_UP = NEXT_UP.concat(remaining.slice(0, HOW_MANY_E));
    }
    shuffle(NEXT_UP);
    cand = NEXT_UP.shift();
  }
  CURR_FC = cand;
  return _currFlashcard();
}

function reverse_scores_index() {
  let toSort = FC_SCORE.slice().map((s, i) => [s, i]);
  toSort.sort((a, b) => b[0] - a[0]);
  return toSort.map(x => x[1]);
}

function _setFlashcard() {
  const fc = _currFlashcard();
  fcstat(`${CURR_FC + 1}/${FC_SCORE.length} (${FC_SCORE[CURR_FC].toFixed(1)}s)`);
  const fcf = `<div class="flashcard-prompt">${fc.key}</div>`;
  $('flashcard-front').innerHTML = fcf;
  let fcb = `<div class="flashcard-full-answer">${fc.answer}</div>`;
  fcb += `<div class="flashcard-full-key">${fc.key}</div>`;
  fcb += `<div class="flashcard-full-alt">${fc.alt || ''}</div>`;
  $('flashcard-back').innerHTML = fcb;
}

function _unsetFlashcard() {
  if ($('flashcard-front')) $('flashcard-front').innerHTML = '';
  if ($('flashcard-back')) $('flashcard-back').innerHTML = '';
}

function showFrontFlashcard() {
  FC_STATUS = 'front';
  const flashcard = $('flashcard');
  flashcard.classList.remove('back');
  flashcard.classList.add('front');
  const fcf = $('flashcard-front');
  const fcb = $('flashcard-back');
  if (fcf && fcb) {
    fcf.parentNode.insertBefore(fcf, fcb);
    fcf.style.visibility = 'visible';
    fcb.style.visibility = 'hidden';
    fcf.style.opacity = '1';
    fcb.style.opacity = '0';
  }
  _playAudioPrompt();
}

function showBackFlashcard() {
  FC_STATUS = 'back';
  if (FIRST_FLIP) {
    startwatch();
    FIRST_FLIP = false;
    const okay = $('flashcard-okay');
    if (okay) {
      const en = 'next';
      okay.innerHTML = label('next', en);
      okay.title = en;
      okay.classList.add('next-flipped');
    }
  }
  const flashcard = $('flashcard');
  flashcard.classList.remove('front');
  flashcard.classList.add('back');
  const fcf = $('flashcard-front');
  const fcb = $('flashcard-back');
  if (fcf && fcb) {
    fcf.parentNode.insertBefore(fcb, fcf);
    fcf.style.visibility = 'hidden';
    fcb.style.visibility = 'visible';
    fcf.style.opacity = '0';
    fcb.style.opacity = '1';
  }
  _playAudio();
}

function showNextFlashcard() {
  if (!FIRST_FLIP) {
    let wait_s = stopwatch();
    wait_s = wait_s < MAX_WAIT ? wait_s : MAX_WAIT;
    const oldscore = getScore(CURR_FC);
    setScore(CURR_FC, (oldscore * 3 + wait_s) / 4);
  }
  FIRST_FLIP = true;
  const okay = $('flashcard-okay');
  if (okay) {
    const en = 'flip';
    okay.innerHTML = label('flip', en);
    okay.title = en;
    okay.classList.remove('next-flipped');
  }
  _stopAudio();
  _nextFlashcard();
  _setFlashcard();
  showFrontFlashcard();
}

function flipNext() {
  if (FIRST_FLIP) {
    showBackFlashcard();
  } else {
    showNextFlashcard();
  }
}

function toggleFlashcard() {
  if (FC_STATUS === 'front') {
    showBackFlashcard();
  } else {
    showFrontFlashcard();
  }
}

function fcstat(msg) {
  const el = $('fc-status');
  if (el) el.innerHTML = msg;
}

async function loadDeck(deck) {
  // deck e.g. 'zh/tones'
  const [lang, name] = deck.split('/');
  const jsonUrl = `${BASE}/languages/${lang}/decks/${name}.json`;

  _showModal();
  pauseLoad();
  fcstat(label('loading', 'loading'));

  try {
    const res = await fetch(jsonUrl);
    if (!res.ok) throw new Error('Deck not found');
    FC_DATA = await res.json();

    initScores(deck);

    // Prepare audio arrays
    FC_AUDIO = new Array(FC_DATA.length).fill(false);
    FC_AUDIO_PROMPT = new Array(FC_DATA.length).fill(false);

    CURR_FC = 0;
    FIRST_FLIP = true;
    NEXT_UP = [];

    _nextFlashcard();
    _setFlashcard();
    showFrontFlashcard();

    // Preload audio for this deck (best effort)
    preloadDeckAudio(lang, name);

    if (audioCount === 0) {
      unpause();
    }
  } catch (e) {
    console.error(e);
    quitDeck();
  }
}

function _showModal() {
  const container = document.createElement('div');
  container.id = 'flashcards-root';
  container.innerHTML = templates.modal;

  // Inject card
  const flashcardEl = container.querySelector('#flashcard');
  if (flashcardEl) {
    flashcardEl.innerHTML = templates.card;
  }

  // Attach the pause template base
  const pauseContainer = container.querySelector('#flashcard-pause-modal');
  if (pauseContainer) {
    pauseContainer.innerHTML = templates.pause;
  }

  // Remove any previous
  const old = document.getElementById('flashcards-root');
  if (old) old.remove();

  document.body.appendChild(container);

  // Wire buttons now that DOM exists
  wireControls();
}

function wireControls() {
  const skip = $('flashcard-skip');
  const pauseBtn = $('flashcard-pause');
  const okay = $('flashcard-okay');
  const close = $('flashcard-close');
  const card = $('flashcard');

  if (skip) skip.onclick = (e) => { e.stopPropagation(); showNextFlashcard(); };
  if (pauseBtn) pauseBtn.onclick = (e) => { e.stopPropagation(); pause(); };
  if (okay) okay.onclick = (e) => { e.stopPropagation(); flipNext(); };
  if (close) close.onclick = (e) => { e.stopPropagation(); quitDeck(); };
  if (card) card.onclick = (e) => {
    if (e.target.closest('.flashcard-buttons-bar') || e.target.closest('#flashcard-close')) {
      return;
    }
    toggleFlashcard();
  };

  // Wire pause menu actions (delegated)
  const pauseModal = $('flashcard-pause-modal');
  if (pauseModal) {
    pauseModal.onclick = (e) => {
      const t = e.target;
      if (t.id === 'flashcard-pause-quit') quitDeck();
      if (t.id === 'flashcard-pause-reset') { clearScores(INIT_SCORE); pause(); }
      if (t.id === 'flashcard-pause-resume') unpause();
      if (t.id === 'kc-x' || t.id === 'kc-esc') quitDeck();
      if (t.id === 'kc-space') unpause();
      if (t.id === 'kc-enter') { unpause(); flipNext(); }
      if (t.id === 'kc-f') { unpause(); toggleFlashcard(); }
      if (t.id === 'kc-s') { unpause(); showNextFlashcard(); }
    };
  }

  applyCardLabels();
}

function applyCardLabels() {
  const skip = $('flashcard-skip');
  if (skip) {
    const en = skip.textContent.trim();
    skip.textContent = label('skip', en);
    skip.title = en;
  }
  const pauseBtn = $('flashcard-pause');
  if (pauseBtn) {
    const en = pauseBtn.textContent.trim();
    pauseBtn.textContent = label('pause', en);
    pauseBtn.title = en;
  }
  const okay = $('flashcard-okay');
  if (okay) {
    const en = okay.textContent.trim();
    okay.textContent = label('flip', en);
    okay.title = en;
  }
  const x = $('flashcard-close');
  if (x && !x.title) {
    x.title = 'Close';
  }
}

function _closeModal() {
  const root = document.getElementById('flashcards-root');
  if (root) root.remove();
}

function quitDeck() {
  unpause();
  _stopAudio();
  _unsetFlashcard();
  const okay = $('flashcard-okay');
  if (okay) {
    const en = 'flip';
    okay.innerHTML = label('flip', en);
    okay.title = en;
    okay.classList.remove('next-flipped');
  }
  _closeModal();
}

function pause() {
  const pauseModal = $('flashcard-pause-modal');
  if (!pauseModal) return;

  const statsText = getStats();
  const enQuit = '× quit';
  const enReset = 'reset scores';
  const enResume = 'resume';
  let paused = `<div id="flashcard-stats">`;
  paused += `<div id="flashcard-pause-quit" class="hand" title="${enQuit}">${label('quit', enQuit)}</div>`;
  paused += `<div class="pause-stats">${statsText}</div>`;
  paused += `<div id="flashcard-pause-reset" class="hand" title="${enReset}">${label('reset_scores', enReset)}</div>`;
  paused += `<div class="pause-info">${label('depth_first', '+ depth-first (3 seconds)')}</div>`;
  paused += `<div class="pause-info">${label('breadth_first', '+ breadth-first (20 seconds)')}</div>`;
  paused += `<div id="flashcard-pause-resume" class="hand" title="${enResume}">${label('resume', enResume)}</div>`;
  paused += `<div class="pause-kbd">${label('kbd_header', 'Keyboard controls:')}<br>`;
  paused += `(<span id="kc-x" class="hand" title="x">x</span> <span id="kc-esc" class="hand" title="esc">esc</span>) ${label('kbd_close_app', 'close the app')}<br>`;
  paused += `(<span id="kc-space" class="hand" title="space">space</span>) ${label('kbd_pause_unpause', 'pause / unpause')}<br>`;
  paused += `(<span id="kc-enter" class="hand" title="enter">enter</span>) ${label('kbd_flip_next', 'flip / next')}<br>`;
  paused += `(<span id="kc-f" class="hand" title="f">f</span>) ${label('kbd_flip', 'flip')}<br>`;
  paused += `(<span id="kc-s" class="hand" title="s">s</span>) ${label('kbd_skip', 'skip')}</div>`;
  paused += `</div>`;

  pauseModal.style.visibility = 'visible';
  pauseModal.style.opacity = '1';
  pauseModal.innerHTML = paused;
}

function pauseLoad() {
  const pauseModal = $('flashcard-pause-modal');
  if (!pauseModal) return;
  pauseModal.style.visibility = 'visible';
  pauseModal.style.opacity = '1';
  pauseModal.innerHTML = `<div id="flashcard-stats">${label('loading', 'loading...')}</div>`;
}

function unpause() {
  const pauseModal = $('flashcard-pause-modal');
  if (pauseModal) {
    pauseModal.style.visibility = 'hidden';
    pauseModal.style.opacity = '0';
  }
}

function getStats() {
  const cards = label('cards', 'cards');
  const average = label('average', 'average');
  let stats = `${FC_DATA.length} ${cards}, `;
  let avg = 0;
  for (let i = 0; i < FC_DATA.length; i++) {
    avg += FC_SCORE[i] || 0;
  }
  stats += `${(avg / FC_DATA.length).toFixed(2)}s ${average}`;
  return stats;
}

let audioCount = 0;
let audioReady = 0;

function preloadDeckAudio(lang, name) {
  // Best-effort preload for current deck
  audioCount = 0;
  audioReady = 0;

  FC_DATA.forEach((item, i) => {
    if (item.audio) {
      FC_AUDIO[i] = new Audio();
      FC_AUDIO[i].addEventListener('canplaythrough', loadedAudio);
      FC_AUDIO[i].src = `${BASE}/languages/${lang}/audio/${item.audio}`;
      audioCount++;
    }
    if (item.audio_prompt) {
      FC_AUDIO_PROMPT[i] = new Audio();
      FC_AUDIO_PROMPT[i].addEventListener('canplaythrough', loadedAudio);
      FC_AUDIO_PROMPT[i].src = `${BASE}/languages/${lang}/audio/${item.audio_prompt}`;
      audioCount++;
    }
  });

  if (audioCount === 0) {
    // no audio, just go
  }
}

function loadedAudio() {
  audioReady++;
  const stats = $('flashcard-stats');
  if (stats) {
    const enForce = 'force start';
    stats.innerHTML = `${label('loading', 'loading')} ${audioReady}/${audioCount} <span id="force-start" class="hand" title="${enForce}">${label('force_start', enForce)}</span>`;
    const force = $('force-start');
    if (force) force.onclick = () => unpause();
  }
  if (audioReady >= audioCount) {
    unpause();
  }
}

function _playAudio() {
  const player = $('flashcard-audio');
  if (!player) return;

  if (FC_AUDIO[CURR_FC]) {
    player.src = FC_AUDIO[CURR_FC].src;
    player.play().catch(() => {});
  } else if (FC_DATA[CURR_FC] && FC_DATA[CURR_FC].audio) {
    const [lang] = 'zh'; // default, improve if needed
    // For now assume current deck context; in real use the lang is known
    console.log('lazy audio not fully resolved in this port');
  }
}

function _playAudioPrompt() {
  const player = $('flashcard-audio');
  if (!player) return;

  if (FC_AUDIO_PROMPT[CURR_FC]) {
    player.src = FC_AUDIO_PROMPT[CURR_FC].src;
    player.play().catch(() => {});
  } else if (FC_DATA[CURR_FC] && FC_DATA[CURR_FC].audio_prompt) {
    console.log('lazy prompt audio');
  }
}

function _stopAudio() {
  const player = $('flashcard-audio');
  if (player) player.pause();
}

// Keyboard (global when active)
document.addEventListener('keydown', (evt) => {
  const root = document.getElementById('flashcards-root');
  if (!root) return;

  if (evt.key === ' ' || evt.key === 'Spacebar') {
    evt.preventDefault();
    const pauseEl = $('flashcard-pause-modal');
    if (pauseEl && pauseEl.style.visibility === 'visible') {
      unpause();
    } else {
      pause();
    }
  }
  if (evt.key === 'Enter') {
    evt.preventDefault();
    const pauseEl = $('flashcard-pause-modal');
    if (pauseEl && pauseEl.style.visibility === 'visible') {
      unpause();
    }
    flipNext();
  }
  if (evt.key.toLowerCase() === 'f') {
    toggleFlashcard();
  }
  if (evt.key.toLowerCase() === 's') {
    showNextFlashcard();
  }
  if (evt.key.toLowerCase() === 'x') {
    pause();
    quitDeck();
  }
  if (evt.key === 'Escape' || evt.key === 'Esc') {
    evt.preventDefault();
    pause();
    quitDeck();
  }
});

// Touch swipe (simplified)
let xDown = null;
document.addEventListener('touchstart', (evt) => {
  const root = document.getElementById('flashcards-root');
  if (!root) return;
  xDown = evt.touches[0].clientX;
});

document.addEventListener('touchmove', (evt) => {
  const root = document.getElementById('flashcards-root');
  if (!root || !xDown) return;
  const xUp = evt.touches[0].clientX;
  const xDiff = xDown - xUp;
  if (Math.abs(xDiff) > 60) {
    if (xDiff > 0) flipNext();
  }
  xDown = null;
});

// Public API
const Flashcards = {
  async open(deck) {
    // deck e.g. 'zh/tones'
    currentOverrides = await loadOverrides(deck);
    await loadTemplates();

    // Create modal shell
    const root = document.createElement('div');
    root.id = 'flashcards-root';
    document.body.appendChild(root);

    // Load the deck (this will populate)
    await loadDeck(deck);
  }
};

// Expose globally for onclick etc. in markdown
window.Flashcards = Flashcards;

export default Flashcards;
