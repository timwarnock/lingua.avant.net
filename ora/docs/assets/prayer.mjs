/*
 * prayer.mjs
 * Unified audio-enabled prayer viewer.
 * createApp supports two modes:
 * - Locked (data-json or jsonPath): per-prayer pages and audio-testing. Fixed text/phonetic from one JSON, heading repurposing + fallback hide.
 * - Full (no json): home multi-lang with choosers, swap, bilingual dropdown.
 * Legacy selectors (.prayer-interactive, #dual-rosary) supported with zero markdown changes.
 * All audio co-located with the JSON. Passages and segments drive playback.
 */

const PRAYERS = [
  { id: 'sign-of-the-cross', label: 'Sign of the Cross' },
  { id: 'apostles-creed', label: "Apostles' Creed" },
  { id: 'our-father', label: 'Our Father' },
  { id: 'hail-mary', label: 'Hail Mary' },
  { id: 'glory-be', label: 'Glory Be' },
  { id: 'fatima-prayer', label: 'Fatima Prayer' },
  { id: 'hail-holy-queen', label: 'Hail Holy Queen' },
  { separator: true },
  { id: 'jesus-prayer', label: 'Jesus Prayer', subdir: 'extras' }
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

function createApp(container, opts = {}) {
  const jsonRel = opts.jsonPath || container.dataset.json;
  const locked = !!jsonRel;

  // Defaults per plan. Full mode (home) enables choosers by default.
  const prayer = locked ? (container.dataset.prayer || opts.prayer || 'prayer') : (opts.prayer || 'hail-mary');
  const primaryLang = locked ? null : (opts.primaryLang || 'latin');
  const secondaryLang = locked ? null : (opts.secondaryLang || 'english');
  const primaryMode = locked ? 'text' : (opts.primaryMode || 'text');
  const secondaryMode = locked ? 'phonetic' : (opts.secondaryMode || 'text');
  const langChoosers = !locked && (opts.langChoosers !== false);
  const prayerChooser = !locked && (opts.prayerChooser !== false);
  const embedded = !!opts.embedded;
  const hideSecondary = !!opts.hideSecondary;
  const defaultShowPhonetic = opts.showPhonetic !== undefined ? !!opts.showPhonetic : (container.dataset.showPhonetic === 'true');

  const state = {
    prayerId: prayer,
    primaryLang,
    primaryMode,
    secondaryLang,
    secondaryMode,
    langChoosers,
    prayerChooser
  };

  const audioMap = {};
  let mainPlayBtn = null;
  let activeEl = null;
  let loadedData = null;
  let currentViewer = null;
  let primaryToggleBtn = null;
  let secondaryToggleBtn = null;

  function audioKey(tag, key) {
    return `${tag || 'local'}:${key}`;
  }

  function getAudio(tag, key, base, pid) {
    const k = audioKey(tag, key);
    if (audioMap[k]) return audioMap[k];
    const a = new Audio();
    const suffix = (key === 'full') ? '' : `-${key}`;
    a.src = `${base}${pid}${suffix}.mp3`;
    a.preload = 'auto';
    audioMap[k] = a;
    return a;
  }

  function addAudio(tag, key, base, pid) {
    const k = audioKey(tag, key);
    if (audioMap[k]) return audioMap[k];
    const a = getAudio(tag, key, base, pid);
    a.addEventListener('play', () => setMainPlaying(true));
    a.addEventListener('ended', maybeRevertMain);
    a.addEventListener('pause', maybeRevertMain);
    audioMap[k] = a;
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
    const any = Object.values(audioMap).some(a => !a.paused && a.currentTime > 0);
    if (!any) setMainPlaying(false);
  }

  function play(tag, key, base, pid, targetEl = null) {
    const a = audioMap[audioKey(tag, key)] || getAudio(tag, key, base, pid);
    Object.values(audioMap).forEach(aa => {
      if (aa !== a) {
        aa.pause();
        aa.currentTime = 0;
      }
    });
    // If rosary player autoplay is active, stop it on any manual play
    if (typeof window !== 'undefined' && typeof window.stopRosaryAuto === 'function') {
      window.stopRosaryAuto();
    }
    clearActive();
    if (targetEl) setActive(targetEl);
    setMainPlaying(true);
    a.currentTime = 0;
    a.play().catch(() => {});
  }

  const titlesCache = {};

  async function loadTitles(lang) {
    if (titlesCache[lang]) return titlesCache[lang];
    titlesCache[lang] = {};
    await Promise.all(PRAYERS.map(async p => {
      if (p.separator || !p.id) return;
      try {
        const dir = p.subdir ? `${p.subdir}/${p.id}` : p.id;
        const url = `${lang}/${dir}/${p.id}.json`;
        const r = await fetch(url);
        const data = r.ok ? await r.json() : null;
        titlesCache[lang][p.id] = (data && data.title) || p.label;
      } catch (e) {
        titlesCache[lang][p.id] = p.label;
      }
    }));
    return titlesCache[lang];
  }

  function getPdef(id) {
    return PRAYERS.find(pp => pp.id === id) || {};
  }

  function getDir(pdef, id) {
    return pdef.subdir ? `${pdef.subdir}/${id}` : id;
  }

  function resetAudios() {
    Object.keys(audioMap).forEach(k => delete audioMap[k]);
  }

  function render() {
    container.innerHTML = '';
    mainPlayBtn = null;
    activeEl = null;
    currentViewer = null;
    primaryToggleBtn = null;
    secondaryToggleBtn = null;
    if (locked) {
      renderLocked();
    } else {
      renderFull();
    }
  }

  function renderLocked() {
    const jsonUrl = new URL(jsonRel, window.location.href);
    fetch(jsonUrl)
      .then(r => {
        if (!r.ok) throw new Error('Could not load ' + jsonRel);
        return r.json();
      })
      .then(data => {
        const base = jsonUrl.href.substring(0, jsonUrl.href.lastIndexOf('/') + 1);
        const pid = data.id || state.prayerId;

        addAudio('local', 'full', base, pid);
        (data.passages || []).forEach(p => {
          const ps = String(p.passage_id);
          addAudio('local', ps, base, pid);
          (p.segments || []).forEach(s => {
            if (s.passage_segment_id) addAudio('local', s.passage_segment_id, base, pid);
          });
        });

        if (!embedded) {
          // Locked always reuses heading + play button (old prayer behavior)
          doRepurposeHeading(data.title || pid, () => {
            if (mainPlayBtn && mainPlayBtn.textContent === '⏸') stopAll();
            else play('local', 'full', base, pid);
          });

          // Phonetics toggle for this prayer page. Default is off unless data-show-phonetic="true" on the div (or opts.showPhonetic).
          let showPhonetic = defaultShowPhonetic;
          const tog = makePhoneticToggle(showPhonetic, (val) => {
            showPhonetic = val;
            container.querySelectorAll('.dual-viewer').forEach(el => el.remove());
            renderLockedLines(container, data, base, pid, !showPhonetic);
          });
          if (mainPlayBtn && mainPlayBtn.parentNode) {
            mainPlayBtn.insertAdjacentElement('afterend', tog);
          }
          renderLockedLines(container, data, base, pid, !showPhonetic);
          hideFallbacks();
        } else {
          renderLockedLines(container, data, base, pid, hideSecondary);
        }
      })
      .catch(err => {
        console.warn('[prayer]', err);
        container.innerHTML = '<em style="opacity:0.6">Audio view unavailable.</em>';
      });
  }

  function doRepurposeHeading(titleText, onPlayFull) {
    const h = container.previousElementSibling;
    if (h && (h.tagName === 'H1' || h.tagName === 'H2')) {
      h.innerHTML = '';
      h.classList.add('prayer-with-player');
      const t = document.createElement('span');
      t.className = 'prayer-title';
      t.textContent = titleText;
      const b = document.createElement('button');
      b.className = 'play-btn';
      b.textContent = '▶';
      b.title = 'Play full prayer';
      mainPlayBtn = b;
      b.addEventListener('click', onPlayFull);
      h.appendChild(t);
      h.appendChild(b);
    } else {
      const hdr = document.createElement('div');
      hdr.className = 'prayer-header';
      const t = document.createElement('span');
      t.className = 'prayer-title';
      t.textContent = titleText;
      const b = document.createElement('button');
      b.className = 'play-btn';
      b.textContent = '▶';
      b.title = 'Play full prayer';
      mainPlayBtn = b;
      b.addEventListener('click', onPlayFull);
      hdr.appendChild(t);
      hdr.appendChild(b);
      container.appendChild(hdr);
    }
    const prev = container.previousElementSibling;
    if (prev && (prev.tagName === 'H1' || prev.tagName === 'H2') && !prev.classList.contains('prayer-with-player')) {
      prev.style.display = 'none';
    }
  }

  function hideFallbacks() {
    document.querySelectorAll('.prayer-fallback').forEach(el => el.style.display = 'none');
  }

  function buildDualPassages(psgs1, psgs2, base1, base2, lang1, lang2, mode1, mode2, pid) {
    const wrap = document.createElement('div');
    wrap.className = 'prayer-passages dual-passages';

    psgs1.forEach((p, i) => {
      const sp = psgs2[i] || p;
      const ps = String(p.passage_id);
      const el = document.createElement('div');
      el.className = 'prayer-passage';

      // primary line
      const lp = document.createElement('div');
      lp.className = 'dual-line primary';
      const bp = document.createElement('button');
      bp.className = 'dual-play';
      bp.textContent = '▶';
      bp.title = 'Play passage (primary)';
      lp.appendChild(bp);
      const tp1 = document.createElement('span');
      tp1.className = 'dual-text primary-text';
      (p.segments || []).forEach((s, j) => {
        const seg = document.createElement('span');
        seg.className = 'dual-seg';
        seg.textContent = (mode1 === 'text' ? (s.text || '') : (s.phonetic || ''));
        seg.dataset.sid = s.passage_segment_id;
        const sid = s.passage_segment_id;
        seg.addEventListener('click', () => play(lang1, sid, base1, pid, seg));
        tp1.appendChild(seg);
        if (j < (p.segments || []).length - 1) tp1.appendChild(document.createTextNode(' '));
      });
      lp.appendChild(tp1);
      bp.addEventListener('click', () => play(lang1, ps, base1, pid, tp1));
      tp1.addEventListener('click', e => {
        if (e.target.classList.contains('dual-seg')) return;
        play(lang1, ps, base1, pid, tp1);
      });

      // secondary line
      const ls = document.createElement('div');
      ls.className = 'dual-line secondary';
      const bs = document.createElement('button');
      bs.className = 'dual-play';
      bs.textContent = '▶';
      bs.title = 'Play passage (secondary)';
      ls.appendChild(bs);
      const tp2 = document.createElement('span');
      tp2.className = 'dual-text secondary-text';
      (sp.segments || []).forEach((s, j) => {
        const seg = document.createElement('span');
        seg.className = 'dual-seg';
        seg.textContent = (mode2 === 'text' ? (s.text || '') : (s.phonetic || ''));
        seg.dataset.sid = s.passage_segment_id;
        const sid = s.passage_segment_id;
        seg.addEventListener('click', () => play(lang2, sid, base2, pid, seg));
        tp2.appendChild(seg);
        if (j < (sp.segments || []).length - 1) tp2.appendChild(document.createTextNode(' '));
      });
      ls.appendChild(tp2);
      bs.addEventListener('click', () => play(lang2, ps, base2, pid, bs));
      tp2.addEventListener('click', e => {
        if (e.target.classList.contains('dual-seg')) return;
        play(lang2, ps, base2, pid, tp2);
      });

      el.appendChild(lp);
      el.appendChild(ls);
      wrap.appendChild(el);
    });

    return wrap;
  }

  function renderLockedLines(cont, data, base, pid, hideSecondary = false) {
    const view = document.createElement('div');
    view.className = 'dual-viewer';
    cont.appendChild(view);

    if (hideSecondary) {
      // Single primary text only (no phonetic secondary)
      const wrap = document.createElement('div');
      wrap.className = 'prayer-passages';

      (data.passages || []).forEach((p) => {
        const el = document.createElement('div');
        el.className = 'prayer-passage';

        const lp = document.createElement('div');
        lp.className = 'dual-line primary';
        const bp = document.createElement('button');
        bp.className = 'dual-play';
        bp.textContent = '▶';
        bp.title = 'Play passage';
        lp.appendChild(bp);
        const tp = document.createElement('span');
        tp.className = 'dual-text primary-text';
        (p.segments || []).forEach((s, j) => {
          const seg = document.createElement('span');
          seg.className = 'dual-seg';
          seg.textContent = (s.text || '');
          seg.dataset.sid = s.passage_segment_id;
          const sid = s.passage_segment_id;
          seg.addEventListener('click', () => play('local', sid, base, pid, seg));
          tp.appendChild(seg);
          if (j < (p.segments || []).length - 1) tp.appendChild(document.createTextNode(' '));
        });
        lp.appendChild(tp);
        bp.addEventListener('click', () => play('local', String(p.passage_id), base, pid, tp));
        tp.addEventListener('click', e => {
          if (e.target.classList.contains('dual-seg')) return;
          play('local', String(p.passage_id), base, pid, tp);
        });

        el.appendChild(lp);
        wrap.appendChild(el);
      });

      view.appendChild(wrap);
    } else {
      const wrap = buildDualPassages(data.passages, data.passages, base, base, 'local', 'local', 'text', 'phonetic', pid);
      view.appendChild(wrap);
    }
  }

  function updateModesOnly() {
    if (!currentViewer || !loadedData) {
      render();
      return;
    }
    const oldWrap = currentViewer.querySelector('.prayer-passages');
    if (oldWrap) oldWrap.remove();
    const newWrap = buildDualPassages(
      loadedData.d1.passages || [],
      loadedData.d2.passages || [],
      loadedData.b1,
      loadedData.b2,
      state.primaryLang,
      state.secondaryLang,
      state.primaryMode,
      state.secondaryMode,
      loadedData.pid
    );
    currentViewer.appendChild(newWrap);

    // sync toggle visuals (since we didn't full re-render the langbar)
    if (primaryToggleBtn) {
      const isPh = state.primaryMode === 'phonetic';
      primaryToggleBtn.className = 'dual-mode-toggle' + (isPh ? ' selected' : '');
      primaryToggleBtn.title = isPh ? 'Showing phonetic' : 'Showing text';
    }
    if (secondaryToggleBtn) {
      const isPh = state.secondaryMode === 'phonetic';
      secondaryToggleBtn.className = 'dual-mode-toggle' + (isPh ? ' selected' : '');
      secondaryToggleBtn.title = isPh ? 'Showing phonetic' : 'Showing text';
    }
  }

  function renderFull() {
    if (state.langChoosers) {
      const bar = document.createElement('div');
      bar.className = 'dual-langbar';

      const pWrap = document.createElement('div');
      pWrap.className = 'dual-lang primary';
      pWrap.appendChild(makeLangSelect(state.primaryLang, v => {
        state.primaryLang = v;
        stopAll();
        resetAudios();
        loadedData = null;
        currentViewer = null;
        primaryToggleBtn = null;
        secondaryToggleBtn = null;
        render();
      }));
      const tog1 = makeModeToggle(state.primaryMode, m => {
        state.primaryMode = m;
        updateModesOnly();
      });
      pWrap.appendChild(tog1);
      primaryToggleBtn = tog1;

      const sw = document.createElement('button');
      sw.className = 'dual-swap dual-swap-between';
      sw.textContent = '⇄';
      sw.title = 'Swap languages';
      sw.addEventListener('click', () => {
        const pl = state.primaryLang, pm = state.primaryMode;
        state.primaryLang = state.secondaryLang;
        state.primaryMode = state.secondaryMode;
        state.secondaryLang = pl;
        state.secondaryMode = pm;
        stopAll();
        resetAudios();
        render();
      });

      const sWrap = document.createElement('div');
      sWrap.className = 'dual-lang secondary';
      sWrap.appendChild(makeLangSelect(state.secondaryLang, v => {
        state.secondaryLang = v;
        stopAll();
        resetAudios();
        loadedData = null;
        currentViewer = null;
        primaryToggleBtn = null;
        secondaryToggleBtn = null;
        render();
      }));
      const tog2 = makeModeToggle(state.secondaryMode, m => {
        state.secondaryMode = m;
        updateModesOnly();
      });
      sWrap.appendChild(tog2);
      secondaryToggleBtn = tog2;

      bar.appendChild(pWrap);
      bar.appendChild(sw);
      bar.appendChild(sWrap);
      container.appendChild(bar);
    }

    const view = document.createElement('div');
    view.className = 'dual-viewer';
    container.appendChild(view);
    currentViewer = view;

    const pid = state.prayerId;
    const pd = getPdef(pid);
    const d1 = getDir(pd, pid);
    const u1 = `${state.primaryLang}/${d1}/${pid}.json`;
    const d2 = getDir(pd, pid);
    const u2 = `${state.secondaryLang}/${d2}/${pid}.json`;

    const needTitles = state.langChoosers || state.prayerChooser;
    Promise.all([
      needTitles ? loadTitles(state.primaryLang) : Promise.resolve({}),
      needTitles ? loadTitles(state.secondaryLang) : Promise.resolve({}),
      fetch(u1).then(r => r.ok ? r.json() : Promise.reject()),
      fetch(u2).then(r => r.ok ? r.json() : Promise.reject())
    ]).then(([t1, t2, dat1, dat2]) => {
      const b1 = u1.substring(0, u1.lastIndexOf('/') + 1);
      const b2 = u2.substring(0, u2.lastIndexOf('/') + 1);

      addAudio(state.primaryLang, 'full', b1, pid);
      (dat1.passages || []).forEach(p => {
        const ps = String(p.passage_id);
        addAudio(state.primaryLang, ps, b1, pid);
        (p.segments || []).forEach(s => s.passage_segment_id && addAudio(state.primaryLang, s.passage_segment_id, b1, pid));
      });
      addAudio(state.secondaryLang, 'full', b2, pid);
      (dat2.passages || []).forEach(p => {
        const ps = String(p.passage_id);
        addAudio(state.secondaryLang, ps, b2, pid);
        (p.segments || []).forEach(s => s.passage_segment_id && addAudio(state.secondaryLang, s.passage_segment_id, b2, pid));
      });

      loadedData = {d1: dat1, d2: dat2, b1, b2, pid, t1, t2};
      renderFullViewer(view, dat1, dat2, b1, b2, pid, t1, t2);
    }).catch(() => {
      view.innerHTML = '<em style="opacity:0.6">Unable to load prayer.</em>';
    });
  }

  function makeLangSelect(cur, onCh) {
    const sel = document.createElement('select');
    sel.className = 'dual-lang-select';
    LANGS.forEach(l => {
      const o = document.createElement('option');
      o.value = l.id;
      o.textContent = l.label;
      if (l.id === cur) o.selected = true;
      sel.appendChild(o);
    });
    sel.addEventListener('change', e => onCh(e.target.value));
    return sel;
  }

  function makeModeToggle(cur, onCh) {
    const btn = document.createElement('button');
    btn.className = 'dual-mode-toggle' + (cur === 'phonetic' ? ' selected' : '');
    btn.title = (cur === 'phonetic') ? 'Showing phonetic' : 'Showing text';
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
      // use live class to compute next (works even if button not recreated on mode updates)
      const isPhonetic = btn.classList.contains('selected');
      const next = isPhonetic ? 'text' : 'phonetic';
      onCh(next);
    });
    return btn;
  }

  function makePhoneticToggle(initialShow, onChange) {
    const btn = document.createElement('button');
    btn.className = 'dual-mode-toggle' + (initialShow ? ' selected' : '');
    btn.title = initialShow ? 'Hide phonetic' : 'Show phonetic';
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
      const nowShow = !btn.classList.contains('selected');
      btn.classList.toggle('selected', nowShow);
      btn.title = nowShow ? 'Hide phonetic' : 'Show phonetic';
      onChange(nowShow);
    });
    return btn;
  }

  function renderFullViewer(view, d1, d2, b1, b2, pid, tp = {}, ts = {}) {
    view.innerHTML = '';
    mainPlayBtn = null;

    const hdr = document.createElement('div');
    hdr.className = 'prayer-header';

    const ta = document.createElement('div');
    ta.className = 'prayer-title-area';

    const tw = document.createElement('div');
    tw.className = 'prayer-title-wrapper';

    const ttl = document.createElement('h2');
    ttl.className = 'prayer-title';
    ttl.textContent = (d1 && d1.title) || getPdef(pid).label || 'Prayer';

    const arr = document.createElement('span');
    arr.className = 'prayer-dropdown-arrow';
    arr.textContent = '▼';

    tw.appendChild(ttl);
    tw.appendChild(arr);

    const menu = document.createElement('div');
    menu.className = 'prayer-dropdown-menu';
    menu.style.display = 'none';

    if (state.prayerChooser) {
      PRAYERS.forEach(p => {
        if (p.separator) {
          const sep = document.createElement('div');
          sep.className = 'prayer-dropdown-separator';
          menu.appendChild(sep);
          return;
        }
        const it = document.createElement('div');
        it.className = 'prayer-dropdown-item' + (p.id === state.prayerId ? ' active' : '');
        const l1 = document.createElement('span');
        l1.className = 'primary-title';
        l1.textContent = tp[p.id] || (p.id === pid && d1 ? d1.title : p.label);
        const sep = document.createTextNode(' / ');
        const l2 = document.createElement('span');
        l2.className = 'secondary-title';
        l2.textContent = ts[p.id] || (p.id === pid && d2 ? d2.title : p.label);
        it.appendChild(l1);
        it.appendChild(sep);
        it.appendChild(l2);
        it.addEventListener('click', e => {
          e.stopPropagation();
          if (p.id !== state.prayerId) {
            state.prayerId = p.id;
            stopAll();
            resetAudios();
            render();
          }
        });
        menu.appendChild(it);
      });

      tw.addEventListener('click', e => {
        e.stopPropagation();
        const open = menu.style.display === 'block';
        menu.style.display = open ? 'none' : 'block';
        if (!open) {
          setTimeout(() => {
            const cl = ev => {
              if (!ta.contains(ev.target)) {
                menu.style.display = 'none';
                document.removeEventListener('click', cl);
              }
            };
            document.addEventListener('click', cl, { once: true });
          }, 10);
        }
      });
    } else {
      arr.style.display = 'none';
    }

    ta.appendChild(tw);
    if (state.prayerChooser) ta.appendChild(menu);

    const fb = document.createElement('button');
    fb.className = 'play-btn';
    fb.textContent = '▶';
    fb.title = 'Play full prayer (primary)';
    mainPlayBtn = fb;
    fb.addEventListener('click', () => {
      if (mainPlayBtn && mainPlayBtn.textContent === '⏸') stopAll();
      else play(state.primaryLang, 'full', b1, pid);
    });

    hdr.appendChild(ta);
    hdr.appendChild(fb);
    view.appendChild(hdr);

    const ps1 = (d1 && d1.passages) || [];
    const ps2 = (d2 && d2.passages) || [];
    const wrap = buildDualPassages(ps1, ps2, b1, b2, state.primaryLang, state.secondaryLang, state.primaryMode, state.secondaryMode, pid);
    view.appendChild(wrap);
  }

  render();
}

