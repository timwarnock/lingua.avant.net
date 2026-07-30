#!/usr/bin/env python3
"""Scaffold ora/docs/italian/ prayer JSON + markdown (no audio).

TTS: it-IT-ElsaNeural @ -10%, input phonetic (= text for Italian).
Passages align 1:1 with English. Segments aim to match English counts.

Run from repo root:
  python audio-utils/scaffold-italian.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ora" / "docs" / "italian"

TTS = {
    "voice": "it-IT-ElsaNeural",
    "rate": "-10%",
    "input": "phonetic",
}
LANG = "italian"


def segs(pairs: list[tuple[str, str]]) -> list[dict]:
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


def prayer_md(title: str, prayer_id: str, italian_fallback: str, english_fallback: str) -> str:
    return f"""---
icon: material/cross
---

# {title}

<div class="prayer-interactive"
     data-prayer="{prayer_id}"
     data-json="{prayer_id}.json"></div>

<div class="prayer-fallback" markdown="1">

**Italiano**

{italian_fallback}

**English**

{english_fallback}

</div>
"""


def main() -> None:
    # --- Sign of the Cross ---
    write_json(
        "sign-of-the-cross/sign-of-the-cross.json",
        "sign-of-the-cross",
        "Segno della Croce",
        [
            [
                ("1a", "Nel nome del Padre,"),
                ("1b", "e del Figlio,"),
                ("1c", "e dello Spirito Santo."),
            ],
            [("2a", "Amen.")],
        ],
    )
    write_md(
        "sign-of-the-cross.md",
        prayer_md(
            "Segno della Croce",
            "sign-of-the-cross",
            "Nel nome del Padre e del Figlio e dello Spirito Santo. Amen.",
            "In the name of the Father, and of the Son, and of the Holy Spirit. Amen.",
        ),
    )

    # --- Hail Mary ---
    write_json(
        "hail-mary/hail-mary.json",
        "hail-mary",
        "Ave Maria",
        [
            [
                ("1a", "Ave Maria,"),
                ("1b", "piena di grazia,"),
                ("1c", "il Signore è con te."),
            ],
            [
                ("2a", "Tu sei benedetta fra le donne,"),
                ("2b", "e benedetto è il frutto del tuo seno,"),
                ("2c", "Gesù."),
            ],
            [
                ("3a", "Santa Maria,"),
                ("3b", "Madre di Dio,"),
                ("3c", "prega per noi peccatori,"),
            ],
            [("4a", "adesso e nell'ora della nostra morte.")],
            [("5a", "Amen.")],
        ],
    )
    write_md(
        "hail-mary.md",
        prayer_md(
            "Ave Maria",
            "hail-mary",
            "Ave Maria, piena di grazia, il Signore è con te. "
            "Tu sei benedetta fra le donne, e benedetto è il frutto del tuo seno, Gesù. "
            "Santa Maria, Madre di Dio, prega per noi peccatori, "
            "adesso e nell'ora della nostra morte. Amen.",
            "Hail Mary, full of grace, the Lord is with thee. Blessed art thou amongst women, "
            "and blessed is the fruit of thy womb, Jesus. Holy Mary, Mother of God, "
            "pray for us sinners, now and at the hour of our death. Amen.",
        ),
    )

    # --- Our Father ---
    write_json(
        "our-father/our-father.json",
        "our-father",
        "Padre Nostro",
        [
            [
                ("1a", "Padre nostro,"),
                ("1b", "che sei nei cieli,"),
                ("1c", "sia santificato il tuo nome."),
            ],
            [("2a", "Venga il tuo regno.")],
            [("3a", "Sia fatta la tua volontà, come in cielo così in terra.")],
            [("4a", "Dacci oggi il nostro pane quotidiano,")],
            [
                ("5a", "e rimetti a noi i nostri debiti,"),
                ("5b", "come noi li rimettiamo ai nostri debitori."),
            ],
            [
                ("6a", "E non ci indurre in tentazione,"),
                ("6b", "ma liberaci dal male."),
            ],
            [("7a", "Amen.")],
        ],
    )
    write_md(
        "our-father.md",
        prayer_md(
            "Padre Nostro",
            "our-father",
            "Padre nostro che sei nei cieli, sia santificato il tuo nome. "
            "Venga il tuo regno. Sia fatta la tua volontà, come in cielo così in terra. "
            "Dacci oggi il nostro pane quotidiano, e rimetti a noi i nostri debiti, "
            "come noi li rimettiamo ai nostri debitori. "
            "E non ci indurre in tentazione, ma liberaci dal male. Amen.",
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
        "Gloria al Padre",
        [
            [
                ("1a", "Gloria al Padre,"),
                ("1b", "e al Figlio,"),
                ("1c", "e allo Spirito Santo."),
            ],
            [
                ("2a", "Come era nel principio,"),
                ("2b", "ora"),
                ("2c", "e sempre,"),
                ("2d", "nei secoli dei secoli."),
            ],
            [("3a", "Amen.")],
        ],
    )
    write_md(
        "glory-be.md",
        prayer_md(
            "Gloria al Padre",
            "glory-be",
            "Gloria al Padre e al Figlio e allo Spirito Santo. "
            "Come era nel principio, ora e sempre, nei secoli dei secoli. Amen.",
            "Glory be to the Father, and to the Son, and to the Holy Spirit. "
            "As it was in the beginning, is now, and ever shall be, world without end. Amen.",
        ),
    )

    # --- Fatima ---
    write_json(
        "fatima-prayer/fatima-prayer.json",
        "fatima-prayer",
        "Preghiera di Fatima",
        [
            [
                ("1a", "O Gesù mio,"),
                ("1b", "perdona le nostre colpe,"),
            ],
            [("2a", "preservaci dal fuoco dell'inferno,")],
            [("3a", "porta in cielo tutte le anime,")],
            [("4a", "specialmente le più bisognose della tua misericordia.")],
            [("5a", "Amen.")],
        ],
    )
    write_md(
        "fatima-prayer.md",
        prayer_md(
            "Preghiera di Fatima",
            "fatima-prayer",
            "O Gesù mio, perdona le nostre colpe, preservaci dal fuoco dell'inferno, "
            "porta in cielo tutte le anime, specialmente le più bisognose della tua misericordia. Amen.",
            "O my Jesus, forgive us our sins, save us from the fires of hell, "
            "lead all souls to heaven, especially those who are most in need of thy mercy. Amen.",
        ),
    )

    # --- Apostles' Creed ---
    write_json(
        "apostles-creed/apostles-creed.json",
        "apostles-creed",
        "Simbolo degli Apostoli",
        [
            [
                ("1a", "Io credo in Dio,"),
                ("1b", "Padre onnipotente,"),
                ("1c", "Creatore del cielo e della terra;"),
            ],
            [
                ("2a", "e in Gesù Cristo,"),
                ("2b", "suo unico Figlio,"),
                ("2c", "nostro Signore,"),
            ],
            [("3a", "il quale fu concepito di Spirito Santo,")],
            [("4a", "nacque da Maria Vergine,")],
            [
                ("5a", "patì sotto Ponzio Pilato,"),
                ("5b", "fu crocifisso,"),
                ("5c", "morì e fu sepolto;"),
            ],
            [("6a", "discese agli inferi;")],
            [("7a", "il terzo giorno risuscitò da morte;")],
            [("8a", "salì al cielo,")],
            [("9a", "siede alla destra di Dio Padre onnipotente;")],
            [("10a", "di là verrà a giudicare i vivi e i morti.")],
            [
                ("11a", "Credo nello Spirito Santo,"),
                ("11b", "la santa Chiesa cattolica,"),
                ("11c", "la comunione dei santi,"),
                ("11d", "la remissione dei peccati,"),
                ("11e", "la risurrezione della carne,"),
                ("11f", "la vita eterna."),
            ],
            [("12a", "Amen.")],
        ],
    )
    write_md(
        "apostles-creed.md",
        prayer_md(
            "Simbolo degli Apostoli",
            "apostles-creed",
            "Io credo in Dio, Padre onnipotente, Creatore del cielo e della terra; "
            "e in Gesù Cristo, suo unico Figlio, nostro Signore, "
            "il quale fu concepito di Spirito Santo, nacque da Maria Vergine, "
            "patì sotto Ponzio Pilato, fu crocifisso, morì e fu sepolto; "
            "discese agli inferi; il terzo giorno risuscitò da morte; "
            "salì al cielo, siede alla destra di Dio Padre onnipotente; "
            "di là verrà a giudicare i vivi e i morti. "
            "Credo nello Spirito Santo, la santa Chiesa cattolica, la comunione dei santi, "
            "la remissione dei peccati, la risurrezione della carne, la vita eterna. Amen.",
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
        "Salve, Regina",
        [
            [
                ("1a", "Salve, Regina,"),
                ("1b", "Madre di misericordia,"),
                ("1c", "vita,"),
                ("1d", "dolcezza"),
                ("1e", "e speranza nostra, salve."),
            ],
            [
                ("2a", "A te ricorriamo,"),
                ("2b", "esuli figli di Eva;"),
            ],
            [
                ("3a", "a te sospiriamo,"),
                ("3b", "gementi e piangenti"),
                ("3c", "in questa valle di lacrime."),
            ],
            [
                ("4a", "Orsù dunque,"),
                ("4b", "avvocata nostra,"),
                ("4c", "rivolgi a noi gli occhi tuoi misericordiosi."),
            ],
            [
                ("5a", "E mostraci, dopo questo esilio,"),
                ("5b", "Gesù,"),
                ("5c", "il frutto benedetto del tuo seno."),
                ("5d", "O clemente,"),
            ],
            [
                ("6a", "o pia,"),
                ("6b", "o dolce"),
                ("6c", "Vergine Maria."),
            ],
            [
                ("7a", "Prega per noi,"),
                ("7b", "santa Madre di Dio."),
            ],
            [("8a", "Perché siamo resi degni delle promesse di Cristo.")],
        ],
    )
    # Fix P5 to match EN: exile | show unto us | blessed fruit | Jesus.
    # Italian traditional groups O clement with next - EN has 4 segs in P5 and 3 in P6.
    # EN P5: And after this our exile, | show unto us | the blessed fruit of thy womb, | Jesus.
    # EN P6: O clement, | O loving, | O sweet Virgin Mary.
    write_json(
        "hail-holy-queen/hail-holy-queen.json",
        "hail-holy-queen",
        "Salve, Regina",
        [
            [
                ("1a", "Salve, Regina,"),
                ("1b", "Madre di misericordia,"),
                ("1c", "vita,"),
                ("1d", "dolcezza"),
                ("1e", "e speranza nostra, salve."),
            ],
            [
                ("2a", "A te ricorriamo,"),
                ("2b", "esuli figli di Eva;"),
            ],
            [
                ("3a", "a te sospiriamo,"),
                ("3b", "gementi e piangenti"),
                ("3c", "in questa valle di lacrime."),
            ],
            [
                ("4a", "Orsù dunque,"),
                ("4b", "avvocata nostra,"),
                ("4c", "rivolgi a noi gli occhi tuoi misericordiosi."),
            ],
            [
                ("5a", "E mostraci, dopo questo esilio,"),
                ("5b", "Gesù,"),
                ("5c", "il frutto benedetto del tuo seno,"),
                ("5d", "Gesù."),
            ],
            [
                ("6a", "O clemente,"),
                ("6b", "o pia,"),
                ("6c", "o dolce Vergine Maria."),
            ],
            [
                ("7a", "Prega per noi,"),
                ("7b", "santa Madre di Dio."),
            ],
            [("8a", "Perché siamo resi degni delle promesse di Cristo.")],
        ],
    )
    # Fix P5 properly - EN has show | fruit | Jesus as separate, not double Gesù
    write_json(
        "hail-holy-queen/hail-holy-queen.json",
        "hail-holy-queen",
        "Salve, Regina",
        [
            [
                ("1a", "Salve, Regina,"),
                ("1b", "Madre di misericordia,"),
                ("1c", "vita,"),
                ("1d", "dolcezza"),
                ("1e", "e speranza nostra, salve."),
            ],
            [
                ("2a", "A te ricorriamo,"),
                ("2b", "esuli figli di Eva;"),
            ],
            [
                ("3a", "a te sospiriamo,"),
                ("3b", "gementi e piangenti"),
                ("3c", "in questa valle di lacrime."),
            ],
            [
                ("4a", "Orsù dunque,"),
                ("4b", "avvocata nostra,"),
                ("4c", "rivolgi a noi gli occhi tuoi misericordiosi."),
            ],
            [
                ("5a", "E dopo questo esilio"),
                ("5b", "mostraci"),
                ("5c", "il frutto benedetto del tuo seno,"),
                ("5d", "Gesù."),
            ],
            [
                ("6a", "O clemente,"),
                ("6b", "o pia,"),
                ("6c", "o dolce Vergine Maria."),
            ],
            [
                ("7a", "Prega per noi,"),
                ("7b", "santa Madre di Dio."),
            ],
            [("8a", "Perché siamo resi degni delle promesse di Cristo.")],
        ],
    )

    write_json(
        "hail-holy-queen/rosary-prayer.json",
        "rosary-prayer",
        "Preghiera del Rosario",
        [
            [("1a", "Preghiamo.")],
            [
                ("2a", "O Dio,"),
                ("2b", "il cui Figlio unigenito"),
                ("2c", "con la sua vita,"),
                ("2d", "morte e risurrezione"),
                ("2e", "ci ha acquistato i beni"),
                ("2f", "della vita eterna,"),
            ],
            [
                ("3a", "concedi, ti preghiamo,"),
                ("3b", "che meditando questi misteri"),
                ("3c", "del santissimo Rosario della beata Vergine Maria,"),
            ],
            [
                ("4a", "ne imitiamo ciò che contengono"),
                ("4b", "e otteniamo ciò che promettono,"),
            ],
            [("5a", "per lo stesso Cristo nostro Signore.")],
            [("6a", "Amen.")],
            [
                ("7a", "Sacro Cuore di Gesù,"),
                ("7b", "abbi pietà di noi."),
            ],
            [
                ("8a", "Cuore Immacolato di Maria,"),
                ("8b", "prega per noi."),
            ],
        ],
    )

    write_md(
        "hail-holy-queen.md",
        """---
