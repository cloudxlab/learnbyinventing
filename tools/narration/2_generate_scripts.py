#!/usr/bin/env python3
"""Generate narration scripts for each slide+fragment using Claude CLI.

Usage:
    python 2_generate_scripts.py <path/to/slides.html> [--topic "Differentiation"]
                                                        [--force]
                                                        [--dry-run]

Reads:  <chapter>/narration/slides_data.json  (from step 1)
Writes: <chapter>/narration/scripts/slide-NN.txt
        <chapter>/narration/scripts/slide-NN-frag-K.txt

Each .txt file has a header comment with the on-screen content,
followed by the generated narration script.

Use --force to regenerate scripts that already exist.
Use --dry-run to see what would be generated without calling Claude.
"""

import sys
import os
import json
import subprocess
import argparse
import re


SYSTEM_PROMPT = """You are writing a voice-over narration script for an educational slide presentation.

Rules:
- The audience is a motivated 10th grader who knows Python and algebra but is new to calculus.
- Tone: warm, conversational, encouraging. Like a friendly teacher talking to one student.
- Keep each script 10-30 seconds when spoken (~25-75 words).
- NEVER read LaTeX or math notation literally (no "x squared", not "$x^2$"). Describe the math in natural words.
- NEVER say "click next" or "press space" — just say "let's move on" or similar if needed.
- Don't describe UI elements (tables, colors, formatting). Describe the IDEAS.
- For exercise slides, encourage the learner to try it themselves before moving on.
- For answer/check slides, be congratulatory and explain why the answer makes sense.
- For fragment reveals, be brief — the learner just clicked to see more.
- Output ONLY the narration text. No headers, no quotes, no stage directions.
- Use contractions naturally (you'll, that's, let's, we've).
- End naturally — don't trail off or say "and that's it".

Context about the presentation:
- Topic: {topic}
- This is a "learn by inventing" presentation where learners discover concepts themselves.
- The presentation follows a guided discovery approach — never reveal answers, guide to discover."""


def get_narration_dir(slides_path):
    chapter_dir = os.path.dirname(os.path.abspath(slides_path))
    return os.path.join(chapter_dir, "narration")


def script_filename(slide_index, frag_index=None):
    if frag_index is not None:
        return f"slide-{slide_index:02d}-frag-{frag_index}.txt"
    return f"slide-{slide_index:02d}.txt"


def build_prompt(slide, frag=None, topic="", slide_count=0):
    parts = []
    parts.append(f"Slide {slide['slide_index'] + 1} of {slide_count}.")
    parts.append(f"Base slide content: {slide['slide_text']}")

    if frag is not None:
        parts.append(f"\nThis is fragment {frag['fragment_index']} being revealed.")
        parts.append(f"Fragment content: {frag['text']}")
        parts.append("\nWrite a SHORT narration (1-3 sentences) for just this fragment reveal.")
    else:
        if slide["fragments"]:
            parts.append(f"\n(This slide has {len(slide['fragments'])} fragments that will reveal later — narrate only what's visible now, before any fragments.)")
        parts.append("\nWrite the narration for when the learner first lands on this slide.")

    return "\n".join(parts)


def call_claude(prompt, system_prompt):
    full_prompt = f"{system_prompt}\n\n---\n\n{prompt}"
    try:
        result = subprocess.run(
            ["claude", "-p", full_prompt, "--model", "sonnet"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            print(f"  Claude error: {result.stderr.strip()}", file=sys.stderr)
            return None
        return result.stdout.strip()
    except FileNotFoundError:
        print("Error: 'claude' CLI not found. Install it first.", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("  Claude timed out", file=sys.stderr)
        return None


def write_script(path, on_screen_text, narration):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# ON SCREEN:\n")
        for line in on_screen_text.split("\n"):
            f.write(f"# {line}\n")
        f.write(f"# ---\n")
        f.write(narration + "\n")


def read_existing_narration(path):
    """Read narration from existing script file (skip comment header)."""
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    narration_lines = []
    past_header = False
    for line in lines:
        if past_header:
            narration_lines.append(line)
        elif line.strip() == "# ---":
            past_header = True
    return "".join(narration_lines).strip() if narration_lines else None


def main():
    parser = argparse.ArgumentParser(description="Generate narration scripts using Claude CLI")
    parser.add_argument("slides_html", help="Path to slides.html")
    parser.add_argument("--topic", default="", help="Topic name for context (e.g. 'Differentiation')")
    parser.add_argument("--force", action="store_true", help="Regenerate existing scripts")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    parser.add_argument("--only", type=str, help="Only generate for specific slides, e.g. '3,5,7' or '3-7'")
    args = parser.parse_args()

    narration_dir = get_narration_dir(args.slides_html)
    data_path = os.path.join(narration_dir, "slides_data.json")

    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Run 1_extract_slides.py first.")
        sys.exit(1)

    with open(data_path, "r", encoding="utf-8") as f:
        slides = json.load(f)

    if not args.topic:
        dirname = os.path.basename(os.path.dirname(os.path.abspath(args.slides_html)))
        args.topic = dirname.replace("_", " ").title()

    scripts_dir = os.path.join(narration_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    only_indices = None
    if args.only:
        only_indices = set()
        for part in args.only.split(","):
            if "-" in part:
                lo, hi = part.split("-")
                only_indices.update(range(int(lo), int(hi) + 1))
            else:
                only_indices.add(int(part))

    system = SYSTEM_PROMPT.format(topic=args.topic)

    to_generate = []
    for slide in slides:
        idx = slide["slide_index"]
        if only_indices and idx not in only_indices:
            continue

        path = os.path.join(scripts_dir, script_filename(idx))
        if not args.force and read_existing_narration(path):
            pass
        else:
            to_generate.append(("slide", slide, None, path))

        for frag in slide["fragments"]:
            fpath = os.path.join(scripts_dir, script_filename(idx, frag["fragment_index"]))
            if not args.force and read_existing_narration(fpath):
                pass
            else:
                to_generate.append(("frag", slide, frag, fpath))

    if not to_generate:
        print("All scripts already exist. Use --force to regenerate.")
        return

    print(f"Topic: {args.topic}")
    print(f"Scripts to generate: {len(to_generate)}")

    if args.dry_run:
        for kind, slide, frag, path in to_generate:
            print(f"  Would generate: {os.path.basename(path)}")
        return

    for i, (kind, slide, frag, path) in enumerate(to_generate):
        label = os.path.basename(path)
        print(f"[{i+1}/{len(to_generate)}] Generating {label}...", end=" ", flush=True)

        prompt = build_prompt(slide, frag, args.topic, len(slides))
        narration = call_claude(prompt, system)

        if narration:
            on_screen = slide["slide_text"]
            if frag:
                on_screen += f"\n[Fragment {frag['fragment_index']}]: {frag['text']}"
            write_script(path, on_screen, narration)
            word_count = len(narration.split())
            print(f"OK ({word_count} words)")
        else:
            print("FAILED")

    print(f"\nDone. Scripts saved to: {scripts_dir}")
    print("Review and edit the scripts, then run 3_generate_audio.py")


if __name__ == "__main__":
    main()
