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

**Goal:** Help learners pronounce the Rosary language faster than unguided exposure. Dense, accurate notes; exact inventories; rules that matter for prayer; clickable audio; Rosary examples.

**Widdowson:** Include the Henry Widdowson quote (short-circuiting natural discovery) on each language’s pronunciation page. Readers usually work one language at a time, so the framing is worth repeating in context rather than treating it as site-wide duplication.

**Quality bar (read these pages; copy quality, not outline):**

+ `latin/resources/pronunciation.md` -- clarity, inventory, audio, prayer tips, named recommendations, substantive Not Recommended
+ `chinese/resources/pronunciation.md` -- how a language-specific system (tones) can earn its own section when inventory alone is insufficient

Each language keeps its own history, inventory, and systems. Structure follows what that language needs.

**Usual pieces (order and extras vary by language):** intro with language/Church/Rosary context; phonemes with prose between blocks; optional further sections only when the language has a real combination system that needs room; prayer tips; Recommendations and Not Recommended (section titles in the language of the section, with English tooltips).

**Audio:** reserve bold for clickable audio only (phoneme label = isolate; word = that word). Use italics for non-audio emphasis. Prefer Rosary vocabulary for examples. When prose names a sound, link audio for that sound (and an example word when helpful). Phoneme audio lives under each language's `resources/phonemes/` with matching `phonemes.json`. If mp3 files are removed from `ora/docs/`, remove the same paths under `ora/site/`.

**Page content** teaches the target language to a learner. Agent process, other languages, and UI mechanics stay out of the page.

**Editing:** change what was asked; keep existing good prose (especially history) unless asked to revise it. Accumulate quality across passes. Leave checklist items open until the user has reviewed.




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

- [x] pronunciation.md

### French

- [ ] pronunciation.md (awaiting user review)

### Greek

- [ ] pronunciation.md

### Japanese

- [ ] pronunciation.md

### Polish

- [ ] pronunciation.md

### Portuguese

- [ ] pronunciation.md




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

In Latin sections use the full word Sanctus (not English St. or abbreviated S.).

This convention applies specifically to the author name in the landing-page `!!! quote` blocks that appear immediately after each language's title.

Update existing quotes to follow this as new language pages or quotes are added.




---

## Greek prayer text and TTS (always)

Edge `el-GR-*` voices misread heavy polytonic, mid-dots (`·` / `·`), and elisions (`ἀπ'`, `δι'`). That can sound like letter-names or nonsense (e.g. wrong chunks that do not match *και το*).

**Always for Greek prayer JSON:**

1. **`tts.input`: `"text"`** with `el-GR-NestorasNeural` (same as other Greek prayers).
2. **`text`**: TTS-safe **monotonic** Greek (stress accents OK), matching site style of hail-mary / our-father / nicene.
   - Drop mid-dot / ano teleia: use comma or period.
   - Expand elisions: `ἀπ'` / `απ'` → `από `, `δι'` → `δια `, etc.
   - Prefer forms Edge reads as words, not letter-by-letter.
3. **`phonetic`**: Latin-script learner guide with **modern Greek** pronunciation of the Koine text (display only; not sent to TTS).
4. After generating audio, **always run** the letter-spelling detector:

```bash
uv run --with edge-tts python audio-utils/generate-rosary-audio.py ora/docs/greek/.../prayer.json
uv run --with edge-tts python audio-utils/detect-greek-letter-spelling.py ora/docs/greek/.../prayer.json
# or whole language:
uv run --with edge-tts python audio-utils/detect-greek-letter-spelling.py --all
```

5. **FLAG** = fix `text` and regenerate. **WARN** on very short segments is often hold/silence padding; check by ear.
6. Septuagint/Vulgate numbering note (Psalm 51 = 50): only on Latin / French / Greek psalm-51 pages, as `warning` with title tooltip and English italics after a blank line.

Do not paste raw polytonic Septuagint into `text` without the TTS cleanup above.

