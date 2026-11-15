# Presentation Specification

Reference implementation: `differentiation/slides.html`

Every `*/slides.html` in this repository MUST conform to the following structure and styling rules.

---

## 1. HTML Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>{Chapter Title} — Slides</title>
  <!-- Reveal.js CSS -->
  <!-- Reveal.js theme (white) -->
  <!-- MathJax (if used) -->
  <!-- Optional: Plotly, other libs -->
  <style>/* base + mobile CSS */</style>
  <!-- Google Analytics -->
</head>
<body>
  <!-- Top nav bar -->
  <!-- Progress bar -->
  <!-- Bottom copyright with Index link -->
  <div class="reveal"><div class="slides">
    <!-- Title slide -->
    <!-- Challenge slide (chapter-level) -->
    <!-- Part sections (id="part1", id="part2", ...) -->
    <!-- Index slide (id="slide-index") -->
  </div></div>
  <!-- Reveal.js script + initialization -->
  <!-- Progress bar update script -->
  <!-- Chapter footer (hidden in slide mode) -->
  <!-- Narration player script -->
</body>
</html>
```

---

## 2. Head Section

### 2.1 Viewport Meta Tag (REQUIRED)
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
```

### 2.2 Base CSS Styles (REQUIRED)
```css
.reveal { font-family: Georgia, serif; margin-top: 25px; }
.reveal .slide-content { font-size: 0.55em; }
.reveal h1 { font-size: 1.8em; }
.reveal h2 { font-size: 1.4em; color: #7a6b3a; border-bottom: 2px solid #c8a96e; padding-bottom: 0.3em; }
.reveal h3 { font-size: 1.1em; }
.reveal pre { font-size: 0.55em; box-shadow: none; }
.reveal code { font-family: 'SF Mono', 'Menlo', 'Consolas', monospace; }
.reveal p code, .reveal li code {
  background: #f0ede6; padding: 0.1em 0.3em; border-radius: 3px;
  color: #c7254e; font-size: 0.85em;
}
.reveal pre code { background: #282c34; color: #abb2bf; padding: 0.8em; border-radius: 5px; }
.reveal table { font-size: 0.7em; margin: 0 auto; }
.reveal th { background: #f5f3ef; }
.reveal th, .reveal td { border: 1px solid #ddd; padding: 0.3em 0.6em; }
.reveal .slide-title { color: #555; font-style: italic; font-size: 0.9em; }
.reveal ul, .reveal ol { text-align: left; font-size: 0.85em; }
```

### 2.3 Reveal.js Progress Bar Hidden (REQUIRED)
```css
.reveal .progress { display: none !important; }
```

### 2.4 Chapter Footer CSS (REQUIRED)
The chapter footer MUST be hidden in slide mode:
```css
.chapter-footer { display: none; }
```

### 2.5 Top Progress Bar CSS (REQUIRED)
```css
#top-progress { position: fixed; top: 26px; left: 0; right: 0; height: 5px; background: #ddd; z-index: 200; }
#top-progress-bar { height: 100%; width: 0%; background: #c8a96e; transition: width 0.3s ease; min-width: 2%; }
```

### 2.6 Bottom Copyright CSS (REQUIRED)
```css
#bottom-copyright { position: fixed; bottom: 6px; left: 12px; font-size: 11px; color: #aaa; font-family: sans-serif; z-index: 200; }
#bottom-copyright a { color: #aaa; text-decoration: none; }
#bottom-copyright a:hover { color: #c8a96e; }
```

### 2.7 Mobile-Friendly CSS Overrides (REQUIRED)
```css
@media screen and (max-width: 768px) {
  .reveal .slide-content { font-size: 1.1em; }
  .reveal h2 { font-size: 1.4em; }
  .reveal h3 { font-size: 1.15em; }
  .reveal pre { font-size: 0.9em; }
  .reveal table { font-size: 1.0em; }
  .reveal ul, .reveal ol { font-size: 1.1em; }
  .reveal p code, .reveal li code { font-size: 1.0em; }
  .reveal th, .reveal td { padding: 0.25em 0.5em; }
  .slides-topnav { font-size: 11px !important; padding: 2px 8px !important; }
  #bottom-copyright { font-size: 9px; }
}
```

### 2.8 Google Analytics (REQUIRED)
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9TZCPED97E"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-9TZCPED97E');
</script>
```

---

## 3. Body Structure

### 3.1 Top Navigation Bar (REQUIRED)
```html
<nav class="slides-topnav" style="position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(255,255,255,0.95);padding:4px 16px;font-size:13px;font-family:sans-serif;border-bottom:1px solid #ddd;display:flex;justify-content:space-between;align-items:center;">
  <a href="../index.html" style="color:#888;text-decoration:none;">&larr; All chapters</a>
  <span style="display:flex;gap:10px;align-items:center;">
    <strong style="color:#333;">Slides</strong>
  </span>
