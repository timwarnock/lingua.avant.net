#!/usr/bin/env python3
"""
Audio generator for rosary prayers.

The JSON structure (with passages and segments) is the source of truth.
We always generate three levels exhaustively:
- full (concatenation of all segments)
- one per passage (concatenation of segments in that passage)
- one per passage_segment

Filenames are derived by convention from the "id" in the JSON:
- full: {id}.mp3
- passage: {id}-{passage_id}.mp3
- segment: {id}-{passage_segment_id}.mp3

Usage:
  python audio-utils/generate-rosary-audio.py ora/docs/latin/our-father/our-father.json

The JSON must contain at minimum:
  "id": "our-father",
  "tts": {
    "voice": "it-IT-DiegoNeural",
    "rate": "-15%",
    "input": "phonetic"   # default "phonetic". Set to "text" for languages like Chinese.
  },
  "passages": [
    {
      "passage_id": 1,
      "segments": [
        { "passage_segment_id": "1a", "text": "...", "phonetic": "..." },
        ...
      ]
    },
    ...
  ]

Every passage has one or more segments.
Segment ids are always in the form "Xa" (e.g. "2a" even if the passage has only one segment).
No special casing for single-segment passages.
"""

import asyncio
import edge_tts
import json
import os
import sys


def get_segment_text(seg, tts_input):
    if tts_input == "text":
        return seg.get("text") or seg.get("phonetic", "")
    else:
        return seg.get("phonetic") or seg.get("text", "")


async def main():
    if len(sys.argv) != 2:
        print("Usage: python audio-utils/generate-rosary-audio.py <path/to/prayer.json>")
        sys.exit(1)

    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"JSON not found: {json_path}")
        sys.exit(1)

    with open(json_path, encoding="utf-8") as f:
        jdata = json.load(f)

    tts = jdata.get("tts", {})
    voice = tts.get("voice")
    rate = tts.get("rate", "+0%")
    if not voice:
        print("JSON must contain tts.voice")
        sys.exit(1)

    prayer_id = jdata.get("id")
    if not prayer_id:
        print("JSON must contain 'id'")
        sys.exit(1)

    tts_input = tts.get("input", "phonetic")

    # Walk the structure to collect segments in order and per-passage groups
    segment_list = []          # list of (passage_segment_id, text)
    passage_order = []
    passage_groups = {}        # passage_id -> list of texts

    for p in jdata.get("passages", []):
        pid = str(p.get("passage_id"))
        passage_order.append(pid)
        p_texts = []
        for seg in p.get("segments", []):
            sid = seg.get("passage_segment_id")
            if not sid:
                print(f"Missing passage_segment_id in passage {pid}")
                continue
            txt = get_segment_text(seg, tts_input)
            segment_list.append((sid, txt))
            p_texts.append(txt)
        passage_groups[pid] = p_texts

    if not segment_list:
        print("No segments found")
        sys.exit(1)

    out_dir = os.path.dirname(os.path.abspath(json_path))

    print(f"Generating from {json_path} using voice={voice} rate={rate} input={tts_input} ...")

    async def generate(key, text):
        if key == "full":
            filename = f"{prayer_id}.mp3"
        else:
            filename = f"{prayer_id}-{key}.mp3"
        out_path = os.path.join(out_dir, filename)
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(out_path)
        print(f"  -> {out_path}")

    # 1. Generate every segment
    for sid, txt in segment_list:
        await generate(sid, txt)

    # 2. Generate every passage (concat of its segments)
    for pid in passage_order:
        txt = " ".join(passage_groups[pid])
        await generate(pid, txt)

    # 3. Generate full (concat of all)
    all_texts = []
    for pid in passage_order:
        all_texts.extend(passage_groups[pid])
    full_text = " ".join(all_texts)
    await generate("full", full_text)

    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
