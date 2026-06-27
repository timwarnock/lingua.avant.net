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
- Keep the TODO section at the bottom of AGENTS.md. Do not add new sections or slop to this document.
- Never document or reference what not to do, avoided steps, or negative instructions (context poison).


## Current Status

We will use [Zensical](https://zensical.org/) to manage all content.
Dev server on :7007 for local dev.

Zensical project set up in `ora/`. Special preview at `/ora/site/`. 
Migrated old /v/ content organized directly in language/topic sections under docs/. 
Site cutover executed with .htaccess (root now serves ora/site/, /v/ preserved)

Language sections present: chinese, espanol, vietnamese, tips.

## TODO

+ Organize new language sections, each focused on learning the Rosary in that language
+ Restored root index.php (redirect to /v/) and removed .htaccess per user direction

