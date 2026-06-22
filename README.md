# lingua.avant.net

Reviving lingua.avant.net to focus on traditional Christian prayers (especially the Rosary) for language learning.

## The Site

The main content is powered by [Zensical](https://zensical.org/) and lives under `ora/`.

A special preview of the new site is available at `/ora/site/` (built output is committed so it serves directly from the repo).

Current focus:
- Traditional prayers in Latin
- English and Spanish translations for language learners
- The Rosary and core prayers

More languages and content will be added over time.

## Development

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (for running Zensical)

### Makefile

A Makefile is provided at the root for common tasks.

```bash
make          # build the site (default)
make build    # same as above
make serve    # start the dev server on localhost:7007
make help     # list targets
```

Run `make serve` in a separate terminal while editing content in `ora/docs/`.

The dev server will be available at http://localhost:7007

### Building

The site builds to `ora/site/`. This directory is intentionally committed so the preview is live at `/ora/site/`.

### Notes

- All original content (flashcards under `/es`, `/vi`, `/zh`, etc.) remains untouched.
- The new Zensical section is isolated in `ora/`.
- Full cutover and routing changes will come later.

## Existing Content

The legacy language learning materials (Spanish, Vietnamese, Chinese flashcards) are preserved at their original paths and will not be removed until the new site is fully migrated.