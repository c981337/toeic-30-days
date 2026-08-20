(function () {
  const days = window.TOEIC_DAYS || [];
  const total = days.length || 30;
  const summary = ToeicProgress.summary(total);
  const suggest = summary.suggest;

  const cta = document.getElementById("cta-start");
  const ctaLabel = document.getElementById("cta-label");
  const statsDone = document.getElementById("stat-done");
  const statsAcc = document.getElementById("stat-acc");
  const statsSuggest = document.getElementById("stat-suggest");
  const grid = document.getElementById("day-grid");
  const resetBtn = document.getElementById("reset-progress");

  if (cta) {
    cta.href = "day.html?d=" + suggest;
    if (ctaLabel) {
      ctaLabel.textContent = summary.done === 0 ? "開始 Day 1" : "繼續 Day " + String(suggest).padStart(2, "0");
    }
  }

  if (statsDone) statsDone.textContent = summary.done + " / " + total;
  if (statsAcc) statsAcc.textContent = summary.avgAccuracy == null ? "—" : summary.avgAccuracy + "%";
  if (statsSuggest) statsSuggest.textContent = "Day " + String(suggest).padStart(2, "0");

  if (grid) {
    grid.innerHTML = "";
    for (let i = 1; i <= total; i++) {
      const a = document.createElement("a");
      a.className = "day-cell";
      a.href = "day.html?d=" + i;
      a.textContent = String(i).padStart(2, "0");
      const st = ToeicProgress.statusOf(i);
      if (st === "done") a.classList.add("is-done");
      if (st === "progress") a.classList.add("is-progress");
      if (i === suggest) a.classList.add("is-today");
      const dayMeta = days.find((d) => d.day === i);
      a.title = dayMeta ? "Day " + i + " — " + dayMeta.title : "Day " + i;
      grid.appendChild(a);
    }
  }

  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      if (confirm("確定要清除全部學習進度？此動作無法復原。")) {
        ToeicProgress.resetAll();
        location.reload();
      }
    });
  }
})();
