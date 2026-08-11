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
- [x] English rosary prayers audited vs Vatican/USCCB/EWTN/DRA/KJV (2026-08-10): fixed Nicene Filioque; Fatima "those most in need"; psalm-51 MD casing to DRA

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
6. Septuagint/Vulgate numbering notes: only on Latin / French / Greek psalm pages, as `warning` with title tooltip and English italics after a blank line. Psalm 51 = 50 (Miserere); Psalm 23 = 22 (Dominus regit me / The Lord is my shepherd).

Do not paste raw polytonic Septuagint into `text` without the TTS cleanup above.





---

## Latin TTS (Italian voice)

Latin uses `it-IT-DiegoNeural` with `tts.input: "phonetic"`, rate `-15%`. Display `text` stays proper Latin; `phonetic` is for TTS and the clickable learner line.

Latin A/B regenerator: `audio-utils/generate-latin-ab.py` (Sancta / sanct- hard-k tests).


---

## German TTS

Production: **`de-DE-KillianNeural`** at rate **`-10%`** (user pick from audio-testing, 2026-07-30).

- Full section: `ora/docs/german/` (rosary prayers, extras, mysteries, pronunciation)
- Scaffold (text only): `audio-utils/scaffold-german.py`
- A/B regenerator: `audio-utils/generate-german-voice-ab.py`
- Nav: `Deutsch` tab in `ora/zensical.toml`; `prayer.mjs` LANGS includes `german`
- Languages dropdown English label: `extra.tooltips` `"Deutsch" = "German"`
- TTS input: `phonetic` (same as display text for German)


---

## Italian TTS

Production: **`it-IT-ElsaNeural`** at rate **`-10%`** (user pick from audio-testing, 2026-07-30).

- Full section: `ora/docs/italian/`
- Scaffold: `audio-utils/scaffold-italian.py`
- A/B regenerator: `audio-utils/generate-italian-voice-ab.py`
- Nav: `Italiano` in `zensical.toml` (after Français); tooltip `"Italiano" = "Italian"`
- `prayer.mjs` LANGS includes `italian`
- Other female candidate tested: Isabella

**Sancta / sanct- (ear-locked):** Edge often says Spanish/Italian *Santa* (no k). Target SAHNK-tah.

| Form | Winner phonetic |
|------|-----------------|
| Sancta | Sànkta |
| sancta | sànkta |
| sanctam | sànktam |
| Sancto | Sànkto |
| Sancti | Sànkti |
| Sanctum | Sanctum (cur -- no change) |

Leave other sanct- forms (`sanctorum`, `sanctissimo`, …) unless a later A/B pass locks them.

### Ear-checked inventory (complete)

A/B listening with `it-IT-DiegoNeural` @ `-15%`. Prefer simpler monophthong when both cel* and ciel* win.

