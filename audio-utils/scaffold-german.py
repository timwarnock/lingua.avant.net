#!/usr/bin/env python3
"""Scaffold ora/docs/german/ prayer JSON + markdown (no audio).

TTS: de-DE-KillianNeural @ -10%, input phonetic (= text for German).
Passages align 1:1 with English. Segments aim to match English counts.

Run from repo root:
  python audio-utils/scaffold-german.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ora" / "docs" / "german"

TTS = {
    "voice": "de-DE-KillianNeural",
    "rate": "-10%",
    "input": "phonetic",
}
LANG = "german"


def segs(pairs: list[tuple[str, str]]) -> list[dict]:
    """pairs: list of (passage_segment_id, text); phonetic defaults to text."""
    out = []
    for sid, text in pairs:
        out.append(
            {
                "passage_segment_id": sid,
                "text": text,
                "phonetic": text,
            }
        )
    return out


def passages_from(groups: list[list[tuple[str, str]]]) -> list[dict]:
    result = []
    for i, group in enumerate(groups, 1):
        result.append({"passage_id": i, "segments": segs(group)})
    return result


def write_json(rel: str, prayer_id: str, title: str, groups: list[list[tuple[str, str]]]) -> Path:
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "id": prayer_id,
        "lang": LANG,
        "title": title,
        "tts": TTS,
        "passages": passages_from(groups),
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")
    return path


def write_md(rel: str, content: str) -> None:
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip("\n"), encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")


def prayer_md(title: str, prayer_id: str, german_fallback: str, english_fallback: str) -> str:
    return f"""---
icon: material/cross
---

# {title}

<div class="prayer-interactive"
     data-prayer="{prayer_id}"
     data-json="{prayer_id}.json"></div>

<div class="prayer-fallback" markdown="1">

**Deutsch**

{german_fallback}

**English**

{english_fallback}

