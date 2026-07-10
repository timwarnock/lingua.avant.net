# Audio Utils

This directory contains the script for generating audio MP3 files from JSON input using Microsoft Edge TTS (via the `edge-tts` package).

## Setup

```bash
uv pip install edge-tts
```

(You may use a virtual environment. `uv` makes this straightforward.)

List all available voices:

```bash
edge-tts --list-voices
```

Or with uv: `uvx edge-tts --list-voices`

## Usage

The generator is driven entirely by a JSON file.

```bash
python audio-utils/generate-rosary-audio.py path/to/prayer.json
```

With uv (no separate install step required):

```bash
uv run --with edge-tts python audio-utils/generate-rosary-audio.py path/to/prayer.json
```

### Required JSON structure

The JSON must contain at minimum:

```json
{
  "id": "prayer-name",
  "tts": {
    "voice": "en-US-AvaNeural",
    "rate": "-5%",
    "input": "phonetic"
  },
  "passages": [
    {
      "passage_id": 1,
      "segments": [
        { "passage_segment_id": "1a", "text": "Display text.", "phonetic": "Phonetic text." }
      ]
    }
  ]
}
```

- `"id"`: base name used for all output files.
- `"tts.voice"`: **required**.
- `"tts.rate"`: optional (defaults to `+0%`).
- `"tts.input"`: optional, either `"phonetic"` (default) or `"text"`. Determines which field is sent to TTS.
- `passages`: array of objects. Each must have `passage_id` and a `segments` array.
- Every segment must have a `passage_segment_id` (always lettered form e.g. `"1a"`, even for single-segment passages), plus `"text"` and `"phonetic"`.
- Optional `"filenameOverride"` (string) at top level, on a passage, or on a segment: overrides the output filename for that level. Use `""` (empty) or false to suppress output for the level entirely (no file and no associated timings).

### What gets generated

For a JSON with id `"hail-mary"`, the script produces (next to the JSON):

- `hail-mary.mp3` -- full concatenation of all segments
- `hail-mary-1.mp3`, `hail-mary-2.mp3`, ... -- one per passage (concatenation of segments in that passage)
- `hail-mary-1a.mp3`, `hail-mary-1b.mp3`, ... -- one per segment

Filenames are derived directly from `"id"`, `passage_id`, and `passage_segment_id` unless overridden by `"filenameOverride"` (see above). Suppressed levels produce no file.

After generation, commit the `.mp3` files.

## Controlling pronunciation

edge-tts accepts plain text only (no SSML or IPA). Adjust pronunciation by editing the string passed to it.

- Edit the `"phonetic"` field (or `"text"` if using `input: "text"`).
- Re-run the generator on the JSON to update the affected files.
- Test the specific segment, passage, and full MP3s.
- Common respelling example for two-syllable "blessed": use `"blessid"` (not `"bless-ed"`).
- Punctuation inside the phonetic string can influence prosody (e.g. adding a comma before "Amen").

See `generate-rosary-audio.py` for exact behavior.

## Script notes

- The script walks the `passages` and `segments` in order.
- It always generates the full set: all segments, then all passages, then the full prayer.
- Output directory is the directory containing the input JSON.
- Requires the JSON to be valid; missing required fields will cause an error.

Last updated: 2026-06-28

## Greek TTS (required workflow)

Edge Greek voices (`el-GR-NestorasNeural`) need **TTS-safe** `text`:

- Use **monotonic** Greek (modern stress accents OK); avoid dense polytonic paste-ins.
- Drop mid-dot / ano teleia (`·` / `·`); use comma or period.
- Expand elisions (`δι'` → `δια`, `ἀπ'` → `από`, …).
- Keep `tts.input` = `"text"`. Put learner Latin-script help only in `"phonetic"`.

After every Greek audio generate, scan for letter-spelling (voices reading δέλτα, γιώτα, … instead of words):

```bash
uv run --with edge-tts python audio-utils/generate-rosary-audio.py ora/docs/greek/.../prayer.json
uv run --with edge-tts python audio-utils/detect-greek-letter-spelling.py ora/docs/greek/.../prayer.json
uv run --with edge-tts python audio-utils/detect-greek-letter-spelling.py --all
uv run --with edge-tts python audio-utils/detect-greek-letter-spelling.py --all --fresh-tts
```

- **FLAG** = likely letter-spelling (high seconds-per-letter and seconds-per-syllable). Fix `text`, regenerate, re-scan.
- **WARN** = slow / suspicious; check short segments by ear (Amen holds and padding can warn without letter-spelling).

See also `notes-agents.md` section **Greek prayer text and TTS**.
