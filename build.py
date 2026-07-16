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
import json
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
    blocks = data["blocks"]
    total_parts = sum(
        1 for b in blocks
        if b["type"] == "part" and b.get("number") is not None
    )
    glossary = data["chapter"].get("glossary", [])
    return template.render(
        chapter=data["chapter"],
        blocks=blocks,
        total_parts=total_parts,
        glossary=glossary,
    )


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


def _nb_cell(cell_type, source):
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": source.splitlines(True),
        **({"outputs": [], "execution_count": None} if cell_type == "code" else {}),
    }


def render_notebook(data, chapter_dir):
    chapter = data["chapter"]
    cells = [_nb_cell("markdown", f"# {chapter['title']}\n\n{chapter.get('intro', '')}")]

    for block in data["blocks"]:
        btype = block["type"]

        if btype == "part":
            num = block.get("number")
            prefix = f"Part {num}: " if num is not None else ""
            cells.append(_nb_cell("markdown", f"## {prefix}{block['title']}"))
            if block.get("intro"):
                cells.append(_nb_cell("markdown", block["intro"]))

        elif btype in ("text", "reveal"):
            cells.append(_nb_cell("markdown", block.get("text", "")))

        elif btype == "table":
            headers = block.get("headers", [])
            rows = block.get("rows", [])
            lines = [f"### {block.get('title', '')}", ""]
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join("---" for _ in headers) + " |")
            for row in rows:
                lines.append("| " + " | ".join(str(c) for c in row) + " |")
            cells.append(_nb_cell("markdown", "\n".join(lines)))

        elif btype == "exercise":
            kind = block.get("kind", "coding")
            title = block.get("title", "")
            part = block.get("part", "")
            number = block.get("number", "")
            desc = block.get("description", "")

            if kind == "mcq":
                label = f"Quick Check {part}.{number}"
                lines = [f"### {label} — {title}", "", desc]
                for opt in block.get("options", []):
                    lines.append(f"- **{opt['label']}.** {opt['text']}")
                cells.append(_nb_cell("markdown", "\n".join(lines)))
            else:
                label = "Exercise" if kind != "challenge" else ""
                if label:
                    label = f"{label} {part}.{number} — "
                cells.append(_nb_cell("markdown", f"### {label}{title}\n\n{desc}"))

            for pc in block.get("provided_code", []):
                if isinstance(pc, dict) and pc.get("code"):
                    cells.append(_nb_cell("code", pc["code"].rstrip()))

            if kind == "conceptual":
                for prompt in block.get("prompts", []):
                    cells.append(_nb_cell("markdown", f"**Your answer:** {prompt}"))

            if kind in ("coding", "challenge"):
                cells.append(_nb_cell("code", "# YOUR CODE HERE\n"))

            hints = block.get("hints", [])
            if hints:
                hint_parts = []
                for i, h in enumerate(hints, 1):
                    hint_parts.append(f"<details><summary>Hint {i}</summary>\n\n{h}\n</details>")
                cells.append(_nb_cell("markdown", "\n\n".join(hint_parts)))

            sol = block.get("solution")
            if sol:
                sol_parts = ["<details><summary>Solution</summary>\n"]
                if sol.get("text"):
                    sol_parts.append(sol["text"])
                if sol.get("code"):
                    sol_parts.append(f"```python\n{sol['code']}```")
                sol_parts.append("\n</details>")
                cells.append(_nb_cell("markdown", "\n".join(sol_parts)))

    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.10.0"},
        },
        "cells": cells,
    }
    out_path = chapter_dir / f"{chapter['id']}.ipynb"
    out_path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False))
    print(f"  wrote {out_path}")

    colab_url = chapter.get("colab_url")
    if not colab_url:
        colab_url = (
            f"https://colab.research.google.com/github/cloudxlab/learnbyinventing"
            f"/blob/main/{chapter['id']}/{chapter['id']}.ipynb"
        )
        chapter["colab_url"] = colab_url


def build_chapter(chapter_name, fmt="all", env=None):
    chapter_dir = REPO_ROOT / chapter_name
    data = load_chapter(chapter_dir)
    if env is None:
        env = create_jinja_env()

    if fmt in ("all", "html", "notebook"):
        render_notebook(data, chapter_dir)

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


def build_index(env):
    site_path = REPO_ROOT / "site.yaml"
    if not site_path.exists():
        print("  site.yaml not found — skipping index generation", file=sys.stderr)
        return
    with open(site_path) as f:
        data = yaml.safe_load(f)
    template = env.get_template("index.html.j2")
    html_out = template.render(**data)
    out_path = REPO_ROOT / "index.html"
    out_path.write_text(html_out)
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
    parser.add_argument("--format", choices=["all", "html", "slides", "notebook"], default="all")
    parser.add_argument("--check", action="store_true", help="Validate content files only")
    args = parser.parse_args()

    chapters = args.chapters or find_chapters()
    if not chapters:
        print("No chapters with content.yaml found.")
        return

    env = create_jinja_env()

    print("Building index.html...")
    build_index(env)

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
                build_chapter(ch, args.format, env)
        except Exception as e:
            print(f"  {ch}: ERROR: {e}", file=sys.stderr)
            errors += 1

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
