(function (global) {
  const KEY = "toeic30_progress_v2";

  function emptyDay() {
    return {
      vocabDone: false,
      speakDone: false,
      listenDone: false,
      listenScore: null,
      listenTotal: null,
      grammarDone: false,
      grammarScore: null,
      grammarTotal: null,
      readDone: false,
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

  function isComplete(cur) {
    return !!(
      cur.vocabDone &&
      cur.speakDone &&
      cur.listenDone &&
      cur.grammarDone &&
      cur.readDone &&
      cur.quizScore != null &&
      cur.listenScore != null &&
      cur.grammarScore != null
    );
  }

  function updateDay(day, patch) {
    const all = load();
    const cur = Object.assign(emptyDay(), all[String(day)] || {}, patch);
    if (isComplete(cur) && !cur.completedAt) cur.completedAt = new Date().toISOString();
    if (!isComplete(cur)) cur.completedAt = null;
    all[String(day)] = cur;
    save(all);
    return cur;
  }

  function resetAll() {
    localStorage.removeItem(KEY);
    // also clear legacy key so old partial state does not confuse
    localStorage.removeItem("toeic30_progress");
  }

  function statusOf(day) {
    const d = getDay(day);
    if (d.completedAt) return "done";
    const started =
      d.vocabDone ||
      d.speakDone ||
      d.listenDone ||
      d.grammarDone ||
      d.readDone ||
      d.quizScore != null ||
      d.listenScore != null ||
      d.grammarScore != null;
    return started ? "progress" : "idle";
  }

  function pillarStats(totalDays) {
    const pillars = {
      vocab: 0,
      speak: 0,
      listen: 0,
      grammar: 0,
      read: 0,
    };
    for (let i = 1; i <= totalDays; i++) {
      const d = getDay(i);
      if (d.vocabDone) pillars.vocab++;
      if (d.speakDone) pillars.speak++;
      if (d.listenDone) pillars.listen++;
      if (d.grammarDone) pillars.grammar++;
      if (d.readDone && d.quizScore != null) pillars.read++;
    }
    return pillars;
  }

  function summary(totalDays) {
    let done = 0;
    let scoreSum = 0;
    let scoreCount = 0;
    let suggest = 1;
    for (let i = 1; i <= totalDays; i++) {
      if (statusOf(i) === "done") done++;
      const d = getDay(i);
      [
        [d.quizScore, d.quizTotal],
        [d.listenScore, d.listenTotal],
        [d.grammarScore, d.grammarTotal],
      ].forEach(([s, t]) => {
        if (s != null && t) {
          scoreSum += s / t;
          scoreCount++;
        }
      });
    }
    for (let i = 1; i <= totalDays; i++) {
      if (statusOf(i) !== "done") {
        suggest = i;
        break;
      }
      suggest = totalDays;
    }
    return {
      done,
      total: totalDays,
      avgAccuracy: scoreCount ? Math.round((scoreSum / scoreCount) * 100) : null,
      suggest,
      pillars: pillarStats(totalDays),
    };
  }

  global.ToeicProgress = { load, getDay, updateDay, resetAll, statusOf, summary, pillarStats };
})(window);
