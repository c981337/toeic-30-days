(function (global) {
  const KEY = "toeic30_progress";

  function emptyDay() {
    return {
      vocabDone: false,
      readDone: false,
      listened: false,
      quizScore: null,
      quizTotal: null,
      completedAt: null,
    };
  }

  function load() {
    try {
      const raw = JSON.parse(localStorage.getItem(KEY) || "{}");
      return raw && typeof raw === "object" ? raw : {};
    } catch {
      return {};
    }
  }

  function save(data) {
    localStorage.setItem(KEY, JSON.stringify(data));
  }

  function getDay(day) {
    const all = load();
    return Object.assign(emptyDay(), all[String(day)] || {});
  }

  function updateDay(day, patch) {
    const all = load();
    const cur = Object.assign(emptyDay(), all[String(day)] || {}, patch);
    const done =
      cur.vocabDone &&
      cur.readDone &&
      cur.quizScore != null &&
      cur.quizTotal != null;
    if (done && !cur.completedAt) cur.completedAt = new Date().toISOString();
    if (!done) cur.completedAt = null;
    all[String(day)] = cur;
    save(all);
    return cur;
  }

  function resetAll() {
    localStorage.removeItem(KEY);
  }

  function statusOf(day) {
    const d = getDay(day);
    if (d.completedAt) return "done";
    if (d.vocabDone || d.readDone || d.listened || d.quizScore != null) return "progress";
    return "idle";
  }

  function summary(totalDays) {
    let done = 0;
    let scoreSum = 0;
    let scoreCount = 0;
    let suggest = 1;
    for (let i = 1; i <= totalDays; i++) {
      const st = statusOf(i);
      if (st === "done") done++;
      const d = getDay(i);
      if (d.quizScore != null && d.quizTotal) {
        scoreSum += d.quizScore / d.quizTotal;
        scoreCount++;
      }
    }
    for (let i = 1; i <= totalDays; i++) {
      if (statusOf(i) !== "done") {
        suggest = i;
        break;
      }
      if (i === totalDays) suggest = totalDays;
    }
    return {
      done,
      total: totalDays,
      avgAccuracy: scoreCount ? Math.round((scoreSum / scoreCount) * 100) : null,
      suggest,
    };
  }

  global.ToeicProgress = { load, getDay, updateDay, resetAll, statusOf, summary };
})(window);
