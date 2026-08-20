(function (global) {
  function createQuiz(questions, opts) {
    const qs = questions || [];
    const answers = Array(qs.length).fill(null);
    let submitted = false;
    const onChange = opts.onChange || (() => {});

    function score() {
      let s = 0;
      qs.forEach((q, i) => {
        if (answers[i] === q.answer) s += 1;
      });
      return { score: s, total: qs.length };
    }

    function state() {
      return {
        questions: qs,
        answers: answers.slice(),
        submitted,
        ...score(),
        allAnswered: answers.every((a) => a != null),
      };
    }

    function emit() {
      onChange(state());
    }

    return {
      state,
      select(qi, ci) {
        if (submitted) return;
        answers[qi] = ci;
        emit();
      },
      submit() {
        if (answers.some((a) => a == null)) return false;
        submitted = true;
        emit();
        return true;
      },
      reset() {
        for (let i = 0; i < answers.length; i++) answers[i] = null;
        submitted = false;
        emit();
      },
    };
  }

  global.ToeicQuiz = { createQuiz };
})(window);
