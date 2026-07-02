---
icon: lucide/languages
---

# English

<div class="mystery-chooser">
<span class="mystery-set" data-set="joyful">Joyful Mysteries</span>
<span class="mystery-set" data-set="sorrowful">Sorrowful Mysteries</span>
<span class="mystery-set" data-set="glorious">Glorious Mysteries</span>
<span class="mystery-set" data-set="luminous">Luminous Mysteries</span>
</div>

<div id="rosary-player">
  <div id="rosary-indicators" class="rosary-indicators"></div>
  <div class="rosary-controls">
    <button id="rosary-prev" class="rosary-btn" title="Previous">◀◀</button>
    <button id="rosary-play" class="rosary-btn" title="Play / pause auto">▶</button>
    <button id="rosary-phonetic" class="rosary-btn" title="Toggle phonetic"></button>
    <button id="rosary-next" class="rosary-btn" title="Next">▶▶</button>
  </div>
  <div id="rosary-viewer"></div>
</div>

<script type="application/json" id="rosary-mysteries">
{
  "titles": {
    "joyful": "Joyful Mysteries",
    "sorrowful": "Sorrowful Mysteries",
    "glorious": "Glorious Mysteries",
    "luminous": "Luminous Mysteries"
  },
  "mysteries": {
    "joyful": [
      "The First Joyful Mystery, the Annunciation",
      "The Second Joyful Mystery, the Visitation",
      "The Third Joyful Mystery, the Nativity",
      "The Fourth Joyful Mystery, the Presentation",
      "The Fifth Joyful Mystery, the Finding of Jesus in the Temple"
    ],
    "sorrowful": [
      "The First Sorrowful Mystery, the Agony in the Garden",
      "The Second Sorrowful Mystery, the Scourging at the Pillar",
      "The Third Sorrowful Mystery, the Crowning with Thorns",
      "The Fourth Sorrowful Mystery, the Carrying of the Cross",
      "The Fifth Sorrowful Mystery, the Crucifixion"
    ],
    "glorious": [
      "The First Glorious Mystery, the Resurrection",
      "The Second Glorious Mystery, the Ascension",
      "The Third Glorious Mystery, the Descent of the Holy Spirit",
      "The Fourth Glorious Mystery, the Assumption",
      "The Fifth Glorious Mystery, the Coronation of Mary"
    ],
    "luminous": [
      "The First Luminous Mystery, the Baptism of Jesus",
      "The Second Luminous Mystery, the Wedding at Cana",
      "The Third Luminous Mystery, the Proclamation of the Kingdom",
      "The Fourth Luminous Mystery, the Transfiguration",
      "The Fifth Luminous Mystery, the Institution of the Eucharist"
    ]
  }
}
</script>
