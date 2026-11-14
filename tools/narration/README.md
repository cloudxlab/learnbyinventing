# Narration Pipeline

Generate voice-over narration for any Reveal.js presentation.

## Installation

```bash
bash tools/narration/install.sh
```

This installs Kokoro TTS (best quality), ffmpeg, and downloads the voice model (~340 MB). The `claude` CLI is also needed for script generation.

## Quick Start (Incremental Build)

```bash
# Build everything (only regenerates what changed):
python tools/narration/build_narration.py <chapter>/slides.html --topic "<Topic>"

# Add to slides.html before </body>:
#   <script src="narration-player.js"></script>

# Test:
cd <chapter> && python3 -m http.server 8000
```

The build script runs all three pipeline steps incrementally:
- Re-extracts slide data only if `slides.html` changed
- Regenerates scripts only for slides whose data changed
- Regenerates audio only for scripts newer than their audio file

Options:
- `--force` — full rebuild from scratch
- `--only extract|scripts|audio` — run a single step
- `--engine kokoro|say|piper` — choose TTS backend
- `--voice <name>` — voice name (default: am_michael for Kokoro)

## Manual Pipeline

### Step 1: Extract slide text

```bash
python tools/narration/1_extract_slides.py <chapter>/slides.html
```

Produces `<chapter>/narration/slides_data.json`.

### Step 2: Generate narration scripts

```bash
python tools/narration/2_generate_scripts.py <chapter>/slides.html --topic "Differentiation"
```

Produces `<chapter>/narration/scripts/slide-00.txt`, `slide-00-frag-0.txt`, etc.

Each `.txt` file has a comment header showing what's on screen, then the narration text below `# ---`. **Edit these freely** — re-running step 3 picks up your changes.

Options: `--force`, `--dry-run`, `--only "3,5,7"`

### Step 3: Generate audio

```bash
python tools/narration/3_generate_audio.py <chapter>/slides.html
```

Produces `<chapter>/narration/audio/slide-00.mp3`, etc.

TTS engines (auto-detected, best first):
- **Kokoro** — natural neural voice (`pip install kokoro-onnx soundfile`)
- **macOS say** — built-in, no install needed
- **Piper** — open-source neural TTS (`pip install piper-tts`)

Options: `--engine kokoro|say|piper`, `--voice <name>`, `--force`, `--dry-run`

### Audio player

The build script auto-copies `narration-player.js` into the chapter folder. Add to slides HTML before `</body>`:

```html
<script src="narration-player.js"></script>
```

Features:
- Auto-plays narration on slide/fragment changes
- Mute/unmute and replay buttons (top-right)
- Animated equalizer bars when audio is playing
- Pulsing speaker icon during playback
- Mute state persists in localStorage
- Hides itself if no audio files exist

**Note:** Must be served via HTTP (`python3 -m http.server`), not `file://`.

## File Layout

```
<chapter>/
├── slides.html
├── narration-player.js        ← auto-copied by build
├── narration/
│   ├── slides_data.json       ← step 1 output
│   ├── scripts/               ← step 2 output (edit these)
│   │   ├── slide-00.txt
│   │   ├── slide-00-frag-0.txt
│   │   └── ...
│   └── audio/                 ← step 3 output
│       ├── slide-00.mp3
│       ├── slide-00-frag-0.mp3
│       └── ...
```

## Iterating

1. Run `build_narration.py` to generate everything.
2. Review scripts in `narration/scripts/` — edit any that sound off.
3. Run `build_narration.py` again — only changed scripts get new audio.
4. Listen in the browser and repeat.

## Making Slides Mobile-Friendly

Add these to your `slides.html` for readable text on phones:

1. **Viewport meta tag** in `<head>`:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
```

2. **Mobile CSS overrides** inside `<style>`:

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
}
```

3. **Flexible Reveal.js scaling** in `Reveal.initialize()`:

```js
minScale: 0.1,
maxScale: 2.0,
```
