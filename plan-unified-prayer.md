# Unified Prayer Module Design (Consolidated)

## Goal
Consolidate `prayer.mjs` and `dual-prayer.mjs` into a single module (`prayer.mjs` in `ora/docs/assets/`).

Support two modes cleanly:
- Locked mode for per-language prayer pages (and audio-testing): simple, fixed to one language's text + phonetic, no choosers.
- Full mode for the home page: language/prayer choosers enabled, with initial defaults.

Everything stays simple and direct. The JSON file (when provided) is the source of truth for locked mode. The caller provides arguments for the full mode. The prayer audio UX from the dual-prayer.mjs can be used for all prayers (per prayer page) which includes per-passage playback of the phonetic text, and clickable segments in both text and phonetic.

## Two Modes in One Function

Function: `createApp(container, opts = {})`

### Mode 1: Locked (JSON Reference) – Per-Prayer Pages & Audio-Testing
- Triggered when `opts.jsonPath` is provided (or div has `data-json`).
- Load the JSON relative to the current page location.
- Audio files are always in the **same directory** as the loaded JSON. No reconstruction using lang/prayer is needed.
- Use the JSON's `"id"` (or filename base) as the audio filename prefix: `${id}.mp3`, `${id}-${segment}.mp3`.
- Title, passages, segments (text + phonetic) come directly from the JSON.
- Force:
  - primary = `.text`
  - secondary = `.phonetic`
  - same data for both sides
- No language chooser, no primary/secondary language swap, no prayer dropdown/chooser.
- Still supports old heading repurposing (H1/H2 + play button) and hides `.prayer-fallback`.
- The div only needs `data-json="..."`. `data-prayer` is optional (used only as fallback for ID).
- Lang can be derived from path convention when present; JSON's internal `"lang"` is only a fallback for non-convention cases (e.g. audio-testing).

### Mode 2: Arguments Mode – Home Page (and explicit cases)
- Triggered when no `jsonPath`.
- Required initial defaults:
  - `prayer` (relative path, e.g. `"hail-mary"` or `"extras/jesus-prayer"`)
  - `primaryLang`, `secondaryLang`
  - `primaryMode`, `secondaryMode`
- Optional enable flags (false by default):
  - `langChoosers: true/false`
  - `prayerChooser: true/false`
- When either chooser flag is true: load and use `PRAYERS` / `LANGS` registry to build UI (dropdown, selects).
- When both flags are false: still locked to the supplied initial values (no registry, no extra UI).
- Path construction uses the provided relative `prayer` value directly.
- For the home page div (no `data-json`): hard-code the full opts with sensible initial values + both chooser flags = true.

## Divs & Auto-Init (Unified)
- Single class for containers: `prayer-app`
- Auto-init on DOMContentLoaded:
  - Find `.prayer-app` elements.
  - If the element has `data-json`: locked mode (json reference).
  - If the element has no `data-json`: full arguments mode (home) using the hard-coded opts.
- This keeps markup declarative and the same style for both uses.

## Key Rules
- JSON (when provided) is authoritative for locked mode: audio location, title, content, ID for filenames.
- No subdir lookup tables in arguments mode – caller supplies relative path for `prayer`.
- Registry (`PRAYERS` / `LANGS`) is **only** loaded/used when chooser flags are enabled.
- Locked mode always uses the dual-line viewer style (text primary + phonetic secondary).
- Full mode shows chooser UI only when the corresponding flag is true.
- Audio files are always co-located with the resolved JSON.

## Current Use Cases
1. Per-prayer pages (locked):
   ```html
   <div class="prayer-app" data-json="hail-mary.json"></div>
   ```

2. Home page (full):
   ```html
   <div class="prayer-app"></div>
   ```
   (Module hard-codes the opts with initial values + choosers enabled.)

3. Audio-testing (locked, custom JSON):
   ```html
   <div class="prayer-app" data-json="antonio.json"></div>
   ```

## Next Steps (Once Confirmed)
- Implement `createApp` in new `ora/docs/assets/prayer.mjs`.
- Update auto-init logic.
- Use unified class (update or support existing divs).
- Remove the old `dual-prayer.mjs`.
- Ensure locked mode still does heading repurposing + fallback hiding.

