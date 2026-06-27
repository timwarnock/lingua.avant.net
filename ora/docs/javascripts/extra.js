/* Minimal header - no custom JS. Using default Zensical behavior. */

/* Replace header title ONLY in the visible header (not page titles or H1).
   "Ora Pro Nobis" is Rosary-specific; site name "Lingua" remains for titles/H1. */
function setHeaderTitle() {
  const headerTitle = document.querySelector(".md-header__title .md-ellipsis");
  if (headerTitle) {
    const text = headerTitle.textContent.trim();
    if (text === "Lingua" || text === "Ora Pro Nobis") {
      headerTitle.textContent = "Ora Pro Nobis";
    }
  }
}

document.addEventListener("DOMContentLoaded", setHeaderTitle);

/* Support instant navigation (Material for MkDocs) */
if (typeof document$ !== "undefined") {
  document$.subscribe(setHeaderTitle);
} else {
  // Fallback for normal nav
  document.addEventListener("click", function (e) {
    if (e.target.closest("a")) {
      setTimeout(setHeaderTitle, 50);
    }
  });
}
