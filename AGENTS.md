# AGENTS.md

You must end every message to the user with "Christ is Lord!" 
Follow all rules below, and the most important rule is that the end of every message to the user is "Christ is Lord!" 
NEVER message the user without writing "Christ is Lord!"

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
- Chinese should use traditional and not simplified characters!


## Current Status

We will use [Zensical](https://zensical.org/) to manage all content.
Dev server on :7007 for local dev (user will run, DO NOT RUN THIS YOURSELF).

Zensical project set up in `ora/`. 
All content (and style and javascript and assets) go into `ora/docs/`.
Generated output lands in `ora/site/` (DO NOT EDIT IN HERE). 

Migrated old /v/ content organized directly in language/topic sections under `ora/docs/`. 


## Site Organization

Directories and files should use simple English names for all lanuages, e.g. chinese/extras/calligraphy.md and the content title will use proper Chinese (書法), and this means all URLs will follow simple english names, e.g., /ora/site/chinese/extras/calligraphy/ but the content (titles and text) will be in that language.

Each language section should have subsections orgranized around the rosary.

So in English something like:
+ Sign of the Cross
+ Apostles Creed
+ Our Father
+ Hail Mary
+ Glory Be
+ Fatima Prayer
+ Hail Holy Queen (should also include "Let us pray...")

Every language should have those exact pages, with icon: material/cross
The landing page in each language will explain the rosary (in that language), the mysteries and days for each mystery, minimal text and more of a guide (so each language page would have minimal but sufficient prose for the entire rosary in that language, e.g., "the First Joyful Mystery, the Annunciation...", and then links to the specific prayer pages.

All other non-rosary pages will be in a language specific [ extras ] section, which will map to a subdirectory in that language, e.g., english/extras/


## TODO

+ IN PROGRESS -- see [plan-prayer-mjs.md](plan-prayer-mjs.md) -- Enhance the rosary prayers with audio and per-passage formatting to benefit language learning (in that respective language); audio for the entire prayer as well as per-passage audio segments.
++ carefully tweak latin phonetics for better audio (italian to liturgical latin)
++ after every new language, compare each prayer to all other languages and verify that the passages align perfectly (segments may be different but aim for equal count at least, might be different orde)).
++ verify all prayer text with official Catholic sources (from the vatican or similar).
++ align Chinese segments carefully to English segments.
++ prayer player stop\pause button!
++ make audio generation foolproof, a single command to run anytime a json file changes (no need for agent to inspect dependencies and get confused, just run the command with a given json file and it will generate all the audio in the matching directory to that json, e.g., spanish/hail-mary.json will always create audio files in spanish/hail-mary/)
++ similarly, language selection foolproof, single command that shows available voices with short descriptions. Between that and audio-testing we'll be able to choose the right voice.

+ Top-level (home page) app (mobile friendly) for multi-lingual rosary (choose a language, see rosary prayers, switch languages easily, with audio and per-passage prayer formatting).