icon: material/cross
---

# Salve, Regina

<div class="prayer-interactive"
     data-prayer="hail-holy-queen"
     data-json="hail-holy-queen.json"></div>

---

## Preghiera del Rosario

<div class="prayer-interactive"
     data-prayer="rosary-prayer"
     data-json="rosary-prayer.json"></div>

<div class="prayer-fallback" markdown="1">

**Italiano**

Salve, Regina, Madre di misericordia, vita, dolcezza e speranza nostra, salve. A te ricorriamo, esuli figli di Eva; a te sospiriamo, gementi e piangenti in questa valle di lacrime. Orsù dunque, avvocata nostra, rivolgi a noi gli occhi tuoi misericordiosi. E dopo questo esilio mostraci il frutto benedetto del tuo seno, Gesù. O clemente, o pia, o dolce Vergine Maria.

Prega per noi, santa Madre di Dio.

Perché siamo resi degni delle promesse di Cristo.

Preghiamo.

O Dio, il cui Figlio unigenito con la sua vita, morte e risurrezione ci ha acquistato i beni della vita eterna, concedi, ti preghiamo, che meditando questi misteri del santissimo Rosario della beata Vergine Maria, ne imitiamo ciò che contengono e otteniamo ciò che promettono, per lo stesso Cristo nostro Signore. Amen.

