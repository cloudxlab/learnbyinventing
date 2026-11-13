# Narration Pipeline

Generate voice-over narration for any Reveal.js presentation in three steps.

## Prerequisites

```bash
brew install ffmpeg       # AIFF/WAV → MP3 conversion (recommended)
```

The `claude` CLI must be installed for script generation (step 2).

On macOS, the default TTS engine is the built-in `say` command (no install needed). Alternatively, install Piper TTS (`pip install piper-tts`) and use `--engine piper`.

## Quick Start

```bash
# Step 1: Extract slide text → JSON
python tools/narration/1_extract_slides.py <chapter>/slides.html

# Step 2: Generate narration scripts via claude CLI
python tools/narration/2_generate_scripts.py <chapter>/slides.html --topic "<Topic Name>"

# Step 3: Generate MP3 audio from scripts
python tools/narration/3_generate_audio.py <chapter>/slides.html

# Step 4: Wire up the player
cp tools/narration/narration-player.js <chapter>/narration-player.js
# Add <script src="narration-player.js"></script> before </body> in slides.html

# Step 5: Test
cd <chapter> && python3 -m http.server 8000
# Open http://localhost:8000/slides.html
```

## Pipeline Details

### Step 1: Extract slide text

```bash
python tools/narration/1_extract_slides.py differentiation/slides.html
```

Produces `<chapter>/narration/slides_data.json` — a JSON array of slides with their text and fragment content.

### Step 2: Generate narration scripts

```bash
python tools/narration/2_generate_scripts.py differentiation/slides.html --topic "Differentiation"
```

Produces `<chapter>/narration/scripts/slide-00.txt`, `slide-00-frag-0.txt`, etc.

Each `.txt` file has a comment header showing what's on screen, then the narration text below `# ---`. **Edit these freely** — re-running step 3 will pick up your changes.

Options:
- `--force` — regenerate all scripts (overwrites edits)
- `--dry-run` — show what would be generated
- `--only "3,5,7"` — only specific slide indices

### Step 3: Generate audio

```bash
python tools/narration/3_generate_audio.py differentiation/slides.html
```

Produces `<chapter>/narration/audio/slide-00.mp3`, etc.

Auto-detects TTS engine: macOS `say` (default on Mac) or Piper TTS.

Options:
- `--engine say|piper` — choose TTS backend (default: auto-detect)
- `--voice <name>` — voice name (default: Samantha for `say`, en_US-lessac-medium for Piper)
- `--force` — regenerate all audio
- `--dry-run` — show what would be generated
- `--only slide-03.txt,slide-05-frag-0.txt` — only specific files

### Audio player

Copy `narration-player.js` into the chapter folder and add to your slides HTML before `</body>`:

```html
<script src="narration-player.js"></script>
```

The player auto-plays narration on slide/fragment changes. Controls (mute/unmute + replay) appear in the bottom-right corner. Mute state persists in localStorage. If no `narration/audio/` folder exists, the player hides itself.

**Note:** Must be served via HTTP (e.g., `python3 -m http.server`), not opened as a local file, because the player uses XHR to probe for audio files.

## File Layout

```
<chapter>/
├── slides.html
├── narration-player.js        ← copy from tools/narration/
├── narration/
│   ├── slides_data.json       ← step 1 output
│   ├── scripts/               ← step 2 output (edit these)
│   │   ├── slide-00.txt
│   │   ├── slide-00-frag-0.txt
│   │   ├── slide-01.txt
│   │   └── ...
│   └── audio/                 ← step 3 output
│       ├── slide-00.mp3
│       ├── slide-00-frag-0.mp3
│       ├── slide-01.mp3
│       └── ...
```

## Iterating

1. Run steps 1–3 to generate everything.
2. Review scripts in `narration/scripts/` — edit any that sound off.
3. Re-run step 3 — it only regenerates audio for scripts newer than their audio file.
4. Listen in the browser. Edit scripts and re-run step 3 as needed.
