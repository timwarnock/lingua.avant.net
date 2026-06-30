/*
 * dual-prayer.mjs
 * Top-level multi-lingual rosary home app.
 * One prayer at a time. Two languages side-by-side (full audio + segments on primary, segments on secondary).
 * Clean intuitive UI modeled on the single-lang prayer player.
 * Independent language + text/phonetic mode per side.
 * No instructions needed.
 */

const PRAYERS = [
  { id: 'sign-of-the-cross', label: 'Sign of the Cross' },
  { id: 'apostles-creed', label: "Apostles' Creed" },
  { id: 'our-father', label: 'Our Father' },
  { id: 'hail-mary', label: 'Hail Mary' },
  { id: 'glory-be', label: 'Glory Be' },
  { id: 'fatima-prayer', label: 'Fatima Prayer' },
  { id: 'hail-holy-queen', label: 'Hail Holy Queen' }
];

const LANGS = [
  { id: 'english', label: 'English' },
  { id: 'spanish', label: 'Español' },
  { id: 'french', label: 'Français' },
  { id: 'latin', label: 'Latin' },
  { id: 'polish', label: 'Polski' },
  { id: 'portuguese', label: 'Português' },
  { id: 'vietnamese', label: 'Tiếng Việt' },
  { id: 'greek', label: 'Ἑλληνικά' },
  { id: 'chinese', label: '中文' },
  { id: 'japanese', label: '日本語' }
];

