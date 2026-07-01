# Rosary Player Plan

## Purpose
This document captures the design and implementation of the full Rosary player: a linear, sequenced, audio-enabled experience for praying the Rosary while learning the language. It builds directly on the existing per-prayer player (prayer.mjs) and mystery chooser (rosary.mjs).

The player lets the user:
- Navigate the entire Rosary prayer-by-prayer via visual progress indicators.
- Interact manually (click dots, prev/next, click segments for audio).
- Or click "auto" (via the play button) and have it play the full audio for the current step then automatically advance through the whole sequence to the end.

Phase 1 scope: English only, living on the English landing page (`english/index.md`).

## Scope (Current Phase)
- English only.
- Player UI and logic added to `ora/docs/english/index.md` (the landing page for English).
- All other languages and their landing pages remain unchanged for now.
- Reuse the existing mystery chooser and per-language mystery name data.
- New: `rosary-player.mjs` (if the logic grows beyond a simple addition to rosary.mjs).
- New mystery announcement audio/JSON for the 5 decades (English first).
- Direct linear sequence model (easy to represent as a flat ordered list of steps).
- 7 rows of indicator dots.
- Three-button player control bar (prev / play-pause / next) directly under the indicator nav.
- The prayer view area re-uses the same dual text + phonetic presentation from prayer.mjs (locked to English, text primary + phonetic secondary).

Future phases (not now): other languages, dedicated /rosary page, full multi-lang, etc.

## Guiding Principles
- Keep it a direct linear sequence — no branches, no choices inside the player except the top-level mystery set chooser.
- The same `prayer.mjs` view (locked English text/phonetic) is used for every standard prayer step.
- Mystery announcements are treated as first-class steps (new short JSON + audio) so they render and play consistently.
- Progress is one-way for the dots (a progress bar made of 7 rows): jumping ahead marks everything up to that point as completed (golden yellow).
- Manual navigation always available; auto mode is optional chaining of "play full then advance".
- Minimal new UI: indicators + 3-button control + viewer area. Reuse existing CSS classes where possible.
- Data-driven where it makes sense (steps defined in JS, mystery names from existing `#rosary-mysteries` script).
- English defines the exact sequence and order of steps.
- All assets co-located with content (new mysteries go under `english/mysteries/` following companion pattern).
- No changes to individual prayer pages or other languages yet.

## Exact Linear Sequence (English)
The sequence is a flat list of steps. Each step is either a standard prayer or a mystery announcement.

### Intro (Row 0)
1. Sign of the Cross
2. Apostles' Creed
3. Our Father
4. Hail Mary
5. Hail Mary
6. Hail Mary
7. Glory Be
8. Fatima Prayer

### Decade Rows (Rows 1–5)
For each of the 5 decades (order depends on active mystery set from the chooser):
- Mystery announcement (e.g. "The First Joyful Mystery, the Annunciation")
- Our Father
- Hail Mary
- Hail Mary
- Hail Mary
- Hail Mary
- Hail Mary
- Hail Mary
- Hail Mary
- Hail Mary
- Hail Mary
- Hail Mary
- Glory Be
- Fatima Prayer

Each Hail Mary step is labeled simply "Hail Mary" (repeated exactly as many times as recited; 10 per decade). This produces exactly 14 indicators per decade row.

### Conclusion (Row 6)
1. Hail, Holy Queen
2. Rosary Prayer (the "Let us pray..." section that follows Hail Holy Queen)

Total steps: 8 (intro) + 5×14 (70) + 2 (conclusion) = 80 steps.

The mystery set chooser (Joyful / Sorrowful / Glorious / Luminous) only affects the 5 mystery announcement steps (their displayed label and which audio file is used). All other steps are fixed.

## Data Model
A simple array in JS:

