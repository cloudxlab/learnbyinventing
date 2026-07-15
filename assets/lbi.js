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

  function initGlobalControls() {
    var revealBtn = document.getElementById("reveal-all");
    var hideBtn = document.getElementById("hide-all");

    if (revealBtn) {
      revealBtn.addEventListener("click", function () {
        document.querySelectorAll("details.hint, details.solution").forEach(function (d) {
          d.classList.remove("locked");
          d.open = true;
        });
      });
    }

    if (hideBtn) {
      hideBtn.addEventListener("click", function () {
        document.querySelectorAll("details.hint, details.solution").forEach(function (d) {
          d.open = false;
        });
        initProgressiveHints();
      });
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    initProgressiveHints();
    initGlobalControls();
  });
})();