</div>
"""


def main() -> None:
    # --- Sign of the Cross ---
    write_json(
        "sign-of-the-cross/sign-of-the-cross.json",
        "sign-of-the-cross",
        "Kreuzzeichen",
        [
            [
                ("1a", "Im Namen des Vaters,"),
                ("1b", "und des Sohnes,"),
                ("1c", "und des Heiligen Geistes."),
            ],
            [("2a", "Amen.")],
        ],
    )
    write_md(
        "sign-of-the-cross.md",
        prayer_md(
            "Kreuzzeichen",
            "sign-of-the-cross",
            "Im Namen des Vaters und des Sohnes und des Heiligen Geistes. Amen.",
            "In the name of the Father, and of the Son, and of the Holy Spirit. Amen.",
        ),
    )

    # --- Hail Mary ---
    write_json(
        "hail-mary/hail-mary.json",
        "hail-mary",
        "Gegrüßet seist du, Maria",
        [
            [
                ("1a", "Gegrüßet seist du, Maria,"),
                ("1b", "voll der Gnade,"),
                ("1c", "der Herr ist mit dir."),
            ],
            [
                ("2a", "Du bist gebenedeit unter den Frauen,"),
                ("2b", "und gebenedeit ist die Frucht deines Leibes,"),
                ("2c", "Jesus."),
            ],
            [
                ("3a", "Heilige Maria,"),
                ("3b", "Mutter Gottes,"),
                ("3c", "bitte für uns Sünder,"),
            ],
            [("4a", "jetzt und in der Stunde unseres Todes.")],
            [("5a", "Amen.")],
        ],
    )
    write_md(
        "hail-mary.md",
        prayer_md(
            "Gegrüßet seist du, Maria",
            "hail-mary",
            "Gegrüßet seist du, Maria, voll der Gnade, der Herr ist mit dir. "
            "Du bist gebenedeit unter den Frauen, und gebenedeit ist die Frucht deines Leibes, Jesus. "
            "Heilige Maria, Mutter Gottes, bitte für uns Sünder, jetzt und in der Stunde unseres Todes. Amen.",
            "Hail Mary, full of grace, the Lord is with thee. Blessed art thou amongst women, "
            "and blessed is the fruit of thy womb, Jesus. Holy Mary, Mother of God, "
            "pray for us sinners, now and at the hour of our death. Amen.",
        ),
    )

    # --- Our Father (official German liturgical form, segments 1:1 with EN) ---
    write_json(
        "our-father/our-father.json",
        "our-father",
        "Vater unser",
        [
            [
                ("1a", "Vater unser"),
                ("1b", "im Himmel,"),
                ("1c", "geheiligt werde dein Name."),
            ],
            [("2a", "Dein Reich komme.")],
            [("3a", "Dein Wille geschehe, wie im Himmel so auf Erden.")],
            [("4a", "Unser tägliches Brot gib uns heute.")],
            [
                ("5a", "Und vergib uns unsere Schuld,"),
                ("5b", "wie auch wir vergeben unsern Schuldigern."),
            ],
            [
                ("6a", "Und führe uns nicht in Versuchung,"),
                ("6b", "sondern erlöse uns von dem Bösen."),
            ],
            [("7a", "Amen.")],
        ],
    )
    write_md(
        "our-father.md",
        prayer_md(
            "Vater unser",
            "our-father",
            "Vater unser im Himmel, geheiligt werde dein Name. Dein Reich komme. "
            "Dein Wille geschehe, wie im Himmel so auf Erden. Unser tägliches Brot gib uns heute. "
            "Und vergib uns unsere Schuld, wie auch wir vergeben unsern Schuldigern. "
            "Und führe uns nicht in Versuchung, sondern erlöse uns von dem Bösen. Amen.",
            "Our Father, who art in heaven, hallowed be thy name. Thy kingdom come. "
            "Thy will be done on earth as it is in heaven. Give us this day our daily bread, "
            "and forgive us our trespasses, as we forgive those who trespass against us. "
            "And lead us not into temptation, but deliver us from evil. Amen.",
        ),
    )

    # --- Glory Be ---
    write_json(
        "glory-be/glory-be.json",
        "glory-be",
        "Ehre sei dem Vater",
        [
            [
                ("1a", "Ehre sei dem Vater"),
                ("1b", "und dem Sohn"),
                ("1c", "und dem Heiligen Geist."),
            ],
            [
                ("2a", "Wie im Anfang,"),
                ("2b", "so auch jetzt"),
                ("2c", "und alle Zeit"),
                ("2d", "und in Ewigkeit."),
            ],
            [("3a", "Amen.")],
        ],
    )
    write_md(
        "glory-be.md",
        prayer_md(
            "Ehre sei dem Vater",
            "glory-be",
            "Ehre sei dem Vater und dem Sohn und dem Heiligen Geist. "
            "Wie im Anfang, so auch jetzt und alle Zeit und in Ewigkeit. Amen.",
            "Glory be to the Father, and to the Son, and to the Holy Spirit. "
            "As it was in the beginning, is now, and ever shall be, world without end. Amen.",
        ),
    )

    # --- Fatima ---
    write_json(
        "fatima-prayer/fatima-prayer.json",
        "fatima-prayer",
        "Fatimagebet",
        [
            [
                ("1a", "O mein Jesus,"),
                ("1b", "verzeih uns unsere Sünden,"),
            ],
            [("2a", "bewahre uns vor dem Feuer der Hölle,")],
            [("3a", "führe alle Seelen in den Himmel,")],
            [("4a", "besonders jene, die deiner Barmherzigkeit am meisten bedürfen.")],
            [("5a", "Amen.")],
        ],
    )
    write_md(
        "fatima-prayer.md",
        prayer_md(
            "Fatimagebet",
            "fatima-prayer",
            "O mein Jesus, verzeih uns unsere Sünden, bewahre uns vor dem Feuer der Hölle, "
            "führe alle Seelen in den Himmel, besonders jene, die deiner Barmherzigkeit am meisten bedürfen. Amen.",
            "O my Jesus, forgive us our sins, save us from the fires of hell, "
            "lead all souls to heaven, especially those who are most in need of thy mercy. Amen.",
        ),
    )

    # --- Apostles' Creed (official German form; P6 Reich des Todes = hell) ---
    write_json(
        "apostles-creed/apostles-creed.json",
        "apostles-creed",
        "Apostolisches Glaubensbekenntnis",
        [
            [
                ("1a", "Ich glaube an Gott,"),
                ("1b", "den Vater, den Allmächtigen,"),
                ("1c", "den Schöpfer des Himmels und der Erde,"),
            ],
            [
                ("2a", "und an Jesus Christus,"),
                ("2b", "seinen eingeborenen Sohn,"),
                ("2c", "unsern Herrn,"),
            ],
            [("3a", "empfangen durch den Heiligen Geist,")],
            [("4a", "geboren von der Jungfrau Maria,")],
            [
                ("5a", "gelitten unter Pontius Pilatus,"),
                ("5b", "gekreuzigt,"),
                ("5c", "gestorben und begraben,"),
            ],
            [("6a", "hinabgestiegen in das Reich des Todes,")],
            [("7a", "am dritten Tage auferstanden von den Toten,")],
            [("8a", "aufgefahren in den Himmel;")],
            [("9a", "er sitzt zur Rechten Gottes, des allmächtigen Vaters;")],
            [("10a", "von dort wird er kommen, zu richten die Lebenden und die Toten.")],
            [
                ("11a", "Ich glaube an den Heiligen Geist,"),
                ("11b", "die heilige katholische Kirche,"),
                ("11c", "Gemeinschaft der Heiligen,"),
                ("11d", "Vergebung der Sünden,"),
                ("11e", "Auferstehung der Toten"),
                ("11f", "und das ewige Leben."),
            ],
            [("12a", "Amen.")],
        ],
    )
    write_md(
        "apostles-creed.md",
        prayer_md(
            "Apostolisches Glaubensbekenntnis",
            "apostles-creed",
            "Ich glaube an Gott, den Vater, den Allmächtigen, den Schöpfer des Himmels und der Erde, "
            "und an Jesus Christus, seinen eingeborenen Sohn, unsern Herrn, "
            "empfangen durch den Heiligen Geist, geboren von der Jungfrau Maria, "
            "gelitten unter Pontius Pilatus, gekreuzigt, gestorben und begraben, "
            "hinabgestiegen in das Reich des Todes, am dritten Tage auferstanden von den Toten, "
            "aufgefahren in den Himmel; er sitzt zur Rechten Gottes, des allmächtigen Vaters; "
            "von dort wird er kommen, zu richten die Lebenden und die Toten. "
            "Ich glaube an den Heiligen Geist, die heilige katholische Kirche, Gemeinschaft der Heiligen, "
            "Vergebung der Sünden, Auferstehung der Toten und das ewige Leben. Amen.",
            "I believe in God, the Father almighty, Creator of heaven and earth, "
            "and in Jesus Christ, his only Son, our Lord, who was conceived by the Holy Spirit, "
            "born of the Virgin Mary, suffered under Pontius Pilate, was crucified, died and was buried; "
            "he descended into hell; on the third day he rose again from the dead; "
            "he ascended into heaven, and is seated at the right hand of God the Father almighty; "
            "from there he will come to judge the living and the dead. "
            "I believe in the Holy Spirit, the holy catholic Church, the communion of saints, "
            "the forgiveness of sins, the resurrection of the body, and life everlasting. Amen.",
        ),
    )

    # --- Hail Holy Queen ---
    write_json(
        "hail-holy-queen/hail-holy-queen.json",
        "hail-holy-queen",
        "Sei gegrüßt, o Königin",
        [
            [
                ("1a", "Sei gegrüßt, o Königin,"),
                ("1b", "Mutter der Barmherzigkeit,"),
                ("1c", "unser Leben,"),
                ("1d", "unsere Süßigkeit"),
                ("1e", "und unsere Hoffnung."),
            ],
            [
                ("2a", "Zu dir rufen wir,"),
                ("2b", "verbannte Kinder Evas."),
            ],
            [
                ("3a", "Zu dir seufzen wir,"),
                ("3b", "trauernd und weinend"),
                ("3c", "in diesem Tal der Tränen."),
            ],
            [
                ("4a", "Wohlan denn,"),
                ("4b", "unsere Fürsprecherin,"),
                ("4c", "wende deine barmherzigen Augen uns zu."),
            ],
            [
                ("5a", "Und nach diesem Elend"),
                ("5b", "zeige uns"),
                ("5c", "Jesus,"),
                ("5d", "die gebenedeite Frucht deines Leibes."),
            ],
            [
                ("6a", "O gütige,"),
                ("6b", "o milde,"),
                ("6c", "o süße Jungfrau Maria."),
            ],
            [
                ("7a", "Bitte für uns,"),
                ("7b", "o heilige Gottesmutter."),
            ],
            [("8a", "Auf dass wir würdig werden der Verheißungen Christi.")],
        ],
    )

    # English hail-holy-queen has 4 segs in P5 including "Jesus." as separate in some langs.
    # EN: "And after this our exile, | show unto us | the blessed fruit of thy womb, | Jesus."
    # I used 5a-5d with Jesus as 5c and fruit as 5d - wrong order. Fix to match EN:
    # 5a exile, 5b show, 5c blessed fruit, 5d Jesus - wait EN is: exile | show | fruit | Jesus
    # My 5c is Jesus and 5d is fruit - swap needed. Fix below by rewriting file.

    write_json(
        "hail-holy-queen/hail-holy-queen.json",
        "hail-holy-queen",
        "Sei gegrüßt, o Königin",
        [
            [
                ("1a", "Sei gegrüßt, o Königin,"),
                ("1b", "Mutter der Barmherzigkeit,"),
                ("1c", "unser Leben,"),
                ("1d", "unsere Süßigkeit"),
                ("1e", "und unsere Hoffnung."),
            ],
            [
                ("2a", "Zu dir rufen wir,"),
                ("2b", "verbannte Kinder Evas."),
            ],
            [
                ("3a", "Zu dir seufzen wir,"),
                ("3b", "trauernd und weinend"),
                ("3c", "in diesem Tal der Tränen."),
            ],
            [
                ("4a", "Wohlan denn,"),
                ("4b", "unsere Fürsprecherin,"),
                ("4c", "wende deine barmherzigen Augen uns zu."),
            ],
            [
                ("5a", "Und nach diesem Elend"),
                ("5b", "zeige uns"),
                ("5c", "die gebenedeite Frucht deines Leibes,"),
                ("5d", "Jesus."),
            ],
            [
                ("6a", "O gütige,"),
                ("6b", "o milde,"),
                ("6c", "o süße Jungfrau Maria."),
            ],
            [
                ("7a", "Bitte für uns,"),
                ("7b", "o heilige Gottesmutter."),
            ],
            [("8a", "Auf dass wir würdig werden der Verheißungen Christi.")],
        ],
    )

    write_json(
        "hail-holy-queen/rosary-prayer.json",
        "rosary-prayer",
        "Rosenkranzgebet",
        [
            [("1a", "Lasset uns beten.")],
            [
                ("2a", "Gott,"),
                ("2b", "dessen eingeborener Sohn"),
                ("2c", "durch sein Leben,"),
                ("2d", "seinen Tod und seine Auferstehung"),
                ("2e", "uns den Lohn"),
                ("2f", "des ewigen Lebens erworben hat,"),
            ],
            [
                ("3a", "gewähre uns, wir bitten dich,"),
                ("3b", "dass wir, die wir diese Geheimnisse betrachten"),
                ("3c", "des heiligsten Rosenkranzes der seligen Jungfrau Maria,"),
            ],
            [
                ("4a", "nachahmen, was sie enthalten,"),
                ("4b", "und erlangen, was sie verheißen,"),
            ],
            [("5a", "durch denselben Christus, unseren Herrn.")],
            [("6a", "Amen.")],
            [
                ("7a", "Heiligstes Herz Jesu,"),
                ("7b", "erbarme dich unser."),
            ],
            [
                ("8a", "Unbeflecktes Herz Mariä,"),
                ("8b", "bitte für uns."),
            ],
        ],
    )

    write_md(
        "hail-holy-queen.md",
        """---
