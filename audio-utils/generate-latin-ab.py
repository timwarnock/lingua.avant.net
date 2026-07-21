#!/usr/bin/env python3
"""Generate Latin Edge TTS A/B samples and index.md for audio-testing.

Voice and rate match ora/docs/latin prayer JSON (it-IT-DiegoNeural, -15%).
Writes only web content into ora/docs/audio-testing/ (mp3 + index.md).

Run from repo root:

  uv run --with edge-tts python audio-utils/generate-latin-ab.py
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import edge_tts

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "ora" / "docs" / "audio-testing"
VOICE = "it-IT-DiegoNeural"
RATE = "-15%"

# Focus: Sancta -- Italian Edge often drops the c and says Spanish/Italian "Santa".
# Target: SAHNK-tah (hard k before t).
SECTIONS: list[dict] = [
    {
        "id": "sancta-maria",
        "title": "Sancta (Ave Maria 3a)",
        "source": "Ave Maria 3a -- Sancta Maria,",
        "display": "Sancta Maria,",
        "target": (
            "SAHNK-tah mah-REE-ah: hard k in Sancta before t (sanc-ta), "
            "not Spanish/Italian Santa without the k. Two clear syllables in Sancta."
        ),
        "variants": [
            ("cur", "Sancta Maria,"),
            ("sankta", "Sankta Maria,"),
            ("sànkta", "Sànkta Maria,"),
            ("sanc-ta", "Sanc-ta Maria,"),
            ("sank-ta", "Sank-ta Maria,"),
            ("sangta", "Sangta Maria,"),
            ("santa", "Santa Maria,"),
        ],
    },
    {
        "id": "sancta-dei",
        "title": "sancta (Salve Regina 7b)",
        "source": "Salve Regina 7b -- sancta Dei Genitrix.",
        "display": "sancta Dei Genitrix.",
        "target": (
            "SAHNK-tah DEH-ee: same hard k in sancta; lowercase as in the prayer. "
            "Dei already locked as Déi in production phonetic."
        ),
        "variants": [
            ("cur", "sancta Déi Genitrix."),
            ("sankta", "sankta Déi Genitrix."),
            ("sànkta", "sànkta Déi Genitrix."),
            ("sanc-ta", "sanc-ta Déi Genitrix."),
            ("sank-ta", "sank-ta Déi Genitrix."),
        ],
    },
    {
        "id": "sanctam",
        "title": "sanctam (Apostles Creed 11b)",
        "source": "Symbolum Apostolorum 11b -- sanctam Ecclesiam catholicam,",
        "display": "sanctam Ecclesiam catholicam,",
        "target": (
            "SAHNK-tahm: hard k before t; final -am as ahm. Not \"san-tam\" without k."
        ),
        "variants": [
            ("cur", "sanctam Ecclesiam catholicam,"),
            ("sanktam", "sanktam Ecclesiam catholicam,"),
            ("sànktam", "sànktam Ecclesiam catholicam,"),
            ("sanc-tam", "sanc-tam Ecclesiam catholicam,"),
        ],
    },
    {
        "id": "sancto",
        "title": "Sancto (Gloria 1c / Creed)",
        "source": "Gloria Patri 1c -- et Spiritui Sancto.",
        "display": "et Spiritui Sancto.",
        "target": (
            "SAHNK-to: hard k in Sancto. Same sanct- stem as Sancta."
        ),
        "variants": [
            ("cur", "et Spiritui Sancto."),
            ("sankto", "et Spiritui Sankto."),
            ("sànkto", "et Spiritui Sànkto."),
            ("sanc-to", "et Spiritui Sanc-to."),
        ],
    },
    {
        "id": "sancti",
        "title": "Sancti (Sign of the Cross 1c)",
        "source": "Signum Crucis 1c -- et Spiritus Sancti.",
        "display": "et Spiritus Sancti.",
        "target": (
            "SAHNK-tee: hard k in Sancti; final -i as ee."
        ),
        "variants": [
            ("cur", "et Spiritus Sancti,"),
            ("sankti", "et Spiritus Sankti,"),
            ("sànkti", "et Spiritus Sànkti,"),
            ("sanc-ti", "et Spiritus Sanc-ti,"),
        ],
    },
    {
        "id": "sanctum",
        "title": "Sanctum (Apostles Creed 11a)",
        "source": "Symbolum Apostolorum 11a -- Credo in Spiritum Sanctum,",
        "display": "Credo in Spiritum Sanctum,",
        "target": (
            "SAHNK-toom: hard k in Sanctum; -um as oom."
        ),
        "variants": [
            ("cur", "Credo in Spiritum Sanctum,"),
            ("sanktum", "Credo in Spiritum Sanktum,"),
            ("sànktum", "Credo in Spiritum Sànktum,"),
            ("sanc-tum", "Credo in Spiritum Sanc-tum,"),
        ],
    },
]


def play_span(filename: str, label: str) -> str:
    return (
        f'<span onclick="new Audio(\'{filename}\').play()" '
        f'style="cursor:pointer; text-decoration:underline">'
        f"<strong>{label}</strong></span>"
    )


def render_md() -> str:
    lines: list[str] = [
        "# Latin Edge TTS A/B -- Sancta / sanct-",
        "",
        "Qualitative listen tests for ecclesiastical Latin with "
        f"**{VOICE}** at rate **{RATE}** (same as production Latin prayers).",
        "",
        "Focus: **Sancta** and the **sanct-** stem. Italian Edge often reduces "
        "these toward Spanish/Italian **Santa** (no hard **k**). Liturgical Latin "
        "keeps the **k**: **SAHNK-tah** (sanc-ta).",
        "",
        "Each section is a real prayer segment. Play variants and note the winning slug.",
        "",
        "Regenerate samples:",
        "",
        "```bash",
        "uv run --with edge-tts python audio-utils/generate-latin-ab.py",
        "```",
        "",
    ]

    for i, sec in enumerate(SECTIONS, 1):
        lines.append("---")
        lines.append("")
        lines.append(f"## {i}. {sec['title']}")
        lines.append("")
        lines.append(f"**Source:** {sec['source']}")
        lines.append("")
        lines.append(f"**Display text:** `{sec['display']}`")
        lines.append("")
        lines.append(f"**Liturgical Latin target:** {sec['target']}")
        lines.append("")
        lines.append("**Variants** (click label to play):")
        lines.append("")
        for slug, phonetic in sec["variants"]:
            fn = f"{sec['id']}-{slug}.mp3"
            lines.append(
                f"+ {play_span(fn, slug)} -- phonetic: `{phonetic}`"
            )
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Checklist")
    lines.append("")
    lines.append("| # | Focus | Winner slug | Notes |")
    lines.append("|---|-------|-------------|-------|")
    for i, sec in enumerate(SECTIONS, 1):
        lines.append(f"| {i} | {sec['title']} |  |  |")
    lines.append("")

    return "\n".join(lines)


async def generate_all() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # Drop previous A/B mp3s in the output dir so old tests do not linger.
    for old in OUT.glob("*.mp3"):
        old.unlink()

    tasks = []
    for sec in SECTIONS:
        for slug, phonetic in sec["variants"]:
            path = OUT / f"{sec['id']}-{slug}.mp3"
            tasks.append((path, phonetic))

    print(f"Generating {len(tasks)} files with {VOICE} @ {RATE} ...")
    print(f"Output: {OUT}")
    for path, phonetic in tasks:
        communicate = edge_tts.Communicate(phonetic, VOICE, rate=RATE)
        await communicate.save(str(path))
        print(f"  {path.name}")

    md_path = OUT / "index.md"
    md_path.write_text(render_md(), encoding="utf-8")
    print(f"Wrote {md_path}")


def main() -> None:
    asyncio.run(generate_all())


if __name__ == "__main__":
    main()