| # | Focus | Winner | Phonetic change |
|---|-------|--------|-----------------|
| 1 | caelis | celis (cielis also ok) | `caelis`/`cieli(s)` → `celis` |
| 2 | caelo | celo (cielo also ok) | `caelo`/`cielo` → `celo` |
| 3 | caelos | celos (cielos also ok) | `caelos`/`cielos` → `celos` |
| 4 | caelum | celum (cielum also ok) | `caelum`/`cielum` → `celum` |
| 5 | saecula saeculorum | secula | `saecul` → `secul` |
| 6 | aeternam | eternam | `aetern` → `etern` |
| 7 | aeternae | eterne | `aeternae` → `eterne` |
| 8 | Deus | Déus | `Deus` → `Déus` |
| 9 | Deum | Déum | `Deum` → `Déum` |
| 10 | Dei | Déi | `Dei` → `Déi` |
| 11 | Deum de Deo | Déum de Déo | both forms accented |
| 12 | gratia | gratsia | `gratia` → `gratsia` |
| 13 | regnum | regnum (cur) | no change |
| 14 | digni | digni (cur) | no change |
| 15 | Iesus | Yesus | `Iesus` → `Yesus` |
| 16 | Iesu Christe | Yesu Christe | `Iesu` → `Yesu`; keep `Christe` |
| 17 | Iesum Christum | cur | no change (`Iesum` stays) |
| 18 | terrae | cur | no change |
| 19 | hora / nostrae | cur | no change |
| 20 | praesertim | cur | no change |
| 21 | haec | èc | `haec` → `èc` |
| 22 | quaesumus | quèsumus | `quaesumus` → `quèsumus` |
| 23 | beatae Mariae | cur | no change |
| 24 | hodie | odie | `hodie` → `odie` |
| 25 | hora | cur | no change |
| 26 | hoc exsilium | cur | no change |
| 27 | Hevae | cur | no change |
| 28 | catholicam | cur | no change |
| 29 | prophetas | cur | no change |
| 30 | resurrectionem | resurretsionem | `resurrection` → `resurretsion` |
| 31 | tentationem | tentatsionem | `tentationem` → `tentatsionem` |
| 32 | Spiritui | cur | no change |
| 33 | mihi | michi | `mihi` → `michi` (others collapse to "mee") |
| 34 | homines | cur | no change |
| 35 | expecto resurrectionem | expecto resurretsionem | keep `expecto`; ti → tsi |
| 36 | iustitiam | iustitsiam | `iustitiam`/`justitiam` → `iustitsiam` |

**Production phonetic rules (ear-locked):**

+ `cael*` / legacy `ciel*` → `cel*` (`celis`, `celo`, `celos`, `celum`, `celi`)
+ `saecul*` → `secul*`; `aetern*` → `etern*` (`aeternae` → `eterne`)
+ `Deus`/`Deum`/`Dei`/`Deo` → `Déus`/`Déum`/`Déi`/`Déo`
+ `gratia` → `gratsia`
+ `Iesus` → `Yesus`; `Iesu` → `Yesu`; leave `Iesum` and all `Christ*` as written
+ `haec` → `èc`; `quaesumus` → `quèsumus`; `hodie` → `odie`
+ `resurrection*` → `resurretsion*`; `tentationem` → `tentatsionem`
+ `mihi` → `michi`; `iustitiam`/`justitiam` → `iustitsiam`
+ Leave alone: `regnum`, `digni`, `terrae`, `hora`, `nostrae`, `praesertim`, `beatae`, `Mariae`, `hoc`, `exsilium`, `Hevae`, `catholicam`, `prophetas`, `Spiritui`, `homines`, `Christe`/`Christum`

**Deus note:** plain `Deus` is often misread (English *douse* / *Dawson*). Use **`Déus`**. Do not use `De-us` / `De us` -- those make the voice say "US" / "Stati Uniti".



---

## iOS app

See `plan-ios.md` for Ora Pro Nobis native iPhone plan (aligned decisions, content bundling, App Store path).


---

## Chinese Hail Mary (聖母經) -- official text

Restored exact official vernacular Chinese (Taiwan CRBC / Vatican News traditional), which differs in word order from English in the second half:

Official: 萬福瑪利亞，妳充滿聖寵，主與妳同在。妳在婦女中受讚頌，妳的親子耶穌同受讚頌。天主聖母瑪利亞，求妳現在和我們臨終時，為我們罪人祈求天主。阿們。

Passages 1-2 align cleanly with English. Passages 3-4 follow Chinese order (time phrase before "for us sinners"), so meaning is imperfect vs English P3/P4; Amen is 阿們 (matches other Chinese prayers, not 阿門).

## Latin prayer audit (2026-08-10)
- Fixed Nicene Filioque + exspecto (Missale Romanum)
- Fixed Fatima: added animas; eas quae (no single official Latin exists)
- Fixed Salve: Genetrix; Rosary prayer: sacratissimo; moved concede to P3
- Removed orphan mp3s (apostles-creed, our-father, rosary-prayer-2f)
- Regenerated audio: nicene, fatima, hail-holy-queen, rosary-prayer
- English Nicene still lacks "and the Son" (Filioque) for 1:1 with fixed Latin

