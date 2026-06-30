# Prayer Player Plan (prayer.mjs)

## Purpose
This document captures the design and implementation of the interactive rosary prayer player for language learning on lingua.avant.net.

The player turns each rosary prayer into a rich, audio-enabled, per-passage learning tool while keeping the site simple, maintainable, and aligned with the Zensical content model.

## Guiding Principles
- Interactive experience is the **primary** content for language learners.
- Static Markdown text serves only as a **fallback** (no-JS, JS error, or very old browsers).
- Content is data-driven via JSON so it can power future features (side-by-side languages, top-level multi-lingual app, etc.).
- Passages are aligned 1:1 across every language.
- Segments follow the alignment rule below.
- Keep everything simple, direct, and co-located with the prayer content.
- Use full lowercase English directory names (e.g. `latin/`, not `la/`).
- Do not centralize everything under `assets/`.

## Core Concepts

### Passages (1:1 across languages)
Every prayer is broken into passages identified by passage_id (numeric). English defines the specific passages and breaks for each prayer. Other languages use the same passage_ids for 1:1 alignment.

The passage_id ensures the high-level structure matches exactly between languages.

### Segments
A passage consists of one or more segments.

Segments are the lowest-level, atomic, uniquely addressable units of text.

- Every segment has a unique "passage_segment_id" within the prayer (e.g. "1a", "1b", "2"). These are unique across all segments.
- Segments within a passage are lettered (a, b, c...); the full passage_segment_id combines passage and segment letter for clarity and uniqueness.
- Each segment carries two distinct fields:
  - "text": the proper written form for display — correct spelling, grammar, traditional punctuation and presentation as it should appear in the prayer (used to assemble the main passage text lines in the player).
  - "phonetic": the pronunciation form. This is fed to TTS for audio generation (default tts.input="phonetic") and displayed in the clickable sub-segments/chunks. It may (and frequently will for better learning audio) differ from "text" to achieve correct pronunciation (e.g. "blessid" for two-syllable "blessed", adjusted punctuation for prosody such as commas before "Amen", etc.). Proper display spelling/grammar lives in "text"; phonetic prioritizes how it should sound.
- Given the full list of segments (with their passage_segment_ids), the passages and the full prayer text can be reconstructed.

Alignment rule (English is the source of truth):
Passages are the hard 1:1 rule across languages (via numeric passage_id).
Segments should match the English reference. Due to linguistic and grammatical differences they may not match perfectly. Aim to match English. When not a perfect match, aim for equal segment counts. Different segment counts are rare and require explicit approval (as it violates the goal of matching segments perfectly).

There is no independent content on a passage object itself — passages are only groupings of their segments under the passage_id. passage_id is kept explicitly for clarity and self-documenting even if derivable from the passage_segment_ids.

### JSON as the source of truth for interactivity
Each prayer page loads a sibling JSON file that describes:
- Passages (by numeric ID; English defines the structure)
- Segments under each passage (atomic units with unique passage_segment_id, "text" for proper display form, and "phonetic" for pronunciation/TTS form)

Audio is derived automatically from the segment structure (no separate audio map in JSON). Filenames follow convention. The Markdown file remains human-readable and contains the traditional plain text only as fallback.

### Companion directory layout
For a prayer page `english/hail-mary.md`, assets live in a matching companion directory:

```
ora/docs/english/hail-mary.md
ora/docs/english/hail-mary/
  hail-mary.json
  hail-mary.mp3          (when recorded)
```

This keeps data next to the content that owns it. Relative references are straightforward once the page is rendered under directory URLs.

The same pattern will be used for every prayer in every language:
- `english/our-father/our-father.json`
- `latin/hail-mary/hail-mary.json`
- etc.

### Audio model (per-segment files)
The JSON structure (passages + segments) is the complete source of truth.

We always generate three levels of MP3s exhaustively:
- full (concatenation of all segments in order)
- one per passage (concatenation of the segments belonging to that passage_id)
- one per passage_segment

No separate "audio" map exists in the JSON. Filenames are derived by convention from the prayer id and the identifiers (full, passage_id, passage_segment_id).

The generator walks the passages/segments directly and derives content for full and passages by concatenation. Only segments hold the actual text and phonetic.