icon: material/cross
---

# Sei gegrüßt, o Königin

<div class="prayer-interactive"
     data-prayer="hail-holy-queen"
     data-json="hail-holy-queen.json"></div>

---

## Rosenkranzgebet

<div class="prayer-interactive"
     data-prayer="rosary-prayer"
     data-json="rosary-prayer.json"></div>

<div class="prayer-fallback" markdown="1">

**Deutsch**

Sei gegrüßt, o Königin, Mutter der Barmherzigkeit, unser Leben, unsere Süßigkeit und unsere Hoffnung. Zu dir rufen wir, verbannte Kinder Evas. Zu dir seufzen wir trauernd und weinend in diesem Tal der Tränen. Wohlan denn, unsere Fürsprecherin, wende deine barmherzigen Augen uns zu. Und nach diesem Elend zeige uns die gebenedeite Frucht deines Leibes, Jesus. O gütige, o milde, o süße Jungfrau Maria.

Bitte für uns, o heilige Gottesmutter.

Auf dass wir würdig werden der Verheißungen Christi.

Lasset uns beten.

Gott, dessen eingeborener Sohn durch sein Leben, seinen Tod und seine Auferstehung uns den Lohn des ewigen Lebens erworben hat, gewähre uns, wir bitten dich, dass wir, die wir diese Geheimnisse des heiligsten Rosenkranzes der seligen Jungfrau Maria betrachten, nachahmen, was sie enthalten, und erlangen, was sie verheißen, durch denselben Christus, unseren Herrn. Amen.

