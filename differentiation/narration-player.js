/**
 * Narration Player for Reveal.js presentations.
 *
 * Expected audio files (relative to the HTML file):
 *   narration/audio/slide-00.mp3
 *   narration/audio/slide-00-frag-0.mp3
 *   narration/audio/slide-01.mp3  ...
 *
 * Copy this file next to slides.html and add before </body>:
 *   <script src="narration-player.js"></script>
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'narration-muted';
  var audio = new Audio();
  var muted = localStorage.getItem(STORAGE_KEY) === 'true';
  var currentFile = null;
  var userHasInteracted = false;
  var pendingPlay = null;

  // ── CSS for animations ──────────────────────────────────────────────

  var style = document.createElement('style');
  style.textContent =
    '@keyframes narration-pulse { 0%,100%{box-shadow:0 0 0 0 rgba(59,130,246,0.5)} 50%{box-shadow:0 0 0 8px rgba(59,130,246,0)} }' +
    '@keyframes narration-bar1 { 0%,100%{height:4px} 50%{height:14px} }' +
    '@keyframes narration-bar2 { 0%,100%{height:6px} 50%{height:16px} }' +
    '@keyframes narration-bar3 { 0%,100%{height:8px} 50%{height:12px} }' +
    '#narration-controls.playing #narration-mute { animation: narration-pulse 2s ease-in-out infinite; }' +
    '.narration-bars { display:none; align-items:center; gap:2px; height:18px; margin-left:6px; }' +
    '#narration-controls.playing .narration-bars { display:flex; }' +
    '.narration-bars span { display:block; width:3px; background:#3b82f6; border-radius:1px; }' +
    '.narration-bars span:nth-child(1) { animation:narration-bar1 0.8s ease-in-out infinite; }' +
    '.narration-bars span:nth-child(2) { animation:narration-bar2 0.6s ease-in-out infinite 0.1s; }' +
    '.narration-bars span:nth-child(3) { animation:narration-bar3 0.7s ease-in-out infinite 0.2s; }' +
    '.narration-bars span:nth-child(4) { animation:narration-bar1 0.9s ease-in-out infinite 0.15s; }';
  document.head.appendChild(style);

  // ── UI ──────────────────────────────────────────────────────────────

  var container = document.createElement('div');
  container.id = 'narration-controls';
  container.style.cssText =
    'position:fixed;bottom:16px;right:16px;z-index:100;display:flex;align-items:center;gap:6px;' +
    'opacity:0;transition:opacity 0.3s;pointer-events:none;';

  function makeBtn(id, title, svg) {
    var btn = document.createElement('button');
    btn.id = id;
    btn.title = title;
    btn.innerHTML = svg;
    btn.style.cssText =
      'background:rgba(0,0,0,0.55);border:none;border-radius:50%;' +
      'width:36px;height:36px;cursor:pointer;display:flex;align-items:center;' +
      'justify-content:center;color:#fff;padding:0;transition:background 0.2s;';
    btn.onmouseenter = function () { btn.style.background = 'rgba(0,0,0,0.8)'; };
    btn.onmouseleave = function () { btn.style.background = 'rgba(0,0,0,0.55)'; };
    return btn;
  }

  var SVG_UNMUTED =
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
    '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>' +
    '<path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>' +
    '<path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>';

  var SVG_MUTED =
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
    '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>' +
    '<line x1="23" y1="9" x2="17" y2="15"/>' +
    '<line x1="17" y1="9" x2="23" y2="15"/></svg>';

  var SVG_REPLAY =
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
    '<polyline points="1 4 1 10 7 10"/>' +
    '<path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>';

  var muteBtn = makeBtn('narration-mute', 'Mute/Unmute', muted ? SVG_MUTED : SVG_UNMUTED);
  var replayBtn = makeBtn('narration-replay', 'Replay', SVG_REPLAY);

  var bars = document.createElement('div');
  bars.className = 'narration-bars';
  for (var b = 0; b < 4; b++) bars.appendChild(document.createElement('span'));

  container.appendChild(muteBtn);
  container.appendChild(replayBtn);
  container.appendChild(bars);

  // ── Playing state ───────────────────────────────────────────────────

  function setPlaying(isPlaying) {
    if (isPlaying) {
      container.classList.add('playing');
    } else {
      container.classList.remove('playing');
    }
  }

  audio.addEventListener('play', function () { setPlaying(true); });
  audio.addEventListener('pause', function () { setPlaying(false); });
  audio.addEventListener('ended', function () { setPlaying(false); });

  // ── Button handlers ─────────────────────────────────────────────────

  muteBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    muted = !muted;
    localStorage.setItem(STORAGE_KEY, String(muted));
    muteBtn.innerHTML = muted ? SVG_MUTED : SVG_UNMUTED;
    if (muted) {
      audio.pause();
    } else {
      playCurrentSlide();
    }
  });

  replayBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    if (currentFile && !muted) {
      audio.currentTime = 0;
      audio.play().catch(function () {});
    }
  });

  // ── Autoplay unlock ─────────────────────────────────────────────────

  function onFirstInteraction() {
    if (userHasInteracted) return;
    userHasInteracted = true;
    document.removeEventListener('click', onFirstInteraction, true);
    document.removeEventListener('keydown', onFirstInteraction, true);
    document.removeEventListener('touchstart', onFirstInteraction, true);
    if (pendingPlay) {
      playFile(pendingPlay);
      pendingPlay = null;
    }
  }

  document.addEventListener('click', onFirstInteraction, true);
  document.addEventListener('keydown', onFirstInteraction, true);
  document.addEventListener('touchstart', onFirstInteraction, true);

  // ── Audio logic ─────────────────────────────────────────────────────

  function pad(n) { return n < 10 ? '0' + n : '' + n; }

  function slideKey(flatIdx, fragIdx) {
    var name = 'slide-' + pad(flatIdx);
    if (typeof fragIdx === 'number' && fragIdx >= 0) {
      name += '-frag-' + fragIdx;
    }
    return name;
  }

  function flatIndex(h, v) {
    var slides = Reveal.getSlides();
    var current = Reveal.getSlide(h, v);
    for (var i = 0; i < slides.length; i++) {
      if (slides[i] === current) return i;
    }
    return h;
  }

  function audioPath(key) {
    return 'narration/audio/' + key + '.mp3';
  }

  function playFile(path) {
    audio.pause();
    currentFile = path;
    if (muted) return;
    if (!userHasInteracted) {
      pendingPlay = path;
      return;
    }
    audio.src = path;
    audio.play().catch(function (err) {
      console.log('[narration] play blocked:', err.message);
    });
  }

  function playCurrentSlide() {
    var indices = Reveal.getIndices();
    var flat = flatIndex(indices.h, indices.v);
    var fragIdx = (indices.f != null && indices.f >= 0) ? indices.f : undefined;
    var key = slideKey(flat, fragIdx);
    playFile(audioPath(key));
  }

  // ── Probe for audio files ───────────────────────────────────────────

  function probeNarration(callback) {
    var probe = new XMLHttpRequest();
    probe.open('HEAD', audioPath('slide-00'), true);
    probe.onload = function () {
      callback(probe.status >= 200 && probe.status < 400);
    };
    probe.onerror = function () { callback(false); };
    probe.send();
  }

  // ── Init ────────────────────────────────────────────────────────────

  function init() {
    probeNarration(function (found) {
      if (!found) {
        console.log('[narration] No audio files found at narration/audio/slide-00.mp3');
        return;
      }
      console.log('[narration] Audio files found, player active');

      document.body.appendChild(container);
      container.style.opacity = '1';
      container.style.pointerEvents = 'auto';

      Reveal.on('slidechanged', function () {
        playCurrentSlide();
      });

      Reveal.on('fragmentshown', function (event) {
        var indices = Reveal.getIndices();
        var flat = flatIndex(indices.h, indices.v);
        var fragIndex = event.fragment.getAttribute('data-fragment-index');
        if (fragIndex == null) fragIndex = indices.f;
        var key = slideKey(flat, parseInt(fragIndex, 10));
        var path = audioPath(key);

        var check = new XMLHttpRequest();
        check.open('HEAD', path, true);
        check.onload = function () {
          if (check.status >= 200 && check.status < 400) {
            playFile(path);
          }
        };
        check.send();
      });

      Reveal.on('fragmenthidden', function () {
        audio.pause();
      });

      playCurrentSlide();
    });
  }

  function waitForReveal() {
    if (typeof Reveal === 'undefined') {
      document.addEventListener('DOMContentLoaded', waitForReveal);
      return;
    }
    if (typeof Reveal.isReady === 'function' && Reveal.isReady()) {
      init();
    } else {
      Reveal.addEventListener('ready', init);
    }
  }

  waitForReveal();
})();
