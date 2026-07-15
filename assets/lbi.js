/* Learn By Inventing — shared chapter interactions */

(function () {
  "use strict";

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

  function initGlobalControls() {
    var revealBtn = document.getElementById("reveal-all");
    var hideBtn = document.getElementById("hide-all");

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
  }

  document.addEventListener("DOMContentLoaded", function () {
    initProgressiveHints();
    initMCQ();
    initGlobalControls();
  });
})();
