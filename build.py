#!/usr/bin/env python3
"""Build LearnByInventing chapters from content.yaml to HTML and reveal.js slides.

Usage:
    python build.py                      # build all chapters with content.yaml
    python build.py binary_search        # build one chapter
    python build.py --format slides      # slides only
    python build.py --check              # validate YAML without generating
"""

import argparse
import html
import sys
from pathlib import Path

import markdown2
import yaml
from jinja2 import Environment, FileSystemLoader

REPO_ROOT = Path(__file__).parent
TEMPLATES_DIR = REPO_ROOT / "templates"

MARKDOWN_EXTRAS = ["fenced-code-blocks", "tables", "cuddled-lists", "code-friendly"]


def md(text):
    if not text:
        return ""
    return markdown2.markdown(str(text), extras=MARKDOWN_EXTRAS)


def md_inline(text):
    if not text:
        return ""
    result = md(text).strip()
    if result.startswith("<p>") and result.endswith("</p>"):
        result = result[3:-4]
    return result


def escape_html(text):
    if not text:
        return ""
    return html.escape(str(text), quote=False)


def load_chapter(chapter_dir):
    content_path = chapter_dir / "content.yaml"
    if not content_path.exists():
        raise FileNotFoundError(f"{content_path} not found")
    with open(content_path) as f:
        data = yaml.safe_load(f)
    validate_chapter(data, content_path)
    return data


def validate_chapter(data, path):
    if "chapter" not in data:
        raise ValueError(f"{path}: missing 'chapter' key")
    chapter = data["chapter"]
    for field in ("id", "title"):
        if field not in chapter:
            raise ValueError(f"{path}: chapter missing '{field}'")
    if "blocks" not in data:
        raise ValueError(f"{path}: missing 'blocks' key")
    for i, block in enumerate(data["blocks"]):
        if "type" not in block:
            raise ValueError(f"{path}: block {i} missing 'type'")


def create_jinja_env():
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
        keep_trailing_newline=True,
    )
    env.filters["md"] = md
    env.filters["md_inline"] = md_inline
    env.filters["escape_html"] = escape_html
    return env


def render_html(env, data):
    template = env.get_template("chapter.html.j2")
    return template.render(chapter=data["chapter"], blocks=data["blocks"])


def render_slides(env, data):
    template = env.get_template("slides.html.j2")
    slides = []
    current_part = None
    for block in data["blocks"]:
        if block["type"] == "part":
            if current_part:
                slides.append(current_part)
            current_part = {"part": block, "blocks": []}
        elif current_part is not None:
            current_part["blocks"].append(block)
        else:
            if not slides and current_part is None:
                current_part = {"part": None, "blocks": [block]}
    if current_part:
        slides.append(current_part)
    return template.render(chapter=data["chapter"], slides=slides)


def build_chapter(chapter_name, fmt="all"):
    chapter_dir = REPO_ROOT / chapter_name
    data = load_chapter(chapter_dir)
    env = create_jinja_env()

    if fmt in ("all", "html"):
        html_out = render_html(env, data)
        out_path = chapter_dir / "index.html"
        out_path.write_text(html_out)
        print(f"  wrote {out_path}")

    if fmt in ("all", "slides"):
        slides_out = render_slides(env, data)
        out_path = chapter_dir / "slides.html"
        out_path.write_text(slides_out)
        print(f"  wrote {out_path}")


def find_chapters():
    chapters = []
    for path in sorted(REPO_ROOT.iterdir()):
        if path.is_dir() and (path / "content.yaml").exists():
            chapters.append(path.name)
    return chapters


def main():
    parser = argparse.ArgumentParser(description="Build LearnByInventing chapters")
    parser.add_argument("chapters", nargs="*", help="Chapter name(s) (builds all if omitted)")
    parser.add_argument("--format", choices=["all", "html", "slides"], default="all")
    parser.add_argument("--check", action="store_true", help="Validate content files only")
    args = parser.parse_args()

    chapters = args.chapters or find_chapters()
    if not chapters:
        print("No chapters with content.yaml found.")
        return

    errors = 0
    for ch in chapters:
        chapter_dir = REPO_ROOT / ch
        if not (chapter_dir / "content.yaml").exists():
            print(f"  {ch}: content.yaml not found", file=sys.stderr)
            errors += 1
            continue
        try:
            if args.check:
                load_chapter(chapter_dir)
                print(f"  {ch}: OK")
            else:
                print(f"Building {ch}...")
                build_chapter(ch, args.format)
        except Exception as e:
            print(f"  {ch}: ERROR: {e}", file=sys.stderr)
            errors += 1

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
