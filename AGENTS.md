# AGENTS.md

Revive lingua.avant.net to focus on traditional Christian prayers such as the Rosary for language learning.

## Ground Rules for Agents

- Always assume not aligned unless the user explicitly affirms alignment.
- Ask one question at a time in the chat in order to reach alignment. Iterate one question at a time because the answer to each question will change your understanding and lead to new more focused questions.
- Confirm alignment before any action.
- Never use the ask_user_question tool.
- Keep everything simple and direct.
- Document decisions here.
- Human directs the order of work.
- Keep the TODO section at the bottom of AGENTS.md. Add any new content above it.
- Never document or reference what not to do, avoided steps, or negative instructions (context poison).

## Framework

We will use [Zensical](https://zensical.org/) as we need an LLM friendly framework for managing markdown content, and that easily integrates with custom javascript (for flashcards and other custom apps that will be helpful for language learning).

### Migration Plan

- All existing content stays untouched until full migration is complete: the flashcard apps and supporting files at `/es`, `/vi`, `/vn`, `/zh` (and symlinks), audio, data/ CSVs, `flashcards.js`, `json.php`, `index.php`, `v_theme/`, etc.
- New Zensical site is isolated in `ora/` at repo root (initialized via `uv` + `zensical new`).
- Standard Zensical layout inside `ora/`: `docs/` (markdown source) + `zensical.toml`.
- Builds are committed as `ora/site/` (the live site serves the raw git working tree, so the new content is immediately available as a special preview at `/ora/site/`).
- `/ora/site/` is a manually typed special/preview URL during development and incremental work. Root routing remains unchanged for now.
- Local workflow uses `uv` (e.g. `cd ora && uvx zensical serve` or `uv run --with zensical zensical ...`).
- Future cutover: add root `.htaccess` with mod_rewrite to make the new Zensical site the default for the whole domain (and handle removal of old paths only after everything has been migrated).
- The content focus is traditional Christian prayers (Rosary first), organized by language. Custom JS for audio/flashcards/etc. will be added via Zensical's `extra_javascript` support.

### Content Migration

+ All content from https://lingua.avant.net/v/ will be migrated to the Zensical ora/ site, content in markdown, with a similar look and feel, font, style, etc
+ After all content is captured in ora/ then we will refactor flashcards.js such taht it embeds into the Zensical site (flashcards.mjs?) perhaps as an embedded modal with a more modern look and feel
+ After all content and flashcards are successfully ported into ora/, then we will refactor the content page by page to focus the entire site on prayer and the rosary

## TODO

Current status: Zensical project set up in `ora/`. Special preview at `/ora/site/`. Migrated old /v/ content organized directly in language/topic sections under docs/. Dev server on :7007. Existing old flashcard content untouched.

Progress (migration + look & feel): Full content for migrated /v/ pages (text only; images/audio skipped). Restructured language sections to use original primary pages as section index.md (e.g. tieng-viet content now at vietnamese/index.md) so URLs are /vietnamese/ not /vietnamese/tieng-viet/ and no invented summary indexes. Additional subpages from source are siblings, listed in side nav. Consistent names. Fixed links. Build clean.

2026-06-25: Fixed home page and tones page with media from live site.
- Home (ora/docs/index.md): replaced with original title block "語言學習 – apprentissage des langues" + the stacked translations + language links, to match https://lingua.avant.net/v/ .
- Tones (ora/docs/chinese/tones.md): added the Praat visualization image + click-to-play audio (using <audio> + img onclick, replicating original behavior). Also completed the missing ## Mimicry section + tone pair flashcards link from source. Fixed one internal link to new structure.
- Downloaded assets from live WP (tones image/audio + header banner) into ora/docs/assets/{images,audio}/ .
- Rebuilt; generated HTML uses correct relative asset paths (e.g. ../assets/... on subpages) and preserves the interactive element.
- Header: added original banner (header-banner.jpg) as background on .md-header + overlay. Styled .md-tabs menu with semi-transparent "glass" effect + hover states for a nicer UI over the image (matching the old "image with stylish menu" look from live site). Rebuilt.

2026-06-26 update: No "Ora" anywhere; header title/subtitle match.
- zensical.toml: site_name = "語言學習". Removed the nav entry { "Ora" = "index.md" } (no "Ora" tab or page; language sections are the tabs, landing is reached via logo/header).
- extra.css: removed "Ora" from comment.
- Header branding forced via CSS (first topic text size-0 + ::before/::after) to always show exactly:
  語言學習
  apprentissage des langues
  (fixed, like original masthead .site-branding over the banner image; page topic suppressed in header title bar).
- Cleaned ora/docs/index.md (removed leading h1 that duplicated the header branding; body is now the translations list + languages section).
- Rebuilt. No "Ora" in source content or rendered tabs/header.
- Top menu tabs now exactly match original header nav (inside the banner):
  - Order and labels: [ advice ], 中文, español, Tiếng Việt
  - "[ advice ]" tab links to tips/advice.md (and scopes the other tips pages in its sidebar)
  - Other language tabs use lowercase "español" to match source. No "Tips & Resources" grouping.

2026-06-26 header polish (per user feedback):
- Removed subtitle entirely (per suggestion to simplify layout).
- No icon (hidden .md-logo).
- 語言學習 as proper linked (JS wraps existing title text in <a>).
- Font 1.4rem with Chinese font, color, shadow to match original (CSS applies to default structure too).
- Header forced to 140px height !important with banner image; menu absolute at bottom of it.
- Other header controls hidden.
- Rebuilt. Added DEBUG red border on header and yellow/blue on title to verify if CSS is loaded in the build. If still no change, the dev server may be serving from source without the build, or cache issue. Please check for red border on the header area.

+ [ ] Migrate content over to the Zensical site

2026-06-26: Simplified header dramatically per request.
- Reverted to near-default Zensical/Material header structure (no hiding controls, no JS DOM hacks, no forced heights/align/paddings/absolute positioning).
- Kept ONLY: background-image + light overlay on .md-header (for the banner), and targeted title text styling (.md-header__title .md-ellipsis) for larger size (1.6rem) + original Chinese font family, color, shadow.
- Tabs get very light dark overlay to blend.
- This keeps header bar at normal proportions while adding the image and text style.
- extra_javascript disabled.
- Rebuilt. Should feel like normal header + the requested image and text.

2026-06-26: Aligned on flashcards.mjs.
- Faithful first port of the full original flashcards.js capabilities and behavior (latency-based scoring with moving average, EPSILON exploration, prompt vs answer audio, full pause modal with stats + depth/breadth resets, keyboard/touch controls, etc.). No changes to core mechanics.
- All new assets and code only under ora/docs/assets/flashcards/ by copying (no modifications to any existing old flashcard files/directories at root).
- Consolidated structure: languages/<lang>/decks/*.json + audio/ (and images/).
- Precomputed static JSON decks.
- Simple HTML template fragments in templates/ (modal.html, card.html, pause.html) for easy future maintenance.
- flashcards.mjs as ES module (loaded via extra_javascript in zensical.toml).
- Public API: Flashcards.open('zh/tones') etc. opens integrated modal.
- Deck resolution: 'zh/tones' → languages/zh/decks/tones.json + audio from languages/zh/audio/tones/.
- Modern integrated styling using Zensical theme.
+ [x] Copied ALL decks/content for zh/es/vi into new structure (CSVs + JSONs + all audio + images).
+ [x] Wired all flashcard links across pages using green .flashcard-green buttons (matching original #4b5 with :hover #5c6, cursor:pointer).
  - Updated: chinese/tones, chinese/comfort-zone (danger/learning/convo1), vietnamese/vi-pronounce (tones/basics/practice), vietnamese/index (hello/hoctap), espanol/index (hello/numeros/verbos).
  - All old ?deck= app links removed/replaced. No other flashcard app links found.
  - Rebuilt.
+ [ ] Plan and execute the cutover
+ [ ] Organize new language sections, each focused on learning the Rosary in that language