Heiligstes Herz Jesu, erbarme dich unser.

Unbeflecktes Herz Mariä, bitte für uns.

**English**

Hail, Holy Queen, Mother of mercy; our life, our sweetness and our hope. To thee do we cry, poor banished children of Eve. To thee do we send up our sighs, mourning and weeping in this valley of tears. Turn then, most gracious advocate, thine eyes of mercy toward us. And after this our exile, show unto us the blessed fruit of thy womb, Jesus. O clement, O loving, O sweet Virgin Mary.

Pray for us, O holy Mother of God.

That we may be made worthy of the promises of Christ.

Let us pray.

O God, whose only-begotten Son, by his life, death and resurrection, has purchased for us the rewards of eternal life, grant, we beseech thee, that while meditating on these mysteries of the most holy Rosary of the Blessed Virgin Mary, we may imitate what they contain and obtain what they promise, through the same Christ our Lord. Amen.

Most Sacred Heart of Jesus, have mercy on us.

Immaculate Heart of Mary, pray for us.

</div>
""",
    )

    # --- Jesus Prayer ---
    write_json(
        "extras/jesus-prayer/jesus-prayer.json",
        "jesus-prayer",
        "Jesusgebet",
        [
            [
                ("1a", "Herr Jesus Christus,"),
                ("1b", "Sohn Gottes,"),
            ],
            [
                ("2a", "erbarme dich meiner,"),
                ("2b", "eines Sünders."),
            ],
        ],
    )
    write_md(
        "extras/jesus-prayer.md",
        prayer_md(
            "Jesusgebet",
            "jesus-prayer",
            "Herr Jesus Christus, Sohn Gottes, erbarme dich meiner, eines Sünders.",
            "Lord Jesus Christ, Son of God, have mercy on me, a sinner.",
        ),
    )

    # --- Nicene Creed (German Messbuch form, aligned to EN passage structure) ---
    write_json(
        "extras/nicene/nicene.json",
        "nicene",
        "Nizänisches Glaubensbekenntnis",
        [
            [
                ("1a", "Ich glaube an den einen Gott,"),
                ("1b", "den Vater, den Allmächtigen,"),
                ("1c", "der alles geschaffen hat, Himmel und Erde,"),
                ("1d", "die sichtbare und die unsichtbare Welt."),
            ],
            [
                ("2a", "Und an den einen Herrn Jesus Christus,"),
                ("2b", "Gottes eingeborenen Sohn,"),
                ("2c", "aus dem Vater geboren vor aller Zeit:"),
            ],
            [
                ("3a", "Gott von Gott,"),
                ("3b", "Licht vom Licht,"),
                ("3c", "wahrer Gott vom wahren Gott,"),
                ("3d", "gezeugt, nicht geschaffen,"),
                ("3e", "eines Wesens mit dem Vater;"),
            ],
            [("4a", "durch ihn ist alles geschaffen.")],
            [
                ("5a", "Für uns Menschen und zu unserem Heil"),
                ("5b", "ist er vom Himmel gekommen,"),
            ],
            [
                ("6a", "hat Fleisch angenommen durch den Heiligen Geist von der Jungfrau Maria"),
                ("6b", "und ist Mensch geworden."),
            ],
            [
                ("7a", "Er wurde für uns gekreuzigt unter Pontius Pilatus,"),
                ("7b", "hat gelitten und ist begraben worden,"),
            ],
            [
                ("8a", "ist am dritten Tage auferstanden"),
                ("8b", "nach der Schrift"),
            ],
            [
                ("9a", "und aufgefahren in den Himmel."),
                ("9b", "Er sitzt zur Rechten des Vaters"),
            ],
            [
                ("10a", "und wird wiederkommen in Herrlichkeit,"),
                ("10b", "zu richten die Lebenden und die Toten;"),
                ("10c", "seiner Herrschaft wird kein Ende sein."),
            ],
            [
                ("11a", "Ich glaube an den Heiligen Geist,"),
                ("11b", "der Herr ist und lebendig macht,"),
                ("11c", "der aus dem Vater und dem Sohn hervorgeht,"),
                ("11d", "der mit dem Vater und dem Sohn angebetet und verherrlicht wird,"),
                ("11e", "der gesprochen hat durch die Propheten,"),
            ],
            [("12a", "und die eine, heilige, katholische und apostolische Kirche.")],
            [
                ("13a", "Ich bekenne die eine Taufe"),
                ("13b", "zur Vergebung der Sünden."),
            ],
            [
                ("14a", "Ich erwarte die Auferstehung der Toten"),
                ("14b", "und das Leben der kommenden Welt."),
            ],
            [("15a", "Amen.")],
        ],
    )
    write_md(
        "extras/nicene.md",
        prayer_md(
            "Nizänisches Glaubensbekenntnis",
            "nicene",
            "Ich glaube an den einen Gott, den Vater, den Allmächtigen, "
            "der alles geschaffen hat, Himmel und Erde, die sichtbare und die unsichtbare Welt. "
            "Und an den einen Herrn Jesus Christus, Gottes eingeborenen Sohn, "
            "aus dem Vater geboren vor aller Zeit: Gott von Gott, Licht vom Licht, "
            "wahrer Gott vom wahren Gott, gezeugt, nicht geschaffen, eines Wesens mit dem Vater; "
            "durch ihn ist alles geschaffen. Für uns Menschen und zu unserem Heil ist er vom Himmel gekommen, "
            "hat Fleisch angenommen durch den Heiligen Geist von der Jungfrau Maria und ist Mensch geworden. "
            "Er wurde für uns gekreuzigt unter Pontius Pilatus, hat gelitten und ist begraben worden, "
            "ist am dritten Tage auferstanden nach der Schrift und aufgefahren in den Himmel. "
            "Er sitzt zur Rechten des Vaters und wird wiederkommen in Herrlichkeit, "
            "zu richten die Lebenden und die Toten; seiner Herrschaft wird kein Ende sein. "
            "Ich glaube an den Heiligen Geist, der Herr ist und lebendig macht, "
            "der aus dem Vater und dem Sohn hervorgeht, der mit dem Vater und dem Sohn angebetet und verherrlicht wird, "
            "der gesprochen hat durch die Propheten, und die eine, heilige, katholische und apostolische Kirche. "
            "Ich bekenne die eine Taufe zur Vergebung der Sünden. "
            "Ich erwarte die Auferstehung der Toten und das Leben der kommenden Welt. Amen.",
            "I believe in one God, the Father almighty, maker of heaven and earth, "
            "of all things visible and invisible. I believe in one Lord Jesus Christ, "
            "the Only Begotten Son of God, born of the Father before all ages. "
            "God from God, Light from Light, true God from true God, begotten, not made, "
            "consubstantial with the Father; through him all things were made. "
            "For us men and for our salvation he came down from heaven, "
            "and by the Holy Spirit was incarnate of the Virgin Mary, and became man. "
            "For our sake he was crucified under Pontius Pilate, he suffered death and was buried, "
            "and rose again on the third day in accordance with the Scriptures. "
            "He ascended into heaven and is seated at the right hand of the Father. "
            "He will come again in glory to judge the living and the dead and his kingdom will have no end. "
            "I believe in the Holy Spirit, the Lord, the giver of life, who proceeds from the Father, "
            "who with the Father and the Son is adored and glorified, who has spoken through the prophets. "
            "I believe in one, holy, catholic and apostolic Church. "
            "I confess one Baptism for the forgiveness of sins "
            "and I look forward to the resurrection of the dead and the life of the world to come. Amen.",
        ),
    )

    # --- Psalm 23 (Einheitsübersetzung style, passage-aligned) ---
    write_json(
        "extras/psalm-23/psalm-23.json",
        "psalm-23",
        "Psalm 23",
        [
            [("1a", "Ein Psalm Davids.")],
            [
                ("2a", "Der Herr ist mein Hirte;"),
                ("2b", "nichts wird mir fehlen."),
            ],
            [
                ("3a", "Er lässt mich lagern auf grünen Auen"),
                ("3b", "und führt mich zum Ruheplatz am Wasser."),
            ],
            [
                ("4a", "Er stillt mein Verlangen;"),
                ("4b", "er leitet mich auf rechten Pfaden"),
                ("4c", "treu seinem Namen."),
            ],
            [
                ("5a", "Muss ich auch wandern in dunkler Schlucht,"),
                ("5b", "ich fürchte kein Unheil;"),
                ("5c", "denn du bist bei mir;"),
            ],
            [
                ("6a", "dein Stock und dein Stab"),
                ("6b", "geben mir Zuversicht."),
            ],
            [
                ("7a", "Du deckst mir den Tisch"),
                ("7b", "im Angesicht meiner Feinde."),
            ],
            [
                ("8a", "Du salbst mein Haupt mit Öl;"),
                ("8b", "du füllst mir reichlich den Becher."),
            ],
            [
                ("9a", "Lauter Güte und Huld werden mir folgen"),
                ("9b", "mein Leben lang,"),
            ],
            [
                ("10a", "und im Haus des Herrn darf ich wohnen"),
                ("10b", "für lange Zeit."),
            ],
        ],
    )
    write_md(
        "extras/psalm-23.md",
        prayer_md(
            "Psalm 23",
            "psalm-23",
            "Ein Psalm Davids. Der Herr ist mein Hirte; nichts wird mir fehlen. "
            "Er lässt mich lagern auf grünen Auen und führt mich zum Ruheplatz am Wasser. "
            "Er stillt mein Verlangen; er leitet mich auf rechten Pfaden treu seinem Namen. "
            "Muss ich auch wandern in dunkler Schlucht, ich fürchte kein Unheil; denn du bist bei mir; "
            "dein Stock und dein Stab geben mir Zuversicht. "
            "Du deckst mir den Tisch im Angesicht meiner Feinde. Du salbst mein Haupt mit Öl; "
            "du füllst mir reichlich den Becher. Lauter Güte und Huld werden mir folgen mein Leben lang, "
            "und im Haus des Herrn darf ich wohnen für lange Zeit.",
            "A Psalm of David. The LORD is my shepherd; I shall not want. "
            "He maketh me to lie down in green pastures: he leadeth me beside the still waters. "
            "He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake. "
            "Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; "
            "thy rod and thy staff they comfort me. "
            "Thou preparest a table before me in the presence of mine enemies: "
            "thou anointest my head with oil; my cup runneth over. "
            "Surely goodness and mercy shall follow me all the days of my life: "
            "and I will dwell in the house of the LORD for ever.",
        ),
    )

    # --- Psalm 51 (aligned to EN Douay structure; German Catholic sense) ---
    write_json(
        "extras/psalm-51/psalm-51.json",
        "psalm-51",
        "Psalm 51",
        [
            [
                ("1a", "Zum Ende,"),
                ("1b", "ein Psalm Davids,"),
            ],
            [
                ("2a", "als der Prophet Natan zu ihm kam,"),
                ("2b", "nachdem er mit Batseba gesündigt hatte."),
            ],
            [
                ("3a", "Erbarme dich meiner, o Gott,"),
                ("3b", "nach deiner großen Barmherzigkeit."),
                ("3c", "Und nach der Fülle deines Erbarmens"),
                ("3d", "tilge meine Schuld."),
            ],
            [
                ("4a", "Wasche mich noch mehr von meiner Schuld,"),
                ("4b", "und reinige mich von meiner Sünde."),
            ],
            [
                ("5a", "Denn ich kenne meine Schuld,"),
                ("5b", "und meine Sünde ist immer vor mir."),
            ],
            [
                ("6a", "Gegen dich allein habe ich gesündigt"),
                ("6b", "und getan, was böse ist in deinen Augen,"),
                ("6c", "damit du Recht behältst in deinen Worten"),
                ("6d", "und siegst, wenn man mit dir hadert."),
            ],
            [
                ("7a", "Siehe, in Schuld bin ich geboren;"),
                ("7b", "in Sünde hat mich meine Mutter empfangen."),
            ],
            [
                ("8a", "Siehe, du liebst die Wahrheit:"),
                ("8b", "das Verborgene und Geheime deiner Weisheit"),
                ("8c", "hast du mir kundgetan."),
            ],
            [
                ("9a", "Entsündige mich mit Ysop,"),
                ("9b", "dann werde ich rein;"),
                ("9c", "wasche mich,"),
                ("9d", "dann werde ich weißer als Schnee."),
            ],
            [
                ("10a", "Lass mich Freude und Jubel hören,"),
                ("10b", "dann jauchzen die Gebeine, die du zerschlagen hast."),
            ],
            [
                ("11a", "Verbirg dein Antlitz vor meinen Sünden,"),
                ("11b", "und tilge alle meine Verschuldungen."),
            ],
            [
                ("12a", "Erschaffe mir, Gott, ein reines Herz,"),
                ("12b", "und gib mir einen neuen, beständigen Geist."),
            ],
            [
                ("13a", "Verwirf mich nicht von deinem Angesicht,"),
                ("13b", "und nimm deinen heiligen Geist nicht von mir."),
            ],
            [
                ("14a", "Gib mir wieder die Freude deines Heils,"),
                ("14b", "und stärke mich mit willigem Geist."),
            ],
            [
                ("15a", "Ich will die Abtrünnigen deine Wege lehren,"),
                ("15b", "und die Sünder werden sich zu dir bekehren."),
            ],
            [
                ("16a", "Errette mich von Blutschuld, o Gott,"),
                ("16b", "du Gott meines Heils,"),
                ("16c", "und meine Zunge wird deine Gerechtigkeit preisen."),
            ],
            [
                ("17a", "Herr, öffne meine Lippen,"),
                ("17b", "und mein Mund wird deinen Ruhm verkünden."),
            ],
            [
                ("18a", "Denn an Opfern hast du kein Gefallen,"),
                ("18b", "sonst würde ich sie darbringen;"),
                ("18c", "an Brandopfern hast du kein Wohlgefallen."),
            ],
            [
                ("19a", "Das Opfer, das Gott gefällt, ist ein zerknirschter Geist;"),
                ("19b", "ein zerbrochenes und zerschlagenes Herz wirst du, o Gott,"),
                ("19c", "nicht verschmähen."),
            ],
            [
                ("20a", "Tue wohl, o Herr,"),
                ("20b", "an Zion nach deiner Gnade;"),
                ("20c", "baue die Mauern Jerusalems wieder auf."),
            ],
            [
                ("21a", "Dann wirst du Gefallen haben an rechten Opfern,"),
                ("21b", "an Gaben und Brandopfern;"),
                ("21c", "dann wird man Stiere opfern auf deinem Altar."),
            ],
        ],
    )
    # Fix psalm-51 P16 - English has 3 segments: Deliver me... | thou God... | and my tongue...
    # I had 3 - good. P18 EN has 3 segs - good. P3 EN has 4 - good.

    write_md(
        "extras/psalm-51.md",
        prayer_md(
            "Psalm 51",
            "psalm-51",
            "Zum Ende, ein Psalm Davids, als der Prophet Natan zu ihm kam, nachdem er mit Batseba gesündigt hatte. "
            "Erbarme dich meiner, o Gott, nach deiner großen Barmherzigkeit. "
            "Und nach der Fülle deines Erbarmens tilge meine Schuld. "
            "Wasche mich noch mehr von meiner Schuld, und reinige mich von meiner Sünde. "
            "Denn ich kenne meine Schuld, und meine Sünde ist immer vor mir. "
            "Gegen dich allein habe ich gesündigt und getan, was böse ist in deinen Augen, "
            "damit du Recht behältst in deinen Worten und siegst, wenn man mit dir hadert. "
            "Siehe, in Schuld bin ich geboren; in Sünde hat mich meine Mutter empfangen. "
            "Siehe, du liebst die Wahrheit im Innern; im Verborgenen lehrst du mich Weisheit. "
            "Entsündige mich mit Ysop, dann werde ich rein; wasche mich, dann werde ich weißer als Schnee. "
            "Lass mich Freude und Jubel hören, dann jauchzen die Gebeine, die du zerschlagen hast. "
            "Verbirg dein Antlitz vor meinen Sünden, und tilge alle meine Verschuldungen. "
            "Erschaffe mir, Gott, ein reines Herz, und gib mir einen neuen, beständigen Geist. "
            "Verwirf mich nicht von deinem Angesicht, und nimm deinen heiligen Geist nicht von mir. "
            "Gib mir wieder die Freude deines Heils, und stärke mich mit willigem Geist. "
            "Ich will die Abtrünnigen deine Wege lehren, und die Sünder werden sich zu dir bekehren. "
            "Errette mich von Blutschuld, o Gott, du Gott meines Heils, und meine Zunge wird deine Gerechtigkeit preisen. "
            "Herr, öffne meine Lippen, und mein Mund wird deinen Ruhm verkünden. "
            "Denn an Opfern hast du kein Gefallen, sonst würde ich sie darbringen; an Brandopfern hast du kein Wohlgefallen. "
            "Das Opfer, das Gott gefällt, ist ein zerknirschter Geist; ein zerbrochenes und zerschlagenes Herz wirst du, o Gott, nicht verschmähen. "
            "Tue wohl an Zion nach deiner Gnade; baue die Mauern Jerusalems wieder auf. "
            "Dann wirst du Gefallen haben an rechten Opfern, an Gaben und Brandopfern; dann wird man Stiere opfern auf deinem Altar.",
            "Unto the end, a psalm of David, When Nathan the prophet came to him after he had sinned with Bethsabee. "
            "Have mercy on me, O God, according to thy great mercy. "
            "And according to the multitude of thy tender mercies blot out my iniquity. "
            "Wash me yet more from my iniquity, and cleanse me from my sin. "
            "For I know my iniquity, and my sin is always before me. "
            "To thee only have I sinned, and have done evil before thee: "
            "that thou mayst be justified in thy words and mayst overcome when thou art judged. "
            "For behold I was conceived in iniquities; and in sins did my mother conceive me. "
            "For behold thou hast loved truth: the uncertain and hidden things of thy wisdom thou hast made manifest to me. "
            "Thou shalt sprinkle me with hyssop, and I shall be cleansed: thou shalt wash me, and I shall be made whiter than snow. "
            "To my hearing thou shalt give joy and gladness: and the bones that have been humbled shall rejoice. "
            "Turn away thy face from my sins, and blot out all my iniquities. "
            "Create a clean heart in me, O God: and renew a right spirit within my bowels. "
            "Cast me not away from thy face; and take not thy holy spirit from me. "
            "Restore unto me the joy of thy salvation, and strengthen me with a perfect spirit. "
            "I will teach the unjust thy ways: and the wicked shall be converted to thee. "
            "Deliver me from blood, O God, thou God of my salvation: and my tongue shall extol thy justice. "
            "O Lord, thou wilt open my lips: and my mouth shall declare thy praise. "
            "For if thou hadst desired sacrifice, I would indeed have given it: with burnt offerings thou wilt not be delighted. "
            "A sacrifice to God is an afflicted spirit: a contrite and humbled heart, O God, thou wilt not despise. "
            "Deal favourably, O Lord, in thy good will with Sion; that the walls of Jerusalem may be built up. "
            "Then shalt thou accept the sacrifice of justice, oblations and whole burnt offerings: then shall they lay calves upon thy altar.",
        ),
    )

    # --- Mysteries ---
    mysteries = [
        ("joyful1", "Das erste freudenreiche Geheimnis, die Verkündigung"),
        ("joyful2", "Das zweite freudenreiche Geheimnis, die Heimsuchung"),
        ("joyful3", "Das dritte freudenreiche Geheimnis, die Geburt Jesu"),
        ("joyful4", "Das vierte freudenreiche Geheimnis, die Darstellung im Tempel"),
        ("joyful5", "Das fünfte freudenreiche Geheimnis, das Finden Jesu im Tempel"),
        ("sorrowful1", "Das erste schmerzhafte Geheimnis, die Todesangst am Ölberg"),
        ("sorrowful2", "Das zweite schmerzhafte Geheimnis, die Geißelung"),
        ("sorrowful3", "Das dritte schmerzhafte Geheimnis, die Dornenkrönung"),
        ("sorrowful4", "Das vierte schmerzhafte Geheimnis, die Kreuztragung"),
        ("sorrowful5", "Das fünfte schmerzhafte Geheimnis, die Kreuzigung"),
        ("glorious1", "Das erste glorreiche Geheimnis, die Auferstehung"),
        ("glorious2", "Das zweite glorreiche Geheimnis, die Himmelfahrt"),
        ("glorious3", "Das dritte glorreiche Geheimnis, die Sendung des Heiligen Geistes"),
        ("glorious4", "Das vierte glorreiche Geheimnis, die Aufnahme Mariens in den Himmel"),
        ("glorious5", "Das fünfte glorreiche Geheimnis, die Krönung Mariens"),
        ("luminous1", "Das erste lichtreiche Geheimnis, die Taufe Jesu"),
        ("luminous2", "Das zweite lichtreiche Geheimnis, die Hochzeit zu Kana"),
        ("luminous3", "Das dritte lichtreiche Geheimnis, die Verkündigung des Reiches Gottes"),
        ("luminous4", "Das vierte lichtreiche Geheimnis, die Verklärung"),
        ("luminous5", "Das fünfte lichtreiche Geheimnis, die Einsetzung der Eucharistie"),
    ]
    for mid, title in mysteries:
        write_json(
            f"mysteries/{mid}.json",
            mid,
            title,
            [[("1a", title + ".")]],
        )

    # --- Index ---
    write_md(
        "index.md",
        """---