```js
const steps = [
  { row: 0, label: 'Sign of the Cross', kind: 'prayer', prayerId: 'sign-of-the-cross' },
  { row: 0, label: "Apostles' Creed", kind: 'prayer', prayerId: 'apostles-creed' },
  ...
  // mystery steps carry decade + slot instead of fixed label
  { row: 1, label: null, kind: 'mystery', decade: 0 },
  { row: 1, label: 'Our Father', kind: 'prayer', prayerId: 'our-father' },
  // Hail Mary repeated (labeled simply "Hail Mary" each time)
  { row: 1, label: 'Hail Mary', kind: 'prayer', prayerId: 'hail-mary' },
  ... (9 more)
  ...
  { row: 6, label: 'Hail, Holy Queen', kind: 'prayer', prayerId: 'hail-holy-queen' },
  { row: 6, label: 'Rosary Prayer', kind: 'prayer', prayerId: 'rosary-prayer', jsonPath: 'hail-holy-queen/rosary-prayer.json' },
];
```

- `row`: 0–6 for the 7 visual rows.
- For mysteries the label is resolved at render time from the active set (shared with rosary.mjs via `#rosary-mysteries`).
- `jsonPath` (optional) for the special rosary-prayer case that lives inside the hail-holy-queen directory.
- Audio for a step is always the "full" version of that item (the player control plays full; segments remain clickable inside the viewer for manual practice).

Mystery JSONs (new, English only for now):
- Follow the exact same format as other prayers.
- One passage, minimal segments (e.g. 1–2 segments).
- Example location: `english/mysteries/joyful1.json` + `english/mysteries/joyful1/` audio (or flat siblings per the "joyful1.json kind of format" guidance).
- 5 files for the default set initially; all 20 can be added for English before expanding languages.
- Use the same English TTS voice/rate as the other prayers.
- Text and phonetic fields can be nearly identical for these short announcements.

## UI Structure on the English Landing Page
Current page starts with:
- Title "English"
- `.mystery-chooser` (already present and functional)
- The mystery-set-title and decade-labels inside the collapsible quotes (these stay for reference)

New player content will be added after the chooser (or in a prominent section):

1. **7-row indicator nav**
   - Left column or prefix: row label ("Intro", "1st Decade", "2nd Decade", ..., "5th Decade", "Conclusion").
   - For decade rows the row label can dynamically include the current mystery name (reacts when user clicks a mystery-set pill).
   - Horizontal row of small dots (circle buttons).
   - Visual rules:
     - Default: grey / muted.
     - Completed (progress): golden yellow (e.g. `#d4af37` or `#f1c40f`).
     - Current position: highlighted (ring, bolder, or primary color) in addition to progress.
     - Clicking any dot jumps directly to that step (sets current, loads viewer, marks all prior steps completed).
   - Progress is cumulative: once you have visited or played past a dot, it stays lit even if you go back.

2. **Three-button player control** (directly beneath the indicator rows, above the viewer)
   - ◀  (previous step)
   - ▶ / ⏸  (play / pause — this button activates or pauses the auto-play chain)
   - ▶  (next step)
   - Use the same unicode / icon style already in prayer.mjs (`▶` `⏸`).
   - Play button starts auto mode from the current step: play full audio of current → on ended advance → repeat until the end or user pauses.
   - While auto is running the button shows pause icon; clicking it stops the chain (but leaves the user at the current step).
   - Prev / Next always stop any running auto and move + load.

3. **Current step viewer**
   - Re-uses the exact same presentation produced by `prayer.mjs` locked mode:
     - For prayer steps: text line (primary) + phonetic line (secondary), passage groups, clickable segment spans for individual audio, passage play buttons.
     - For mystery steps: the mystery text (large, clear) with its own audio (full play via the top control or a dedicated button).
   - The viewer container is a plain div; `createApp` (or a thin wrapper) is called with the appropriate json for the step.
   - Because we have our own 3-button bar we will likely need a small enhancement to prayer.mjs (e.g. `opts.embedded = true` or `opts.showFullPlayHeader = false`) so it does not duplicate a play button inside the viewer.
   - Rely on the lit dot + row label for context. Steps simply repeat their label (e.g. "Hail Mary" for repeats); no counts or fancy numbering.

The existing collapsible description below the player area can remain as a static reference / fallback outline.

## Auto Mode Behavior
- "Play" (the middle button) = start auto from current position.
- Plays the **full** audio for the current step (exactly as the per-prayer full play works today).
- On `ended` event: if not last step, advance one step, immediately play full for the new step.
- Continues until the final step completes or the user clicks pause / prev / next / a dot.
- Manual clicks on segments inside the viewer are still allowed even during auto (they temporarily override the main audio).
- At end: auto stops, final step remains visible.