Sacro Cuore di Gesù, abbi pietà di noi.

Cuore Immacolato di Maria, prega per noi.

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
        "Preghiera di Gesù",
        [
            [
                ("1a", "Signore Gesù Cristo,"),
                ("1b", "Figlio di Dio,"),
            ],
            [
                ("2a", "abbi pietà di me,"),
                ("2b", "peccatore."),
            ],
        ],
    )
    write_md(
        "extras/jesus-prayer.md",
        prayer_md(
            "Preghiera di Gesù",
            "jesus-prayer",
            "Signore Gesù Cristo, Figlio di Dio, abbi pietà di me, peccatore.",
            "Lord Jesus Christ, Son of God, have mercy on me, a sinner.",
        ),
    )

    # --- Nicene Creed (Italian Missal / CEI form, passage-aligned) ---
    write_json(
        "extras/nicene/nicene.json",
        "nicene",
        "Credo di Nicea",
        [
            [
                ("1a", "Credo in un solo Dio,"),
                ("1b", "Padre onnipotente,"),
                ("1c", "Creatore del cielo e della terra,"),
                ("1d", "di tutte le cose visibili e invisibili."),
            ],
            [
                ("2a", "Credo in un solo Signore, Gesù Cristo,"),
                ("2b", "unigenito Figlio di Dio,"),
                ("2c", "nato dal Padre prima di tutti i secoli:"),
            ],
            [
                ("3a", "Dio da Dio,"),
                ("3b", "Luce da Luce,"),
                ("3c", "Dio vero da Dio vero,"),
                ("3d", "generato, non creato,"),
                ("3e", "della stessa sostanza del Padre;"),
            ],
            [("4a", "per mezzo di lui tutte le cose sono state create.")],
            [
                ("5a", "Per noi uomini e per la nostra salvezza"),
                ("5b", "discese dal cielo,"),
            ],
            [
                ("6a", "e per opera dello Spirito Santo si è incarnato nel seno della Vergine Maria"),
                ("6b", "e si è fatto uomo."),
            ],
            [
                ("7a", "Fu crocifisso per noi sotto Ponzio Pilato,"),
                ("7b", "morì e fu sepolto."),
            ],
            [
                ("8a", "Il terzo giorno è risuscitato,"),
                ("8b", "secondo le Scritture,"),
            ],
            [
                ("9a", "è salito al cielo,"),
                ("9b", "siede alla destra del Padre."),
            ],
            [
                ("10a", "E di nuovo verrà, nella gloria,"),
                ("10b", "per giudicare i vivi e i morti,"),
                ("10c", "e il suo regno non avrà fine."),
            ],
            [
                ("11a", "Credo nello Spirito Santo,"),
                ("11b", "che è Signore e dà la vita,"),
                ("11c", "e procede dal Padre e dal Figlio."),
                ("11d", "Con il Padre e il Figlio è adorato e glorificato,"),
                ("11e", "e ha parlato per mezzo dei profeti."),
            ],
            [("12a", "Credo la Chiesa, una santa cattolica e apostolica.")],
            [
                ("13a", "Professo un solo battesimo"),
                ("13b", "per il perdono dei peccati."),
            ],
            [
                ("14a", "Aspetto la risurrezione dei morti"),
                ("14b", "e la vita del mondo che verrà."),
            ],
            [("15a", "Amen.")],
        ],
    )
    write_md(
        "extras/nicene.md",
        prayer_md(
            "Credo di Nicea",
            "nicene",
            "Credo in un solo Dio, Padre onnipotente, Creatore del cielo e della terra, "
            "di tutte le cose visibili e invisibili. Credo in un solo Signore, Gesù Cristo, "
            "unigenito Figlio di Dio, nato dal Padre prima di tutti i secoli: "
            "Dio da Dio, Luce da Luce, Dio vero da Dio vero, generato, non creato, "
            "della stessa sostanza del Padre; per mezzo di lui tutte le cose sono state create. "
            "Per noi uomini e per la nostra salvezza discese dal cielo, "
            "e per opera dello Spirito Santo si è incarnato nel seno della Vergine Maria e si è fatto uomo. "
            "Fu crocifisso per noi sotto Ponzio Pilato, morì e fu sepolto. "
            "Il terzo giorno è risuscitato, secondo le Scritture, è salito al cielo, siede alla destra del Padre. "
            "E di nuovo verrà, nella gloria, per giudicare i vivi e i morti, e il suo regno non avrà fine. "
            "Credo nello Spirito Santo, che è Signore e dà la vita, e procede dal Padre e dal Figlio. "
            "Con il Padre e il Figlio è adorato e glorificato, e ha parlato per mezzo dei profeti. "
            "Credo la Chiesa, una santa cattolica e apostolica. "
            "Professo un solo battesimo per il perdono dei peccati. "
            "Aspetto la risurrezione dei morti e la vita del mondo che verrà. Amen.",
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

    # --- Psalm 23 (CEI-style sense, passage-aligned) ---
    write_json(
        "extras/psalm-23/psalm-23.json",
        "psalm-23",
        "Salmo 23",
        [
            [("1a", "Salmo di Davide.")],
            [
                ("2a", "Il Signore è il mio pastore:"),
                ("2b", "non manco di nulla."),
            ],
            [
                ("3a", "Su pascoli erbosi mi fa riposare,"),
                ("3b", "ad acque tranquille mi conduce."),
            ],
            [
                ("4a", "Rinfranca l'anima mia,"),
                ("4b", "mi guida per il giusto cammino"),
                ("4c", "per amore del suo nome."),
            ],
            [
                ("5a", "Se dovessi camminare in una valle oscura,"),
                ("5b", "non temerei alcun male,"),
                ("5c", "perché tu sei con me."),
            ],
            [
                ("6a", "Il tuo bastone e il tuo vincastro"),
                ("6b", "mi danno sicurezza."),
            ],
            [
                ("7a", "Davanti a me tu prepari una mensa"),
                ("7b", "sotto gli occhi dei miei nemici."),
            ],
            [
                ("8a", "Ungi di olio il mio capo;"),
                ("8b", "il mio calice trabocca."),
            ],
            [
                ("9a", "Felicità e grazia mi saranno compagne"),
                ("9b", "tutti i giorni della mia vita,"),
            ],
            [
                ("10a", "e abiterò nella casa del Signore"),
                ("10b", "per lunghi giorni."),
            ],
        ],
    )
    write_md(
        "extras/psalm-23.md",
        prayer_md(
            "Salmo 23",
            "psalm-23",
            "Salmo di Davide. Il Signore è il mio pastore: non manco di nulla. "
            "Su pascoli erbosi mi fa riposare, ad acque tranquille mi conduce. "
            "Rinfranca l'anima mia, mi guida per il giusto cammino per amore del suo nome. "
            "Se dovessi camminare in una valle oscura, non temerei alcun male, perché tu sei con me. "
            "Il tuo bastone e il tuo vincastro mi danno sicurezza. "
            "Davanti a me tu prepari una mensa sotto gli occhi dei miei nemici. "
            "Ungi di olio il mio capo; il mio calice trabocca. "
            "Felicità e grazia mi saranno compagne tutti i giorni della mia vita, "
            "e abiterò nella casa del Signore per lunghi giorni.",
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

    # --- Psalm 51 (aligned to EN Douay structure) ---
    write_json(
        "extras/psalm-51/psalm-51.json",
        "psalm-51",
        "Salmo 51",
        [
            [
                ("1a", "Al termine,"),
                ("1b", "salmo di Davide,"),
            ],
            [
                ("2a", "quando il profeta Natan venne a lui,"),
                ("2b", "dopo che ebbe peccato con Betsabea."),
            ],
            [
                ("3a", "Pietà di me, o Dio,"),
                ("3b", "secondo la tua misericordia;"),
                ("3c", "nella tua grande bontà"),
                ("3d", "cancella il mio peccato."),
            ],
            [
                ("4a", "Lavami da ogni mia colpa,"),
                ("4b", "purificami da ogni mio peccato."),
            ],
            [
                ("5a", "Riconosco la mia colpa,"),
                ("5b", "il mio peccato mi sta sempre dinanzi."),
            ],
            [
                ("6a", "Contro di te, contro te solo ho peccato,"),
                ("6b", "quello che è male ai tuoi occhi, io l'ho fatto:"),
                ("6c", "perciò sei giusto quando parli,"),
                ("6d", "retto nel tuo giudizio."),
            ],
            [
                ("7a", "Ecco, nella colpa sono stato generato,"),
                ("7b", "nel peccato mi ha concepito mia madre."),
            ],
            [
                ("8a", "Ma tu vuoi la sincerità del cuore,"),
                ("8b", "e nell'intimo m'insegni la sapienza."),
                ("8c", "Purificami con issòpo e sarò mondo;"),
            ],
            [
                ("9a", "lavami e sarò più bianco della neve."),
                ("9b", "Fammi sentire gioia e letizia:"),
                ("9c", "esulteranno le ossa che hai spezzato."),
                ("9d", "Distogli lo sguardo dai miei peccati,"),
            ],
            [
                ("10a", "cancella tutte le mie colpe."),
                ("10b", "Crea in me, o Dio, un cuore puro,"),
            ],
            [
                ("11a", "rinnova in me uno spirito saldo."),
                ("11b", "Non respingermi dalla tua presenza"),
            ],
            [
                ("12a", "e non privarmi del tuo santo spirito."),
                ("12b", "Rendimi la gioia di essere salvato,"),
            ],
            [
                ("13a", "sostieni in me un animo generoso."),
                ("13b", "Insegnerò ai ribelli le tue vie"),
            ],
            [
                ("14a", "e i peccatori a te ritorneranno."),
                ("14b", "Liberami dal sangue, o Dio, Dio mia salvezza,"),
            ],
            [
                ("15a", "e la mia lingua esalterà la tua giustizia."),
                ("15b", "Signore, apri le mie labbra"),
            ],
            [
                ("16a", "e la mia bocca proclami la tua lode;"),
                ("16b", "poiché non gradisci il sacrificio"),
                ("16c", "e, se offro olocausti, non li accetti."),
            ],
            [
                ("17a", "Uno spirito contrito è sacrificio a Dio;"),
                ("17b", "un cuore affranto e umiliato, o Dio, non disprezzi."),
            ],
            [
                ("18a", "Nel tuo amore fa grazia a Sion,"),
                ("18b", "rialza le mura di Gerusalemme."),
                ("18c", "Allora gradirai i sacrifici prescritti,"),
            ],
            [
                ("19a", "l'olocausto e l'intera oblazione,"),
                ("19b", "allora immoleranno vittime"),
                ("19c", "sul tuo altare."),
            ],
            [
                ("20a", "Fa' grazia, o Signore,"),
                ("20b", "a Sion secondo la tua bontà;"),
                ("20c", "siano riedificate le mura di Gerusalemme."),
            ],
            [
                ("21a", "Allora gradirai i sacrifici di giustizia,"),
                ("21b", "oblazioni e olocausti;"),
                ("21c", "allora si offriranno vitelli sul tuo altare."),
            ],
        ],
    )
    # Psalm 51 structure got mangled - rewrite carefully matching EN segment counts exactly
    write_json(
        "extras/psalm-51/psalm-51.json",
        "psalm-51",
        "Salmo 51",
        [
            [
                ("1a", "Al termine,"),
                ("1b", "salmo di Davide,"),
            ],
            [
                ("2a", "quando il profeta Natan venne a lui,"),
                ("2b", "dopo che ebbe peccato con Betsabea."),
            ],
            [
                ("3a", "Pietà di me, o Dio,"),
                ("3b", "secondo la tua misericordia;"),
                ("3c", "nella tua grande bontà"),
                ("3d", "cancella il mio peccato."),
            ],
            [
                ("4a", "Lavami da ogni mia colpa,"),
                ("4b", "purificami da ogni mio peccato."),
            ],
            [
                ("5a", "Riconosco la mia colpa,"),
                ("5b", "il mio peccato mi sta sempre dinanzi."),
            ],
            [
                ("6a", "Contro di te, contro te solo ho peccato,"),
                ("6b", "quello che è male ai tuoi occhi, io l'ho fatto:"),
                ("6c", "perciò sei giusto quando parli,"),
                ("6d", "retto nel tuo giudizio."),
            ],
            [
                ("7a", "Ecco, nella colpa sono stato generato,"),
                ("7b", "nel peccato mi ha concepito mia madre."),
            ],
            [
                ("8a", "Ma tu vuoi la sincerità del cuore:"),
                ("8b", "nell'intimo m'insegni la sapienza."),
                ("8c", "Purificami con issòpo e sarò mondo;"),
            ],
            [
                ("9a", "lavami"),
                ("9b", "e sarò più bianco della neve."),
                ("9c", "Fammi sentire gioia e letizia:"),
                ("9d", "esulteranno le ossa che hai spezzato."),
            ],
            [
                ("10a", "Distogli lo sguardo dai miei peccati,"),
                ("10b", "cancella tutte le mie colpe."),
            ],
            [
                ("11a", "Crea in me, o Dio, un cuore puro,"),
                ("11b", "rinnova in me uno spirito saldo."),
            ],
            [
                ("12a", "Non respingermi dalla tua presenza"),
                ("12b", "e non privarmi del tuo santo spirito."),
            ],
            [
                ("13a", "Rendimi la gioia di essere salvato,"),
                ("13b", "sostieni in me un animo generoso."),
            ],
            [
                ("14a", "Insegnerò ai ribelli le tue vie"),
                ("14b", "e i peccatori a te ritorneranno."),
            ],
            [
                ("15a", "Liberami dal sangue, o Dio,"),
                ("15b", "Dio mia salvezza,"),
                ("15c", "e la mia lingua esalterà la tua giustizia."),
            ],
            [
                ("16a", "Signore, apri le mie labbra"),
                ("16b", "e la mia bocca proclami la tua lode."),
            ],
            [
                ("17a", "Poiché non gradisci il sacrificio,"),
                ("17b", "e, se offro olocausti, non li accetti."),
            ],
            [
                ("18a", "Uno spirito contrito è sacrificio a Dio;"),
                ("18b", "un cuore affranto e umiliato, o Dio,"),
                ("18c", "non disprezzi."),
            ],
            [
                ("19a", "Nel tuo amore fa grazia a Sion,"),
                ("19b", "rialza le mura di Gerusalemme."),
            ],
            [
                ("20a", "Fa' grazia, o Signore,"),
                ("20b", "a Sion secondo la tua bontà;"),
                ("20c", "siano riedificate le mura di Gerusalemme."),
            ],
            [
                ("21a", "Allora gradirai i sacrifici di giustizia,"),
                ("21b", "oblazioni e olocausti;"),
                ("21c", "allora si offriranno vitelli sul tuo altare."),
            ],
        ],
    )
    # Still wrong - EN psalm-51:
    # P8 has 3, P9 has 4, P10 has 2, ... P15 has 2, P16 has 3, P17 has 2, P18 has 3, P19 has 3, P20 has 3, P21 has 3
    # My last version:
    # P8=3 ok, P9=4 ok, P10=2 ok, P11=2 but EN P11 is turn away face (2), P12 create heart (2)
    # Wait I have P10=2, P11=2, P12=2, P13=2, P14=2, P15=3 - EN P15 is teach unjust (2), P16 deliver blood (3)
    # I shifted. Fix properly from German scaffold which was verified.

    write_json(
        "extras/psalm-51/psalm-51.json",
        "psalm-51",
        "Salmo 51",
        [
            [("1a", "Al termine,"), ("1b", "salmo di Davide,")],
            [
                ("2a", "quando il profeta Natan venne a lui,"),
                ("2b", "dopo che ebbe peccato con Betsabea."),
            ],
            [
                ("3a", "Pietà di me, o Dio,"),
                ("3b", "secondo la tua misericordia;"),
                ("3c", "nella tua grande bontà"),
                ("3d", "cancella il mio peccato."),
            ],
            [
                ("4a", "Lavami da ogni mia colpa,"),
                ("4b", "purificami da ogni mio peccato."),
            ],
            [
                ("5a", "Riconosco la mia colpa,"),
                ("5b", "il mio peccato mi sta sempre dinanzi."),
            ],
            [
                ("6a", "Contro di te, contro te solo ho peccato,"),
                ("6b", "quello che è male ai tuoi occhi, io l'ho fatto:"),
                ("6c", "perciò sei giusto quando parli,"),
                ("6d", "retto nel tuo giudizio."),
            ],
            [
                ("7a", "Ecco, nella colpa sono stato generato,"),
                ("7b", "nel peccato mi ha concepito mia madre."),
            ],
            [
                ("8a", "Ma tu vuoi la sincerità del cuore:"),
                ("8b", "le cose nascoste e segrete della tua sapienza"),
                ("8c", "mi hai manifestato."),
            ],
            [
                ("9a", "Aspergimi con issòpo,"),
                ("9b", "e sarò mondato;"),
                ("9c", "lavami,"),
                ("9d", "e sarò più bianco della neve."),
            ],
            [
                ("10a", "Fammi udire gioia e letizia:"),
                ("10b", "e le ossa umiliate esulteranno."),
            ],
            [
                ("11a", "Distogli lo sguardo dai miei peccati,"),
                ("11b", "e cancella tutte le mie iniquità."),
            ],
            [
                ("12a", "Crea in me, o Dio, un cuore puro,"),
                ("12b", "e rinnova in me uno spirito retto."),
            ],
            [
                ("13a", "Non respingermi dalla tua presenza,"),
                ("13b", "e non togliermi il tuo santo spirito."),
            ],
            [
                ("14a", "Rendimi la gioia della tua salvezza,"),
                ("14b", "e sostienimi con uno spirito generoso."),
            ],
            [
                ("15a", "Insegnerò agli empi le tue vie,"),
                ("15b", "e i peccatori a te ritorneranno."),
            ],
            [
                ("16a", "Liberami dal sangue, o Dio,"),
                ("16b", "Dio della mia salvezza,"),
                ("16c", "e la mia lingua esalterà la tua giustizia."),
            ],
            [
                ("17a", "Signore, apri le mie labbra,"),
                ("17b", "e la mia bocca proclamerà la tua lode."),
            ],
            [
                ("18a", "Poiché se avessi voluto un sacrificio,"),
                ("18b", "te l'avrei dato;"),
                ("18c", "ma non ti diletti di olocausti."),
            ],
            [
                ("19a", "Sacrificio a Dio è uno spirito contrito;"),
                ("19b", "un cuore contrito e umiliato, o Dio,"),
                ("19c", "tu non disprezzi."),
            ],
            [
                ("20a", "Tratta favorevolmente, o Signore,"),
                ("20b", "Sion nella tua benevolenza;"),
                ("20c", "siano riedificate le mura di Gerusalemme."),
            ],
            [
                ("21a", "Allora gradirai i sacrifici di giustizia,"),
                ("21b", "oblazioni e olocausti;"),
                ("21c", "allora si offriranno vitelli sul tuo altare."),
            ],
        ],
    )

    write_md(
        "extras/psalm-51.md",
        prayer_md(
            "Salmo 51",
            "psalm-51",
            "Al termine, salmo di Davide, quando il profeta Natan venne a lui, "
            "dopo che ebbe peccato con Betsabea. "
            "Pietà di me, o Dio, secondo la tua misericordia; nella tua grande bontà cancella il mio peccato. "
            "Lavami da ogni mia colpa, purificami da ogni mio peccato. "
            "Riconosco la mia colpa, il mio peccato mi sta sempre dinanzi. "
            "Contro di te, contro te solo ho peccato, quello che è male ai tuoi occhi, io l'ho fatto: "
            "perciò sei giusto quando parli, retto nel tuo giudizio. "
            "Ecco, nella colpa sono stato generato, nel peccato mi ha concepito mia madre. "
            "Ma tu vuoi la sincerità del cuore: le cose nascoste e segrete della tua sapienza mi hai manifestato. "
            "Aspergimi con issòpo, e sarò mondato; lavami, e sarò più bianco della neve. "
            "Fammi udire gioia e letizia: e le ossa umiliate esulteranno. "
            "Distogli lo sguardo dai miei peccati, e cancella tutte le mie iniquità. "
            "Crea in me, o Dio, un cuore puro, e rinnova in me uno spirito retto. "
            "Non respingermi dalla tua presenza, e non togliermi il tuo santo spirito. "
            "Rendimi la gioia della tua salvezza, e sostienimi con uno spirito generoso. "
            "Insegnerò agli empi le tue vie, e i peccatori a te ritorneranno. "
            "Liberami dal sangue, o Dio, Dio della mia salvezza, e la mia lingua esalterà la tua giustizia. "
            "Signore, apri le mie labbra, e la mia bocca proclamerà la tua lode. "
            "Poiché se avessi voluto un sacrificio, te l'avrei dato; ma non ti diletti di olocausti. "
            "Sacrificio a Dio è uno spirito contrito; un cuore contrito e umiliato, o Dio, tu non disprezzi. "
            "Tratta favorevolmente, o Signore, Sion nella tua benevolenza; siano riedificate le mura di Gerusalemme. "
            "Allora gradirai i sacrifici di giustizia, oblazioni e olocausti; allora si offriranno vitelli sul tuo altare.",
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
        ("joyful1", "Il primo mistero gaudioso, l'Annunciazione"),
        ("joyful2", "Il secondo mistero gaudioso, la Visitazione"),
        ("joyful3", "Il terzo mistero gaudioso, la Natività"),
        ("joyful4", "Il quarto mistero gaudioso, la Presentazione"),
        ("joyful5", "Il quinto mistero gaudioso, il Ritrovamento di Gesù nel Tempio"),
        ("sorrowful1", "Il primo mistero doloroso, l'Agonia nell'Orto"),
        ("sorrowful2", "Il secondo mistero doloroso, la Flagellazione"),
        ("sorrowful3", "Il terzo mistero doloroso, la Coronazione di spine"),
        ("sorrowful4", "Il quarto mistero doloroso, la Salita al Calvario"),
        ("sorrowful5", "Il quinto mistero doloroso, la Crocifissione"),
        ("glorious1", "Il primo mistero glorioso, la Risurrezione"),
        ("glorious2", "Il secondo mistero glorioso, l'Ascensione"),
        ("glorious3", "Il terzo mistero glorioso, la Discesa dello Spirito Santo"),
        ("glorious4", "Il quarto mistero glorioso, l'Assunzione"),
        ("glorious5", "Il quinto mistero glorioso, l'Incoronazione di Maria"),
        ("luminous1", "Il primo mistero luminoso, il Battesimo di Gesù"),
        ("luminous2", "Il secondo mistero luminoso, le Nozze di Cana"),
        ("luminous3", "Il terzo mistero luminoso, l'Annuncio del Regno"),
        ("luminous4", "Il quarto mistero luminoso, la Trasfigurazione"),
        ("luminous5", "Il quinto mistero luminoso, l'Istituzione dell'Eucaristia"),
    ]
    for mid, title in mysteries:
        write_json(
            f"mysteries/{mid}.json",
            mid,
            title,
            [[("1a", title + ".")]],
        )

    write_md(
        "index.md",
        """---
icon: lucide/languages
---

# <span tooltip="Italian">Italiano</span>

!!! quote "San Luigi Maria Grignion de Montfort"

    Il Rosario è dunque un misto benedetto di preghiera mentale e vocale, con cui onoriamo e impariamo a imitare i misteri e le virtù della vita, della morte, della passione e della gloria di Gesù e di Maria.

    *The Rosary is therefore a blessed mixture of mental and vocal prayer by which we honor and learn to imitate the mysteries and virtues of the life, death, passion and glory of Jesus and Mary.*

<div class="mystery-chooser">
<span class="mystery-set" data-set="joyful">Misteri Gaudiosi</span>
<span class="mystery-set" data-set="sorrowful">Misteri Dolorosi</span>
<span class="mystery-set" data-set="glorious">Misteri Gloriosi</span>
<span class="mystery-set" data-set="luminous">Misteri Luminosi</span>
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

    write_md(
        "resources/pronunciation.md",
        """---
icon: lucide/mic
---

# <span tooltip="Pronunciation">Pronuncia</span>

Italian is a Romance language that grew from the Latin of the peninsula. Written standards were shaped by Dante, Petrarch, and Boccaccio, and later by the Accademia della Crusca. The Rosary in Italian -- <span tooltip="Our Father">Padre Nostro</span>, <span tooltip="Hail Mary">Ave Maria</span>, <span tooltip="Glory Be">Gloria al Padre</span> -- is prayed with clear, open vowels and a steady, song-like rhythm well suited to the beads.

Pronunciation is often left to natural exposure. English speakers commonly reduce pure vowels to glides, under-roll **r**, and soften double consonants. Clear rules and Rosary examples short-circuit that.

!!! quote "Henry Widdowson"
    The whole point of language pedagogy is that it is a way of short-circuiting the slow process of natural discovery and can make arrangements for learning to happen more easily and more efficiently than it does in natural surroundings.




---

## Vowels

Italian has five pure vowels. Hold each quality steady; do not glide as in English "go" or "name".

!!! success "Core vowels"
    + **a** as in father -- e.g. <span tooltip="Father">Padre</span>, <span tooltip="Mary">Maria</span>
    + **e** (open or closed) -- e.g. <span tooltip="is">è</span>, <span tooltip="full">piena</span>
    + **i** as ee in see -- e.g. <span tooltip="Spirit">Spirito</span>
    + **o** pure o, lips rounded -- e.g. <span tooltip="name">nome</span>, <span tooltip="death">morte</span>
    + **u** as oo in boot -- e.g. <span tooltip="one">uno</span>, <span tooltip="fruit">frutto</span>




---

## Consonants that matter for the Rosary

!!! success "Hard spots for English speakers"
    + **c** before e/i is **ch** as in church -- e.g. <span tooltip="heaven">cieli</span>, <span tooltip="peace">pace</span>
    + **ch** is always hard **k** -- e.g. <span tooltip="who">che</span>, <span tooltip="Church">Chiesa</span>
    + **g** before e/i is soft (**j** as in judge) -- e.g. <span tooltip="Jesus">Gesù</span>
    + **gh** is hard **g** -- e.g. in loan words; rosary text rarely needs it
    + **gl** before i often like Spanish ll / English "million" y -- e.g. <span tooltip="Son">Figlio</span>
    + **gn** like Spanish ñ -- e.g. <span tooltip="every">ogni</span>, <span tooltip="worthy">degni</span>
    + **r** is tapped or lightly rolled
    + Double consonants are held longer: <span tooltip="Father">Padre</span> vs a hypothetical single **d**; <span tooltip="all">tutte</span>, <span tooltip="sins">peccati</span>




---

## Prayer tips

!!! tip "Rosary delivery"
    Keep a steady, unhurried pace. Elsa at **-10%** matches a prayerful tempo.
    Stress content words: **Pa**-dre **no**-stro, **A**-ve **Ma**-ri-a, **pie**-na di **gra**-zia, **Ge**-sù.
    Final vowels stay clear; Italian rarely drops them.




---

## Recommendations

!!! success "<span tooltip='Recommended'>Consigliato</span>"
    Pure vowels. Clear double consonants. Soft **c/g** before e/i; hard **ch**. Match the prayer audio line by line.

!!! failure "<span tooltip='Not recommended'>Sconsigliato</span>"
    English diphthongs on Italian vowels. Softening doubles. Reading **ch** as English "church". Swallowing final vowels.
""",
    )

    print("Done scaffolding italian/")


if __name__ == "__main__":
    main()