icon: lucide/languages
---

# <span tooltip="German">Deutsch</span>

!!! quote "Heiliger Ludwig Maria Grignion de Montfort"

    Der Rosenkranz ist also eine gesegnete Mischung aus geistigem und mündlichem Gebet, durch die wir die Geheimnisse und Tugenden des Lebens, des Todes, des Leidens und der Herrlichkeit Jesu und Mariens ehren und lernen, sie nachzuahmen.

    *The Rosary is therefore a blessed mixture of mental and vocal prayer by which we honor and learn to imitate the mysteries and virtues of the life, death, passion and glory of Jesus and Mary.*

<div class="mystery-chooser">
<span class="mystery-set" data-set="joyful">Freudenreiche Geheimnisse</span>
<span class="mystery-set" data-set="sorrowful">Schmerzhafte Geheimnisse</span>
<span class="mystery-set" data-set="glorious">Glorreiche Geheimnisse</span>
<span class="mystery-set" data-set="luminous">Lichtreiche Geheimnisse</span>
</div>

<div id="rosary-player">
  <div id="rosary-indicators" class="rosary-indicators"></div>
  <div class="rosary-controls">
    <button id="rosary-prev" class="rosary-btn" tooltip="Previous">◀◀</button>
    <button id="rosary-play" class="rosary-btn" tooltip="Play / pause auto"></button>
    <button id="rosary-phonetic" class="rosary-btn" tooltip="Toggle phonetic"></button>
    <button id="rosary-next" class="rosary-btn" tooltip="Next">▶▶</button>
  </div>
  <div id="rosary-viewer"></div>
