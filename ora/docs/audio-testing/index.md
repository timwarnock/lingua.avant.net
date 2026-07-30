# Italian Edge TTS -- female voices

Qualitative listen tests for **Italiano** Rosary audio. Prefer a clear female voice suitable for prayer (not rushed, not theatrical).

**Voices** (female only):

+ `it-IT-ElsaNeural` -- slug **elsa**
+ `it-IT-IsabellaNeural` -- slug **isabella**

**Rates:** `+0%`, `-5%`, `-10%`

Each section is a short real prayer line (first two Hail Mary passages). Play variants and note the winning voice + rate.

Regenerate samples:

```bash
uv run --with edge-tts python audio-utils/generate-italian-voice-ab.py
```

---

## 1. Hail Mary passage 1

**Source:** Ave Maria -- passage 1 (EN: Hail Mary, full of grace, the Lord is with thee.)

**Text:** `Ave Maria, piena di grazia, il Signore è con te.`

**Variants** (click label to play):

+ <span onclick="new Audio('hm1-elsa-0.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>elsa @ +0%</strong></span> -- `it-IT-ElsaNeural` rate `+0%`
+ <span onclick="new Audio('hm1-elsa-m5.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>elsa @ -5%</strong></span> -- `it-IT-ElsaNeural` rate `-5%`
+ <span onclick="new Audio('hm1-elsa-m10.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>elsa @ -10%</strong></span> -- `it-IT-ElsaNeural` rate `-10%`
+ <span onclick="new Audio('hm1-isabella-0.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>isabella @ +0%</strong></span> -- `it-IT-IsabellaNeural` rate `+0%`
+ <span onclick="new Audio('hm1-isabella-m5.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>isabella @ -5%</strong></span> -- `it-IT-IsabellaNeural` rate `-5%`
+ <span onclick="new Audio('hm1-isabella-m10.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>isabella @ -10%</strong></span> -- `it-IT-IsabellaNeural` rate `-10%`

---

## 2. Hail Mary passage 2

**Source:** Ave Maria -- passage 2 (EN: Blessed art thou amongst women, and blessed is the fruit of thy womb, Jesus.)

**Text:** `Tu sei benedetta fra le donne, e benedetto è il frutto del tuo seno, Gesù.`

**Variants** (click label to play):

+ <span onclick="new Audio('hm2-elsa-0.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>elsa @ +0%</strong></span> -- `it-IT-ElsaNeural` rate `+0%`
+ <span onclick="new Audio('hm2-elsa-m5.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>elsa @ -5%</strong></span> -- `it-IT-ElsaNeural` rate `-5%`
+ <span onclick="new Audio('hm2-elsa-m10.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>elsa @ -10%</strong></span> -- `it-IT-ElsaNeural` rate `-10%`
+ <span onclick="new Audio('hm2-isabella-0.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>isabella @ +0%</strong></span> -- `it-IT-IsabellaNeural` rate `+0%`
+ <span onclick="new Audio('hm2-isabella-m5.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>isabella @ -5%</strong></span> -- `it-IT-IsabellaNeural` rate `-5%`
+ <span onclick="new Audio('hm2-isabella-m10.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>isabella @ -10%</strong></span> -- `it-IT-IsabellaNeural` rate `-10%`

---

## Checklist

| # | Sample | Winner voice | Rate | Notes |
|---|--------|--------------|------|-------|
| 1 | Hail Mary passage 1 |  |  |  |
| 2 | Hail Mary passage 2 |  |  |  |

**Overall pick:** voice `______` rate `______`
