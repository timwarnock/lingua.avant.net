# Agent Notes

The resource sections are written in English for English-speaking language learners of the target language. 
Focus is on traditional Christian prayers and the Rosary for language learning.

We use the custom `tooltip="..."` HTML attribute (with simple pure CSS) everywhere for hover glosses and UI hints. This is the single clean HTML-only tooltip system. Use `<span tooltip="pinyin = meaning">文字</span>` (Chinese example only) or `<span tooltip="Heavens">Caelis</span>` (Latin example: tooltip holds only the English meaning) extensively as a learning aid on prayer text, resources, etc. If the visible text is Title Case then the tooltip must also be Title Case.

Before each top-level section: a few newlines, then --- , then another newline, then ## Section Title.




---

## Admonition Formatting

Admonitions must use this exact format:

!!! type "Title"
    Body starts on the next line indented with four spaces.
    Use two spaces at the end if you want a standalone line.  

    Additional paragraphs are separated by a blank line,
    with each starting indented.
    These lines are part of the paragraph,
    even though they are on separate lines in the markdown.

    These lines  
    Are on their own line  
    with no paragraph breaks  
    because of the two extra spaces  
    after each line  .

To have separate lines: 1, 2, 3, 4 where each number is on its own line, you need two spaces at the end of a line where you want a rendered line break. Example:

!!! note "Separate lines"
    1  
    2  
    3  
    4  

If you need a tooltip on an admonition title, do NOT escape the quote, that fails to render, just use single quotes, e.g., `!!! success "Initial Consonants (<span tooltip='Shēng Mǔ = Initial Consonants'>聲母</span>)"`

Common types are: note, success, warning, failure, tip (for prayers)

See chinese/resources/pronunciation.md or vietnamese/resources/pronunciation.md for examples.



---

## Pronunciation pages

The structure uses these sections in order: intro paragraph(s), then ## Phonemes, then ## Recommendations, then ## Not Recommended.

Recommendations and Not Recommended will be written in the native language with tooltips for translation (e.g., in spanish "Recomendaciones" or in chinese "推薦").

The purpose of these pages is to provide high-quality information that will directly help language learners to more quickly pick up the language. The goal is to short-circuit the slow natural discovery process of immersion in the language and provide precise and highly useful information so that learning to pronounce the language will be quicker and easier.

Latin pronunciation.md is the reference benchmark for all remaining pronunciation.md pages (structure, phonemes section with audio examples, recommendations/not recommended, tooltip usage per the rules above, overall quality and focus on Rosary prayers).

We do not recommend our own page. On no page should the content recommend or point readers to the page being read itself.



---

## Pages to Work On

### English

- [x] advice.md
- [x] bad-advice.md
- [x] fsi-diff.md
- [x] fsi.md
- [x] introverts.md
- [x] pronunciation.md

### Spanish

- [x] cognates.md
- [x] conjugations.md
- [x] pronunciation.md

### Chinese

- [x] writing.md
- [x] pronunciation.md

### Vietnamese

- [x] pronunciation.md
- [x] writing.md

### Latin

- [x] pronunciation.md (reference benchmark for all other pronunciation pages)

### French

- [ ] pronunciation.md (needs a lot more work to get to the quality of the latin benchmark)

### Greek

- [ ] pronunciation.md (match latin benchmark)

### Japanese

- [ ] pronunciation.md (match latin benchmark)

### Polish

- [ ] pronunciation.md (match latin benchmark)

### Portuguese

- [ ] pronunciation.md (match latin benchmark)


---

## Saint Name Conventions for Language Landing Page Quotes

To respect each language while keeping the site accessible:

- Use the proper form of address for "Saint" + the saint's name **in the language of that section**.
- English sections: "St. [Common English name]" (e.g. "St. John Henry Newman").
- Spanish sections: "San [Name]" (e.g. "San Josemaría Escrivá").
- French sections: "Saint [Name]" (e.g. "Saint Louis de Montfort").
- Latin sections: "Sanctus [Latin name]" (full word, not abbreviated). Example: "Sanctus Hieronymus".
- For the main/general index (ora/docs/index.md), continue using the English "St. [Name]" forms since it is not tied to a specific language section.

When the English name is significantly more familiar to readers (common for Latin saints), wrap the native form in a tooltip using the project's standard `<span tooltip="...">` syntax:

- Latin example: `<span tooltip="St. Jerome">Sanctus Hieronymus</span>`
- This renders as: Sanctus Hieronymus (hover shows "St. Jerome")

In the quote syntax:

!!! quote "<span tooltip=\"St. Jerome\">Sanctus Hieronymus</span>"

    [Latin text of the quote]

    *[English translation]*

Do not use abbreviated forms like "S. Hieronymus" or "St." inside Latin sections — "St." is English; use the full Latin "Sanctus".

This convention applies specifically to the author name in the landing-page `!!! quote` blocks that appear immediately after each language's title (as described in AGENTS.md TODO).

Update existing quotes to follow this as new language pages or quotes are added.