</nav>
```

### 3.2 Top Progress Bar (REQUIRED)
```html
<div id="top-progress"><div id="top-progress-bar"></div></div>
```

### 3.3 Bottom Copyright with Index and Report a Bug Links (REQUIRED)
```html
<div id="bottom-copyright"><a href="#/slide-index">Index</a> &middot; <a href="https://github.com/cloudxlab/learnbyinventing/issues/new?template=bug_report.md" target="_blank">Report a Bug</a> &middot; &copy; <a href="https://cloudxlab.com">CloudxLab</a></div>
```

### 3.4 Title Slide (REQUIRED)
The first `<section>` must be the title slide containing:
- `<h1>` with the chapter title
- `<div class="slide-content slide-title">` with a subtitle/tagline
- Navigation instructions with `<kbd>` styled keys explaining arrow/space navigation

### 3.5 Chapter-Level Challenge Slide (REQUIRED)
Immediately after the title slide, a challenge slide:
- Wrapped in `<div class="slide-content"><div style="font-size:1.3em;">`
- Opens with `<p style="color:#7a6b3a;"><strong>Challenge (skip ahead if you can):</strong></p>`
- Contains a concrete coding/problem challenge representing the chapter's final outcome
- Ends with a note like "Already got it? The next slides will guide you step by step."

### 3.6 Part Sections (REQUIRED)
Each part/topic section MUST:
- Have an `id` attribute: `id="part1"`, `id="part2"`, etc.
- Contain an `<h2>` header: `<h2>Part N: Title</h2>`
- Content slides follow the part header

### 3.7 Index Slide (REQUIRED, last content slide)
```html
<section id="slide-index">
  <h2>Index</h2>
  <div class="slide-content"><div style="font-size:1.2em; text-align:left; max-width:600px; margin:0 auto;">
    <ol style="line-height:2;">
      <li><a href="#/part1">Part 1 Title</a></li>
      <li><a href="#/part2">Part 2 Title</a></li>
      <!-- ... one entry per part ... -->
    </ol>
  </div></div>
</section>
```

---

## 4. Scripts

### 4.1 Reveal.js Initialization (REQUIRED)
```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.js"></script>
<script>
  Reveal.initialize({
    hash: true,
    slideNumber: true,
    progress: true,
    transition: 'slide',
    width: 1200,
    height: 700,
    minScale: 0.1,
    maxScale: 2.0,
  });
</script>
```

Key settings:
- `minScale: 0.1` and `maxScale: 2.0` — enables mobile-friendly scaling
- `hash: true` — enables URL-based navigation (required for index links)

### 4.2 Progress Bar Update (REQUIRED)
```javascript
function updateProgress() {
  var total = Reveal.getTotalSlides();
  var current = Reveal.getSlidePastCount() + 1;
  var pct = Math.min(100, (current / total) * 100);
  document.getElementById('top-progress-bar').style.width = pct + '%';
}
Reveal.on('slidechanged', function() { updateProgress(); });
Reveal.on('ready', function() { updateProgress(); });
```

### 4.3 Chapter Footer (REQUIRED, placed after closing `</script>`)
```html
<div class="chapter-footer">
  <p>Source on <a href="https://github.com/cloudxlab/learnbyinventing">GitHub</a> &middot; <a href="../index.html">Back to all chapters</a></p>
  <p>&copy; 2026 <a href="https://cloudxlab.com">CloudxLab</a>. All rights reserved.</p>
</div>
```

### 4.4 Narration Player (REQUIRED, last script before `</body>`)
```html
<script src="narration-player.js"></script>
```

---

## 5. Summary Checklist

| # | Check | Required |
|---|-------|----------|
| 1 | Viewport meta tag | YES |
| 2 | Mobile CSS `@media (max-width: 768px)` block | YES |
| 3 | `.chapter-footer { display: none; }` (not visible styling) | YES |
| 4 | `.reveal .progress { display: none !important; }` | YES |
| 5 | Top progress bar (`#top-progress`) | YES |
| 6 | Bottom copyright with Index + Report a Bug links | YES |
| 7 | Top nav bar (`slides-topnav`) | YES |
| 8 | Google Analytics tag (G-9TZCPED97E) | YES |
| 9 | Title slide with `<h1>`, subtitle, navigation instructions | YES |
| 10 | Challenge slide after title | YES |
| 11 | Part sections with `id="partN"` attributes | YES |
| 12 | Index slide (`id="slide-index"`) as last content slide | YES |
| 13 | `Reveal.initialize` with `minScale: 0.1, maxScale: 2.0` | YES |
| 14 | Progress bar update script (`updateProgress`) | YES |
| 15 | Chapter footer div (hidden via CSS) | YES |
| 16 | `narration-player.js` script tag before `</body>` | YES |
