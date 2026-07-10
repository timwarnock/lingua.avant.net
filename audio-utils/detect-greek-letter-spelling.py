#!/usr/bin/env python3
"""
Detect Edge TTS "letter spelling" on Greek prayer segments.

When the Greek neural voices (e.g. el-GR-NestorasNeural) do not recognize a
token, they often read letter *names* (δέλτα, γιώτα, όμικρον, ταυ, ...).
That is far slower per character than real word reading.

Heuristic:
  - Measure MP3 duration (existing file next to the JSON, or fresh TTS).
  - Count Greek letters in the TTS input text.
  - Flag high seconds-per-letter (and high seconds-per-syllable estimate).

Usage:
  python audio-utils/detect-greek-letter-spelling.py [path/to/prayer.json ...]
  python audio-utils/detect-greek-letter-spelling.py --all
  python audio-utils/detect-greek-letter-spelling.py --all --fresh-tts

Exit code 1 if any segment is flagged.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import edge_tts
except ImportError:
    edge_tts = None

GREEK_LETTER_RE = re.compile(r"[Α-Ωα-ωΆ-ώΪΫϊϋΰΐἈ-Ῥἀ-ῷ]")
ROOT = Path(__file__).resolve().parents[1]
GREEK_DOCS = ROOT / "ora" / "docs" / "greek"

# Empirically: real speech ~0.06–0.14 s/letter; letter-name spelling often >0.35 s/letter
# on short tokens. Use dual thresholds so long clean phrases are not false-positives.
SEC_PER_LETTER_FLAG = 0.28
SEC_PER_LETTER_WARN = 0.18
# Short segments (few letters) spelling is especially obvious
SHORT_LETTER_COUNT = 8
SHORT_SEC_PER_LETTER_FLAG = 0.35
# Amen is often held / slow in prayer audio -- not letter-spelling
AMEN_RE = re.compile(r"^\s*ἀμήν\.?\s*$", re.I)
AMEN_RE2 = re.compile(r"^\s*αμήν\.?\s*$", re.I)
# Letter-name spelling is also slow per *syllable* (~0.6–1.0s/syl). Normal speech ~0.2–0.35s/syl.
SEC_PER_SYLLABLE_FLAG = 0.55
# Edge TTS MP3s include leading/trailing silence; subtract before ratios so short
# segments (e.g. "και νυν", "Αμήν.") are not false-flagged.
PADDING_SEC = 0.85


def greek_letter_count(text: str) -> int:
    return len(GREEK_LETTER_RE.findall(text))


def estimate_syllables(text: str) -> int:
    """Rough Modern Greek syllable estimate: count vowel letters / diphthongs."""
    t = text.lower()
    # collapse common diphthongs to one unit
    for d in ("αι", "ει", "οι", "υι", "αυ", "ευ", "ου", "ηυ"):
        t = t.replace(d, "V")
    vowels = set("αεηιουωάέήίόύώϊϋΰΐvV")
    return max(1, sum(1 for c in t if c in vowels))


def mp3_duration(path: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(r.stdout.strip())


def tts_input_for_segment(seg: dict, tts: dict) -> str:
    mode = (tts or {}).get("input", "phonetic")
    if mode == "text":
        return seg.get("text") or seg.get("phonetic") or ""
    return seg.get("phonetic") or seg.get("text") or ""


async def fresh_duration(text: str, voice: str, rate: str) -> float:
    if edge_tts is None:
        raise RuntimeError("edge-tts not installed; use existing MP3s or pip install edge-tts")
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        tmp = Path(f.name)
    try:
        await edge_tts.Communicate(text, voice, rate=rate).save(str(tmp))
        return mp3_duration(tmp)
    finally:
        tmp.unlink(missing_ok=True)


def classify(text: str, n_letters: int, n_syllables: int, duration: float) -> str:
    if n_letters <= 0 or duration <= 0:
        return "skip"
    # Liturgical Amen is drawn out on purpose
    if AMEN_RE.match(text) or AMEN_RE2.match(text) or text.strip() in {"Αμήν.", "Αμην.", "ἀμήν.", "ΑΜΗΝ."}:
        return "ok"
    # Use padding-adjusted duration for density ratios
    effective = max(duration - PADDING_SEC, 0.05)
    spl = effective / n_letters
    sps = effective / max(1, n_syllables)
    # Strong flag: both slow per letter and slow per syllable (letter names are multi-syllabic)
    if n_letters <= SHORT_LETTER_COUNT and spl >= SHORT_SEC_PER_LETTER_FLAG and sps >= SEC_PER_SYLLABLE_FLAG:
        return "FLAG"
    if spl >= SEC_PER_LETTER_FLAG and sps >= SEC_PER_SYLLABLE_FLAG:
        return "FLAG"
    if spl >= SEC_PER_LETTER_WARN or sps >= 0.45:
        return "WARN"
    return "ok"


def iter_prayer_jsons(paths: list[Path] | None, all_greek: bool) -> list[Path]:
    if all_greek:
        out = []
        for p in sorted(GREEK_DOCS.rglob("*.json")):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
            if "passages" in data and "tts" in data:
                out.append(p)
        return out
    return paths or []


async def scan_file(path: Path, fresh_tts: bool) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    tts = data.get("tts", {})
    voice = tts.get("voice", "el-GR-NestorasNeural")
    rate = tts.get("rate", "+0%")
    prayer_id = data.get("id") or path.stem
    base = path.parent
    rows = []

    for p in data.get("passages", []):
        for seg in p.get("segments", []):
            sid = seg.get("passage_segment_id", "?")
            text = tts_input_for_segment(seg, tts)
            n_let = greek_letter_count(text)
            n_syl = estimate_syllables(text)
            mp3 = base / f"{prayer_id}-{sid}.mp3"
            duration = None
            source = None
            if fresh_tts:
                duration = await fresh_duration(text, voice, rate)
                source = "fresh-tts"
            elif mp3.is_file():
                duration = mp3_duration(mp3)
                source = "mp3"
            else:
                if edge_tts is None:
                    rows.append(
                        {
                            "file": str(path),
                            "sid": sid,
                            "status": "skip",
                            "reason": "no mp3 and no edge-tts",
                            "text": text,
                        }
                    )
                    continue
                duration = await fresh_duration(text, voice, rate)
                source = "fresh-tts-fallback"

            spl = duration / n_let if n_let else 0.0
            sps = duration / n_syl if n_syl else 0.0
            status = classify(text, n_let, n_syl, duration)
            rows.append(
                {
                    "file": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                    "sid": sid,
                    "status": status,
                    "duration": round(duration, 3),
                    "letters": n_let,
                    "syllables": n_syl,
                    "sec_per_letter": round(spl, 3),
                    "sec_per_syllable": round(sps, 3),
                    "source": source,
                    "text": text,
                }
            )
    return rows


async def main_async(args: argparse.Namespace) -> int:
    paths = [Path(p) for p in (args.paths or [])]
    files = iter_prayer_jsons(paths, args.all)
    if not files:
        print("No prayer JSON files to scan.", file=sys.stderr)
        return 2

    all_rows = []
    for f in files:
        print(f"Scanning {f} ...", flush=True)
        all_rows.extend(await scan_file(f, args.fresh_tts))

    flags = [r for r in all_rows if r["status"] == "FLAG"]
    warns = [r for r in all_rows if r["status"] == "WARN"]
    oks = [r for r in all_rows if r["status"] == "ok"]

    def show(title, rows):
        if not rows:
            return
        print(f"\n=== {title} ({len(rows)}) ===")
        for r in sorted(rows, key=lambda x: -x.get("sec_per_letter", 0)):
            print(
                f"  {r['status']:4} {r.get('sec_per_letter', 0):5.3f}s/let  "
                f"{r.get('duration', 0):5.2f}s  L={r.get('letters', 0):2}  "
                f"{r['file']}#{r['sid']}"
            )
            print(f"       {r.get('text', '')!r}")

    show("FLAG likely letter-spelling", flags)
    show("WARN slow / suspicious", warns)
    print(f"\nSummary: {len(flags)} FLAG, {len(warns)} WARN, {len(oks)} ok, {len(all_rows)} total")

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(all_rows, ensure_ascii=False, indent=2) + "\n")
        print(f"Wrote {args.json_out}")

    return 1 if flags else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="*", help="Prayer JSON paths")
    ap.add_argument("--all", action="store_true", help=f"Scan all prayer JSON under {GREEK_DOCS}")
    ap.add_argument(
        "--fresh-tts",
        action="store_true",
        help="Re-synthesize each segment with edge-tts instead of using existing MP3s",
    )
    ap.add_argument("--json-out", help="Write full results JSON")
    args = ap.parse_args()
    raise SystemExit(asyncio.run(main_async(args)))


if __name__ == "__main__":
    main()
