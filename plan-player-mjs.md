# Prayer Player Plan (prayer.mjs)

## Purpose
This document captures the design and implementation of the interactive rosary prayer player for language learning on lingua.avant.net.

The player turns each rosary prayer into a rich, audio-enabled, per-passage learning tool while keeping the site simple, maintainable, and aligned with the Zensical content model.

## Guiding Principles
- Interactive experience is the **primary** content for language learners.
- Static Markdown text serves only as a **fallback** (no-JS, JS error, or very old browsers).
- Content is data-driven via JSON so it can power future features (side-by-side languages, top-level multi-lingual app, etc.).
- Passages are aligned 1:1 across every language.
- Sub-passages are mostly aligned (best-effort for grammar/order differences in languages like Chinese or Vietnamese).
- Keep everything simple, direct, and co-located with the prayer content.
- Use full lowercase English directory names (e.g. `latin/`, not `la/`).
- Do not centralize everything under `assets/`.

## Core Concepts

### Passages (1:1 across languages)
Every prayer is broken into passages identified by passage_id (numeric). These passages have direct semantic equivalents across languages for 1:1 alignment.

The passage_id ensures the high-level structure matches exactly between languages.

### Segments
A passage consists of one or more segments.

Segments are the lowest-level, atomic, uniquely addressable units of text.

- Every segment has a unique "passage_segment_id" within the prayer (e.g. "1a", "1b", "2"). These are unique across all segments.
- Segments within a passage are lettered (a, b, c...); the full passage_segment_id combines passage and segment letter for clarity and uniqueness.
- Each segment carries two distinct fields:
  - "text": the proper written form for display — correct spelling, grammar, traditional punctuation and presentation as it should appear in the prayer (used to assemble the main passage text lines in the player).
  - "phonetic": the pronunciation form. This is fed to TTS for audio generation (default tts.input="phonetic") and displayed in the clickable sub-segments/chunks. It may (and frequently will for better learning audio) differ from "text" to achieve correct pronunciation (e.g. "blessid" for two-syllable "blessed", adjusted punctuation for prosody such as commas before "Amen", etc.). Proper display spelling/grammar lives in "text"; phonetic prioritizes how it should sound.
- The number and ordering of segments within a passage can differ between languages due to grammar and linguistic structure.
- Given the full list of segments (with their passage_segment_ids), the passages and the full prayer text can be reconstructed.

There is no independent content on a passage object itself — passages are only groupings of their segments under the passage_id. passage_id is kept explicitly for clarity and self-documenting even if derivable from the passage_segment_ids.

### JSON as the source of truth for interactivity
Each prayer page loads a sibling JSON file that describes:
- Passages (by numeric ID for cross-language alignment)
- Segments under each passage (atomic units with unique id, "text" for proper display form, and "phonetic" for pronunciation/TTS form)

Audio is derived automatically from the segment structure (no separate audio map in JSON). Filenames follow convention. The Markdown file remains human-readable and contains the traditional plain text only as fallback.

### Companion directory layout
For a prayer page `latin/hail-mary.md`, assets live in a matching companion directory:

```
ora/docs/latin/hail-mary.md
ora/docs/latin/hail-mary/
  hail-mary.json
  hail-mary.mp3          (when recorded)
```

This keeps data next to the content that owns it. Relative references are straightforward once the page is rendered under directory URLs.

The same pattern will be used for every prayer in every language:
- `english/our-father/our-father.json`
- `chinese/hail-mary/hail-mary.json`
- etc.

### Audio model (per-segment files)
The JSON structure (passages + segments) is the complete source of truth.

We always generate three levels of MP3s exhaustively:
- full (concatenation of all segments in order)
- one per passage (concatenation of the segments belonging to that passage_id)
- one per passage_segment

No separate "audio" map exists in the JSON. Filenames are derived by convention from the prayer id and the identifiers (full, passage_id, passage_segment_id).

The generator walks the passages/segments directly and derives content for full and passages by concatenation. Only segments hold the actual text and phonetic.

- Files live in the companion directory next to the JSON (e.g. `latin/hail-mary/hail-mary.mp3`, `latin/hail-mary/hail-mary-1a.mp3`, etc.)
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

Use English as the reference standard. For new prayers or languages, first match passage and segment counts, then tune the "phonetic" values (using the same respelling techniques where needed) to align with the English liturgical delivery.

## Markdown Page Structure

```markdown
---
icon: material/cross
---

# Ave Maria

<div class="prayer-interactive"
     data-prayer="hail-mary"
     data-json="hail-mary.json"></div>

<div class="prayer-fallback">
  <!-- Traditional plain text goes here -->
  **Latin**
  ...

  **English**
  ...
</div>
```

- The `.prayer-interactive` div is the **main** experience.
- `.prayer-fallback` contains the original static bilingual text.
- This is the default content (graceful degradation).
- Only after `prayer.mjs` successfully renders the interactive player does it hide `.prayer-fallback`.
- If JavaScript never runs or fails before reaching the hide, the fallback content remains visible by default. No JS code is responsible for showing the fallback.

