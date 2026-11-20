(function () {
  const input = document.getElementById("archive-query");
  if (!input) return;
  const entries = Array.from(document.getElementById("archive-entries").children);
  const empty = document.getElementById("archive-empty");
  const searchable = entries.map((entry) => entry.textContent.toLocaleLowerCase());
  function filter() {
    const words = input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let matches = 0;
    entries.forEach((entry, i) => {
      entry.hidden = !words.every((word) => searchable[i].includes(word));
      if (!entry.hidden) matches += 1;
    });
    empty.hidden = matches !== 0;
  }
  input.addEventListener("input", filter);
  input.closest(".archive-filter").hidden = false;
  filter();
})();
