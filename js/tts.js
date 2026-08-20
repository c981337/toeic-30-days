(function (global) {
  const TTS_KEY = "toeic30_tts";
  const defaults = { rate: 0.95, voiceURI: "" };

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

  function pickVoice(prefs) {
    const voices = englishVoices();
    if (!voices.length) return null;
    if (prefs.voiceURI) {
      const found = voices.find((v) => v.voiceURI === prefs.voiceURI);
      if (found) return found;
    }
    return (
      voices.find((v) => /en-US/i.test(v.lang) && /enhanced|premium|natural|samantha|daniel|google/i.test(v.name)) ||
      voices.find((v) => /en-US/i.test(v.lang)) ||
      voices.find((v) => /en-GB/i.test(v.lang)) ||
      voices[0]
    );
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
      supported: !!(global.speechSynthesis),
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
      speak(text, opts = {}) {
        if (!this.supported) return false;
        cancel();
        onEnd = opts.onEnd || null;
        queue = splitParagraphs(text);
        if (!queue.length) queue = [String(text || "").trim()].filter(Boolean);
        if (!queue.length) return false;
        // Chrome sometimes needs a kick after cancel
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

  // voices load async on some browsers
  if (global.speechSynthesis) {
    speechSynthesis.getVoices();
    speechSynthesis.addEventListener("voiceschanged", () => speechSynthesis.getVoices());
  }

  global.ToeicTTS = { createTTS, englishVoices, loadPrefs, savePrefs };
})(window);