function initAll() {
  // Locked mode via existing .prayer-interactive (data-json preferred; minimal md impact)
  document.querySelectorAll('.prayer-interactive').forEach(el => {
    if (el.dataset.json || el.dataset.prayer) {
      const initOpts = el.dataset.json ? { jsonPath: el.dataset.json } : {};
      if (el.dataset.showPhonetic) initOpts.showPhonetic = el.dataset.showPhonetic === 'true';
      createApp(el, initOpts);
    }
  });

  // New unified class support (future pages)
  document.querySelectorAll('.prayer-app').forEach(el => {
    if (el.dataset.json) {
      createApp(el, { jsonPath: el.dataset.json });
    } else {
      createApp(el);
    }
  });

  // Full multi-lingual home: explicit opts + choosers (hard-coded for the home case per plan)
  const dual = document.getElementById('dual-rosary');
  if (dual) {
    createApp(dual, {
      prayer: 'hail-mary',
      primaryLang: 'latin',
      secondaryLang: 'english',
      primaryMode: 'text',
      secondaryMode: 'text',
      langChoosers: true,
      prayerChooser: true
    });
  }
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll, { once: true });
  } else {
    initAll();
  }
}

export { createApp, PRAYERS, LANGS };

if (typeof window !== 'undefined') {
  window.createPrayerApp = createApp;
}
