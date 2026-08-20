(function () {
  const params = new URLSearchParams(location.search);
  const dayNum = Math.max(1, Math.min(30, parseInt(params.get("d") || "1", 10) || 1));
  const days = window.TOEIC_DAYS || [];
  const curri = window.TOEIC_CURRICULUM || {};
  const data = days.find((d) => d.day === dayNum);

  const $ = (id) => document.getElementById(id);

  if (!data) {
    document.body.innerHTML =
      '<main class="container" style="padding:3rem 0"><h1>找不到此日課程</h1><a href="index.html">回首頁</a></main>';
    return;
  }

  const tts = ToeicTTS.createTTS();
  const prefs = tts.getPrefs();
  const week =
    (curri.weeks || []).find((w) => {
      const [a, b] = w.days.split("–").map((x) => parseInt(x, 10));
      return dayNum >= a && dayNum <= b;
    }) || { week: data.phase, title: "衝刺", mock: "800–900" };

  $("day-eyebrow").textContent =
    "Week " + week.week + " " + week.title + " · " + (data.themeZh || data.theme);
  $("day-title").textContent = "Day " + String(dayNum).padStart(2, "0") + " — " + data.title;
  $("day-sub").textContent =
    "順序：單字 → 朗讀 → 聽力 → 文法 → 閱讀｜基準 615 → 目標 800–900";

  const prev = $("nav-prev");
  const next = $("nav-next");
  prev.href = dayNum > 1 ? "day.html?d=" + (dayNum - 1) : "#";
  next.href = dayNum < 30 ? "day.html?d=" + (dayNum + 1) : "#";
  if (dayNum <= 1) prev.classList.add("is-disabled");
  if (dayNum >= 30) next.classList.add("is-disabled");

  if ((curri.mockDays || [7, 14, 21, 28]).includes(dayNum)) {
    const tip = $("week-tip");
    tip.hidden = false;
    tip.textContent =
      "模考日：上午完整計時模考，下午檢討。五科仍建議做完本站內容；本週門檻 " +
      (week.mock || "") +
      "。";
  }

  function refreshPillars() {
    const p = ToeicProgress.getDay(dayNum);
    const items = [
      ["vocab", "單字", p.vocabDone],
      ["speak", "朗讀", p.speakDone],
      ["listen", "聽力", p.listenDone],
      ["grammar", "文法", p.grammarDone],
      ["read", "閱讀", p.readDone && p.quizScore != null],
    ];
    const root = $("pillar-track");
    root.innerHTML = items
      .map(
        ([, label, ok]) =>
          '<span class="pillar-chip' +
          (ok ? " is-on" : "") +
          '">' +
          label +
          (ok ? " ✓" : "") +
          "</span>"
      )
      .join("");
  }

  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach((t) => t.classList.remove("is-active"));
      document.querySelectorAll(".panel").forEach((p) => p.classList.remove("is-active"));
      tab.classList.add("is-active");
      $(tab.dataset.panel).classList.add("is-active");
      tts.stop();
    });
  });

  function bindVoiceSelect(selectEl) {
    function fill() {
      const voices = tts.listVoices();
      selectEl.innerHTML = "";
      if (!voices.length) {
        const opt = document.createElement("option");
        opt.textContent = tts.supported ? "載入英文語音中…" : "不支援朗讀";
        selectEl.appendChild(opt);
        selectEl.disabled = true;
        return;
      }
      selectEl.disabled = false;
      voices.forEach((v) => {
        const opt = document.createElement("option");
        opt.value = v.voiceURI;
        opt.textContent = v.name + " (" + v.lang + ")";
        if (prefs.voiceURI === v.voiceURI) opt.selected = true;
        selectEl.appendChild(opt);
      });
    }
    fill();
    if (window.speechSynthesis) speechSynthesis.addEventListener("voiceschanged", fill);
    selectEl.addEventListener("change", () => tts.setVoiceURI(selectEl.value));
  }

  // —— 1 Vocab ——
  const deck = ToeicFlashcards.createFlashcards(data.vocab, { onChange: renderFlash });
  function renderFlash(st) {
    if (st.done) {
      $("flash-card").hidden = true;
      $("flash-done").hidden = false;
      $("flash-progress").textContent = "記住 " + st.knownCount + "／再看 " + st.againCount;
      ToeicProgress.updateDay(dayNum, { vocabDone: true });
      refreshPillars();
      return;
    }
    $("flash-card").hidden = false;
    $("flash-done").hidden = true;
    const it = st.item;
    if (!st.flipped) {
      $("flash-word").textContent = it.word;
      $("flash-sub").textContent = "點卡片查看中文意思";
      $("flash-example").textContent = "";
    } else {
      $("flash-word").textContent = it.meaning;
      $("flash-sub").textContent = it.word;
      $("flash-example").textContent = it.example || "";
    }
    $("flash-progress").textContent = st.index + 1 + " / " + st.total;
  }
  $("flash-card").addEventListener("click", () => deck.flip());
  $("flash-known").addEventListener("click", () => deck.markKnown());
  $("flash-again").addEventListener("click", () => deck.markAgain());
  $("flash-speak").addEventListener("click", () => {
    const st = deck.state();
    if (!st.item) return;
    tts.speak(st.flipped && st.item.example ? st.item.word + ". " + st.item.example : st.item.word);
  });
  $("flash-restart").addEventListener("click", () => deck.restartAll());
  $("flash-restart-wrong").addEventListener("click", () => deck.restartWrongOnly());
  renderFlash(deck.state());

  // —— 2 Speak ——
  $("speak-text").textContent = data.english;
  const L = data.listening || {};
  $("speak-tip").textContent =
    "約 15 分｜" + (L.shadowTip || "聽一句跟讀一句；第二遍可加快語速。");
  const speakRate = $("speak-rate");
  const speakRateLabel = $("speak-rate-label");
  const speakDefault = Math.min(prefs.rate, 0.9);
  speakRate.value = speakDefault;
  speakRateLabel.textContent = Number(speakDefault).toFixed(2) + "×";
  speakRate.addEventListener("input", () => {
    tts.setRate(speakRate.value);
    speakRateLabel.textContent = Number(speakRate.value).toFixed(2) + "×";
  });
  bindVoiceSelect($("speak-voice"));
  $("speak-play").addEventListener("click", () => {
    tts.setRate(speakRate.value);
    tts.speak(data.english);
  });
  $("speak-pause").addEventListener("click", () => tts.pause());
  $("speak-resume").addEventListener("click", () => tts.resume());
  $("speak-stop").addEventListener("click", () => tts.stop());
  $("mark-speak").addEventListener("click", () => {
    ToeicProgress.updateDay(dayNum, { speakDone: true });
    $("mark-speak").textContent = "已完成朗讀";
    $("mark-speak").disabled = true;
    refreshPillars();
  });

  // —— 3 Listen ——
  $("listen-brief").innerHTML =
    "<h2>今日聽力｜" +
    (L.partFocus || "LC") +
    "</h2><ul>" +
    "<li><strong>暖身</strong>：" +
    (L.warmUp || "先用本站播放聽一遍大意") +
    "</li>" +
    "<li><strong>外部練習</strong>：" +
    (L.externalDrill || "依本週 Part 焦點做官方／模擬題") +
    "</li>" +
    "<li><strong>跟讀提醒</strong>：" +
    (L.shadowTip || "") +
    "</li></ul>";

  $("listen-play").addEventListener("click", () => {
    tts.setRate(0.95);
    tts.speak(data.english);
  });
  $("listen-stop").addEventListener("click", () => tts.stop());

  function mountQuiz(rootId, bannerId, submitId, resetId, questions, onSubmit) {
    const quiz = ToeicQuiz.createQuiz(questions || [], { onChange: render });
    function render(st) {
      const root = $(rootId);
      const banner = $(bannerId);
      root.innerHTML = "";
      if (st.submitted) {
        banner.hidden = false;
        banner.textContent =
          "得分：" +
          st.score +
          " / " +
          st.total +
          "（" +
          Math.round((st.score / st.total) * 100) +
          "%）";
        onSubmit(st);
      } else {
        banner.hidden = true;
      }
      st.questions.forEach((q, qi) => {
        const wrap = document.createElement("div");
        wrap.className = "quiz-item";
        const title = document.createElement("p");
        title.className = "quiz-q";
        title.textContent = qi + 1 + ". " + q.q;
        wrap.appendChild(title);
        const choices = document.createElement("div");
        choices.className = "choices";
        q.choices.forEach((c, ci) => {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "choice";
          btn.textContent = String.fromCharCode(65 + ci) + ". " + c;
          if (st.answers[qi] === ci) btn.classList.add("is-selected");
          if (st.submitted) {
            btn.disabled = true;
            if (ci === q.answer) btn.classList.add("is-correct");
            else if (st.answers[qi] === ci) btn.classList.add("is-wrong");
          } else {
            btn.addEventListener("click", () => quiz.select(qi, ci));
          }
          choices.appendChild(btn);
        });
        wrap.appendChild(choices);
        if (st.submitted) {
          const ex = document.createElement("p");
          ex.className = "explain";
          ex.textContent = "解析：" + q.explain;
          wrap.appendChild(ex);
        }
        root.appendChild(wrap);
      });
      $(submitId).disabled = st.submitted || !st.allAnswered;
      $(submitId).textContent = st.submitted ? "已交卷" : "交卷";
    }
    $(submitId).addEventListener("click", () => quiz.submit());
    $(resetId).addEventListener("click", () => quiz.reset());
    render(quiz.state());
    return quiz;
  }

  mountQuiz("listen-root", "listen-banner", "listen-submit", "listen-reset", L.questions, (st) => {
    ToeicProgress.updateDay(dayNum, {
      listenDone: true,
      listenScore: st.score,
      listenTotal: st.total,
    });
    refreshPillars();
  });

  // —— 4 Grammar ——
  const G = data.grammar || {};
  $("grammar-brief").innerHTML =
    "<h2>今日文法｜" +
    (G.focus || "Part 5") +
    "</h2><ul><li>" +
    (G.tip || "先判斷空格需要的詞性，再排除干擾選項。") +
    "</li></ul>";

  mountQuiz(
    "grammar-root",
    "grammar-banner",
    "grammar-submit",
    "grammar-reset",
    G.questions,
    (st) => {
      ToeicProgress.updateDay(dayNum, {
        grammarDone: true,
        grammarScore: st.score,
        grammarTotal: st.total,
      });
      refreshPillars();
    }
  );

  // —— 5 Reading ——
  $("article-en").textContent = data.english;
  $("article-zh").textContent = data.chinese;
  $("article-zh").hidden = true;
  let showZh = false;
  let timerId = null;
  let timerStart = null;

  $("toggle-zh").addEventListener("click", () => {
    showZh = !showZh;
    $("article-zh").hidden = !showZh;
    $("toggle-zh").textContent = showZh ? "隱藏翻譯" : "顯示翻譯";
  });

  $("mark-read").addEventListener("click", () => {
    ToeicProgress.updateDay(dayNum, { readDone: true });
    $("mark-read").textContent = "已標記讀完";
    $("mark-read").disabled = true;
    refreshPillars();
  });

  $("timer-toggle").addEventListener("click", () => {
    const display = $("timer-display");
    if (timerId) {
      clearInterval(timerId);
      timerId = null;
      $("timer-toggle").textContent = "開始計時";
      return;
    }
    timerStart = Date.now();
    $("timer-toggle").textContent = "停止計時";
    timerId = setInterval(() => {
      const sec = Math.floor((Date.now() - timerStart) / 1000);
      const m = String(Math.floor(sec / 60)).padStart(2, "0");
      const s = String(sec % 60).padStart(2, "0");
      display.textContent = m + ":" + s;
    }, 250);
  });

  mountQuiz("quiz-root", "quiz-banner", "quiz-submit", "quiz-reset", data.questions, (st) => {
    ToeicProgress.updateDay(dayNum, {
      quizScore: st.score,
      quizTotal: st.total,
      readDone: true,
    });
    $("mark-read").textContent = "已標記讀完";
    $("mark-read").disabled = true;
    refreshPillars();
  });

  // restore UI state
  const prog = ToeicProgress.getDay(dayNum);
  if (prog.speakDone) {
    $("mark-speak").textContent = "已完成朗讀";
    $("mark-speak").disabled = true;
  }
  if (prog.readDone) {
    $("mark-read").textContent = "已標記讀完";
    $("mark-read").disabled = true;
  }
  refreshPillars();
  window.addEventListener("beforeunload", () => tts.stop());
})();
