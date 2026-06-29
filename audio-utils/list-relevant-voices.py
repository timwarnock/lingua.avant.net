#!/usr/bin/env python3
"""
Helper to list voices that have been identified as good candidates
for rosary prayer audio, especially Latin.

Usage:
  python audio-utils/list-relevant-voices.py

Requires: uv pip install edge-tts (or pip)
"""

import asyncio
import edge_tts

async def main():
    voices = await edge_tts.list_voices()
    print("=== Current recommended voices for rosary audio (2026-06-28) ===\n")

    # Latin / Italian
    print("Latin (using Italian voices as ecclesiastical proxy):")
    italian = [v for v in voices if v["Locale"].startswith("it-")]
    for v in sorted(italian, key=lambda x: x["ShortName"]):
        print(f"  {v['ShortName']} ({v['Gender']})")

    # Portuguese Portugal
    print("\nPortuguese (Portugal) - strong contender:")
    pt = [v for v in voices if v["Locale"] == "pt-PT"]
    for v in pt:
        print(f"  {v['ShortName']} ({v['Gender']})")

    # Spanish Spain
    print("\nSpanish (Spain) - strong contender:")
    es = [v for v in voices if v["Locale"] == "es-ES"]
    for v in es:
        print(f"  {v['ShortName']} ({v['Gender']})")

    # Multilingual (good for Latin phrasing)
    print("\nMultilingual voices (often handle Latin text cleanly):")
    multi = [v for v in voices if "Multilingual" in v["ShortName"]]
    for v in sorted(multi, key=lambda x: x["ShortName"]):
        print(f"  {v['ShortName']} ({v['Locale']}, {v['Gender']})")

    print("\nTip: Use `edge-tts --list-voices` for the complete list of 300+ voices.")
    print("See audio-utils/README.md for testing notes and why these were chosen.")

asyncio.run(main())
