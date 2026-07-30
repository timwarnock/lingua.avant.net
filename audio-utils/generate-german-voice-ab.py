#!/usr/bin/env python3
"""Generate German Edge TTS male-voice A/B samples and index.md for audio-testing.

Prefer de-DE male voices; also includes de-AT and de-CH males for comparison.
Writes only web content into ora/docs/audio-testing/ (mp3 + index.md).

Run from repo root:

  uv run --with edge-tts python audio-utils/generate-german-voice-ab.py
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import edge_tts

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "ora" / "docs" / "audio-testing"

# Male Edge voices for German (de-DE primary; AT/CH for contrast).
VOICES: list[tuple[str, str]] = [
    ("de-DE-ConradNeural", "conrad"),
    ("de-DE-KillianNeural", "killian"),
    ("de-DE-FlorianMultilingualNeural", "florian"),
    ("de-AT-JonasNeural", "jonas-at"),
    ("de-CH-JanNeural", "jan-ch"),
]

# Rates used elsewhere on the site cluster around -5%; include neighbors.
RATES: list[str] = ["+0%", "-5%", "-10%"]

# First two Hail Mary passages (aligned with English passage 1 and 2).
# Standard German Catholic wording for Gegrüßet seist du, Maria.
SAMPLES: list[dict] = [
    {
        "id": "hm1",
        "title": "Hail Mary passage 1",
        "source": "Gegrüßet seist du, Maria -- passage 1 "
        "(EN: Hail Mary, full of grace, the Lord is with thee.)",
        "text": "Gegrüßet seist du, Maria, voll der Gnade, der Herr ist mit dir.",
    },
    {
        "id": "hm2",
        "title": "Hail Mary passage 2",
        "source": "Gegrüßet seist du, Maria -- passage 2 "
        "(EN: Blessed art thou amongst women, and blessed is the fruit of thy womb, Jesus.)",
        "text": (
            "Du bist gebenedeit unter den Frauen, "
            "und gebenedeit ist die Frucht deines Leibes, Jesus."
        ),
    },
]


def slug_rate(rate: str) -> str:
    # "+0%" -> "0", "-5%" -> "m5", "-10%" -> "m10"
    s = rate.strip().replace("%", "")
    if s.startswith("+"):
        s = s[1:]
    if s.startswith("-"):
        return "m" + s[1:]
    return s


def play_span(filename: str, label: str) -> str:
    return (
        f'<span onclick="new Audio(\'{filename}\').play()" '
        f'style="cursor:pointer; text-decoration:underline">'
        f"<strong>{label}</strong></span>"
    )


def render_md() -> str:
    lines: list[str] = [
        "# German Edge TTS -- male voices",
        "",
        "Qualitative listen tests for **Deutsch** Rosary audio. Prefer a clear "
        "male voice suitable for prayer (not rushed, not theatrical).",
        "",
        "**Voices** (male only):",
        "",
    ]
    for voice, slug in VOICES:
        lines.append(f"+ `{voice}` -- slug **{slug}**")
    lines.extend(
        [
            "",
            f"**Rates:** {', '.join(f'`{r}`' for r in RATES)}",
            "",
            "Each section is a short real prayer line. Play variants and note "
            "the winning voice + rate.",
            "",
            "Regenerate samples:",
            "",
            "```bash",
            "uv run --with edge-tts python audio-utils/generate-german-voice-ab.py",
            "```",
            "",
        ]
    )

    for i, sample in enumerate(SAMPLES, 1):
        lines.append("---")
        lines.append("")
        lines.append(f"## {i}. {sample['title']}")
        lines.append("")
        lines.append(f"**Source:** {sample['source']}")
        lines.append("")
        lines.append(f"**Text:** `{sample['text']}`")
        lines.append("")
        lines.append("**Variants** (click label to play):")
        lines.append("")
        for voice, vslug in VOICES:
            for rate in RATES:
                rslug = slug_rate(rate)
                fn = f"{sample['id']}-{vslug}-{rslug}.mp3"
                label = f"{vslug} @ {rate}"
                lines.append(f"+ {play_span(fn, label)} -- `{voice}` rate `{rate}`")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Checklist")
    lines.append("")
    lines.append("| # | Sample | Winner voice | Rate | Notes |")
    lines.append("|---|--------|--------------|------|-------|")
    for i, sample in enumerate(SAMPLES, 1):
        lines.append(f"| {i} | {sample['title']} |  |  |  |")
    lines.append("")
    lines.append("**Overall pick:** voice `______` rate `______`")
    lines.append("")

    return "\n".join(lines)


async def generate_all() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.mp3"):
        old.unlink()

    jobs: list[tuple[Path, str, str, str]] = []
    for sample in SAMPLES:
        for voice, vslug in VOICES:
            for rate in RATES:
                rslug = slug_rate(rate)
                path = OUT / f"{sample['id']}-{vslug}-{rslug}.mp3"
                jobs.append((path, sample["text"], voice, rate))

    print(f"Generating {len(jobs)} files ...")
    print(f"Output: {OUT}")
    for path, text, voice, rate in jobs:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(str(path))
        print(f"  {path.name}  ({voice} {rate})")

    md_path = OUT / "index.md"
    md_path.write_text(render_md(), encoding="utf-8")
    print(f"Wrote {md_path}")


def main() -> None:
    asyncio.run(generate_all())


if __name__ == "__main__":
    main()
