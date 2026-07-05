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
- never use emdash character, use -- instead


---

## Overview

We will use [Zensical](https://zensical.org/) to manage all content.
Dev server on :7007 for local dev (user will run, DO NOT RUN THIS YOURSELF).

Zensical project set up in `ora/`. 
All content (and style and javascript and assets) go into `ora/docs/`.
Generated output lands in `ora/site/` (DO NOT EDIT IN HERE).
DO NOT write logs or plan docs anywhere in `ora/docs/`, webapp content only!

Migrated old /v/ content organized directly in language/topic sections under `ora/docs/`. 


---

## Site Organization

Directories and files should use simple English names for all lanuages, e.g. chinese/resources/calligraphy.md and the content title will use proper Chinese (書法), and this means all URLs will follow simple english names, e.g., /ora/site/chinese/extras/calligraphy/ but the content (titles and text) will be in that language.

Each language section should have subsections orgranized around the rosary.

So in English something like:
+ Sign of the Cross
+ Apostles Creed
+ Our Father
+ Hail Mary
+ Glory Be
+ Fatima Prayer
+ Hail Holy Queen (should also include "Let us pray..." Rosary Prayer)

And then "extras" for extra prayers, such as,
Jesus Prayer
Nicene Creed

Every language should have those exact pages, with icon: material/cross
The landing page in each language will explain the rosary (in that language), the mysteries and days for each mystery, minimal text and more of a guide (so each language page would have minimal but sufficient prose for the entire rosary in that language, e.g., "the First Joyful Mystery, the Annunciation..."

All other non-rosary pages will be in a language specific [ Resources ] section, which will map to a subdirectory in that language, e.g., english/resources/


---

## Passages and Segments for audio alignment

Every prayer will be broken down into passages that must match 1:1 across all languages (same literal meaning across all languages), such that tooling can index any given passage across any given language.

For example, hail-mary passage 1 is "Hail Mary, full of grace, the Lord is with thee."
and thus in Latin passage 1 is "Ave Maria, gratia plena, Dominus tecum."
and this in Vietnamese passage 1 is "Kính mừng Maria, đầy ơn phúc, Đức Chúa Trời ở cùng Bà."

Each passage is broken into segments identified with letters after the passage number (e.g., 1a, 1b, etc); these are the shortest grammatical unit for that language, hail-mary passage 1 has three segment, 1a:"Ave Maria,"  1b:"gratia plena," 1c:"Dominus tecum."

All languages MUST align on passages literally and exactly! The exact meaning for a given passage MUST match across all languages!

Segments are not guaranteed to match due to grammatic and linguistic differences between laguages.

see [plan-prayer-mjs.md](plan-prayer-mjs.md) for details.


---

## TODO

+ see [notes-resources.md](notes-resources.md), revise and modify old content (all pages in the resources sections, e.g., english/resources/advice.md), some are well-written and just need some editing, others need full rewrites, and some probably need to be deleted; go through each page, one by one, and discuss carefully.

+ consolidate one clean HTML only tooltip system (such as the one used on the Chinese pages, use that everywhere, remove the clunky/shitty JS tooltips that come with zensical, they suck balls and are slow af).

+ flashcards.mjs, add top chinese characters (currently broken at /zh)

+ carefully tweak latin phonetics for better audio (italian to liturgical latin)

+ verify all prayer text with official Catholic sources (from the vatican or similar).

+ iOS app! Ora Pro Nobis





























