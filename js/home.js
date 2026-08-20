(function () {
  const days = window.TOEIC_DAYS || [];
  const curri = window.TOEIC_CURRICULUM || {};
  const total = days.length || 30;
  const summary = ToeicProgress.summary(total);
  const suggest = summary.suggest;

  const cta = document.getElementById("cta-start");
  const ctaLabel = document.getElementById("cta-label");
  if (cta) {
    cta.href = "day.html?d=" + suggest;
    if (ctaLabel) {
      ctaLabel.textContent =
        summary.done === 0 ? "開始 Day 1" : "繼續 Day " + String(suggest).padStart(2, "0");
    }
  }

  const statsDone = document.getElementById("stat-done");
  const statsAcc = document.getElementById("stat-acc");
  const statsSuggest = document.getElementById("stat-suggest");
  if (statsDone) statsDone.textContent = summary.done + " / " + total;
  if (statsAcc) statsAcc.textContent = summary.avgAccuracy == null ? "—" : summary.avgAccuracy + "%";
  if (statsSuggest) statsSuggest.textContent = "Day " + String(suggest).padStart(2, "0");

  const pillarCards = document.getElementById("pillar-cards");
  if (pillarCards && curri.pillars) {
    pillarCards.innerHTML = curri.pillars
      .map(
        (p, i) =>
          '<article class="phase-card"><h3>' +
          (i + 1) +
          ". " +
          p.name +
          "</h3><p>" +
          p.role +
          '</p><div class="phase-days">' +
          p.minutes +
          " 分鐘</div></article>"
      )
      .join("");
  }

  const weekCards = document.getElementById("week-cards");
  if (weekCards && curri.weeks) {
    weekCards.innerHTML = curri.weeks
      .map(
        (w) =>
          '<article class="phase-card"><h3>Week ' +
          w.week +
          " " +
          w.title +
          "</h3><p><strong>聽力</strong> " +
          w.listen +
          "<br /><strong>文法</strong> " +
          w.grammar +
          "<br /><strong>閱讀</strong> " +
          w.read +
          '</p><div class="phase-days">Day ' +
          w.days +
          "｜模考 " +
          w.mock +
          "</div></article>"
      )
      .join("");
  }

  const pillarStats = document.getElementById("pillar-stats");
  if (pillarStats && summary.pillars) {
    const labels = [
      ["vocab", "單字"],
      ["speak", "朗讀"],
      ["listen", "聽力"],
      ["grammar", "文法"],
      ["read", "閱讀"],
    ];
    pillarStats.innerHTML = labels
      .map(
        ([k, name]) =>
          '<div class="stat"><strong>' +
          summary.pillars[k] +
          "/" +
          total +
          "</strong><span>" +
          name +
          "</span></div>"
      )
      .join("");
  }

  const grid = document.getElementById("day-grid");
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

  const resetBtn = document.getElementById("reset-progress");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      if (confirm("確定清除全部五科進度？")) {
        ToeicProgress.resetAll();
        location.reload();
      }
    });
  }
})();