function createApp(container) {
  let state = {
    prayerId: 'hail-mary',
    primaryLang: 'latin',
    primaryMode: 'text',
    secondaryLang: 'english',
    secondaryMode: 'text'
  };

  const audioMap = {};
  let mainPlayBtn = null;
  let activeEl = null;

  function getAudio(lang, key, audioBase, prayerId) {
    const mapKey = `${lang}:${key}`;
    if (audioMap[mapKey]) return audioMap[mapKey];
    const a = new Audio();
    const suffix = key === 'full' ? '' : `-${key}`;
    a.src = `${audioBase}${prayerId}${suffix}.mp3`;
    a.preload = 'auto';
    audioMap[mapKey] = a;
    return a;
  }

  function stopAll() {
    Object.values(audioMap).forEach(a => {
      a.pause();
      a.currentTime = 0;
    });
    clearActive();
    setMainPlaying(false);
  }

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

  function setMainPlaying(playing) {
    if (!mainPlayBtn) return;
    mainPlayBtn.classList.toggle('playing', playing);
    mainPlayBtn.textContent = playing ? '⏸' : '▶';
  }

  function maybeRevertMain() {
    const anyActive = Object.values(audioMap).some(aa => !aa.paused && aa.currentTime > 0);
    if (!anyActive) {
      setMainPlaying(false);
    }
  }

  function addAudio(lang, key, audioBase, prayerId) {
    const mapKey = `${lang}:${key}`;
    if (audioMap[mapKey]) return audioMap[mapKey];
    const a = new Audio();
    const suffix = key === 'full' ? '' : `-${key}`;
    a.src = `${audioBase}${prayerId}${suffix}.mp3`;
    a.preload = 'auto';
    // ANY audio (primary or secondary) affects the main play/pause button
    a.addEventListener('play', () => setMainPlaying(true));
    a.addEventListener('ended', maybeRevertMain);
    a.addEventListener('pause', maybeRevertMain);
    audioMap[mapKey] = a;
    return a;
  }

  // Cache for prayer titles per language (for bilingual menu)
  const titlesCache = {};
  async function loadTitles(lang) {
    if (titlesCache[lang]) return titlesCache[lang];
    titlesCache[lang] = {};
    await Promise.all(PRAYERS.map(async p => {
      try {
        const url = `${lang}/${p.id}/${p.id}.json`;
        const r = await fetch(url);
        if (r.ok) {
          const data = await r.json();
          titlesCache[lang][p.id] = data.title || p.label;
        } else {
          titlesCache[lang][p.id] = p.label;
        }
      } catch (e) {
        titlesCache[lang][p.id] = p.label;
      }
    }));
    return titlesCache[lang];
  }

  function play(lang, key, audioBase, prayerId, targetEl = null) {
    const mapKey = `${lang}:${key}`;
    const a = audioMap[mapKey] || getAudio(lang, key, audioBase, prayerId);

    // Stop other audios (same as original prayer.mjs behavior, adapted for dual)
    Object.values(audioMap).forEach(aa => {
      if (aa !== a) {
        aa.pause();
        aa.currentTime = 0;
      }
    });

    clearActive();
    if (targetEl) setActive(targetEl);

    // ANY audio playing sets the main button to pause (same as prayer.mjs)
    setMainPlaying(true);

    a.currentTime = 0;
    a.play().catch(() => {});
  }

  function render() {
    container.innerHTML = '';
    mainPlayBtn = null;
    activeEl = null;
    // keep audioMap across re-renders for smooth

    // No top-level prayer list - selection is via the title dropdown next to play button (much better UX)

    // Top language controls - clean, no per-line clutter
    const langBar = document.createElement('div');
    langBar.className = 'dual-langbar';

    const primWrap = document.createElement('div');
    primWrap.className = 'dual-lang primary';
    const sel1 = makeLangSelect(state.primaryLang, v => {
      state.primaryLang = v;
      stopAll();
      Object.keys(audioMap).forEach(k => delete audioMap[k]);
      render();
    });
    primWrap.appendChild(sel1);
    const tog1 = makeModeToggle(state.primaryMode, m => {
      state.primaryMode = m;
      render();
    });
    primWrap.appendChild(tog1);

    // Swap (intuitive way to exchange)
    const swapBtn = document.createElement('button');
    swapBtn.className = 'dual-swap';
    swapBtn.textContent = '⇄';
    swapBtn.title = 'Swap languages';
    swapBtn.addEventListener('click', () => {
      const pLang = state.primaryLang, pMode = state.primaryMode;
      state.primaryLang = state.secondaryLang;
      state.primaryMode = state.secondaryMode;
      state.secondaryLang = pLang;
      state.secondaryMode = pMode;
      stopAll();
      Object.keys(audioMap).forEach(k => delete audioMap[k]);
      render();
    });

    const secWrap = document.createElement('div');
    secWrap.className = 'dual-lang secondary';
    const sel2 = makeLangSelect(state.secondaryLang, v => {
      state.secondaryLang = v;
      stopAll();
      Object.keys(audioMap).forEach(k => delete audioMap[k]);
      render();
    });
    secWrap.appendChild(sel2);
    const tog2 = makeModeToggle(state.secondaryMode, m => {
      state.secondaryMode = m;
      render();
    });
    secWrap.appendChild(tog2);

    langBar.appendChild(primWrap);
    // swap between the two
    swapBtn.classList.add('dual-swap-between');
    langBar.appendChild(swapBtn);
    langBar.appendChild(secWrap);
    container.appendChild(langBar);

    // Viewer (content + player)
    const viewer = document.createElement('div');
    viewer.className = 'dual-viewer';
    container.appendChild(viewer);

    const pid = state.prayerId;
    const url1 = `${state.primaryLang}/${pid}/${pid}.json`;
    const url2 = `${state.secondaryLang}/${pid}/${pid}.json`;

    Promise.all([
      loadTitles(state.primaryLang),
      loadTitles(state.secondaryLang),
      fetch(url1).then(r => r.ok ? r.json() : Promise.reject()),
      fetch(url2).then(r => r.ok ? r.json() : Promise.reject())
    ]).then(([t1, t2, d1, d2]) => {
      const base1 = url1.substring(0, url1.lastIndexOf('/') + 1);
      const base2 = url2.substring(0, url2.lastIndexOf('/') + 1);

      // Pre-create audios EXACTLY like prayer.mjs
      // ANY audio (primary or secondary segment/passage/full) affects the main play/pause button
      addAudio(state.primaryLang, 'full', base1, pid);
      (d1.passages || []).forEach(p => {
        const pidStr = String(p.passage_id);
        addAudio(state.primaryLang, pidStr, base1, pid);
        (p.segments || []).forEach(s => {
          if (s.passage_segment_id) addAudio(state.primaryLang, s.passage_segment_id, base1, pid);
        });
      });

      addAudio(state.secondaryLang, 'full', base2, pid);
      (d2.passages || []).forEach(p => {
        const pidStr = String(p.passage_id);
        addAudio(state.secondaryLang, pidStr, base2, pid);
        (p.segments || []).forEach(s => {
          if (s.passage_segment_id) addAudio(state.secondaryLang, s.passage_segment_id, base2, pid);
        });
      });

      renderViewer(viewer, d1, d2, base1, base2, pid, t1, t2);
    }).catch(() => {
      viewer.innerHTML = '<em style="opacity:0.6">Unable to load prayer.</em>';
    });
  }

  function makeLangSelect(current, onChange) {
    const sel = document.createElement('select');
    sel.className = 'dual-lang-select';
    LANGS.forEach(l => {
      const o = document.createElement('option');
      o.value = l.id;
      o.textContent = l.label;
      if (l.id === current) o.selected = true;
      sel.appendChild(o);
    });
    sel.addEventListener('change', e => onChange(e.target.value));
    return sel;
  }

  function makeModeToggle(current, onChange) {
    const btn = document.createElement('button');
    btn.className = 'dual-mode-toggle' + (current === 'phonetic' ? ' selected' : '');
    btn.title = current === 'phonetic' ? 'Showing phonetic' : 'Showing text';

    // Use builtin lucide/languages icon (from site nav icons)
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svg.setAttribute('fill', 'none');
    svg.setAttribute('stroke', 'currentColor');
    svg.setAttribute('stroke-linecap', 'round');
    svg.setAttribute('stroke-linejoin', 'round');
    svg.setAttribute('stroke-width', '2');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('width', '14');
    svg.setAttribute('height', '14');
    svg.setAttribute('class', 'lucide lucide-languages');
    svg.innerHTML = '<path d="m5 8 6 6M4 14l6-6 2-3M2 5h12M7 2h1M22 22l-5-10-5 10M14 18h6"/>';
    btn.appendChild(svg);

    btn.addEventListener('click', () => {
      const next = current === 'text' ? 'phonetic' : 'text';
      onChange(next);
    });
    return btn;
  }

  function renderViewer(viewer, d1, d2, base1, base2, prayerId, titlesPrimary = {}, titlesSecondary = {}) {
    viewer.innerHTML = '';
    mainPlayBtn = null;

    // Prayer header with full primary play - EXACT same logic as prayer.mjs
    const header = document.createElement('div');
    header.className = 'prayer-header';

    // Big prayer title (h2) that opens a clean dropdown menu for selection
    const titleArea = document.createElement('div');
    titleArea.className = 'prayer-title-area';

    const titleEl = document.createElement('h2');
    titleEl.className = 'prayer-title';
    titleEl.textContent = (d1 && d1.title) || PRAYERS.find(p => p.id === state.prayerId).label;

    const arrow = document.createElement('span');
    arrow.className = 'prayer-dropdown-arrow';
    arrow.textContent = '▼';

    const titleWrapper = document.createElement('div');
    titleWrapper.className = 'prayer-title-wrapper';
    titleWrapper.appendChild(titleEl);
    titleWrapper.appendChild(arrow);

    // Custom menu (normally sized items) - bilingual: primary / secondary titles
    const menu = document.createElement('div');
    menu.className = 'prayer-dropdown-menu';
    menu.style.display = 'none';

    PRAYERS.forEach(p => {
      const item = document.createElement('div');
      item.className = 'prayer-dropdown-item' + (p.id === state.prayerId ? ' active' : '');
      const l1 = titlesPrimary[p.id] || (p.id === prayerId && d1 ? d1.title : p.label);
      const l2 = titlesSecondary[p.id] || (p.id === prayerId && d2 ? d2.title : p.label);
      const span1 = document.createElement('span');
      span1.className = 'primary-title';
      span1.textContent = l1;
      const sep = document.createTextNode(' / ');
      const span2 = document.createElement('span');
      span2.className = 'secondary-title';
      span2.textContent = l2;
      item.appendChild(span1);
      item.appendChild(sep);
      item.appendChild(span2);
      item.addEventListener('click', (e) => {
        e.stopPropagation();
        if (p.id !== state.prayerId) {
          state.prayerId = p.id;
          stopAll();
          Object.keys(audioMap).forEach(k => delete audioMap[k]);
          render();
        }
      });
      menu.appendChild(item);
    });

    titleWrapper.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = menu.style.display === 'block';
      menu.style.display = isOpen ? 'none' : 'block';
      if (!isOpen) {
        // attach one-time outside click closer
        setTimeout(() => {
          const closer = (ev) => {
            if (!titleArea.contains(ev.target)) {
              menu.style.display = 'none';
              document.removeEventListener('click', closer);
            }
          };
          document.addEventListener('click', closer, { once: true });
        }, 10);
      }
    });

    titleArea.appendChild(titleWrapper);
    titleArea.appendChild(menu);

    const fullBtn = document.createElement('button');
    fullBtn.className = 'play-btn';
    fullBtn.textContent = '▶';
    fullBtn.title = 'Play full prayer (primary)';
    mainPlayBtn = fullBtn;
    fullBtn.addEventListener('click', () => {
      if (mainPlayBtn && mainPlayBtn.textContent === '⏸') {
        stopAll();
      } else {
        play(state.primaryLang, 'full', base1, prayerId);
      }
    });

    header.appendChild(titleArea);
    header.appendChild(fullBtn);
    viewer.appendChild(header);

    // Passages
    const passagesWrap = document.createElement('div');
    passagesWrap.className = 'prayer-passages dual-passages';

    const psgs1 = (d1 && d1.passages) || [];
    const psgs2 = (d2 && d2.passages) || [];

    psgs1.forEach((p, i) => {
      const sp = psgs2[i] || p;
      const pidStr = String(p.passage_id);

      const passageEl = document.createElement('div');
      passageEl.className = 'prayer-passage';

      // PRIMARY line: button + natural flowing text (simple inline, no flex boxes)
      const pLine = document.createElement('div');
      pLine.className = 'dual-line primary';

      const pBtn = document.createElement('button');
      pBtn.className = 'dual-play';
      pBtn.textContent = '▶';
      pBtn.title = 'Play passage (primary)';
      pLine.appendChild(pBtn);

      const text1 = document.createElement('span');
      text1.className = 'dual-text primary-text';
      (p.segments || []).forEach((s, idx) => {
        const seg = document.createElement('span');
        seg.className = 'dual-seg';
        seg.textContent = state.primaryMode === 'text' ? (s.text || '') : (s.phonetic || '');
        seg.dataset.sid = s.passage_segment_id;
        seg.addEventListener('click', () => play(state.primaryLang, s.passage_segment_id, base1, prayerId, seg));
        text1.appendChild(seg);
        if (idx < p.segments.length - 1) text1.appendChild(document.createTextNode(' '));
      });
      pLine.appendChild(text1);

      pBtn.addEventListener('click', () => play(state.primaryLang, pidStr, base1, prayerId, text1));
      text1.addEventListener('click', (e) => {
        if (e.target.classList.contains('dual-seg')) return;
        play(state.primaryLang, pidStr, base1, prayerId, text1);
      });

      // SECONDARY: passage play button (light grey like secondary text) + segments
      const sLine = document.createElement('div');
      sLine.className = 'dual-line secondary';

      const sBtn = document.createElement('button');
      sBtn.className = 'dual-play';
      sBtn.textContent = '▶';
      sBtn.title = `Play passage ${pidStr} (secondary)`;
      sLine.appendChild(sBtn);
      sBtn.addEventListener('click', () => play(state.secondaryLang, pidStr, base2, prayerId, sBtn));

      const text2 = document.createElement('span');
      text2.className = 'dual-text secondary-text';
      (sp.segments || []).forEach((s, idx) => {
        const seg = document.createElement('span');
        seg.className = 'dual-seg';
        seg.textContent = state.secondaryMode === 'text' ? (s.text || '') : (s.phonetic || '');
        seg.dataset.sid = s.passage_segment_id;
        seg.addEventListener('click', () => play(state.secondaryLang, s.passage_segment_id, base2, prayerId, seg));
        text2.appendChild(seg);
        if (idx < sp.segments.length - 1) text2.appendChild(document.createTextNode(' '));
      });
      sLine.appendChild(text2);

      text2.addEventListener('click', (e) => {
        if (e.target.classList.contains('dual-seg')) return;
        play(state.secondaryLang, pidStr, base2, prayerId, text2);
      });

      passageEl.appendChild(pLine);
      passageEl.appendChild(sLine);
      passagesWrap.appendChild(passageEl);
    });

    viewer.appendChild(passagesWrap);
  }

  render();
}

function initAll() {
  const el = document.getElementById('dual-rosary');
  if (el) createApp(el);
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll, { once: true });
  } else {
    initAll();
  }
}

export { createApp, PRAYERS, LANGS };