## Data Model (JSON)

Passages use a numeric ID for 1:1 cross-language alignment.

Each passage groups one or more segments.

Segments are the atomic units and carry unique "id", plus "text" and "phonetic".

Minimal example structure:

```json
{
  "id": "hail-mary",
  "lang": "latin",
  "title": "Ave Maria",
  "tts": {
    "voice": "it-IT-DiegoNeural",
    "rate": "-15%",
    "input": "phonetic"
  },
  "passages": [
    {
      "passage_id": 1,
      "segments": [
        { "passage_segment_id": "1a", "text": "Ave Maria,", "phonetic": "Ave Maria," },
        { "passage_segment_id": "1b", "text": "gratia plena,", "phonetic": "gratia plena," },
        { "passage_segment_id": "1c", "text": "Dominus tecum.", "phonetic": "Dominus tecum." }
      ]
    },
    {
      "passage_id": 2,
      "segments": [
        { "passage_segment_id": "2a", "text": "Benedicta tu in mulieribus, et benedictus fructus ventris tui, Iesus.", "phonetic": "..." }
      ]
    }
  ]
}
```

Every passage has one or more segments. segment ids always use letter suffix (e.g. "2a" even for single-segment passages). No special cases. The structure itself drives audio generation and playback.
Amen is always placed in its own final passage (for better readability in the UI).

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
2. Create the companion folder and `prayer-slug.json` with the same passage_id used in other languages.
   - Group segments under each passage_id.
   - Every segment has a unique "passage_segment_id", "text" (proper display form), and "phonetic" (pronunciation/TTS form; may differ from text for correct audio).
3. Use the script in `audio-utils/generate-rosary-audio.py` to generate the MP3s (full + per passage + per passage_segment). The generator walks the structure directly. For any needed pronunciation adjustments in English (the reference), follow the "Actionable Steps for Phonetic Spellings with edge-tts" section.
4. Add the page to navigation in `zensical.toml` if needed.

### New language
1. Create the language directory (e.g. `polski/`).
2. For each core prayer, create the `.md` + companion `prayer-slug/` folder + JSON.
3. For each passage (by passage_id), provide the segments (unique "passage_segment_id", "text" for proper display, and "phonetic" for pronunciation/TTS which may differ to achieve correct spoken form). Segment structure can vary for linguistic reasons.
4. Use the exact same passage_id as the reference language.
5. Run `audio-utils/generate-rosary-audio.py` with the appropriate voice for that language (respecting tts.input). Tune "phonetic" values to align with English reference using the respelling steps in the dedicated section above.

## Pilot Status (as of 2026-06-28)
- Latin Hail Mary (`latin/hail-mary.md`) is the first implemented prayer.
- Audio is generated with Microsoft Edge TTS (see `audio-utils/`).
- Multiple voices have been tested for Latin (primarily Italian proxies; also multilingual and other Romance languages).
- Static bilingual text is preserved inside `.prayer-fallback` (hidden on successful player render).
- Audio generation tooling lives in `audio-utils/` (outside the Zensical `ora/` tree).
- Restructuring in progress to match the correct model: passages by passage_id, segments as atomic units with unique passage_segment_id + text + phonetic.

## Future Work (from original TODOs)
- Enhance all rosary prayers with this structure.
- Add audio for the entire set of prayers.
- Build the top-level multi-lingual rosary app on the home page that can switch languages while using the same JSON-driven passages.

## Notes for Future Sessions
- Always keep passage_id stable across languages for 1:1 alignment. passage_segment_id values (e.g. "1a", "1b") are unique within a prayer but can differ in count and order between languages. Segments within a passage use a, b, c... letters.
- The companion directory pattern (`lang/prayer/`) is preferred over centralizing in `assets/`.
- Do not introduce two-letter language codes in paths or data unless explicitly decided later.
- The Markdown static text should not be presented as the main view — it is fallback only.
- When adding new features to `prayer.mjs`, keep the UI minimal and the controls integrated into the segment text and phonetic.
- Test that the fallback still appears when the module fails (temporarily break the JSON path to verify).
- Every segment must have both "text" and "phonetic". Content lives on segments.
- For edge-tts pronunciation fixes (English reference), follow the actionable steps in the "Actionable Steps for Phonetic Spellings with edge-tts" section above: edit only "phonetic" with respelling, regenerate, test, iterate.
- Audio generation code and notes live in `audio-utils/`. Do not put Python/generation scripts inside the `ora/` (Zensical) content tree.
- `ora/scripts/` has been removed.

This document (plan-player-mjs.md) should be kept up to date as the implementation evolves.

**Clarification on fields (as of English Hail Mary work):**  
"text" = proper written form for display (spelling, grammar, traditional presentation).  
"phonetic" = pronunciation form for TTS input + clickable chunks (may differ from text for correct liturgical audio and learning).  

Follow the "Actionable Steps for Phonetic Spellings with edge-tts" section for respelling techniques when tuning English (the reference). Any prior notes suggesting text and phonetic must match or that adjustments go in "text" have been removed.