#!/usr/bin/env python3
"""Incremental build for narration pipeline.

Runs all three steps, only regenerating what has changed:
  1. Extract slides  — only if slides.html is newer than slides_data.json
  2. Generate scripts — only for slides whose JSON data is newer than their script
  3. Generate audio   — only for scripts newer than their audio file

Usage:
    python tools/narration/build_narration.py <chapter>/slides.html [--topic "Topic"]
                                                                     [--voice am_michael]
                                                                     [--engine kokoro|say|piper]
                                                                     [--force]

    # Rebuild everything from scratch:
    python tools/narration/build_narration.py <chapter>/slides.html --force

    # Only rebuild audio (e.g. after editing scripts):
    python tools/narration/build_narration.py <chapter>/slides.html --only audio
"""

import sys
import os
import json
import subprocess
import argparse

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))


def needs_rebuild(source, target):
    """True if target doesn't exist or source is newer."""
    if not os.path.exists(target):
        return True
    return os.path.getmtime(source) > os.path.getmtime(target)


def run_step(cmd, label):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}\n")
    result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        print(f"\nError: {label} failed (exit code {result.returncode})")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Incremental narration build")
    parser.add_argument("slides_html", help="Path to slides.html")
    parser.add_argument("--topic", type=str, help="Topic name for script generation")
    parser.add_argument("--voice", type=str, help="Voice name for audio generation")
    parser.add_argument("--engine", type=str, help="TTS engine: kokoro, say, or piper")
    parser.add_argument("--force", action="store_true", help="Force full rebuild")
    parser.add_argument("--only", choices=["extract", "scripts", "audio"],
                        help="Only run a specific step")
    args = parser.parse_args()

    slides_path = os.path.abspath(args.slides_html)
    if not os.path.exists(slides_path):
        print(f"Error: {slides_path} not found")
        sys.exit(1)

    chapter_dir = os.path.dirname(slides_path)
    narration_dir = os.path.join(chapter_dir, "narration")
    data_path = os.path.join(narration_dir, "slides_data.json")
    scripts_dir = os.path.join(narration_dir, "scripts")
    audio_dir = os.path.join(narration_dir, "audio")

    step1 = os.path.join(TOOLS_DIR, "1_extract_slides.py")
    step2 = os.path.join(TOOLS_DIR, "2_generate_scripts.py")
    step3 = os.path.join(TOOLS_DIR, "3_generate_audio.py")

    skip_extract = args.only and args.only != "extract"
    skip_scripts = args.only and args.only != "scripts"
    skip_audio = args.only and args.only != "audio"

    # ── Step 1: Extract slides ─────────────────────────────────────────

    if not skip_extract:
        if args.force or needs_rebuild(slides_path, data_path):
            run_step(
                [sys.executable, step1, slides_path],
                "Step 1: Extracting slide data"
            )
        else:
            print("\nStep 1: slides_data.json is up to date (skipping)")

    # ── Step 2: Generate scripts ───────────────────────────────────────

    if not skip_scripts:
        if not os.path.exists(data_path):
            print("Error: slides_data.json not found. Run step 1 first.")
            sys.exit(1)

        # Check which slides need script regeneration
        with open(data_path) as f:
            slides = json.load(f)

        stale_indices = []
        for slide in slides:
            idx = slide["slide_index"]
            script_path = os.path.join(scripts_dir, f"slide-{idx:02d}.txt")
            if args.force or needs_rebuild(data_path, script_path):
                stale_indices.append(idx)
            for frag in slide.get("fragments", []):
                frag_script = os.path.join(scripts_dir,
                    f"slide-{idx:02d}-frag-{frag['fragment_index']}.txt")
                if args.force or needs_rebuild(data_path, frag_script):
                    if idx not in stale_indices:
                        stale_indices.append(idx)

        if stale_indices:
            cmd = [sys.executable, step2, slides_path]
            if args.topic:
                cmd.extend(["--topic", args.topic])
            if not args.force and len(stale_indices) < len(slides):
                cmd.extend(["--only", ",".join(str(i) for i in sorted(stale_indices))])
            if args.force:
                cmd.append("--force")
            run_step(cmd, f"Step 2: Generating scripts ({len(stale_indices)} slides)")
        else:
            print("\nStep 2: All scripts are up to date (skipping)")

    # ── Step 3: Generate audio ─────────────────────────────────────────

    if not skip_audio:
        cmd = [sys.executable, step3, slides_path]
        if args.engine:
            cmd.extend(["--engine", args.engine])
        if args.voice:
            cmd.extend(["--voice", args.voice])
        if args.force:
            cmd.append("--force")
        # Step 3 already has built-in timestamp checking
        run_step(cmd, "Step 3: Generating audio")

    # ── Copy player ────────────────────────────────────────────────────

    player_src = os.path.join(TOOLS_DIR, "narration-player.js")
    player_dst = os.path.join(chapter_dir, "narration-player.js")
    if needs_rebuild(player_src, player_dst):
        import shutil
        shutil.copy2(player_src, player_dst)
        print(f"\nCopied narration-player.js → {player_dst}")

    print(f"\nBuild complete. Serve and test:")
    print(f"  cd {chapter_dir} && python3 -m http.server 8000")


if __name__ == "__main__":
    main()
