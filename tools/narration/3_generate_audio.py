#!/usr/bin/env python3
"""Generate MP3 audio files from narration scripts.

Supports two TTS backends:
  - macOS 'say' (default on macOS, no install needed)
  - Piper TTS   (use --engine piper)

Usage:
    python 3_generate_audio.py <path/to/slides.html> [--engine say|piper]
                                                      [--voice <voice>]
                                                      [--force]
                                                      [--only slide-03.txt,slide-05-frag-0.txt]

Reads:  <chapter>/narration/scripts/*.txt
Writes: <chapter>/narration/audio/*.mp3

Only regenerates audio for scripts that are newer than their audio file
(or missing audio), unless --force is used.
"""

import sys
import os
import subprocess
import argparse
import glob
import shutil
import platform


DEFAULT_SAY_VOICE = "Samantha"
DEFAULT_PIPER_VOICE = "en_US-lessac-medium"
VOICES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voices")


def read_narration(script_path):
    """Read narration text from a script file (skip # comment header)."""
    lines = []
    past_header = False
    with open(script_path, "r", encoding="utf-8") as f:
        for line in f:
            if past_header:
                lines.append(line)
            elif line.strip() == "# ---":
                past_header = True
    text = "".join(lines).strip()
    if not text and not past_header:
        with open(script_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
    return text


def get_narration_dir(slides_path):
    chapter_dir = os.path.dirname(os.path.abspath(slides_path))
    return os.path.join(chapter_dir, "narration")


def needs_regeneration(script_path, audio_path, force=False):
    if force:
        return True
    if not os.path.exists(audio_path):
        return True
    return os.path.getmtime(script_path) > os.path.getmtime(audio_path)


# ── macOS say backend ──────────────────────────────────────────────────

def generate_audio_say(text, output_path, voice):
    """Generate audio using macOS 'say' command."""
    aiff_path = output_path.replace(".mp3", ".aiff")

    try:
        subprocess.run(
            ["say", "-v", voice, "-o", aiff_path, text],
            capture_output=True, check=True, timeout=120,
        )
    except subprocess.CalledProcessError as e:
        print(f"say error: {e.stderr.decode().strip()}")
        return False
    except subprocess.TimeoutExpired:
        print("say timed out")
        return False

    if not os.path.exists(aiff_path):
        return False

    if shutil.which("ffmpeg"):
        try:
            subprocess.run(
                ["ffmpeg", "-y", "-i", aiff_path, "-codec:a", "libmp3lame",
                 "-qscale:a", "4", output_path],
                capture_output=True, check=True, timeout=30,
            )
            os.remove(aiff_path)
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            pass

    if shutil.which("lame"):
        try:
            subprocess.run(
                ["lame", "--quiet", "-V", "4", aiff_path, output_path],
                capture_output=True, check=True, timeout=30,
            )
            os.remove(aiff_path)
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            pass

    final = output_path.replace(".mp3", ".aiff")
    if aiff_path != final:
        os.rename(aiff_path, final)
    print("(no ffmpeg/lame, kept .aiff)", end=" ")
    return True


# ── Piper backend ─────────────────────────────────────────────────────

def check_piper():
    if shutil.which("piper"):
        return "piper"
    try:
        result = subprocess.run(
            [sys.executable, "-m", "piper", "--help"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return f"{sys.executable} -m piper"
    except Exception:
        pass
    return None


def download_voice_piper(voice_name):
    os.makedirs(VOICES_DIR, exist_ok=True)
    model_path = os.path.join(VOICES_DIR, f"{voice_name}.onnx")
    config_path = os.path.join(VOICES_DIR, f"{voice_name}.onnx.json")

    if os.path.exists(model_path) and os.path.getsize(model_path) > 1_000_000:
        return model_path

    print(f"Downloading voice model: {voice_name}...")
    try:
        from pathlib import Path
        from piper.download_voices import download_voice as piper_dl
        piper_dl(voice_name, Path(VOICES_DIR))
        return model_path
    except Exception as e:
        print(f"Download failed: {e}")
        print("Try downloading manually or use --engine say")
        sys.exit(1)


def generate_audio_piper(text, output_path, voice_model, piper_cmd):
    wav_path = output_path.replace(".mp3", ".wav")

    cmd_parts = piper_cmd.split()
    cmd_parts.extend(["--model", voice_model, "--output_file", wav_path])

    try:
        result = subprocess.run(
            cmd_parts, input=text,
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            print(f"Piper error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print("Piper timed out")
        return False

    if not os.path.exists(wav_path):
        return False

    if shutil.which("ffmpeg"):
        try:
            subprocess.run(
                ["ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame",
                 "-qscale:a", "4", output_path],
                capture_output=True, check=True, timeout=30,
            )
            os.remove(wav_path)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            os.rename(wav_path, output_path.replace(".mp3", ".wav"))
            print("(ffmpeg failed, saved as .wav)", end=" ")
    else:
        final = output_path.replace(".mp3", ".wav")
        if wav_path != final:
            os.rename(wav_path, final)
        print("(no ffmpeg, saved as .wav)", end=" ")

    return True


# ── Main ───────────────────────────────────────────────────────────────

def detect_engine():
    if platform.system() == "Darwin" and shutil.which("say"):
        return "say"
    if check_piper():
        return "piper"
    return None


def main():
    parser = argparse.ArgumentParser(description="Generate audio from narration scripts")
    parser.add_argument("slides_html", help="Path to slides.html")
    parser.add_argument("--engine", choices=["say", "piper"],
                        help="TTS engine (default: auto-detect)")
    parser.add_argument("--voice", type=str,
                        help="Voice name (default depends on engine)")
    parser.add_argument("--force", action="store_true", help="Regenerate all audio files")
    parser.add_argument("--only", type=str, help="Only generate specific files, comma-separated")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    args = parser.parse_args()

    engine = args.engine or detect_engine()
    if not engine and not args.dry_run:
        print("Error: No TTS engine found.")
        print("On macOS: 'say' should be available by default.")
        print("Otherwise: pip install piper-tts")
        sys.exit(1)

    if not args.voice:
        args.voice = DEFAULT_SAY_VOICE if engine == "say" else DEFAULT_PIPER_VOICE

    print(f"Engine: {engine} | Voice: {args.voice}")

    narration_dir = get_narration_dir(args.slides_html)
    scripts_dir = os.path.join(narration_dir, "scripts")
    audio_dir = os.path.join(narration_dir, "audio")

    if not os.path.exists(scripts_dir):
        print(f"Error: {scripts_dir} not found. Run steps 1 and 2 first.")
        sys.exit(1)

    os.makedirs(audio_dir, exist_ok=True)

    script_files = sorted(glob.glob(os.path.join(scripts_dir, "slide-*.txt")))

    if args.only:
        only_names = set(args.only.split(","))
        script_files = [f for f in script_files if os.path.basename(f) in only_names]

    to_generate = []
    for script_path in script_files:
        basename = os.path.splitext(os.path.basename(script_path))[0]
        audio_path = os.path.join(audio_dir, f"{basename}.mp3")

        if needs_regeneration(script_path, audio_path, args.force):
            text = read_narration(script_path)
            if text:
                to_generate.append((script_path, audio_path, text))

    if not to_generate:
        print("All audio files are up to date. Use --force to regenerate.")
        return

    print(f"Audio files to generate: {len(to_generate)}")

    if args.dry_run:
        for script_path, audio_path, _ in to_generate:
            print(f"  Would generate: {os.path.basename(audio_path)}")
        return

    piper_cmd = None
    voice_model = None
    if engine == "piper":
        piper_cmd = check_piper()
        voice_model = download_voice_piper(args.voice)

    for i, (script_path, audio_path, text) in enumerate(to_generate):
        label = os.path.basename(audio_path)
        word_count = len(text.split())
        print(f"[{i+1}/{len(to_generate)}] {label} ({word_count} words)...", end=" ", flush=True)

        if engine == "say":
            ok = generate_audio_say(text, audio_path, args.voice)
        else:
            ok = generate_audio_piper(text, audio_path, voice_model, piper_cmd)

        print("OK" if ok else "FAILED")

    generated = sum(1 for _, p, _ in to_generate
                    if any(os.path.exists(p.replace(".mp3", ext))
                           for ext in [".mp3", ".wav", ".aiff"]))
    print(f"\nDone. {generated}/{len(to_generate)} audio files saved to: {audio_dir}")


if __name__ == "__main__":
    main()
