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

---

???+ quote "<span class='mystery-set-title'>Joyful Mysteries</span>"
    
    [Sign of the Cross](sign-of-the-cross.md)
    
    [Apostles' Creed](apostles-creed.md)
    
    [Our Father](our-father.md)
    
    3 x [Hail Mary](hail-mary.md)
    
    [Glory Be](glory-be.md)
    
    [Fatima Prayer](fatima-prayer.md)


???+ quote "<span class='decade-label'>First Decade</span>"
    
    [Our Father](our-father.md)
    
    10 x [Hail Mary](hail-mary.md)
    
    [Glory Be](glory-be.md)
    
    [Fatima Prayer](fatima-prayer.md)


???+ quote "<span class='decade-label'>Second Decade</span>"
    
    [Our Father](our-father.md)
    
    10 x [Hail Mary](hail-mary.md)
    
    [Glory Be](glory-be.md)
    
    [Fatima Prayer](fatima-prayer.md)

???+ quote "<span class='decade-label'>Third Decade</span>"
    
    [Our Father](our-father.md)
    
    10 x [Hail Mary](hail-mary.md)
    
    [Glory Be](glory-be.md)
    
    [Fatima Prayer](fatima-prayer.md)

???+ quote "<span class='decade-label'>Fourth Decade</span>"
    
    [Our Father](our-father.md)
    
    10 x [Hail Mary](hail-mary.md)
    
    [Glory Be](glory-be.md)
    
    [Fatima Prayer](fatima-prayer.md)

???+ quote "<span class='decade-label'>Fifth Decade</span>"
    
    [Our Father](our-father.md)
    
    10 x [Hail Mary](hail-mary.md)
    
    [Glory Be](glory-be.md)
    
    [Fatima Prayer](fatima-prayer.md)

[Hail, Holy Queen](hail-holy-queen.md)

<script>
const MYSTERIES = {
  joyful: [
    "The First Joyful Mystery, the Annunciation",
    "The Second Joyful Mystery, the Visitation",
    "The Third Joyful Mystery, the Nativity",
    "The Fourth Joyful Mystery, the Presentation",
    "The Fifth Joyful Mystery, the Finding of Jesus in the Temple"
  ],
  sorrowful: [
    "The First Sorrowful Mystery, the Agony in the Garden",
    "The Second Sorrowful Mystery, the Scourging at the Pillar",
    "The Third Sorrowful Mystery, the Crowning with Thorns",
    "The Fourth Sorrowful Mystery, the Carrying of the Cross",
    "The Fifth Sorrowful Mystery, the Crucifixion"
  ],
  glorious: [
    "The First Glorious Mystery, the Resurrection",
    "The Second Glorious Mystery, the Ascension",
    "The Third Glorious Mystery, the Descent of the Holy Spirit",
    "The Fourth Glorious Mystery, the Assumption",
    "The Fifth Glorious Mystery, the Coronation of Mary"
  ],
  luminous: [
    "The First Luminous Mystery, the Baptism of Jesus",
    "The Second Luminous Mystery, the Wedding at Cana",
    "The Third Luminous Mystery, the Proclamation of the Kingdom",
    "The Fourth Luminous Mystery, the Transfiguration",
    "The Fifth Luminous Mystery, the Institution of the Eucharist"
  ]
};

function getDefaultSet() {
  const day = new Date().getDay(); // 0=Sun ... 6=Sat
  if (day === 1 || day === 6) return 'joyful';
  if (day === 2 || day === 5) return 'sorrowful';
  if (day === 3) return 'glorious';
  if (day === 4) return 'luminous';
  return 'glorious';
}

function activate(set) {
  document.querySelectorAll('.mystery-set').forEach(el => {
    el.classList.toggle('active', el.dataset.set === set);
  });
  const setTitleEl = document.querySelector('.mystery-set-title');
  if (setTitleEl) {
    const setTitles = {
      joyful: "Joyful Mysteries",
      sorrowful: "Sorrowful Mysteries",
      glorious: "Glorious Mysteries",
      luminous: "Luminous Mysteries"
    };
    setTitleEl.textContent = setTitles[set] || setTitles.joyful;
  }
  const names = MYSTERIES[set] || MYSTERIES.joyful;
  document.querySelectorAll('.decade-label').forEach((el, i) => {
    if (names[i]) el.textContent = names[i];
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const def = getDefaultSet();
  activate(def);
  document.querySelectorAll('.mystery-set').forEach(el => {
    el.addEventListener('click', () => activate(el.dataset.set));
  });
});
</script>