</div>
""",
    )

    # Minimal pronunciation page (resources for English-speaking learners of German)
    write_md(
        "resources/pronunciation.md",
        """---
icon: lucide/mic
---

# <span tooltip="Pronunciation">Aussprache</span>

German is a West Germanic language. Written High German was shaped for centuries by the Church, the universities, and the printing press. Martin Luther’s Bible translation (1522–1534) fixed a standard that still underlies modern spelling. The Rosary in German -- <span tooltip="Our Father">Vater unser</span>, <span tooltip="Hail Mary">Gegrüßet seist du, Maria</span>, <span tooltip="Glory Be">Ehre sei dem Vater</span> -- is prayed with clear, measured delivery suited to bead-by-bead repetition.

Pronunciation is often left to natural exposure. English speakers commonly transfer English vowel glides, soften final consonants, and under-articulate the German <span tooltip="ch sound">ch</span> and rounded front vowels. Clear rules and Rosary examples short-circuit that.

!!! quote "Henry Widdowson"
    The whole point of language pedagogy is that it is a way of short-circuiting the slow process of natural discovery and can make arrangements for learning to happen more easily and more efficiently than it does in natural surroundings.




---

## Vowels

German vowels are pure: hold one quality from start to finish. English often glides (the o in "go", the a in "name"). In prayer, keep vowels steady.

