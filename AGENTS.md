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


## Current Status

We will use [Zensical](https://zensical.org/) to manage all content.
Dev server on :7007 for local dev.

Zensical project set up in `ora/`. Special preview at `/ora/site/`. 
Migrated old /v/ content organized directly in language/topic sections under docs/. 
Site cutover executed with .htaccess (root now serves ora/site/, /v/ preserved)


## Site Organization

Each language section should have subsections orgranized around the rosary.

So in English something like:
+ Sign of the Cross
+ Apostles Creed
+ Our Father
+ Hail Mary
+ Glory Be
+ Fatima Prayer

Every language should have pages for those, every one.
The landing page in each language will explain the rosary, the mysteries and dates, minimal text and more of a guide (so each language would have sufficient information to say the entire rosary in that language, e.g., "the First Joyful Mystery, the Annunciation...", and then it links to the specific prayer pages.

Then separately we want an optional subsection specific for that language, information about the language and language learning resources... let's plan out the exact name for this; in English we have the tips/ pages, and Chinese and Spanish and Vietnamese have similar pages that would go in this additional catchall section, but it needs a clear name that will be clear across all ten lanuages, so maybe a symbol or icon that holds all the pages? Let's discuss and brainstorm.

## TODO

+ Organize new language sections, each focused on learning the Rosary in that language

