# Audio Utils for Rosary Prayer Audio Generation

This directory contains the tooling and notes for generating audio for the rosary prayers used in the language-learning site.

## Goals
- High-quality, natural-sounding audio for every prayer in every supported language.
- Full prayer + per-passage + per-sub-passage audio so the interactive player (see `prayer.mjs`) can offer fine-grained playback.
- No manual timing/offset work — we use separate small MP3 files per segment.
- Reproducible and documented so future sessions (or humans) can continue the work easily.

## Current Approach (as of 2026-06-28)

We use **Microsoft Edge TTS** via the free `edge-tts` Python package.

- One full prayer MP3.
- Separate MP3s for every passage and sub-passage (defined in the prayer JSON).
- Files live alongside the JSON in the "companion folder":
  `ora/docs/<lang>/<prayer-id>/`

This makes playback trivial in the web player (just `new Audio(src).play()` per segment) and avoids having to maintain precise timestamps in JSON.

### Text vs Phonetic for Audio
The JSON distinguishes roles clearly:
- "text": proper written/display form (spelling, grammar, traditional punctuation). Used for the main lines in the player.
- "phonetic": the form passed to TTS (and shown in clickable chunks). This may differ from "text" to achieve correct pronunciation and natural flow (e.g. "blessid" for two-syllable "blessed"). Note: "bless-ed" does not work (produces "bless Ed"). Punctuation tweaks like commas for pauses before "Amen" in the phonetic only.

Adjustments for better TTS prosody go in the "phonetic" field. "text" keeps the proper traditional written form for display.

## Setup

```bash
pip install edge-tts
```

(You can also use a virtualenv.)

To list all available voices:
```bash
edge-tts --list-voices
```

## Usage

The generator is now a simple app driven entirely by the JSON (the single source of truth).

```bash
python audio-utils/generate-rosary-audio.py ora/docs/latin/hail-mary/hail-mary.json
```

The JSON (current model) contains passages/segments with "text" (proper display) and "phonetic" (TTS/pronunciation form, which may differ).
The generator derives full/passage/segment audio texts from the "phonetic" fields (or "text" per tts.input) and writes all MP3s next to the JSON.
No "full", "audio" map, or other legacy fields are used.

After generation, commit the new `.mp3` files.

## Voice Selection

### Latin (Liturgical / Ecclesiastical)
There are **no native Latin voices** in Edge TTS (322 voices total, none with `la-` or "Latin").

Italian voices are the closest phonetically because ecclesiastical Latin pronunciation is based on modern Italian.

**Italian voices tested (in rough order):**
- `it-IT-ElsaNeural` (Female) — early test
- `it-IT-GiuseppeMultilingualNeural` (Male)
- `it-IT-IsabellaNeural` (Female) — felt noticeably better / smoother
- `it-IT-DiegoNeural` (Male) — also good, maybe slightly better in some passages

None are perfect "liturgical Latin" — they can sound a bit robotic in places. The flow is generally acceptable for language learning.

**Other contenders identified by scanning all languages (worth testing):**
- Portuguese (Portugal) — strong Catholic tradition, clear vowels:
  - `pt-PT-DuarteNeural` (Male)
  - `pt-PT-RaquelNeural` (Female)
- Spanish (Spain / Castilian):
  - `es-ES-AlvaroNeural` (Male)
  - `es-ES-ElviraNeural` (Female)
- Multilingual voices (often handle Latin words/phrasing more naturally because they are trained for language switching):
  - `en-US-AndrewMultilingualNeural` (Male)
  - `en-US-BrianMultilingualNeural` (Male)
  - `en-US-AvaMultilingualNeural` (Female)

Recommendation order for Latin right now (2026-06-28):
1. English multilingual voices (e.g. en-US-AndrewMultilingualNeural) — often cleanest phrasing for Latin text.
2. Portuguese Portugal (pt-PT-DuarteNeural / RaquelNeural).
3. Castilian Spanish (es-ES-AlvaroNeural / ElviraNeural).
4. Italian voices (limited to 4; tested Elsa, Isabella, GiuseppeMultilingual, Diego).

Latest test: en-US-AndrewMultilingualNeural (generated 2026-06-28).

### Other Languages
Voice is specified per-prayer in the JSON under `tts.voice` (see current English examples). Choose natural neural voices per language.

## Adding a New Prayer (current JSON-driven model)

No changes needed in the generator script. Create the prayer's .md + companion folder + JSON with proper passages/segments ("text" for display, "phonetic" for TTS — they may differ).

Run the generator on the JSON. It derives everything from the segment "phonetic" (or "text") fields.

Update Markdown fallback if desired.

## Adding a New Language

1. Create the language directory.
2. For each core prayer, create the .md + companion folder + JSON (using same passage_ids and segment counts as the English reference where possible).
3. In the JSON, specify `tts.voice` and populate "text" (proper display form) + "phonetic" (may differ for pronunciation).
4. Generate audio using the script on the JSON.

## File Layout

```
audio-utils/
  README.md
  generate-rosary-audio.py
  (future helpers, voice logs, etc.)

ora/docs/<lang>/<prayer-id>/
  <prayer-id>.json
  <prayer-id>.mp3
  <prayer-id>-1.mp3
  <prayer-id>-1a.mp3
  ...

ora/docs/assets/prayer.mjs   ← the player that uses the audio
```

## Notes & History

- `ora/scripts/` has been deleted. All audio generation code and notes now live in `audio-utils/` (outside the Zensical `ora/` content tree) to avoid confusion.

- Per-segment files were chosen over a single MP3 + timestamps because:
  - Much simpler and more reliable playback.
  - No need to maintain or debug timing data.
  - Learners can easily repeat tiny phrases.

- Adjustments for TTS (e.g. punctuation or respelling for prosody) are placed only in the "phonetic" field of the segment. The "text" field always keeps the proper traditional written form for display in the player. See current English Hail Mary for examples of differences (e.g. "blessid" works for two-syllable "blessed"; "bless-ed" does not). Comma before Amen in phonetic only.

- Early testing showed that simply changing voices often gave bigger quality jumps than tweaking text or rate.

- For truly excellent liturgical Latin, real human recordings (or specialized tools like eSpeak with custom Latin rules) are superior. Within the free neural options we have here, we're looking for the "least bad" that still sounds pleasant and useful for language learning.

## Related Files

- `ora/docs/assets/prayer.mjs` — the interactive player
- `plan-player-mjs.md` — overall design notes for the player system
- `ora/docs/latin/hail-mary/hail-mary.json` — current example data + audio references

## Future Work Ideas

- Add support for SSML in the generator for finer prosody control on difficult phrases.
- Script to batch-generate for all languages + all prayers.
- Voice preference overrides per prayer (some prayers may sound better in a different voice).
- Explore other free/high-quality TTS backends if edge-tts quality plateaus for certain languages.

---

Last updated: 2026-06-28 (text vs phonetic roles clarified per English standard)
