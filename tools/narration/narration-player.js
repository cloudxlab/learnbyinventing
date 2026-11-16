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
  var manifest = null;

  // ── CSS for animations ──────────────────────────────────────────────

  var style = document.createElement('style');
  style.textContent =
    '@keyframes narration-pulse { 0%,100%{box-shadow:0 0 0 0 rgba(59,130,246,0.5)} 50%{box-shadow:0 0 0 8px rgba(59,130,246,0)} }' +
    '@keyframes narration-bar1 { 0%,100%{height:4px} 50%{height:14px} }' +
    '@keyframes narration-bar2 { 0%,100%{height:6px} 50%{height:16px} }' +
    '@keyframes narration-bar3 { 0%,100%{height:8px} 50%{height:12px} }' +
    '@keyframes narration-spin { to{transform:rotate(360deg)} }' +
    '#narration-controls.playing #narration-mute { animation: narration-pulse 2s ease-in-out infinite; }' +
    '#narration-controls.buffering #narration-mute { animation: none; }' +
    '@keyframes narration-done-glow { 0%{box-shadow:0 0 0 0 rgba(34,197,94,0.7)} 40%{box-shadow:0 0 12px 4px rgba(34,197,94,0.4)} 100%{box-shadow:0 0 0 0 rgba(34,197,94,0)} }' +
    '#narration-controls.done #narration-mute { animation: narration-done-glow 1.8s ease-out; background: rgba(34,197,94,0.55) !important; }' +
    '#narration-done-check { display:none;position:absolute;top:0;left:0;width:36px;height:36px;pointer-events:none;align-items:center;justify-content:center; }' +
    '#narration-controls.done #narration-done-check { display:flex; }' +
    '@keyframes narration-check-in { 0%{opacity:0;transform:scale(0.3)} 50%{opacity:1;transform:scale(1.1)} 100%{opacity:1;transform:scale(1)} }' +
    '#narration-controls.done #narration-done-check svg { animation: narration-check-in 0.4s ease-out; }' +
    '#narration-spinner { display:none;position:absolute;top:0;left:0;width:36px;height:36px;pointer-events:none; }' +
    '#narration-controls.buffering #narration-spinner { display:block; }' +
    '#narration-spinner svg { animation:narration-spin 1s linear infinite; }' +
    '.narration-bars { display:none; align-items:center; gap:2px; height:18px; margin-left:6px; }' +
    '#narration-controls.playing .narration-bars { display:flex; }' +
    '#narration-controls.buffering .narration-bars { display:none; }' +
    '.narration-bars span { display:block; width:3px; background:#3b82f6; border-radius:1px; }' +
    '.narration-bars span:nth-child(1) { animation:narration-bar1 0.8s ease-in-out infinite; }' +
    '.narration-bars span:nth-child(2) { animation:narration-bar2 0.6s ease-in-out infinite 0.1s; }' +
    '.narration-bars span:nth-child(3) { animation:narration-bar3 0.7s ease-in-out infinite 0.2s; }' +
    '.narration-bars span:nth-child(4) { animation:narration-bar1 0.9s ease-in-out infinite 0.15s; }' +
    '@keyframes narration-ellipsis { 0%{content:"."} 33%{content:".."} 66%{content:"..."} }' +
    '.narration-buffering-label { display:none; font-size:12px; color:rgba(255,255,255,0.85); background:rgba(0,0,0,0.55); padding:2px 10px; border-radius:12px; font-family:system-ui,sans-serif; white-space:nowrap; }' +
    '.narration-buffering-label::after { content:"..."; animation:narration-ellipsis 1.2s steps(1) infinite; }' +
    '#narration-controls.buffering .narration-buffering-label { display:block; }';
  document.head.appendChild(style);

  // ── UI ──────────────────────────────────────────────────────────────

  var container = document.createElement('div');
  container.id = 'narration-controls';
  container.style.cssText =
    'position:fixed;top:50px;right:16px;z-index:100;display:flex;align-items:center;gap:6px;' +
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
  muteBtn.style.position = 'relative';
  var replayBtn = makeBtn('narration-replay', 'Replay', SVG_REPLAY);

  var spinner = document.createElement('div');
  spinner.id = 'narration-spinner';
  spinner.innerHTML =
    '<svg width="36" height="36" viewBox="0 0 36 36">' +
    '<circle cx="18" cy="18" r="15" fill="none" stroke="rgba(59,130,246,0.3)" stroke-width="3"/>' +
    '<path d="M18 3a15 15 0 0 1 15 15" fill="none" stroke="#3b82f6" stroke-width="3" stroke-linecap="round"/>' +
    '</svg>';
  muteBtn.appendChild(spinner);

  var doneCheck = document.createElement('div');
  doneCheck.id = 'narration-done-check';
  doneCheck.innerHTML =
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' +
    '<polyline points="20 6 9 17 4 12"/></svg>';
  muteBtn.appendChild(doneCheck);

  var bars = document.createElement('div');
  bars.className = 'narration-bars';
  for (var b = 0; b < 4; b++) bars.appendChild(document.createElement('span'));

  var bufferingLabel = document.createElement('span');
  bufferingLabel.className = 'narration-buffering-label';
  bufferingLabel.textContent = 'Buffering';

  container.appendChild(muteBtn);
  container.appendChild(replayBtn);
  container.appendChild(bars);
  container.appendChild(bufferingLabel);

  // ── Completion chime (Web Audio API) ─────────────────────────────────

  var audioCtx = null;
  var CHIME_ENABLED_KEY = 'narration-chime';
  var chimeEnabled = localStorage.getItem(CHIME_ENABLED_KEY) !== 'false';

  function getAudioCtx() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    return audioCtx;
  }

  function playChime() {
    if (!chimeEnabled || muted) return;
    try {
      var ctx = getAudioCtx();
      var now = ctx.currentTime;
      var gain = ctx.createGain();
      gain.connect(ctx.destination);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.8);

      var o1 = ctx.createOscillator();
      o1.type = 'sine';
      o1.frequency.setValueAtTime(880, now);
      o1.connect(gain);
      o1.start(now);
      o1.stop(now + 0.3);

      var gain2 = ctx.createGain();
      gain2.connect(ctx.destination);
      gain2.gain.setValueAtTime(0, now);
      gain2.gain.setValueAtTime(0.10, now + 0.15);
      gain2.gain.exponentialRampToValueAtTime(0.001, now + 1.0);

      var o2 = ctx.createOscillator();
      o2.type = 'sine';
      o2.frequency.setValueAtTime(1174.66, now + 0.15);
      o2.connect(gain2);
      o2.start(now + 0.15);
      o2.stop(now + 0.6);
    } catch (e) {}
  }

  // ── Playing state ───────────────────────────────────────────────────

  var doneTimer = null;

  function setPlaying(isPlaying) {
    if (isPlaying) {
      container.classList.remove('done');
      if (doneTimer) { clearTimeout(doneTimer); doneTimer = null; }
      container.classList.add('playing');
    } else {
      container.classList.remove('playing');
    }
  }

  function showDone() {
    container.classList.add('done');
    if (doneTimer) clearTimeout(doneTimer);
    doneTimer = setTimeout(function () {
      container.classList.remove('done');
      doneTimer = null;
    }, 2000);
  }

  function setBuffering(isBuffering) {
    if (isBuffering) {
      container.classList.add('buffering');
    } else {
      container.classList.remove('buffering');
    }
  }

  audio.addEventListener('play', function () { setPlaying(true); });
  audio.addEventListener('pause', function () { setPlaying(false); setBuffering(false); });
  audio.addEventListener('ended', function () { setPlaying(false); setBuffering(false); playChime(); showDone(); });
  audio.addEventListener('waiting', function () { setBuffering(true); });
  audio.addEventListener('canplay', function () { setBuffering(false); });
  audio.addEventListener('playing', function () { setBuffering(false); });

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
    if (typeof fragIdx === 'number' && fragIdx >= 0) {
      return flatIdx + '-frag-' + fragIdx;
    }
    return '' + flatIdx;
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
    var name;
    if (manifest && manifest[key]) {
      name = manifest[key];
    } else {
      name = 'slide-' + pad(typeof key === 'string' && key.indexOf('-frag-') > -1
        ? parseInt(key, 10) : parseInt(key, 10));
      if (typeof key === 'string' && key.indexOf('-frag-') > -1) {
        name += key.substring(key.indexOf('-frag-'));
      }
    }
    return 'narration/audio/' + name + '.mp3';
  }

  function playFile(path) {
    audio.pause();
    currentFile = path;
    if (muted) { setBuffering(false); return; }
    if (!userHasInteracted) {
      pendingPlay = path;
      return;
    }
    setBuffering(true);
    audio.src = path;
    audio.play().catch(function (err) {
      setBuffering(false);
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

  // ── Load manifest and probe ─────────────────────────────────────────

  function loadManifest(callback) {
    var req = new XMLHttpRequest();
    req.open('GET', 'narration/manifest.json', true);
    req.onload = function () {
      if (req.status >= 200 && req.status < 400) {
        try {
          manifest = JSON.parse(req.responseText);
          console.log('[narration] Loaded manifest (' + Object.keys(manifest).length + ' entries)');
        } catch (e) {
          manifest = null;
        }
      }
      callback();
    };
    req.onerror = function () { callback(); };
    req.send();
  }

  function probeNarration(callback) {
    var firstPath = audioPath('0');
    var probe = new XMLHttpRequest();
    probe.open('HEAD', firstPath, true);
    probe.onload = function () {
      callback(probe.status >= 200 && probe.status < 400);
    };
    probe.onerror = function () { callback(false); };
    probe.send();
  }

  // ── Init ────────────────────────────────────────────────────────────

  function init() {
    loadManifest(function () {
    probeNarration(function (found) {
      if (!found) {
        console.log('[narration] No audio files found');
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
