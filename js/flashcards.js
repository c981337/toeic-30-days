(function (global) {
  function createFlashcards(vocab, opts) {
    const items = (vocab || []).slice();
    let index = 0;
    let flipped = false;
    let known = new Set();
    let again = new Set();
    const onChange = opts.onChange || (() => {});

    function current() {
      return items[index] || null;
    }

    function state() {
      return {
        index,
        total: items.length,
        flipped,
        item: current(),
        knownCount: known.size,
        againCount: again.size,
        done: index >= items.length,
      };
    }

    function emit() {
      onChange(state());
    }

    return {
      state,
      flip() {
        if (!current()) return;
        flipped = !flipped;
        emit();
      },
      markKnown() {
        const it = current();
        if (!it) return;
        known.add(it.word);
        again.delete(it.word);
        index += 1;
        flipped = false;
        emit();
      },
      markAgain() {
        const it = current();
        if (!it) return;
        again.add(it.word);
        known.delete(it.word);
        index += 1;
        flipped = false;
        emit();
      },
      restartWrongOnly() {
        const wrong = items.filter((v) => again.has(v.word));
        items.length = 0;
        items.push(...(wrong.length ? wrong : vocab.slice()));
        index = 0;
        flipped = false;
        known = new Set();
        again = new Set();
        emit();
      },
      restartAll() {
        items.length = 0;
        items.push(...vocab.slice());
        index = 0;
        flipped = false;
        known = new Set();
        again = new Set();
        emit();
      },
    };
  }

  global.ToeicFlashcards = { createFlashcards };
})(window);
