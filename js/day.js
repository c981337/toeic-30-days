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
      const [a, b] = String(w.days).split("–").map((x) => parseInt(x, 10));
      return dayNum >= a && dayNum <= b;
    }) || { week: data.phase, title: "衝刺" };

  $("day-eyebrow").textContent =
    "Week " + week.week + " " + week.title + " · " + (data.themeZh || data.theme);
  $("day-title").textContent = "Day " + String(dayNum).padStart(2, "0") + " — " + data.title;
  $("day-sub").textContent =
    "單字＋閱讀｜今日 " + (data.vocab || []).length + " 張卡｜615 → 800–900";

  const prev = $("nav-prev");
  const next = $("nav-next");
  prev.href = dayNum > 1 ? "day.html?d=" + (dayNum - 1) : "#";
  next.href = dayNum < 30 ? "day.html?d=" + (dayNum + 1) : "#";
  if (dayNum <= 1) prev.classList.add("is-disabled");
  if (dayNum >= 30) next.classList.add("is-disabled");

  if ((curri.mockDays || [7, 14, 21, 28]).includes(dayNum)) {
    $("week-tip").hidden = false;
    $("week-tip").textContent = "複習日：重做錯字卡，並重練本週閱讀正確率低於 80% 的日子。";
  }

  function refreshPillars() {
    const p = ToeicProgress.getDay(dayNum);
    const readOk = p.readDone && p.quizScore != null;
    $("pillar-track").innerHTML =
      '<span class="pillar-chip' +
      (p.vocabDone ? " is-on" : "") +
      '">單字' +
      (p.vocabDone ? " ✓" : "") +
      '</span><span class="pillar-chip' +
      (readOk ? " is-on" : "") +
      '">閱讀' +
      (readOk ? " ✓" : "") +
      "</span>";
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

  const deck = ToeicFlashcards.createFlashcards(data.vocab, { onChange: renderFlash });
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

  $("article-en").textContent = data.english;
  $("article-zh").textContent = data.chinese;
  $("article-zh").hidden = true;

  const rateInput = $("tts-rate");
  const rateLabel = $("tts-rate-label");
  rateInput.value = prefs.rate;
  rateLabel.textContent = Number(prefs.rate).toFixed(2) + "×";
  rateInput.addEventListener("input", () => {
    tts.setRate(rateInput.value);
    rateLabel.textContent = Number(rateInput.value).toFixed(2) + "×";
  });

  const voiceSelect = $("tts-voice");
  const voiceTip = $("voice-tip");

  function updateVoiceTip(selected) {
    if (!voiceTip) return;
    const best = tts.recommendVoice();
    const bestName = best ? best.name : "（尚未偵測到英文語音）";
    const cur = selected || pickSelectedVoice();
    const curName = cur ? cur.name : bestName;
    voiceTip.innerHTML =
      "目前：<strong>" +
      curName +
      "</strong>。系統推薦較真人：<strong>" +
      bestName +
      "</strong>。" +
      " Mac 可到「系統設定 → 輔助使用 → 朗讀內容 → 系統聲音」下載 <em>Enhanced／Premium</em>（如 Samantha、Nicky、Aaron）。" +
      " 瀏覽器優先試 <em>Safari</em> 或 <em>Edge</em>（Microsoft 自然語音通常最像真人）。";
  }

  function pickSelectedVoice() {
    const uri = voiceSelect.value || prefs.voiceURI;
    return tts.listVoices().find((v) => v.voiceURI === uri) || tts.recommendVoice();
  }

  function fillVoices() {
    const ranked = tts.rankedVoices();
    voiceSelect.innerHTML = "";
    if (!ranked.length) {
      const opt = document.createElement("option");
      opt.textContent = tts.supported ? "載入英文語音中…" : "不支援朗讀";
      voiceSelect.appendChild(opt);
      voiceSelect.disabled = true;
      updateVoiceTip(null);
      return;
    }
    voiceSelect.disabled = false;
    const best = ranked[0].voice;
    let selectedURI = prefs.voiceURI;
    if (!selectedURI || !ranked.some((x) => x.voice.voiceURI === selectedURI)) {
      selectedURI = best.voiceURI;
      tts.setVoiceURI(selectedURI);
      prefs.voiceURI = selectedURI;
    }
    ranked.forEach((x) => {
      const v = x.voice;
      const opt = document.createElement("option");
      opt.value = v.voiceURI;
      opt.textContent = tts.voiceLabel(v);
      if (v.voiceURI === selectedURI) opt.selected = true;
      voiceSelect.appendChild(opt);
    });
    updateVoiceTip(pickSelectedVoice());
  }

  fillVoices();
  if (window.speechSynthesis) speechSynthesis.addEventListener("voiceschanged", fillVoices);
  voiceSelect.addEventListener("change", () => {
    tts.setVoiceURI(voiceSelect.value);
    prefs.voiceURI = voiceSelect.value;
    updateVoiceTip(pickSelectedVoice());
  });
  $("tts-best").addEventListener("click", () => {
    const best = tts.recommendVoice();
    if (!best) return;
    tts.setVoiceURI(best.voiceURI);
    prefs.voiceURI = best.voiceURI;
    fillVoices();
    tts.speak("This is the recommended voice for your TOEIC practice.");
  });
  $("tts-play").addEventListener("click", () => tts.speak(data.english));
  $("tts-pause").addEventListener("click", () => tts.pause());
  $("tts-resume").addEventListener("click", () => tts.resume());
  $("tts-stop").addEventListener("click", () => tts.stop());

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
      $("timer-display").textContent =
        String(Math.floor(sec / 60)).padStart(2, "0") + ":" + String(sec % 60).padStart(2, "0");
    }, 250);
  });

  function renderQuiz(st) {
    const root = $("quiz-root");
    const banner = $("quiz-banner");
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
        "%）" +
        (st.score / st.total < 0.8 ? "｜建議隔日重做單字卡" : "");
      ToeicProgress.updateDay(dayNum, {
        quizScore: st.score,
        quizTotal: st.total,
        readDone: true,
      });
      $("mark-read").textContent = "已標記讀完";
      $("mark-read").disabled = true;
      refreshPillars();
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
    $("quiz-submit").disabled = st.submitted || !st.allAnswered;
    $("quiz-submit").textContent = st.submitted ? "已交卷" : "交卷看解析";
  }

  const quiz = ToeicQuiz.createQuiz(data.questions, { onChange: renderQuiz });
  $("quiz-submit").addEventListener("click", () => quiz.submit());
  $("quiz-reset").addEventListener("click", () => quiz.reset());
  renderQuiz(quiz.state());

  const prog = ToeicProgress.getDay(dayNum);
  if (prog.readDone) {
    $("mark-read").textContent = "已標記讀完";
    $("mark-read").disabled = true;
  }
  refreshPillars();
  window.addEventListener("beforeunload", () => tts.stop());
})();
