#!/usr/bin/env python3
"""
Audio generator for rosary prayers.

The JSON structure (with passages and segments) is the source of truth.
Generates three levels (full, per-passage, per-segment) unless suppressed.

Filenames are derived by convention from the "id" in the JSON:
- full: {id}.mp3
- passage: {id}-{passage_id}.mp3
- segment: {id}-{passage_segment_id}.mp3

Optional "filenameOverride" (string) may appear at top level (full), on a passage object, or on a segment.
If a non-empty string, it is used as the exact output filename instead.
If "" (empty) or false, that level's file output is suppressed entirely.

After generation the script also derives per-segment start/end times (in seconds)
from WordBoundary events on the full and passage renders (only for non-suppressed levels),
then writes "timing": {"full": [start, end], "passage": [start, end]} into each segment in the JSON.

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
    if len(sys.argv) < 2 or len(sys.argv) > 3 or (len(sys.argv) == 3 and sys.argv[2] != "--timings-only"):
        print("Usage: python audio-utils/generate-rosary-audio.py <path/to/prayer.json> [--timings-only]")
        print("  --timings-only : update only the timing data in the JSON (skip writing audio files)")
        sys.exit(1)

    json_path = sys.argv[1]
    timings_only = len(sys.argv) == 3 and sys.argv[2] == "--timings-only"
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
    passage_fo = {}            # passage_id -> filenameOverride or None
    segment_fo = {}            # sid -> filenameOverride or None

    for p in jdata.get("passages", []):
        pid = str(p.get("passage_id"))
        passage_order.append(pid)
        p_fo = p.get("filenameOverride")
        passage_fo[pid] = p_fo
        p_segs = []
        for seg in p.get("segments", []):
            sid = seg.get("passage_segment_id")
            if not sid:
                print(f"Missing passage_segment_id in passage {pid}")
                continue
            txt = get_segment_text(seg, tts_input)
            s_fo = seg.get("filenameOverride")
            segment_fo[sid] = s_fo
            segment_list.append((sid, txt))
            p_segs.append((sid, txt))
        passage_segments[pid] = p_segs

    if not segment_list:
        print("No segments found")
        sys.exit(1)

    out_dir = os.path.dirname(os.path.abspath(json_path))

    mode = " (timings only)" if timings_only else ""
    print(f"Generating from {json_path} using voice={voice} rate={rate} input={tts_input}{mode} ...")

    def get_output_filename(key, override):
        """Return filename or None if suppressed."""
        if override is not None:
            if override == "" or override is False:
                return None
            return str(override)
        if key == "full":
            return f"{prayer_id}.mp3"
        else:
            return f"{prayer_id}-{key}.mp3"

    async def generate(key, text, filename_override=None):
        """Plain save (used for individual segments)."""
        if timings_only:
            return
        fname = get_output_filename(key, filename_override)
        if fname is None:
            return
        out_path = os.path.join(out_dir, fname)
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(out_path)
        print(f"  -> {out_path}")

    async def generate_timed(key, segs_for_this, lang="", filename_override=None):
        """Generate audio from joined seg texts + return {sid: [start, end]} from WordBoundary."""
        if not segs_for_this:
            return {}
        fname = get_output_filename(key, filename_override)
        if fname is None:
            return {}
        if lang in ("chinese", "japanese"):
            joined = "".join(txt for _, txt in segs_for_this)
        else:
            joined = " ".join(txt for _, txt in segs_for_this)
        out_path = os.path.join(out_dir, fname)

        communicate = edge_tts.Communicate(joined, voice, rate=rate, boundary="WordBoundary")
        audio_chunks = []
        word_events = []
        async for msg in communicate.stream():
            if msg["type"] == "audio":
                if not timings_only:
                    audio_chunks.append(msg["data"])
            elif msg["type"] == "WordBoundary":
                offset = msg.get("offset", 0)
                dur = msg.get("duration", 0)
                word_events.append({
                    "text": msg.get("text", ""),
                    "start": offset / 10_000_000.0,
                    "end": (offset + dur) / 10_000_000.0
                })
        if not timings_only:
            audio_bytes = b"".join(audio_chunks)
            with open(out_path, "wb") as f:
                f.write(audio_bytes)
            print(f"  -> {out_path}")
        else:
            print(f"  (timings only) {out_path}")

        return assign_segment_timings(word_events, segs_for_this, lang, joined_text=joined)

    def count_units(txt, lang=""):
        if not txt:
            return 0
        if lang in ("chinese", "japanese"):
            # Count CJK chars (hanzi, kana) - matches WordBoundary granularity for text input.
            # Exclude separators like ・ (middle dot) because TTS WordBoundary omits them from reported text.
            chars = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff\u3040-\u309f\u30a0-\u30ff]', txt)
            return sum(1 for c in chars if c != '・')
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

    def assign_segment_timings(word_events, segs, lang="", joined_text=None):
        """Use actual WordBoundary events to derive per-segment [start, end] that match the spoken audio.
        We map each segment's unit count (words for English/romance/etc, chars for CJK/Greek) onto the
        sequence of reported boundary events and take the real start/end times of the covering events.
        Then post-process so ranges are abutted at the actual start-of-next-segment times and first
        segment starts at 0.0 (so highlight appears as soon as playback begins).
        This gives precise segment-level sync without assuming uniform rate.
        """
        if not word_events or not segs:
            return {}
        n = len(word_events)
        if n == 0:
            return {}
        total_units = sum(count_units(txt, lang) for _, txt in segs)
        if total_units <= 0:
            return {}
        timings = {}
        # cum units: len(btext) for CJK/greek, 1 per event for word-based languages
        cum_units = [0]
        for ev in word_events:
            if lang in ("chinese", "japanese", "greek"):
                delta = len(ev.get('text', '') or '')
            else:
                delta = 1
            cum_units.append(cum_units[-1] + delta)
        pos = 0
        for sid, txt in segs:
            u = count_units(txt, lang)
            sstart = pos
            send = pos + u
            pos += u
            k_start = 0
            for k in range(1, n+1):
                if cum_units[k] > sstart:
                    k_start = k-1
                    break
            k_end = n-1
            for k in range(k_start, n+1):
                if cum_units[k] >= send:
                    k_end = k-1
                    break
            if k_end < k_start:
                k_end = k_start
            st = word_events[k_start]['start']
            et = word_events[k_end]['end']
            if cum_units[k_start] < sstart < cum_units[k_start+1]:
                bstart = cum_units[k_start]
                bend = cum_units[k_start+1]
                frac = (sstart - bstart) / (bend - bstart) if (bend - bstart) > 0 else 0
                st = word_events[k_start]['start'] + frac * (word_events[k_start]['end'] - word_events[k_start]['start'])
            if cum_units[k_end] < send < cum_units[k_end+1]:
                bstart = cum_units[k_end]
                bend = cum_units[k_end+1]
                frac = (send - bstart) / (bend - bstart) if (bend - bstart) > 0 else 0
                et = word_events[k_end]['start'] + frac * (word_events[k_end]['end'] - word_events[k_end]['start'])
            timings[sid] = [round(max(0, st), 3), round(et, 3)]
        # Post-process:
        # - first segment always starts at 0.0
        # - each segment's highlight range ends at its own spoken end (when its audio actually finishes)
        # - the following segment's range starts immediately at the previous segment's spoken end
        # This means: as soon as the current segment's audio finishes, the highlight advances
        # to the *next* segment right away (even during any silence/pause before the next words begin).
        # This moves the learner's attention forward promptly instead of lingering on finished text.
        ordered = [sid for sid, _ in segs]
        if ordered:
            timings[ordered[0]][0] = 0.0
            for i in range(len(ordered) - 1):
                prev_end = timings[ordered[i]][1]  # spoken end of previous
                timings[ordered[i+1]][0] = prev_end
            # ends stay at each segment's raw spoken end
            # last keeps its spoken end
        return timings

    # 1. Generate every segment (plain, no intra-segment timing needed)
    if not timings_only:
        for sid, txt in segment_list:
            fo = segment_fo.get(sid)
            await generate(sid, txt, fo)

    # 2. Passages (timed synthesis for natural audio + accurate segment ranges relative to passage file)
    passage_timings = {}
    for pid in passage_order:
        p_segs = passage_segments[pid]
        p_fo = passage_fo.get(pid)
        p_t = await generate_timed(pid, p_segs, lang, p_fo)
        passage_timings[pid] = p_t

    # 3. Full (timed synthesis)
    full_segs = []
    for pid in passage_order:
        full_segs.extend(passage_segments[pid])
    full_fo = jdata.get("filenameOverride")
    full_timings = await generate_timed("full", full_segs, lang, full_fo)

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
