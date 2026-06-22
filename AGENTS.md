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
- The eventual content focus is traditional Christian prayers (Rosary first), organized by language. Custom JS for audio/flashcards/etc. will be added via Zensical's `extra_javascript` support.
- `.github/workflows` from the Zensical template can remain (it targets GitHub Pages); unused for current direct-git hosting.

## TODO

Current status: Zensical project set up in `ora/`. Special preview at `/ora/site/`. Initial Rosary content with nested prayers/ pages added (Latin + English + Spanish). Dev server on :7007. Existing content untouched.

+ [ ] Decide the migration plan
+ [ ] Build out Zensical for local development
+ [ ] Set up a special hosted Zensical section on the live site
+ [ ] Migrate content over to the Zensical site
+ [ ] Plan and execute the cutover
+ [ ] Organize new language sections, each focused on learning the Rosary in that language





