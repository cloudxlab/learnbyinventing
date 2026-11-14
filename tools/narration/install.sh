#!/bin/bash
# Install dependencies for the narration pipeline.
# Usage: bash tools/narration/install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KOKORO_DIR="$SCRIPT_DIR/voices/kokoro"

echo "=== Narration Pipeline Installer ==="
echo

# ── Python packages ──────────────────────────────────────────────────
echo "[1/3] Installing Python packages..."
pip3 install kokoro-onnx soundfile 2>&1 | tail -1
echo "  Done."
echo

# ── ffmpeg ───────────────────────────────────────────────────────────
echo "[2/3] Checking ffmpeg..."
if command -v ffmpeg &>/dev/null; then
    echo "  ffmpeg already installed: $(ffmpeg -version 2>&1 | head -1)"
else
    echo "  ffmpeg not found."
    if command -v brew &>/dev/null; then
        echo "  Installing via Homebrew..."
        brew install ffmpeg
    else
        echo "  Please install ffmpeg manually:"
        echo "    macOS:  brew install ffmpeg"
        echo "    Ubuntu: sudo apt install ffmpeg"
    fi
fi
echo

# ── Kokoro model files ───────────────────────────────────────────────
echo "[3/3] Downloading Kokoro voice model (~340 MB)..."
mkdir -p "$KOKORO_DIR"

MODEL="$KOKORO_DIR/kokoro-v1.0.onnx"
VOICES="$KOKORO_DIR/voices-v1.0.bin"
BASE_URL="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1"

if [ -f "$MODEL" ] && [ "$(stat -f%z "$MODEL" 2>/dev/null || stat -c%s "$MODEL" 2>/dev/null)" -gt 1000000 ]; then
    echo "  Model already downloaded."
else
    echo "  Downloading kokoro-v1.0.onnx..."
    curl -L -o "$MODEL" "$BASE_URL/kokoro-v1.0.onnx"
fi

if [ -f "$VOICES" ] && [ "$(stat -f%z "$VOICES" 2>/dev/null || stat -c%s "$VOICES" 2>/dev/null)" -gt 1000000 ]; then
    echo "  Voices already downloaded."
else
    echo "  Downloading voices-v1.0.bin..."
    curl -L -o "$VOICES" "$BASE_URL/voices-v1.0.bin"
fi
echo

# ── Verify ───────────────────────────────────────────────────────────
echo "=== Verification ==="
python3 -c "from kokoro_onnx import Kokoro; print('  kokoro-onnx: OK')" 2>/dev/null || echo "  kokoro-onnx: FAILED"
python3 -c "import soundfile; print('  soundfile:   OK')" 2>/dev/null || echo "  soundfile:   FAILED"
command -v ffmpeg &>/dev/null && echo "  ffmpeg:      OK" || echo "  ffmpeg:      MISSING (audio will be .wav instead of .mp3)"
[ -f "$MODEL" ] && echo "  model:       OK" || echo "  model:       MISSING"
[ -f "$VOICES" ] && echo "  voices:      OK" || echo "  voices:      MISSING"
command -v claude &>/dev/null && echo "  claude CLI:  OK" || echo "  claude CLI:  MISSING (needed for step 2: script generation)"
echo
echo "Installation complete. Run the pipeline:"
echo "  python tools/narration/1_extract_slides.py <chapter>/slides.html"
echo "  python tools/narration/2_generate_scripts.py <chapter>/slides.html --topic '<Topic>'"
echo "  python tools/narration/3_generate_audio.py <chapter>/slides.html"