## Integration Points
- **mystery chooser**: already present. When a set is activated the 5 decade rows update their mystery labels. The rosary-player code must react to the same change (either by listening for clicks or by re-reading `#rosary-mysteries` and the active set) and:
  - Update the decade row header texts.
  - If the current step is a mystery, reload the viewer with the new mystery text + corresponding audio.
- **rosary.mjs**: continues to own mystery date logic + chooser activation. rosary-player.mjs can import helpers or duplicate the small `getRosaryData()` / active set logic for isolation.
- **prayer.mjs**: primary reuse via `createApp(container, { jsonPath: '...' })` or a new exported helper for embedded use. Export of `createApp` and `PRAYERS` is already there.
- **extra_javascript**: add `assets/rosary-player.mjs` (safe to load on all pages; it only activates if the player container exists on English index).
- **Zensical nav**: the landing page (`english/index.md`) is already first under English. No immediate nav change required, but the plan can note future options (e.g. a direct "Rosary Player" entry that points to the same page with a hash or just relies on it being the overview).

## New Files & Changes
- `plan-rosary-player.md` (this document)
- `ora/docs/assets/rosary-player.mjs` (new module, self-contained init)
- `ora/docs/english/index.md` (add the indicator rows + controls + viewer container divs after the chooser; keep existing content)
- `ora/docs/stylesheets/extra.css` (new rules for `.rosary-row`, `.rosary-dot`, `.rosary-controls`, progress states, golden yellow, layout)
- Mystery data (English):
  - `ora/docs/english/mysteries/joyful1.json` (and siblings for 2–5)
  - Corresponding generated MP3s in the same directory (or per the companion dir pattern)
  - Later the other three sets for English completeness
- Small optional extension inside `prayer.mjs` for better embedded/ header-less rendering of the viewer area.

Audio generation for mysteries will use the existing `audio-utils/generate-rosary-audio.py` once the JSONs are written (user runs it).

## Visual & Styling Notes
- Dots: small (≈12–16 px), circular, `border-radius: 50%`.
- Completed / progressed: golden yellow fill (choose a readable tone that works in both light and dark: e.g. `#c9a227` or a CSS custom property).
- Current: extra ring or scale + the yellow or primary accent.
- Rows: use flex or grid so the row label + dots stay aligned even on narrow screens.
- The 3-button control bar: centered or left-aligned, generous click targets, same button style as existing `.play-btn`.
- Viewer area uses the existing `.dual-viewer`, `.prayer-passage`, `.dual-line`, `.dual-seg` classes for zero new complexity in the prayer content itself.

## Open Items / Brainstorming (for later alignment)
- Exact golden yellow hex and current-step treatment.
- Whether decade row labels show the full mystery name or keep short "First Decade" + tooltip/dot title.
- How to handle the 10 repeated Hail Marys in auto (just plays the Hail Mary full audio 10 times in succession — this is the intended repetition for learning; each uses the plain label "Hail Mary").
- Whether to persist the "progress" across reloads (localStorage) — probably not for v1.
- Future nav: add an explicit "Play the Rosary" item under English that lands on the player section?
- Once English is solid, replicate the same player UI (with language-specific JSONs) on other language landing pages.

Hail Mary repeats use the simple label "Hail Mary" (no counts or extra numbering, per alignment).

## Implementation Order (suggested)
1. Write the sequence definition + rendering of 7 rows + dots (static at first).
2. Wire click-to-jump + current + progress lighting.
3. Add the 3-button control bar + prev/next.
4. Wire the viewer to load real prayer content via prayer.mjs for normal steps.
5. Add mystery step support (read active set + render simple or via mystery json).
6. Implement auto mode (play full + ended listener + chain).
7. React to mystery set changes.
8. Add styles, polish labels/tooltips.
9. Create the 5 (or 20) English mystery JSONs + generate audio.
10. Test the full flow end-to-end on the English landing page.

This keeps everything simple, direct, and re-uses the mature prayer player and mystery data that already exist.

---

**Status**: Planning document. English-only implementation on the landing page to follow after alignment on this plan.

Christ is Lord! (plan captured for future sessions)