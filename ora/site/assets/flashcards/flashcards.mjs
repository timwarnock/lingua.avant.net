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
  fcstat(`${CURR_FC + 1} of ${FC_SCORE.length} (${FC_SCORE[CURR_FC].toFixed(1)}s avg)`);
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
    if ($('flashcard-okay')) {
      $('flashcard-okay').innerHTML = 'next';
      $('flashcard-okay').classList.add('next-flipped');
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
  if ($('flashcard-okay')) {
    $('flashcard-okay').innerHTML = 'flip';
    $('flashcard-okay').classList.remove('next-flipped');
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
  fcstat('loading');

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

    unpause();
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
  const wrapper = $('flashcard-content-wrapper');
  const close = $('flashcard-close');

  if (skip) skip.onclick = () => showNextFlashcard();
  if (pauseBtn) pauseBtn.onclick = () => pause();
  if (okay) okay.onclick = () => flipNext();
  if (wrapper) wrapper.onclick = () => toggleFlashcard();
  if (close) close.onclick = () => quitDeck();

  // Wire pause menu actions (delegated)
  const pauseModal = $('flashcard-pause-modal');
  if (pauseModal) {
    pauseModal.onclick = (e) => {
      const t = e.target;
      if (t.id === 'flashcard-pause-quit') quitDeck();
      if (t.id === 'flashcard-pause-reset') showResets();
      if (t.id === 'flashcard-pause-reset2') { clearScores(INIT_SCORE); pause(); }
      if (t.id === 'flashcard-pause-reset10') { clearScores(MAX_WAIT); pause(); }
      if (t.id === 'flashcard-pause-resume') unpause();
    };
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
  if ($('flashcard-okay')) {
    $('flashcard-okay').innerHTML = 'flip';
    $('flashcard-okay').classList.remove('next-flipped');
  }
  _closeModal();
}

function pause() {
  const pauseModal = $('flashcard-pause-modal');
  if (!pauseModal) return;

  let paused = `<div id="flashcard-stats">`;
  paused += `<div id="flashcard-pause-quit" class="hand">× quit</div>`;
  paused += getStats();
  paused += `<div id="flashcard-pause-reset" class="hand">reset scores</div>`;
  paused += `<div id="flashcard-pause-reset2" class="hand hidden">- depth first (3 seconds)</div>`;
  paused += `<div id="flashcard-pause-reset10" class="hand hidden">- breadth first (20 seconds)</div>`;
  paused += `<div id="flashcard-pause-resume" class="hand">resume</div>`;
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
  pauseModal.innerHTML = `<div id="flashcard-stats">loading...</div>`;
}

function unpause() {
  const pauseModal = $('flashcard-pause-modal');
  if (pauseModal) {
    pauseModal.style.visibility = 'hidden';
    pauseModal.style.opacity = '0';
  }
}

function getStats() {
  let stats = `${FC_DATA.length} cards, `;
  let avg = 0;
  for (let i = 0; i < FC_DATA.length; i++) {
    avg += FC_SCORE[i] || 0;
  }
  stats += `${(avg / FC_DATA.length).toFixed(2)}s average`;
  return stats;
}

function showResets() {
  const r2 = $('flashcard-pause-reset2');
  const r10 = $('flashcard-pause-reset10');
  if (r2) r2.classList.remove('hidden');
  if (r10) r10.classList.remove('hidden');
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
    stats.innerHTML = `loading ${audioReady} of ${audioCount} <span id="force-start" class="hand">force start</span>`;
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
