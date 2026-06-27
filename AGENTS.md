# AGENTS.md

Develop lingua.avant.net to focus on traditional Christian prayers, specifically the Rosary, for language learning.


## Ground Rules for Agents

- Always assume not aligned unless the user explicitly affirms alignment.
- Ask one question at a time in the chat in order to reach alignment. Iterate one question at a time because the answer to each question will change your understanding and lead to new more focused questions.
- Confirm alignment before any action.
- Never use the ask_user_question tool.
- Keep everything simple and direct.
- Human directs the order of work.
- Never document or reference what not to do, avoided steps, or negative instructions (context poison).
- This document is not for your notes, DO NOT EDIT THIS DOCUMENT UNLESS INSTRUCTED BY USER!
- User (human) will run the dev server, DO NOT RUN `make build` or any `make` commands unless instructed to by the user.


## Current Status

We will use [Zensical](https://zensical.org/) to manage all content.
Dev server on :7007 for local dev (user will run, DO NOT RUN THIS YOURSELF).

Zensical project set up in `ora/`. 
All content (and style and javascript and assets) go into `ora/docs/`.
Generated output lands in `ora/site/` (DO NOT EDIT IN HERE). 

Migrated old /v/ content organized directly in language/topic sections under `ora/docs/`. 


## Site Organization

Directories and files should use simple English names, e.g. chinese/extras/calligraphy.md and the content title will use proper Chinese (書法), and this means all URLs will follow simple english names, e.g., /ora/site/chinese/extras/calligraphy/ but the content (titles and text) will be in that language.

Each language section should have subsections orgranized around the rosary.

So in English something like:
+ Sign of the Cross
+ Apostles Creed
+ Our Father
+ Hail Mary
+ Glory Be
+ Fatima Prayer
+ Hail Holy Queen (should also include "Let us pray...")

Every language should have those exact pages, with icon: lucide/cross
The landing page in each language will explain the rosary (in that language), the mysteries and days for each mystery, minimal text and more of a guide (so each language page would have minimal but sufficient prose for the entire rosary in that language, e.g., "the First Joyful Mystery, the Annunciation...", and then links to the specific prayer pages.

All other non-rosary pages will be in a language specific [ extras ] section, which will map to a subdirectory in that language, e.g., english/extras/


## TODO

+ Create per-language rosary pages (language index.md, e.g., latin/index.md)
+ Enhance the rosary prayers with audio and per-passage formatting to benefit language learning (in that respective language); audio for the entire prayer as well as per-passage audio segments.
+ Top-level (home page) app (mobile friendly) for multi-lingual rosary (choose a language, see rosary prayers, switch languages easily, with audio and per-passage prayer formatting).



