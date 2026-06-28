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

### Text Smoothing for Audio
Some punctuation is adjusted during generation for better flow and rhythm (especially important for Latin prayers).

Example for Hail Mary:
- Display / JSON text: "Ave Maria, gratia plena..."
- Audio generation text: "Ave Maria, gratia plena..." (comma after "Ave" removed)

The traditional punctuation is kept in the JSON `phonetic` fields and the Markdown fallback so the learner sees the proper written form.

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

The JSON must contain:
- `voice`
- `rate`
- `full` (text for the complete prayer audio)
- `passages` (each with required `phonetic`)
- `audio` (map of segment id → filename)

All audio files (full + per passage/sub) are written next to the JSON.
No text copies live in the Python code.

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
See the `VOICE_MAP` in `generate-rosary-audio.py`. These were chosen as high-quality, natural-sounding neural voices.

## Adding a New Prayer

1. Add an entry to the `PRAYERS` dict in this script.
   - `"full"`: the complete text.
   - `"segments"`: exact breaks that match the JSON (stable IDs across languages).
2. Run the generator for each language.
3. Update the prayer's JSON `audio` section with the new filenames.
4. Update the language's Markdown fallback if desired (it is only shown if JS fails).
5. **"phonetic" is required on every passage** in the .json (and on subs when present). Example leaf passage:

```json
{ "n": 2, "phonetic": "Adveniat regnum tuum." }
```

This guarantees a phonetic line is always rendered. (Will matter more when we have cleaner phonetics for Latin too.)

## Adding a New Language

1. Add the language directory name and a good voice to `VOICE_MAP`.
2. Create the prayer Markdown + JSON (copy structure from an existing language).
3. Generate audio.
4. Fill in the phonetic text in the JSON (this is what the player displays and makes clickable).

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

- The comma after "Ave" in "Ave, Maria" consistently produced an awkward pause in every Italian voice tested. We therefore generate that segment (and the full text) without it for audio, while keeping the comma in the visible text.

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

Last updated: 2026-06-28
