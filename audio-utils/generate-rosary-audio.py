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

After generation the script also derives per-segment start/end times (in seconds)
from WordBoundary events on the full and passage renders, then writes
"timing": {"full": [start, end], "passage": [start, end]} into each segment in the JSON.

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
import re
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

    lang = jdata.get("lang", "")
    tts_input = tts.get("input", "phonetic")

    # Walk the structure to collect segments in order and per-passage groups
    segment_list = []          # list of (passage_segment_id, text) for all
    passage_order = []
    passage_segments = {}      # passage_id -> list of (sid, text)  -- preserves order

    for p in jdata.get("passages", []):
        pid = str(p.get("passage_id"))
        passage_order.append(pid)
        p_segs = []
        for seg in p.get("segments", []):
            sid = seg.get("passage_segment_id")
            if not sid:
                print(f"Missing passage_segment_id in passage {pid}")
                continue
            txt = get_segment_text(seg, tts_input)
            segment_list.append((sid, txt))
            p_segs.append((sid, txt))
        passage_segments[pid] = p_segs

    if not segment_list:
        print("No segments found")
        sys.exit(1)

    out_dir = os.path.dirname(os.path.abspath(json_path))

    print(f"Generating from {json_path} using voice={voice} rate={rate} input={tts_input} ...")

    async def generate(key, text):
        """Plain save (used for individual segments)."""
        if key == "full":
            filename = f"{prayer_id}.mp3"
        else:
            filename = f"{prayer_id}-{key}.mp3"
        out_path = os.path.join(out_dir, filename)
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(out_path)
        print(f"  -> {out_path}")

    async def generate_timed(key, segs_for_this, lang=""):
        """Generate audio from joined seg texts + return {sid: [start, end]} from WordBoundary."""
        if not segs_for_this:
            return {}
        if lang in ("chinese", "japanese"):
            joined = "".join(txt for _, txt in segs_for_this)
        else:
            joined = " ".join(txt for _, txt in segs_for_this)
        if key == "full":
            filename = f"{prayer_id}.mp3"
        else:
            filename = f"{prayer_id}-{key}.mp3"
        out_path = os.path.join(out_dir, filename)

        communicate = edge_tts.Communicate(joined, voice, rate=rate, boundary="WordBoundary")
        audio_chunks = []
        word_events = []
        async for msg in communicate.stream():
            if msg["type"] == "audio":
                audio_chunks.append(msg["data"])
            elif msg["type"] == "WordBoundary":
                offset = msg.get("offset", 0)
                dur = msg.get("duration", 0)
                word_events.append({
                    "text": msg.get("text", ""),
                    "start": offset / 10_000_000.0,
                    "end": (offset + dur) / 10_000_000.0
                })
        audio_bytes = b"".join(audio_chunks)
        with open(out_path, "wb") as f:
            f.write(audio_bytes)
        print(f"  -> {out_path}")

        return assign_segment_timings(word_events, segs_for_this, lang)

    def count_units(txt, lang=""):
        if not txt:
            return 0
        if lang in ("chinese", "japanese"):
            # Count CJK chars (hanzi, kana) - matches WordBoundary granularity for text input
            return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff\u3040-\u309f\u30a0-\u30ff]', txt))
        elif lang == "greek":
            # Count Greek letters (including polytonic range) for better alignment with WordBoundary events
            return len(re.findall(r'[\u0370-\u03FF\u1F00-\u1FFF]', txt))
        else:
            tokens = []
            for w in txt.split():
                w = w.strip(".,;:!?\"'()[]—–-，。、；：！？“”‘’")
                if w:
                    tokens.append(w)
            return len(tokens)

    def assign_segment_timings(word_events, segs, lang=""):
        """Proportional assignment based on unit counts (chars for CJK/Greek, words else).
        Uses actual spoken end time from boundaries so timings cover the synthesis exactly.
        This fixes misalignment and missing timings that caused desync.
        """
        if not word_events or not segs:
            return {}
        total_time = word_events[-1]["end"] if word_events else 0
        total_units = sum(count_units(txt, lang) for _, txt in segs)
        if total_units <= 0:
            return {}
        timings = {}
        current = 0.0
        for sid, txt in segs:
            units = count_units(txt, lang)
            dur = (units / total_units) * total_time if total_units > 0 else 0
            timings[sid] = [round(current, 3), round(current + dur, 3)]
            current += dur
        if timings:
            # ensure last exactly matches the last boundary end
            last_sid = segs[-1][0]
            timings[last_sid][1] = round(total_time, 3)
        return timings

    # 1. Generate every segment (plain, no intra-segment timing needed)
    for sid, txt in segment_list:
        await generate(sid, txt)

    # 2. Passages (timed synthesis for natural audio + accurate segment ranges relative to passage file)
    passage_timings = {}
    for pid in passage_order:
        p_segs = passage_segments[pid]
        p_t = await generate_timed(pid, p_segs, lang)
        passage_timings[pid] = p_t

    # 3. Full (timed synthesis)
    full_segs = []
    for pid in passage_order:
        full_segs.extend(passage_segments[pid])
    full_timings = await generate_timed("full", full_segs, lang)

    # Inject the derived timings back into the JSON (so player can use them)
    for p in jdata.get("passages", []):
        pid = str(p.get("passage_id"))
        for seg in p.get("segments", []):
            sid = seg.get("passage_segment_id")
            if not sid:
                continue
            t = {}
            if sid in full_timings:
                t["full"] = full_timings[sid]
            if pid in passage_timings and sid in passage_timings[pid]:
                t["passage"] = passage_timings[pid][sid]
            if t:
                seg["timing"] = t

    # Write updated JSON (preserves original order and other fields)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(jdata, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("Updated JSON with segment timings (full + passage).")

    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