## German prayer audit 2026-08-10
Audited all DE rosary + extras against DBK/Vatican DE/EÜ.
FIXED: sign-of-the-cross (no commas), hail-holy-queen (Wonne/Vatican text), rosary-prayer P3 order, psalm-23 EÜ1980 wording, psalm-51 MD synced to JSON.
OK: apostles-creed, our-father, hail-mary, glory-be, fatima, jesus-prayer, nicene.
Audio regenerated for fixed JSON text prayers.

---

## Chinese prayer audit (2026-08-10)

Audited Traditional Chinese rosary/extras against CRBC Taiwan, Vatican News zht, Legion of Mary HK, and Sigao Bible.

FIXED:
- nicene: Filioque 由聖父聖子所共發; 賦與; 亞孟->阿們
- hail-holy-queen: 甘貽->甘飴; appended 阿們 to last segment
- jesus-prayer: 你->祢 for address to God
- psalm-23: aligned to Sigao (心靈得到舒暢 / 名號的原由 / 凶險 / 安慰舒暢)
- psalm-51: 除淨。->除淨， per Sigao punctuation
- apostles-creed: phonetic 衪 Qí->Tā only

OK (no text change): sign-of-the-cross, our-father, hail-mary, glory-be, fatima (LoM HK form), rosary-prayer, apostles-creed body (Vatican News zht continuous form)

Audio regenerated for fixed prayers via generate-rosary-audio.py.

## Polish prayer audit (2026-08-10)
Audited ora/docs/polish against KEP 2020 unified texts + Biblia Tysiąclecia + traditional creed.
Fixed: our-father (ode złego), hail-mary (Twojego), fatima (KEP wording), hail-holy-queen (Witaj/synowie Ewy/Twojego), nicene (Filioque, dnia trzeciego), psalm-23 (BT), punctuation on several. Regenerated audio. Removed orphan hail-holy-queen-4c.mp3.

---

## Portuguese prayer audit (2026-08-10)

Form used: Brazilian Portuguese (BP) official/devotional Catholic sources, consistent with `pt-BR-FranciscaNeural` voice.

Sources:
- Vatican News PT orações (Pai Nosso, Ave Maria, Glória, Credo, Salve Rainha)
- Canção Nova / Santuário do Pai das Misericórdias (terço pages)
- Santuário de Fátima (fatima.pt) for Oração de Fátima
- Legion of Mary Portuguese for rosary closing (Ó Deus, cujo Filho Unigênito...)
- Traditional liturgical Portuguese for psalms (with BP orthography: retos, hão de)

Notes:
- Apostles Creed keeps traditional "desceu aos infernos" (EN "hell"; ES/FR same traditional form). Modern Missal PT often "mansão dos mortos".
- Nicene omits Filioque in segment 11c to match EN/ES/FR/LA passage structure (official Vatican News PT has "e do Filho").
- Glory Be keeps "pelos séculos dos séculos" for EN "world without end" (Canção Nova short form omits it).
- Fatima keeps "da vossa misericórdia" for EN passage 4 meaning; core wording from Santuário de Fátima "levai as almas todas para o Céu".

---

## Japanese prayer audit (2026-08-10)

Audited all Japanese rosary prayers under `ora/docs/japanese/` against CBCJ / Tokyo Archdiocese / 新共同訳 sources. Fixed JSON + MD + regenerated audio (ja-JP-KeitaNeural). Orphan mp3s removed where segment ids changed (hail-mary-3c, hail-holy-queen-5c/6d, psalm-51-8c).

Key official sources:
- CBCJ アヴェ・マリア: https://www.cbcj.catholic.jp/2011/06/14/5759/
- CBCJ ニケア: https://www.cbcj.catholic.jp/2004/02/18/7451/
- Tokyo 祈りのガイド: https://tokyo.catholic.jp/religious-life/prayer-guide/
- Compendium 元后あわれみの母 (CBCJ 2010)
- 新共同訳 for psalms