- Files live in the companion directory next to the JSON (e.g. `english/hail-mary/hail-mary.mp3`, `english/hail-mary/hail-mary-1a.mp3`, etc.)
- Filenames are derived by convention (e.g. `hail-mary.mp3` for full, `hail-mary-1a.mp3` for segment); no "audio" map in the JSON.
- No timing offsets are stored or needed — the player simply plays the appropriate file for each segment.

Audio is produced using Microsoft Edge TTS via the `edge-tts` Python package (see `audio-utils/` for the generation script and notes). This approach was chosen for simplicity, reliability, and to avoid manual timing work.

The canonical generation tooling lives in `audio-utils/` (not inside `ora/` or the Zensical content tree).

### Text and Phonetic on segments
Every segment has both, with clearly distinct purposes:
- "text": the proper written form for display — correct spelling, grammar, traditional punctuation and presentation as it should appear in the prayer. This is used to assemble the main passage text lines shown in the player (and can be used in fallbacks).
- "phonetic": the pronunciation form for TTS and learning. This is the string passed to the TTS engine (when tts.input="phonetic", the default) and what appears in the clickable phonetic chunks below each passage. It is explicitly allowed (and expected for English and similar) to differ from "text" to achieve correct pronunciation (e.g. "blessid" instead of "Blessed"), or "...death," in phonetic only to produce natural "death, Amen" flow in audio while "text" keeps proper "death.".

TTS uses the field specified in tts.input ("phonetic" by default, or "text" for languages like Chinese where the written form is sufficient).

The main passage lines in the UI use "text". The phonetic sub-chunks are the clickable units using "phonetic".

Segments are the units that are clickable for playback.

### Text and Phonetic for Koine Greek
Greek uses Koine Greek (the ancient form from the New Testament and early Church, as used in official Catholic/Byzantine Greek liturgical sources).

- "text": authentic Koine Greek script (polytonic where traditional for the source text). This is the proper display form and the input sent to TTS.
- "phonetic": practical learner-friendly pronunciation guide in Latin script using **modern Greek pronunciation** applied to the Koine text (how the prayers are actually recited today in Greek Catholic and Orthodox traditions).

**tts.input setting:** Always set `"input": "text"` for Greek (so edge-tts receives the native Greek script for natural audio, exactly as done for Chinese and Japanese).

**Custom phonetic guide rules (use these explicitly and consistently):**
- Base spelling on modern Greek sound values for Koine letters:
  - α = a, ε = e, η/ι/υ/ει/οι = ee (or i), ο/ω = o, ου = oo, υ before consonants sometimes y.
  - β = v, γ = g (or y before e/i sounds), δ = th (as in "this"), θ = th (as in "thin"), χ = ch (as in Scottish "loch").
  - ζ = z, ξ = ks, ψ = ps.
- Indicate primary stress with acute accent on the stressed syllable (e.g. Pá-ter, Ma-rí-a).
- Use hyphens sparingly only for clarity on long words if needed; prefer space-separated syllables where it aids learners.
- Preserve punctuation from the "text" only when it helps prosody (e.g. commas before "Amen" in some cases).
- Example for Hail Mary opening:
  - text: "Χαῖρε, Μαρία, κεχαριτωμένη,"
  - phonetic: "Ché-re, Ma-rí-a, ke-cha-ri-to-mé-ni,"
- Follow the same passage structure as English (1:1 passages with identical meaning per passage_id; English defines the breakdown). Segments follow the alignment rule in Core Concepts.
- Source the Koine text from official Catholic Greek sources (e.g. traditional Byzantine/Greek Catholic liturgical forms of the prayers).
- When generating audio, use an appropriate el-GR voice with input="text". Tune only the "phonetic" display values for learner clarity; do not alter "text".

This keeps consistency across languages: non-Latin scripts use native script in "text" + pronunciation aid in "phonetic".

### Actionable Steps for Phonetic Spellings with edge-tts (English reference)
edge-tts (Microsoft Edge TTS backend) does not support custom <phoneme> SSML or IPA input. Pronunciation control is achieved exclusively through plain-text respelling in the string passed to TTS.

