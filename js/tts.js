(function (global) {
  const TTS_KEY = "toeic30_tts";
  const defaults = { rate: 0.95, voiceURI: "" };

  // Higher = more natural / human-like for study listening
  const PREFERRED_NAMES = [
    "microsoft aria",
    "microsoft jenny",
    "microsoft guy",
    "microsoft michelle",
    "microsoft ana",
    "microsoft andrew",
    "microsoft emma",
    "microsoft brian",
    "google us english",
    "google uk english female",
    "google uk english male",
    "samantha",
    "nicky",
    "aaron",
    "evan",
    "ava",
    "zoe",
    "stephanie",
    "susan",
    "karen",
    "moira",
    "daniel",
    "martha",
    "catherine",
    "arthur",
    "rishi",
  ];

  const AVOID_NAMES = [
    "zarvox",
    "trinoids",
    "whisper",
    "bells",
    "bubbles",
    "bad news",
    "good news",
    "boing",
    "cellos",
    "organ",
    "superstar",
    "jester",
    "junior",
    "kathy",
    "albert",
    "bahh",
    "wobble",
    "princess",
    "ralph",
  ];

  function loadPrefs() {
    try {
      return Object.assign({}, defaults, JSON.parse(localStorage.getItem(TTS_KEY) || "{}"));
    } catch {
      return Object.assign({}, defaults);
    }
  }

  function savePrefs(prefs) {
    localStorage.setItem(TTS_KEY, JSON.stringify(prefs));
  }

  function englishVoices() {
    if (!global.speechSynthesis) return [];
    return speechSynthesis.getVoices().filter((v) => /^en(-|_|$)/i.test(v.lang));
  }

  function scoreVoice(v) {
    const name = (v.name || "").toLowerCase();
    const lang = (v.lang || "").toLowerCase();
    let score = 0;

    if (AVOID_NAMES.some((n) => name.includes(n))) return -100;

    if (/natural|neural|online \(natural\)|premium|enhanced|siri/.test(name)) score += 80;
    if (/microsoft/.test(name) && /online|natural|neural/.test(name)) score += 40;
    if (/google/.test(name)) score += 45;

    PREFERRED_NAMES.forEach((n, i) => {
      if (name.includes(n)) score += 30 - Math.min(i, 20);
    });

    if (/en-us/.test(lang)) score += 12;
    else if (/en-gb/.test(lang)) score += 8;
    else if (/en-au|en-ie|en-za/.test(lang)) score += 4;

    // Compact/local default Mac voices are usually flatter
    if (/compact/.test(name)) score -= 25;
    if (v.localService === false) score += 15; // cloud/neural often remote

    return score;
  }

  function rankedVoices() {
    return englishVoices()
      .map((v) => ({ voice: v, score: scoreVoice(v) }))
      .filter((x) => x.score > -50)
      .sort((a, b) => b.score - a.score || a.voice.name.localeCompare(b.voice.name));
  }

  function isRecommended(v) {
    return scoreVoice(v) >= 40;
  }

  function voiceLabel(v) {
    const tag = isRecommended(v) ? "★推薦 " : "";
    return tag + v.name + " (" + v.lang + ")";
  }

  function pickVoice(prefs) {
    const ranked = rankedVoices();
    if (!ranked.length) return null;
    if (prefs.voiceURI) {
      const found = ranked.find((x) => x.voice.voiceURI === prefs.voiceURI);
      if (found) return found.voice;
    }
    return ranked[0].voice;
  }

  function splitParagraphs(text) {
    return String(text || "")
      .split(/\n\s*\n/)
      .map((p) => p.replace(/\s+/g, " ").trim())
      .filter(Boolean);
  }

  function createTTS() {
    const prefs = loadPrefs();
    let queue = [];
    let paused = false;
    let speaking = false;
    let onEnd = null;

    function cancel() {
      queue = [];
      paused = false;
      speaking = false;
      if (global.speechSynthesis) speechSynthesis.cancel();
    }

    function speakNext() {
      if (!queue.length) {
        speaking = false;
        if (onEnd) onEnd();
        return;
      }
      const chunk = queue.shift();
      const u = new SpeechSynthesisUtterance(chunk);
      const voice = pickVoice(prefs);
      if (voice) u.voice = voice;
      u.lang = (voice && voice.lang) || "en-US";
      u.rate = prefs.rate;
      u.onend = () => {
        if (!paused) speakNext();
      };
      u.onerror = () => {
        if (!paused) speakNext();
      };
      speaking = true;
      speechSynthesis.speak(u);
    }

    return {
      supported: !!global.speechSynthesis,
      getPrefs: () => Object.assign({}, prefs),
      setRate(rate) {
        prefs.rate = Math.min(1.2, Math.max(0.8, Number(rate) || 0.95));
        savePrefs(prefs);
      },
      setVoiceURI(uri) {
        prefs.voiceURI = uri || "";
        savePrefs(prefs);
      },
      listVoices: englishVoices,
      rankedVoices,
      isRecommended,
      voiceLabel,
      recommendVoice() {
        const top = rankedVoices()[0];
        return top ? top.voice : null;
      },
      speak(text, opts = {}) {
        if (!this.supported) return false;
        cancel();
        onEnd = opts.onEnd || null;
        queue = splitParagraphs(text);
        if (!queue.length) queue = [String(text || "").trim()].filter(Boolean);
        if (!queue.length) return false;
        setTimeout(() => speakNext(), 40);
        return true;
      },
      speakWord(word) {
        return this.speak(word);
      },
      pause() {
        if (!this.supported) return;
        paused = true;
        speechSynthesis.pause();
      },
      resume() {
        if (!this.supported) return;
        paused = false;
        if (speechSynthesis.paused) speechSynthesis.resume();
        else if (!speaking && queue.length) speakNext();
      },
      stop() {
        cancel();
      },
      isSpeaking() {
        return speaking || (global.speechSynthesis && speechSynthesis.speaking);
      },
    };
  }

  if (global.speechSynthesis) {
    speechSynthesis.getVoices();
    speechSynthesis.addEventListener("voiceschanged", () => speechSynthesis.getVoices());
  }

  global.ToeicTTS = { createTTS, englishVoices, rankedVoices, loadPrefs, savePrefs };
})(window);