---

## Greek rosary prayer audit (2026-08-10)

Audited all 12 Greek rosary/extra prayers against Byzantine / Greek Catholic / LXX sources.

**Display convention:** TTS-safe monotonic Greek in `text` (edge-tts); Latin-script modern pronunciation in `phonetic`; `tts.input` = `text`.

**Key source fixes:**
- Sign of the Cross: `Εν ονόματι` → official `Εις το όνομα` (Mt 28:19 / GOARCH baptism).
- Our Father: accents + official liturgical forms (Orthodox Prayer / Matthew).
- Glory Be: Eastern Byzantine form kept (`και νυν και αεί...`, no Western "sicut erat").
- Psalm 23 (LXX 22): `καταδιώξει`, added `με` in cup line, nu-movable cleanup (septuagint.bible).
- Nicene: Byzantine Πιστεύω form, no Filioque; kept `Θεόν εκ Θεού` for EN passage alignment (Nicaea 325 / Latin).
- Hail Holy Queen / Rosary / Fatima: Latin-origin learned Koine polish (accents, grammar); no single Byzantine official.

Audio regenerated for all 12. Letter-spelling detector: 0 FLAG.


---

## Full prayer audit (2026-08-10)

12 language subagents audited all rosary + extras prayers against official Catholic sources (Vatican / national bishops / liturgical books). Method: exact official text first, then best-effort passage/segment alignment (same as Chinese Hail Mary).

### Critical cross-cutting fix: Nicene Filioque
Catholic languages now include Filioque (EN, LA, FR, DE, IT, ES, PL, PT, ZH, JA, VI). Greek correctly omits (Byzantine form).

### Highest-impact language fixes (selected)
- **EN**: Fatima wording; Nicene Filioque
- **LA**: Fatima *animas*; Genetrix; Nicene Filioque + *exspecto*
- **ZH**: HHQ 甘飴 + Amen; Jesus Prayer 祢; Nicene Filioque; Sigao Ps 23/51
- **FR**: Notre Père 2017; Hail Mary grâce + pauvres pécheurs; full CEF Salut ô Reine; Filioque
- **DE**: Salve *unsre Wonne*; Sign of Cross commas; EÜ Ps 23
- **EL**: Sign formula Εις το όνομα; Salve *συνήγορος*; Oremus; LXX Ps 23; all audio regen; Eastern Glory Be kept
- **IT**: CEI Our Father (*non abbandonarci*); Ave o Maria; CEI psalms
- **JA**: CBCJ Hail Mary word order; Glory Be rewrite; Fatima colloquial; HHQ 元后; Filioque; 新共同訳 psalms
- **PL**: KEP *ode złego*; Fatima KEP; *Witaj Królowo*; Filioque
- **PT**: BP orthography; Fatima fatima.pt; Filioque restored post-audit
- **ES**: Misal ES Apostles Creed; Our Father *a nosotros*; Filioque
- **VI**: Vatican News forms; Filioque; CGKPV psalms

### Intentional language differences
- Greek Glory Be: Byzantine (no "sicut erat in principio")
- Greek Nicene: no Filioque
- Fatima / Jesus Prayer / Rosary collect: regional variants; best official/common form chosen
- Psalms: track local Catholic Bible (KJV/DRA EN, Vulgate LA, Sigao ZH, AELF FR, CEI IT, 新共同訳 JA, BT PL, CGKPV VI, etc.)


---

## Greek audio sync (2026-08-10)

Two fixes for karaoke desync (Glory Be and other Greek prayers):

1. **Timing silence handling** in `generate-rosary-audio.py`: during pauses after periods, keep highlight on the previous segment until the next words start (do not jump highlight into silence).
2. **Optional segment `tts` override**: Edge `el-GR-NestorasNeural` holds **αεί** ~1.25–1.8s. Glory Be 2b keeps display `και αεί` but sends `και αείι` to TTS (natural length). Regenerated all non-mystery Greek prayer audio with the new timing logic.
