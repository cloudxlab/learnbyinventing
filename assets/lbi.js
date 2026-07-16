/* Learn By Inventing — shared chapter interactions */

(function () {
  "use strict";

  var chapterId = document.body.getAttribute("data-chapter-id") || "";

  /* ── localStorage helpers ─────────────────────────────── */

  function storageKey(exerciseId, field) {
    return "lbi:" + chapterId + ":" + exerciseId + ":" + field;
  }

  function saveItem(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* quota */ }
  }

  function loadItem(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }

  function clearChapterData() {
    var prefix = "lbi:" + chapterId + ":";
    var toRemove = [];
    for (var i = 0; i < localStorage.length; i++) {
      var k = localStorage.key(i);
      if (k && k.indexOf(prefix) === 0) toRemove.push(k);
    }
    toRemove.forEach(function (k) { localStorage.removeItem(k); });
  }

  /* ── Progressive hints ────────────────────────────────── */

  function initProgressiveHints() {
    document.querySelectorAll(".exercise").forEach(function (exercise) {
      var hints = Array.from(exercise.querySelectorAll("details.hint"));
      if (hints.length < 2) return;

      hints.forEach(function (hint, i) {
        if (i === 0) return;
        hint.classList.add("locked");
      });

      hints.forEach(function (hint, i) {
        if (i >= hints.length - 1) return;
        hint.addEventListener("toggle", function () {
          if (hint.open) {
            var next = hints[i + 1];
            if (next && next.classList.contains("locked")) {
              next.classList.remove("locked");
            }
          }
        });
      });
    });
  }

  /* ── MCQ ───────────────────────────────────────────────── */

  function initMCQ() {
    document.querySelectorAll(".mcq-check").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var exercise = btn.closest(".exercise");
        var opts = exercise.querySelector(".mcq-options");
        var correctValue = opts.getAttribute("data-correct");
        var selected = exercise.querySelector('input[type="radio"]:checked');
        var feedback = exercise.querySelector(".mcq-feedback");

        if (!selected) {
          feedback.textContent = "Please select an answer first.";
          feedback.className = "mcq-feedback incorrect";
          feedback.style.display = "block";
          return;
        }

        var isCorrect = selected.value === correctValue;
        opts.classList.add("checked");

        opts.querySelectorAll(".mcq-option").forEach(function (opt) {
          var radio = opt.querySelector('input[type="radio"]');
          radio.disabled = true;
          if (radio.value === correctValue) {
            opt.classList.add("correct");
          } else if (radio.checked && !isCorrect) {
            opt.classList.add("incorrect");
          }
        });

        feedback.className = "mcq-feedback " + (isCorrect ? "correct" : "incorrect");
        feedback.textContent = isCorrect
          ? "Correct!"
          : "Incorrect. The correct answer is highlighted above.";
        feedback.style.display = "block";
        btn.disabled = true;

        var exId = exercise.id;
        if (exId) {
          saveItem(storageKey(exId, "mcq"), selected.value);
          saveItem(storageKey(exId, "mcq-result"), isCorrect ? "1" : "0");
        }
      });
    });
  }

  function resetMCQ() {
    document.querySelectorAll(".exercise.mcq").forEach(function (exercise) {
      var opts = exercise.querySelector(".mcq-options");
      if (!opts) return;
      opts.classList.remove("checked");
      opts.querySelectorAll(".mcq-option").forEach(function (opt) {
        opt.classList.remove("correct", "incorrect");
        var radio = opt.querySelector('input[type="radio"]');
        radio.disabled = false;
        radio.checked = false;
      });
      var feedback = exercise.querySelector(".mcq-feedback");
      if (feedback) {
        feedback.style.display = "none";
        feedback.className = "mcq-feedback";
      }
      var btn = exercise.querySelector(".mcq-check");
      if (btn) btn.disabled = false;
    });
  }

  function revealMCQ() {
    document.querySelectorAll(".exercise.mcq").forEach(function (exercise) {
      var opts = exercise.querySelector(".mcq-options");
      if (!opts) return;
      var correctValue = opts.getAttribute("data-correct");
      opts.classList.add("checked");
      opts.querySelectorAll(".mcq-option").forEach(function (opt) {
        var radio = opt.querySelector('input[type="radio"]');
        radio.disabled = true;
        if (radio.value === correctValue) {
          opt.classList.add("correct");
        }
      });
      var feedback = exercise.querySelector(".mcq-feedback");
      if (feedback) {
        feedback.className = "mcq-feedback correct";
        feedback.textContent = "Answer revealed.";
        feedback.style.display = "block";
      }
      var btn = exercise.querySelector(".mcq-check");
      if (btn) btn.disabled = true;
    });
  }

  /* ── Progress indicator ───────────────────────────────── */

  function initProgressIndicator() {
    var indicator = document.getElementById("progress-indicator");
    if (!indicator) return;
    var total = parseInt(indicator.getAttribute("data-total"), 10);
    if (!total || total < 2) return;

    var parts = document.querySelectorAll(".part[data-part-number]");
    if (!parts.length) return;

    var currentPart = 1;
    indicator.textContent = "Part 1 of " + total;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var num = parseInt(entry.target.getAttribute("data-part-number"), 10);
          if (num && num !== currentPart) {
            currentPart = num;
            indicator.textContent = "Part " + num + " of " + total;
          }
        }
      });
    }, { threshold: 0.1, rootMargin: "-10% 0px -80% 0px" });

    parts.forEach(function (p) { observer.observe(p); });

    window.addEventListener("scroll", function () {
      var scrolled = window.scrollY > 200;
      indicator.style.display = scrolled ? "block" : "none";
    }, { passive: true });
  }

  /* ── Copy code buttons ────────────────────────────────── */

  function initCopyButtons() {
    document.querySelectorAll("pre").forEach(function (pre) {
      var code = pre.querySelector("code");
      if (!code) return;

      var btn = document.createElement("button");
      btn.className = "copy-btn";
      btn.textContent = "Copy";
      btn.setAttribute("type", "button");

      btn.addEventListener("click", function () {
        var text = code.textContent;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () {
            showCopied(btn);
          });
        } else {
          var ta = document.createElement("textarea");
          ta.value = text;
          ta.style.position = "fixed";
          ta.style.opacity = "0";
          document.body.appendChild(ta);
          ta.select();
          document.execCommand("copy");
          document.body.removeChild(ta);
          showCopied(btn);
        }
      });

      pre.appendChild(btn);
    });
  }

  function showCopied(btn) {
    btn.textContent = "Copied!";
    btn.classList.add("copied");
    setTimeout(function () {
      btn.textContent = "Copy";
      btn.classList.remove("copied");
    }, 2000);
  }

  /* ── LocalStorage persistence ─────────────────────────── */

  var saveTimer = null;

  function initLocalStorage() {
    if (!chapterId) return;

    document.querySelectorAll(".answer-input").forEach(function (ta) {
      var exId = ta.getAttribute("data-exercise");
      var prompt = ta.getAttribute("data-prompt");
      if (!exId) return;

      var saved = loadItem(storageKey(exId, "prompt:" + prompt));
      if (saved !== null) ta.value = saved;

      ta.addEventListener("input", function () {
        clearTimeout(saveTimer);
        var val = ta.value;
        var key = storageKey(exId, "prompt:" + prompt);
        saveTimer = setTimeout(function () { saveItem(key, val); }, 500);
      });
    });

    document.querySelectorAll(".completion-check").forEach(function (cb) {
      var exId = cb.getAttribute("data-exercise");
      if (!exId) return;

      var saved = loadItem(storageKey(exId, "done"));
      if (saved === "1") cb.checked = true;

      cb.addEventListener("change", function () {
        saveItem(storageKey(exId, "done"), cb.checked ? "1" : "0");
      });
    });

    // Restore MCQ state
    document.querySelectorAll(".exercise.mcq").forEach(function (exercise) {
      var exId = exercise.id;
      if (!exId) return;
      var savedAnswer = loadItem(storageKey(exId, "mcq"));
      var savedResult = loadItem(storageKey(exId, "mcq-result"));
      if (!savedAnswer) return;

      var radio = exercise.querySelector('input[value="' + savedAnswer + '"]');
      if (radio) {
        radio.checked = true;
        var checkBtn = exercise.querySelector(".mcq-check");
        if (checkBtn) checkBtn.click();
      }
    });
  }

  /* ── Global controls ──────────────────────────────────── */

  function initGlobalControls() {
    var revealBtn = document.getElementById("reveal-all");
    var hideBtn = document.getElementById("hide-all");
    var resetBtn = document.getElementById("reset-all");
    var showCompletedBtn = document.getElementById("show-completed");

    if (revealBtn) {
      revealBtn.addEventListener("click", function () {
        document.querySelectorAll("details.hint, details.solution").forEach(function (d) {
          d.classList.remove("locked");
          d.open = true;
        });
        revealMCQ();
      });
    }

    if (hideBtn) {
      hideBtn.addEventListener("click", function () {
        document.querySelectorAll("details.hint, details.solution").forEach(function (d) {
          d.open = false;
        });
        initProgressiveHints();
        resetMCQ();
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        if (!confirm("Clear all saved answers and progress for this chapter?")) return;

        clearChapterData();

        document.querySelectorAll(".answer-input").forEach(function (ta) {
          ta.value = "";
        });
        document.querySelectorAll(".completion-check").forEach(function (cb) {
          cb.checked = false;
        });

        document.querySelectorAll("details.hint, details.solution").forEach(function (d) {
          d.open = false;
        });
        initProgressiveHints();
        resetMCQ();
      });
    }

    if (showCompletedBtn) {
      showCompletedBtn.addEventListener("click", function () {
        document.querySelectorAll("details.hint, details.solution").forEach(function (d) {
          d.open = false;
        });
        initProgressiveHints();
        resetMCQ();

        document.querySelectorAll(".exercise").forEach(function (exercise) {
          var exId = exercise.id;
          if (!exId) return;
          var done = loadItem(storageKey(exId, "done"));
          if (done === "1") {
            exercise.querySelectorAll("details.hint, details.solution").forEach(function (d) {
              d.classList.remove("locked");
              d.open = true;
            });
          }
        });
      });
    }
  }

  /* ── Glossary panel ───────────────────────────────────── */

  function initGlossary() {
    var toggle = document.getElementById("glossary-toggle");
    var panel = document.getElementById("glossary-panel");
    var close = document.getElementById("glossary-close");
    var search = document.getElementById("glossary-search");
    if (!toggle || !panel) return;

    var overlay = document.createElement("div");
    overlay.className = "glossary-overlay";
    document.body.appendChild(overlay);

    function openPanel() {
      panel.classList.add("open");
      overlay.classList.add("open");
      if (search) search.focus();
    }

    function closePanel() {
      panel.classList.remove("open");
      overlay.classList.remove("open");
    }

    toggle.addEventListener("click", openPanel);
    if (close) close.addEventListener("click", closePanel);
    overlay.addEventListener("click", closePanel);

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && panel.classList.contains("open")) {
        closePanel();
      }
    });

    if (search) {
      search.addEventListener("input", function () {
        var q = search.value.toLowerCase().trim();
        panel.querySelectorAll(".glossary-entry").forEach(function (entry) {
          var term = entry.getAttribute("data-term") || "";
          var text = entry.textContent.toLowerCase();
          entry.classList.toggle("hidden", q && term.indexOf(q) === -1 && text.indexOf(q) === -1);
        });
      });
    }
  }

  /* ── Init ──────────────────────────────────────────────── */

  document.addEventListener("DOMContentLoaded", function () {
    initProgressiveHints();
    initMCQ();
    initGlobalControls();
    initProgressIndicator();
    initCopyButtons();
    initLocalStorage();
    initGlossary();
  });
})();
