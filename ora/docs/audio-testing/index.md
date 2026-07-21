# Latin Edge TTS A/B -- Sancta / sanct-

Qualitative listen tests for ecclesiastical Latin with **it-IT-DiegoNeural** at rate **-15%** (same as production Latin prayers).

Focus: **Sancta** and the **sanct-** stem. Italian Edge often reduces these toward Spanish/Italian **Santa** (no hard **k**). Liturgical Latin keeps the **k**: **SAHNK-tah** (sanc-ta).

Each section is a real prayer segment. Play variants and note the winning slug.

Regenerate samples:

```bash
uv run --with edge-tts python audio-utils/generate-latin-ab.py
```

---

## 1. Sancta (Ave Maria 3a)

**Source:** Ave Maria 3a -- Sancta Maria,

**Display text:** `Sancta Maria,`

**Liturgical Latin target:** SAHNK-tah mah-REE-ah: hard k in Sancta before t (sanc-ta), not Spanish/Italian Santa without the k. Two clear syllables in Sancta.

**Variants** (click label to play):

+ <span onclick="new Audio('sancta-maria-cur.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>cur</strong></span> -- phonetic: `Sancta Maria,`
+ <span onclick="new Audio('sancta-maria-sankta.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sankta</strong></span> -- phonetic: `Sankta Maria,`
+ <span onclick="new Audio('sancta-maria-sànkta.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sànkta</strong></span> -- phonetic: `Sànkta Maria,`
+ <span onclick="new Audio('sancta-maria-sanc-ta.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sanc-ta</strong></span> -- phonetic: `Sanc-ta Maria,`
+ <span onclick="new Audio('sancta-maria-sank-ta.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sank-ta</strong></span> -- phonetic: `Sank-ta Maria,`
+ <span onclick="new Audio('sancta-maria-sangta.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sangta</strong></span> -- phonetic: `Sangta Maria,`
+ <span onclick="new Audio('sancta-maria-santa.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>santa</strong></span> -- phonetic: `Santa Maria,`

---

## 2. sancta (Salve Regina 7b)

**Source:** Salve Regina 7b -- sancta Dei Genitrix.

**Display text:** `sancta Dei Genitrix.`

**Liturgical Latin target:** SAHNK-tah DEH-ee: same hard k in sancta; lowercase as in the prayer. Dei already locked as Déi in production phonetic.

**Variants** (click label to play):

+ <span onclick="new Audio('sancta-dei-cur.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>cur</strong></span> -- phonetic: `sancta Déi Genitrix.`
+ <span onclick="new Audio('sancta-dei-sankta.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sankta</strong></span> -- phonetic: `sankta Déi Genitrix.`
+ <span onclick="new Audio('sancta-dei-sànkta.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sànkta</strong></span> -- phonetic: `sànkta Déi Genitrix.`
+ <span onclick="new Audio('sancta-dei-sanc-ta.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sanc-ta</strong></span> -- phonetic: `sanc-ta Déi Genitrix.`
+ <span onclick="new Audio('sancta-dei-sank-ta.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sank-ta</strong></span> -- phonetic: `sank-ta Déi Genitrix.`

---

## 3. sanctam (Apostles Creed 11b)

**Source:** Symbolum Apostolorum 11b -- sanctam Ecclesiam catholicam,

**Display text:** `sanctam Ecclesiam catholicam,`

**Liturgical Latin target:** SAHNK-tahm: hard k before t; final -am as ahm. Not "san-tam" without k.

**Variants** (click label to play):

+ <span onclick="new Audio('sanctam-cur.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>cur</strong></span> -- phonetic: `sanctam Ecclesiam catholicam,`
+ <span onclick="new Audio('sanctam-sanktam.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sanktam</strong></span> -- phonetic: `sanktam Ecclesiam catholicam,`
+ <span onclick="new Audio('sanctam-sànktam.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sànktam</strong></span> -- phonetic: `sànktam Ecclesiam catholicam,`
+ <span onclick="new Audio('sanctam-sanc-tam.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sanc-tam</strong></span> -- phonetic: `sanc-tam Ecclesiam catholicam,`

---

## 4. Sancto (Gloria 1c / Creed)

**Source:** Gloria Patri 1c -- et Spiritui Sancto.

**Display text:** `et Spiritui Sancto.`

**Liturgical Latin target:** SAHNK-to: hard k in Sancto. Same sanct- stem as Sancta.

**Variants** (click label to play):

+ <span onclick="new Audio('sancto-cur.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>cur</strong></span> -- phonetic: `et Spiritui Sancto.`
+ <span onclick="new Audio('sancto-sankto.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sankto</strong></span> -- phonetic: `et Spiritui Sankto.`
+ <span onclick="new Audio('sancto-sànkto.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sànkto</strong></span> -- phonetic: `et Spiritui Sànkto.`
+ <span onclick="new Audio('sancto-sanc-to.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sanc-to</strong></span> -- phonetic: `et Spiritui Sanc-to.`

---

## 5. Sancti (Sign of the Cross 1c)

**Source:** Signum Crucis 1c -- et Spiritus Sancti.

**Display text:** `et Spiritus Sancti.`

**Liturgical Latin target:** SAHNK-tee: hard k in Sancti; final -i as ee.

**Variants** (click label to play):

+ <span onclick="new Audio('sancti-cur.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>cur</strong></span> -- phonetic: `et Spiritus Sancti,`
+ <span onclick="new Audio('sancti-sankti.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sankti</strong></span> -- phonetic: `et Spiritus Sankti,`
+ <span onclick="new Audio('sancti-sànkti.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sànkti</strong></span> -- phonetic: `et Spiritus Sànkti,`
+ <span onclick="new Audio('sancti-sanc-ti.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sanc-ti</strong></span> -- phonetic: `et Spiritus Sanc-ti,`

---

## 6. Sanctum (Apostles Creed 11a)

**Source:** Symbolum Apostolorum 11a -- Credo in Spiritum Sanctum,

**Display text:** `Credo in Spiritum Sanctum,`

**Liturgical Latin target:** SAHNK-toom: hard k in Sanctum; -um as oom.

**Variants** (click label to play):

+ <span onclick="new Audio('sanctum-cur.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>cur</strong></span> -- phonetic: `Credo in Spiritum Sanctum,`
+ <span onclick="new Audio('sanctum-sanktum.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sanktum</strong></span> -- phonetic: `Credo in Spiritum Sanktum,`
+ <span onclick="new Audio('sanctum-sànktum.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sànktum</strong></span> -- phonetic: `Credo in Spiritum Sànktum,`
+ <span onclick="new Audio('sanctum-sanc-tum.mp3').play()" style="cursor:pointer; text-decoration:underline"><strong>sanc-tum</strong></span> -- phonetic: `Credo in Spiritum Sanc-tum,`

---

## Checklist

| # | Focus | Winner slug | Notes |
|---|-------|-------------|-------|
| 1 | Sancta (Ave Maria 3a) |  |  |
| 2 | sancta (Salve Regina 7b) |  |  |
| 3 | sanctam (Apostles Creed 11b) |  |  |
| 4 | Sancto (Gloria 1c / Creed) |  |  |
| 5 | Sancti (Sign of the Cross 1c) |  |  |
| 6 | Sanctum (Apostles Creed 11a) |  |  |