!!! success "Core vowels"
    + **a** as in father -- e.g. <span tooltip="Father">Vater</span>, <span tooltip="grace">Gnade</span>
    + **e** (short) as in bed -- e.g. <span tooltip="Lord">Herr</span>
    + **e** (long) closer to "ay" without a glide -- e.g. <span tooltip="spirit">Geist</span>
    + **i** as ee in see -- e.g. <span tooltip="with">mit</span>
    + **o** pure o, lips rounded -- e.g. <span tooltip="Son">Sohn</span>, <span tooltip="death">Tod</span>
    + **u** as oo in boot -- e.g. <span tooltip="and">und</span>, <span tooltip="Mother">Mutter</span>
    + **ä** like e in bed (often longer) -- e.g. <span tooltip="Mercy">Barmherzigkeit</span>
    + **ö** tongue as for "ay", lips rounded -- e.g. <span tooltip="highest">höchsten</span>
    + **ü** tongue as for "ee", lips tightly rounded -- e.g. <span tooltip="for">für</span>, <span tooltip="greeted">Gegrüßet</span>

!!! tip "Diphthongs"
    + **ei / ai** as English "eye" -- e.g. <span tooltip="holy">heilig</span>, <span tooltip="your">dein</span>
    + **au** as "ow" in cow -- e.g. <span tooltip="also">auch</span>
    + **eu / äu** as "oy" in boy -- e.g. <span tooltip="people">Leute</span>, <span tooltip="baptism">Taufe</span>




