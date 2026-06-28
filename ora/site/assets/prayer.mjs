/*
 * prayer.mjs
 * Simple interactive audio viewer for rosary prayers.
 * - Loads <lang>/<prayer>.json from companion folder
 * - Full play in header
 * - Play button per passage
 * - Main lines use "text" (proper display). Phonetic chunks (using "phonetic") are clickable for playback. "phonetic" may differ from "text" for pronunciation.
 * - Audio filenames derived from JSON id + passage_id / passage_segment_id
 * - One shared audio per container; stops at segment end
 */

function initPrayer(container) {
  const prayer = container.dataset.prayer;
  const jsonRel = container.dataset.json || `${prayer}.json`;

  // Resolve json url relative to current page (works with the hail-mary/ companion folder)
  const jsonUrl = new URL(jsonRel, window.location.href);

  fetch(jsonUrl)
    .then(r => {
      if (!r.ok) throw new Error('Could not load ' + jsonRel);
      return r.json();
    })
    .then(data => {
      render(container, data, jsonUrl);
    })
    .catch(err => {
      console.warn('[prayer]', err);
      container.innerHTML = '<em style="opacity:0.6">Audio view unavailable.</em>';
    });
}

function render(container, data, jsonUrl) {
  const audioDir = jsonUrl.href.substring(0, jsonUrl.href.lastIndexOf('/') + 1);
  const prayerId = data.id || prayer;

  // Derive audio sources from structure (no audio map in JSON)
  const audioMap = {};
  function addAudio(key) {
    if (audioMap[key]) return;
    const a = new Audio();
    if (key === 'full') {
      a.src = audioDir + `${prayerId}.mp3`;
    } else {
      a.src = audioDir + `${prayerId}-${key}.mp3`;
    }
    a.preload = 'auto';
    audioMap[key] = a;
  }

  addAudio('full');

  (data.passages || []).forEach(p => {
    const pid = String(p.passage_id);
    addAudio(pid);
    (p.segments || []).forEach(s => {
      const sid = s.passage_segment_id;
      if (sid) addAudio(sid);
    });
  });

  let activeEl = null;

  function clearActive() {
    if (activeEl) activeEl.classList.remove('playing');
    activeEl = null;
  }

  function setActive(el) {
    clearActive();
    if (el) {
      el.classList.add('playing');
      activeEl = el;
    }
  }

  function playSegment(id) {
    const a = audioMap[id];
    if (!a) {
      console.warn('[prayer] no audio for segment', id);
      return;
    }

    // Stop any other playing audio
    Object.values(audioMap).forEach(aa => {
      if (aa !== a) {
        aa.pause();
        aa.currentTime = 0;
      }
    });

    clearActive();

    // Find matching element for highlight
    const target = container.querySelector(`[data-segment="${id}"]`);
    if (target) setActive(target);

    a.currentTime = 0;
    a.play().catch(() => {
      // may fail if file missing; UI still works
    });
  }

  // Build UI
  container.innerHTML = '';

  // Replace the original page <h1> (so the title uses the exact same styling as # heading)
  const originalH1 = container.previousElementSibling;
  if (originalH1 && originalH1.tagName === 'H1') {
    originalH1.innerHTML = '';
    originalH1.classList.add('prayer-with-player');

    const title = document.createElement('span');
    title.className = 'prayer-title';
    title.textContent = data.title || 'Prayer';

    const fullBtn = document.createElement('button');
    fullBtn.className = 'play-btn';
    fullBtn.textContent = '▶';
    fullBtn.title = 'Play full prayer';
    fullBtn.addEventListener('click', () => playSegment('full'));

    originalH1.appendChild(title);
    originalH1.appendChild(fullBtn);
  } else {
    // Fallback: build a header if no h1 found
    const header = document.createElement('div');
    header.className = 'prayer-header';

    const title = document.createElement('span');
    title.className = 'prayer-title';
    title.textContent = data.title || 'Prayer';

    const fullBtn = document.createElement('button');
    fullBtn.className = 'play-btn';
    fullBtn.textContent = '▶';
    fullBtn.title = 'Play full prayer';
    fullBtn.addEventListener('click', () => playSegment('full'));

    header.appendChild(title);
    header.appendChild(fullBtn);
    container.appendChild(header);
  }

  // Hide any leftover original title if we didn't repurpose it
  // (in case the h1 wasn't immediately before)
  const prevH1 = container.previousElementSibling;
  if (prevH1 && prevH1.tagName === 'H1' && !prevH1.classList.contains('prayer-with-player')) {
    prevH1.style.display = 'none';
  }

  const passagesWrap = document.createElement('div');
  passagesWrap.className = 'prayer-passages';

  (data.passages || []).forEach(p => {
    const pid = String(p.passage_id);
    const passageEl = document.createElement('div');
    passageEl.className = 'prayer-passage';
    passageEl.dataset.passage = pid;

    // Passage line: small play button + assembled real text for the passage
    const line = document.createElement('div');
    line.className = 'prayer-line';

    const pBtn = document.createElement('button');
    pBtn.className = 'play-btn small';
    pBtn.textContent = '▶';
    pBtn.title = `Play passage ${pid}`;
    pBtn.dataset.segment = pid;
    pBtn.addEventListener('click', () => playSegment(pid));

    line.appendChild(pBtn);

    // Assemble passage text from segment texts
    const passageText = (p.segments || []).map(s => s.text || '').join(' ');
    const pText = document.createElement('span');
    pText.className = 'prayer-text';
    pText.textContent = passageText;
    line.appendChild(pText);

    // Clicking the line also plays the passage
    line.addEventListener('click', (e) => {
      if (e.target === pBtn) return;
      playSegment(pid);
    });
    line.style.cursor = 'pointer';

    // List the phonetic segments (clickable)
    const subs = document.createElement('div');
    subs.className = 'prayer-subs';

    (p.segments || []).forEach(s => {
      const chunk = document.createElement('span');
      chunk.className = 'prayer-chunk';
      chunk.textContent = s.phonetic || '';
      const sid = s.passage_segment_id;
      chunk.dataset.segment = sid;
      chunk.addEventListener('click', () => playSegment(sid));
      subs.appendChild(chunk);
    });

    passageEl.appendChild(line);
    passageEl.appendChild(subs);
    passagesWrap.appendChild(passageEl);
  });

  container.appendChild(passagesWrap);

  // Successful render → hide the static fallback content.
  // This is graceful degradation: the fallback is the default in the HTML.
  // Only successful execution of this code hides it.
  document.querySelectorAll('.prayer-fallback').forEach(el => {
    el.style.display = 'none';
  });
}

// Auto-init
function initAll() {
  document.querySelectorAll('.prayer-interactive').forEach(initPrayer);
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll, { once: true });
  } else {
    initAll();
  }
}

export { initPrayer, initAll };
