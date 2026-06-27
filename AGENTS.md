# AGENTS.md

Revive lingua.avant.net to focus on traditional Christian prayers such as the Rosary for language learning.


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

Zensical project set up in `ora/`. Special preview at `/ora/site/`. 
Migrated old /v/ content organized directly in language/topic sections under docs/. 


## Site Organization

Each language section should have subsections orgranized around the rosary.

So in English something like:
+ Sign of the Cross
+ Apostles Creed
+ Our Father
+ Hail Mary
+ Glory Be
+ Fatima Prayer
+ Hail Holy Queen (should also include "Let us pray...")

Every language should have pages for those, every one.
The landing page in each language will explain the rosary, the mysteries and days for each mystery, minimal text and more of a guide (so each language page would have sufficient information to say the entire rosary in that language, e.g., "the First Joyful Mystery, the Annunciation...", and then it links to the specific prayer pages.

All other non-rosary pages will be in a language specific [ extras ] section, which will map to a subdirectory in that language, e.g., english/extras/


## TODO

+ Create rosary pages (per language) and stub pages for extras section, similar to Latin

