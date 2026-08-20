(function () {
  const params = new URLSearchParams(location.search);
  const dayNum = Math.max(1, Math.min(30, parseInt(params.get("d") || "1", 10) || 1));
  const days = window.TOEIC_DAYS || [];
  const data = days.find((d) => d.day === dayNum);

  const $ = (id) => document.getElementById(id);

  if (!data) {
    document.body.innerHTML = '<main class="container" style="padding:3rem 0"><h1>找不到此日課程</h1><a href="index.html">回首頁</a></main>';
    return;
  }

  const tts = ToeicTTS.createTTS();
  const prefs = tts.getPrefs();

  const weekMeta = [
    { max: 7, label: "Week 1 基礎補洞", mock: "≥680", listen: "Part 1–2 為主（照片／應答）", grammar: "Part 5 詞性、介系詞、連接詞" },
    { max: 14, label: "Week 2 聽讀加速", mock: "≥730", listen: "Part 3–4 對話／短講，練習邊聽邊記關鍵字", grammar: "Part 5–6 限時，文意填空上下句" },
    { max: 22, label: "Week 3 弱點專攻", mock: "≥780", listen: "錯題本最弱 Part 重練＋整回 LC", grammar: "錯題本 Part 5–6 重做，不開新單元硬衝" },
    { max: 30, label: "Week 4 模考衝刺", mock: "800–900", listen: "完整聽力模考節奏，考前兩天減量", grammar: "只複習錯題與高頻陷阱" },
  ];
  const meta = weekMeta.find((w) => dayNum <= w.max) || weekMeta[3];

  $("day-eyebrow").textContent = meta.label + " · " + (data.themeZh || data.theme);
  $("day-title").textContent = "Day " + String(dayNum).padStart(2, "0") + " — " + data.title;
  $("day-sub").textContent = "基準 615 → 目標 800–900｜本站：單字卡 → 朗讀 → 測驗";

  const agenda = document.createElement("aside");
  agenda.className = "agenda-box";
  agenda.innerHTML =
    "<h2>今日全科課表</h2><ul>" +
    "<li><strong>本站（必做）</strong>：單字卡 25 分 → 朗讀＋限時閱讀 → 5 題測驗</li>" +
    "<li><strong>聽力（外部）55 分</strong>：" + meta.listen + "</li>" +
    "<li><strong>文法（外部）30 分</strong>：" + meta.grammar + "</li>" +
    "<li><strong>錯題本 15 分</strong>：記錄錯因與關鍵句</li>" +
    "<li><strong>本週模考門檻</strong>：" + meta.mock + "</li>" +
    "</ul>";
  const header = document.querySelector(".day-header");
  if (header && header.parentNode) header.parentNode.insertBefore(agenda, header.nextSibling);

  const prev = $("nav-prev");
  const next = $("nav-next");
  prev.href = dayNum > 1 ? "day.html?d=" + (dayNum - 1) : "#";
  next.href = dayNum < 30 ? "day.html?d=" + (dayNum + 1) : "#";
  if (dayNum <= 1) prev.classList.add("is-disabled");
  if (dayNum >= 30) next.classList.add("is-disabled");

  if ([7, 14, 21, 28].includes(dayNum)) {
    const tip = $("week-tip");
    tip.hidden = false;
    tip.textContent =
      "模考日：上午完整計時模考，下午檢討（時間不少於模考）。仍完成本站閱讀；未達門檻 " +
      meta.mock +
      " 則隔天只補最弱 Part。";
  }

  // Tabs
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach((t) => t.classList.remove("is-active"));
      document.querySelectorAll(".panel").forEach((p) => p.classList.remove("is-active"));
      tab.classList.add("is-active");
      $(tab.dataset.panel).classList.add("is-active");
      tts.stop();
    });
  });

  // —— Flashcards ——
  const flashUI = {
    card: $("flash-card"),
    word: $("flash-word"),
    sub: $("flash-sub"),
    example: $("flash-example"),
    progress: $("flash-progress"),
    doneBox: $("flash-done"),
  };

  const deck = ToeicFlashcards.createFlashcards(data.vocab, {
    onChange: renderFlash,
  });

  function renderFlash(st) {
    if (st.done) {
      flashUI.card.hidden = true;
      flashUI.doneBox.hidden = false;
      flashUI.progress.textContent = "記住 " + st.knownCount + "／再看 " + st.againCount;
      ToeicProgress.updateDay(dayNum, { vocabDone: true });
      return;
    }
    flashUI.card.hidden = false;
    flashUI.doneBox.hidden = true;
    const it = st.item;
    if (!st.flipped) {
      flashUI.word.textContent = it.word;
      flashUI.sub.textContent = "點卡片查看中文意思";
      flashUI.example.textContent = "";
    } else {
      flashUI.word.textContent = it.meaning;
      flashUI.sub.textContent = it.word;
      flashUI.example.textContent = it.example || "";
    }
    flashUI.progress.textContent = (st.index + 1) + " / " + st.total;
  }

  flashUI.card.addEventListener("click", () => deck.flip());
  $("flash-known").addEventListener("click", () => deck.markKnown());
  $("flash-again").addEventListener("click", () => deck.markAgain());
  $("flash-speak").addEventListener("click", () => {
    const st = deck.state();
    if (!st.item) return;
    const text = st.flipped && st.item.example ? st.item.word + ". " + st.item.example : st.item.word;
    tts.speak(text);
  });
  $("flash-restart").addEventListener("click", () => deck.restartAll());
  $("flash-restart-wrong").addEventListener("click", () => deck.restartWrongOnly());
  renderFlash(deck.state());

  // —— Reading + TTS ——
  const articleEl = $("article-en");
  const translationEl = $("article-zh");
  articleEl.textContent = data.english;
  translationEl.textContent = data.chinese;
  translationEl.hidden = true;

  let showZh = false;
  let timerId = null;
  let timerStart = null;

  $("toggle-zh").addEventListener("click", () => {
    showZh = !showZh;
    translationEl.hidden = !showZh;
    $("toggle-zh").textContent = showZh ? "隱藏翻譯" : "顯示翻譯";
    if (showZh) ToeicProgress.updateDay(dayNum, { readDone: true });
  });

  $("mark-read").addEventListener("click", () => {
    ToeicProgress.updateDay(dayNum, { readDone: true });
    $("mark-read").textContent = "已標記讀完";
    $("mark-read").disabled = true;
  });

  const rateInput = $("tts-rate");
  const rateLabel = $("tts-rate-label");
  rateInput.value = prefs.rate;
  rateLabel.textContent = prefs.rate.toFixed(2) + "×";
  rateInput.addEventListener("input", () => {
    const v = Number(rateInput.value);
    tts.setRate(v);
    rateLabel.textContent = v.toFixed(2) + "×";
  });

  const voiceSelect = $("tts-voice");
  function fillVoices() {
    const voices = tts.listVoices();
    voiceSelect.innerHTML = "";
    if (!voices.length) {
      const opt = document.createElement("option");
      opt.textContent = tts.supported ? "尚無英文語音（請稍候或換瀏覽器）" : "此瀏覽器不支援朗讀";
      voiceSelect.appendChild(opt);
      voiceSelect.disabled = true;
      return;
    }
    voiceSelect.disabled = false;
    voices.forEach((v) => {
      const opt = document.createElement("option");
      opt.value = v.voiceURI;
      opt.textContent = v.name + " (" + v.lang + ")";
      if (prefs.voiceURI === v.voiceURI) opt.selected = true;
      voiceSelect.appendChild(opt);
    });
  }
  fillVoices();
  if (window.speechSynthesis) {
    speechSynthesis.addEventListener("voiceschanged", fillVoices);
  }
  voiceSelect.addEventListener("change", () => tts.setVoiceURI(voiceSelect.value));

  $("tts-play").addEventListener("click", () => {
    const ok = tts.speak(data.english, {
      onEnd: () => ToeicProgress.updateDay(dayNum, { listened: true }),
    });
    if (ok) ToeicProgress.updateDay(dayNum, { listened: true });
  });
  $("tts-pause").addEventListener("click", () => tts.pause());
  $("tts-resume").addEventListener("click", () => tts.resume());
  $("tts-stop").addEventListener("click", () => tts.stop());

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

  // —— Quiz ——
  const quizRoot = $("quiz-root");
  const quizBanner = $("quiz-banner");

  const quiz = ToeicQuiz.createQuiz(data.questions, { onChange: renderQuiz });

  function renderQuiz(st) {
    quizRoot.innerHTML = "";
    if (st.submitted) {
      quizBanner.hidden = false;
      quizBanner.textContent =
        "得分：" + st.score + " / " + st.total +
        "（" + Math.round((st.score / st.total) * 100) + "%）" +
        (st.score / st.total < 0.8 ? "｜建議隔日重做單字卡" : "｜表現優秀");
      ToeicProgress.updateDay(dayNum, {
        quizScore: st.score,
        quizTotal: st.total,
        readDone: true,
      });
    } else {
      quizBanner.hidden = true;
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
      quizRoot.appendChild(wrap);
    });

    $("quiz-submit").disabled = st.submitted || !st.allAnswered;
    $("quiz-submit").textContent = st.submitted ? "已交卷" : "交卷看解析";
  }

  $("quiz-submit").addEventListener("click", () => quiz.submit());
  $("quiz-reset").addEventListener("click", () => quiz.reset());
  renderQuiz(quiz.state());

  // Restore mark-read button if already done
  const prog = ToeicProgress.getDay(dayNum);
  if (prog.readDone) {
    $("mark-read").textContent = "已標記讀完";
    $("mark-read").disabled = true;
  }

  window.addEventListener("beforeunload", () => tts.stop());
})();