When the default written form does not produce the desired liturgical or natural pronunciation:
1. Edit **only** the "phonetic" value for the segment (never alter "text" for display purposes).
2. Apply a respelled version of the word/phrase. Verified working pattern for the two-syllable liturgical "blessed":
   - Glued spelling: "blessid"
   Note: "bless-ed" does not work (produces "bless Ed" or similar).
3. Include any needed punctuation inside the phonetic string for better prosody/flow (e.g. comma before "Amen" in phonetic only).
4. Run `python audio-utils/generate-rosary-audio.py <path-to-json>` to rebuild the affected segment, passage, and full audio files.
5. Test the specific segment audio (and full prayer) with the target voice.
6. Iterate on the spelling string until the output matches the intended pronunciation. Document the final respelling in the English JSON.

If the issue is the voice itself rather than specific words, use `ora/docs/audio-testing/` to quickly compare multiple voices (including cross-language tests) instead of editing main content.

Use English as the reference standard for passage and segment structure. For English prayers, tune the "phonetic" values using the respelling techniques below for natural liturgical delivery. For other languages, follow the alignment rule in Core Concepts, then tune their own "phonetic" values.

## Markdown Page Structure

```markdown
---
icon: material/cross
---

# Hail Mary

<div class="prayer-interactive"
     data-prayer="hail-mary"
     data-json="hail-mary.json"></div>

<div class="prayer-fallback" markdown="1">

**English**

Hail Mary, full of grace, the Lord is with thee. Blessed art thou amongst women, and blessed is the fruit of thy womb, Jesus. Holy Mary, Mother of God, pray for us sinners, now and at the hour of our death. Amen.

</div>
```

- The `.prayer-interactive` div is the **main** experience.
- `.prayer-fallback` contains the original static bilingual text.
- This is the default content (graceful degradation).
- Only after `prayer.mjs` successfully renders the interactive player does it hide `.prayer-fallback`.
- If JavaScript never runs or fails before reaching the hide, the fallback content remains visible by default. No JS code is responsible for showing the fallback.

## Data Model (JSON)

Passages use a numeric ID for 1:1 cross-language alignment. English defines the actual passage and segment structure for each prayer.

Each passage groups one or more segments.

Segments are the atomic units and carry unique "passage_segment_id", plus "text" and "phonetic".

Minimal example structure (English Hail Mary):

```json
{
  "id": "hail-mary",
  "lang": "english",
  "title": "Hail Mary",
  "tts": {
    "voice": "en-US-AvaNeural",
    "rate": "-5%",
    "input": "phonetic"
  },
  "passages": [
    {
      "passage_id": 1,
      "segments": [
        { "passage_segment_id": "1a", "text": "Hail Mary,", "phonetic": "Hail Mary," },
        { "passage_segment_id": "1b", "text": "full of grace,", "phonetic": "full of grace," },
        { "passage_segment_id": "1c", "text": "the Lord is with thee.", "phonetic": "the Lord is with thee." }
      ]
    },
    {
      "passage_id": 2,
      "segments": [
        { "passage_segment_id": "2a", "text": "Blessed art thou amongst women,", "phonetic": "blessid art thou amongst women," },
        { "passage_segment_id": "2b", "text": "and blessed is the fruit of thy womb,", "phonetic": "and blessid is the fruit of thy womb," },
        { "passage_segment_id": "2c", "text": "Jesus.", "phonetic": "Jesus." }
      ]
    }
  ]
}
```

Every passage has one or more segments. passage_segment_id always uses letter suffix (e.g. "2a" even for single-segment passages). No special cases. The structure itself drives audio generation and playback.
Amen is placed in its own final passage (for better readability in the UI). The actual passages and breaks for each prayer are defined in the English JSON.

## UX (as implemented)

- Title area has a small play button → plays the full prayer.
- Each passage shows its segments.
- Main passage lines use the proper "text" (display form). Phonetic pronunciation chunks (using "phonetic") are shown below and are clickable to play their audio segment.
- Light visual highlight on the currently playing unit.
- Very minimal buttons. The content itself is the main interaction surface.
- Designed to be mobile-friendly and non-intrusive.

The plain Markdown text above/below is no longer presented as a "Practice" section — it is purely fallback content.

## Implementation Files