---

## Consonants that matter for the Rosary

!!! success "Hard spots for English speakers"
    + **ch** after a, o, u, au -- like Scottish loch (Ach-Laut): <span tooltip="also">auch</span>, <span tooltip="night">Nacht</span>
    + **ch** after e, i, ä, ö, ü, ei, eu -- soft palatal (Ich-Laut): <span tooltip="I">ich</span>, <span tooltip="not">nicht</span>, <span tooltip="kingdom">Reich</span>
    + **r** -- often uvular (back of the throat) in standard German; a clear trilled or tapped r is also fine in prayer
    + **z** always **ts** -- e.g. <span tooltip="time">Zeit</span>, <span tooltip="to">zu</span>
    + **w** like English **v** -- e.g. <span tooltip="will">Wille</span>, <span tooltip="become">werde</span>
    + **v** often like **f** -- e.g. <span tooltip="Father">Vater</span>, <span tooltip="forgive">vergib</span>
    + **s** before a vowel is often voiced (**z** sound): <span tooltip="be">sei</span>, <span tooltip="sins">Sünden</span>
    + Final consonants stay crisp: pronounce the **t** in <span tooltip="God">Gott</span>, the **d** in <span tooltip="and">und</span> as a clear stop (often unvoiced at the end of a word)




---

## Prayer tips

!!! tip "Rosary delivery"
    Keep a steady pace. Slightly slower than conversation helps each bead land. Killian at **-10%** matches a prayerful tempo.
    Stress the content words: **Va**-ter **un**-ser, **Ge**-grü-ßet seist **du**, **Ma**-ri-a, **Gna**-de, **Je**-sus.
    Final **-e** in words like <span tooltip="Name">Name</span>, <span tooltip="Gnade">Gnade</span> is a light schwa, not a full "ay".




---

## Recommendations

!!! success "<span tooltip='Recommended'>Empfohlen</span>"
    Hold pure vowels. Distinguish **ich**-Laut and **ach**-Laut. Pronounce **z** as **ts**. Keep final consonants clear. Match the prayer audio line by line.

!!! failure "<span tooltip='Not recommended'>Nicht empfohlen</span>"
    English diphthongs on German long vowels. Softening or dropping final **t** / **d**. Reading **w** as English w. Guessing **ch** as English "ch" in "church".
""",
    )

    print("Done scaffolding german/")


if __name__ == "__main__":
    main()