- `ora/docs/assets/prayer.mjs` — the player logic (auto-inits on `.prayer-interactive` elements; derives audio filenames from structure)
- `ora/docs/stylesheets/extra.css` — minimal supporting styles (`.prayer-interactive`, `.play-btn`, `.prayer-chunk`, `.playing`, etc.)
- `ora/zensical.toml` — lists `assets/prayer.mjs` in `extra_javascript`
- Per-prayer JSON (passages + segments define everything; no audio map) + generated MP3s in the companion folder

## How to Add Content

### New prayer in an existing language
1. Create the Markdown page following the structure above (title + interactive div + fallback div).
2. Create the companion folder and `prayer-slug.json`. Use the exact passage_ids from the English version of that prayer (English is the source of truth for the passage breakdown and meaning). Follow the alignment rule in Core Concepts for segments.
   - Group segments under each passage_id.
   - Every segment has a unique "passage_segment_id", "text" (proper display form), and "phonetic" (pronunciation/TTS form; may differ from text for correct audio).
3. Use the script in `audio-utils/generate-rosary-audio.py` to generate the MP3s (full + per passage + per passage_segment). The generator walks the structure directly. For any needed pronunciation adjustments in English, follow the "Actionable Steps for Phonetic Spellings with edge-tts" section.
4. Add the page to navigation in `zensical.toml` if needed.

### New language
1. Create the language directory (e.g. `polski/`).
2. For each core prayer, create the `.md` + companion `prayer-slug/` folder + JSON.
3. Copy the exact passage_ids from the English version of that prayer (English is the source of truth for the structure). Provide the language-specific "text" and "phonetic" for each segment, following the alignment rule in Core Concepts.
4. Run `audio-utils/generate-rosary-audio.py` with the appropriate voice for that language (respecting tts.input). Tune "phonetic" values using the respelling steps in the dedicated section above.

## Pilot Status (as of 2026-06-28)
- English Hail Mary is implemented as the reference (structure and phonetics).
- Audio is generated with Microsoft Edge TTS (see `audio-utils/`).
- Other languages follow the passage and segment structure from the corresponding English JSON.
- Static text is preserved inside `.prayer-fallback` (hidden on successful player render).
- Audio generation tooling lives in `audio-utils/` (outside the Zensical `ora/` tree).

## Future Work (from original TODOs)
- Enhance all rosary prayers with this structure.
- Add audio for the entire set of prayers.
- Build the top-level multi-lingual rosary app on the home page that can switch languages while using the same JSON-driven passages.

## Notes for Future Sessions
- English defines the passage_ids and segment structure for each prayer. Other languages follow the alignment rule in Core Concepts. passage_segment_id values (e.g. "1a", "1b") are unique within a prayer. Segments within a passage use a, b, c... letters.
- The companion directory pattern (`lang/prayer/`) is preferred over centralizing in `assets/`.
- Do not introduce two-letter language codes in paths or data unless explicitly decided later.
- The Markdown static text should not be presented as the main view — it is fallback only.
- When adding new features to `prayer.mjs`, keep the UI minimal and the controls integrated into the segment text and phonetic.
- Test that the fallback still appears when the module fails (temporarily break the JSON path to verify).
- Every segment must have both "text" and "phonetic". Content lives on segments.
- For edge-tts pronunciation fixes in English (the reference), follow the actionable steps in the "Actionable Steps for Phonetic Spellings with edge-tts" section above: edit only "phonetic" with respelling, regenerate, test, iterate.
- Audio generation code and notes live in `audio-utils/`. Do not put Python/generation scripts inside the `ora/` (Zensical) content tree.
- `ora/scripts/` has been removed.

This document (plan-prayer-mjs.md) should be kept up to date as the implementation evolves.

**Clarification on fields (as of English Hail Mary work):**  
"text" = proper written form for display (spelling, grammar, traditional presentation).  
"phonetic" = pronunciation form for TTS input + clickable chunks (may differ from text for correct liturgical audio and learning).  

Follow the "Actionable Steps for Phonetic Spellings with edge-tts" section for respelling techniques when tuning English (the reference). Any prior notes suggesting text and phonetic must match or that adjustments go in "text" have been removed.