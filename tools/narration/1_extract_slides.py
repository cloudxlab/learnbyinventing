#!/usr/bin/env python3
"""Extract slide and fragment text from a Reveal.js slides.html into JSON.

Usage:
    python 1_extract_slides.py <path/to/slides.html> [output.json]

Output JSON structure:
    [
        {
            "slide_index": 0,
            "slide_text": "plain text visible on the slide",
            "fragments": [
                {"fragment_index": 0, "text": "text revealed by this fragment"},
                ...
            ]
        },
        ...
    ]
"""

import sys
import json
import re
from html.parser import HTMLParser


class SlideExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides = []
        self._section_depth = 0
        self._in_section = False
        self._current_slide = None
        self._current_fragment = None
        self._fragment_stack = []
        self._text_parts = []
        self._skip_tags = {"script", "style", "svg", "code", "pre"}
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag in self._skip_tags:
            self._skip_depth += 1
            return

        if self._skip_depth:
            return

        if tag == "section":
            self._section_depth += 1
            if self._section_depth == 1:
                self._current_slide = {
                    "slide_index": len(self.slides),
                    "slide_text": "",
                    "fragments": [],
                }
                self._current_fragment = None
                self._text_parts = []
                self._in_section = True

        frag_index = attrs_dict.get("data-fragment-index")
        classes = attrs_dict.get("class", "")

        if frag_index is not None and "fragment" in classes and self._current_slide is not None:
            self._flush_text()
            self._current_fragment = {
                "fragment_index": int(frag_index),
                "text": "",
            }
            self._fragment_stack.append(self._current_fragment)

    def handle_endtag(self, tag):
        if tag in self._skip_tags and self._skip_depth > 0:
            self._skip_depth -= 1
            return

        if self._skip_depth:
            return

        if tag == "section":
            if self._section_depth == 1 and self._current_slide is not None:
                self._flush_text()
                self.slides.append(self._current_slide)
                self._current_slide = None
                self._in_section = False
            self._section_depth = max(0, self._section_depth - 1)

    def handle_data(self, data):
        if self._skip_depth:
            return
        if self._in_section and self._current_slide is not None:
            text = data.strip()
            if text:
                self._text_parts.append(text)

    def _flush_text(self):
        if not self._text_parts:
            return
        joined = " ".join(self._text_parts)
        joined = re.sub(r"\s+", " ", joined).strip()

        if self._fragment_stack:
            self._fragment_stack[-1]["text"] += (" " + joined if self._fragment_stack[-1]["text"] else joined)
        elif self._current_slide is not None:
            self._current_slide["slide_text"] += (" " + joined if self._current_slide["slide_text"] else joined)

        self._text_parts = []

    def _finalize_fragment(self):
        if self._current_fragment and self._current_slide is not None:
            existing = [f for f in self._current_slide["fragments"]
                        if f["fragment_index"] == self._current_fragment["fragment_index"]]
            if existing:
                existing[0]["text"] += " " + self._current_fragment["text"]
            else:
                self._current_slide["fragments"].append(self._current_fragment)


def extract_slides_raw(html_content):
    """Extract slides using regex-based approach for more reliable results."""
    slides = []

    sections = re.split(r'<section[^>]*>', html_content)
    section_count = 0

    for i, section in enumerate(sections[1:], 1):
        end = section.find('</section>')
        if end == -1:
            continue
        section_content = section[:end]

        if re.search(r'<section', section_content):
            continue

        slide = {
            "slide_index": section_count,
            "slide_text": "",
            "fragments": [],
        }
        section_count += 1

        non_frag = section_content
        frag_pattern = r'<[^>]+class="[^"]*fragment[^"]*"[^>]*data-fragment-index="(\d+)"[^>]*>(.*?)(?=<[^>]+class="[^"]*fragment|$)'

        fragment_blocks = list(re.finditer(
            r'<(?:div|span|p|li|td|tr)[^>]*class="[^"]*fragment[^"]*"[^>]*data-fragment-index="(\d+)"[^>]*>',
            section_content
        ))

        frag_texts = {}
        for fb in fragment_blocks:
            frag_idx = int(fb.group(1))
            start = fb.end()
            remaining = section_content[start:]
            depth = 1
            pos = 0
            tag_name = re.match(r'<(\w+)', fb.group(0)).group(1)
            while depth > 0 and pos < len(remaining):
                open_match = re.search(rf'<{tag_name}[\s>]', remaining[pos:])
                close_match = re.search(rf'</{tag_name}>', remaining[pos:])
                if close_match is None:
                    break
                if open_match and open_match.start() < close_match.start():
                    depth += 1
                    pos += open_match.end()
                else:
                    depth -= 1
                    if depth == 0:
                        frag_content = remaining[:pos + close_match.start()]
                        text = strip_html(frag_content)
                        if frag_idx in frag_texts:
                            frag_texts[frag_idx] += " " + text
                        else:
                            frag_texts[frag_idx] = text
                    pos += close_match.end()

        for frag_idx in sorted(frag_texts.keys()):
            text = frag_texts[frag_idx].strip()
            if text:
                slide["fragments"].append({
                    "fragment_index": frag_idx,
                    "text": text,
                })

        for fb in reversed(fragment_blocks):
            tag_name = re.match(r'<(\w+)', fb.group(0)).group(1)
            start = fb.start()
            end_pos = section_content.find(f'</{tag_name}>', fb.end())
            if end_pos != -1:
                end_pos += len(f'</{tag_name}>')
                non_frag = non_frag[:start] + non_frag[end_pos:]

        base_text = strip_html(non_frag).strip()
        slide["slide_text"] = base_text

        slides.append(slide)

    return slides


def strip_html(html):
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<svg[^>]*>.*?</svg>', '', text, flags=re.DOTALL)
    text = re.sub(r'<pre[^>]*>.*?</pre>', ' [code block] ', text, flags=re.DOTALL)
    text = re.sub(r'<code[^>]*>.*?</code>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&[a-zA-Z]+;', ' ', text)
    text = re.sub(r'&#x?[0-9a-fA-F]+;', ' ', text)
    text = re.sub(r'\$[^$]+\$', '[math]', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <slides.html> [output.json]")
        sys.exit(1)

    slides_path = sys.argv[1]

    with open(slides_path, "r", encoding="utf-8") as f:
        html = f.read()

    slides = extract_slides_raw(html)

    slides = [s for s in slides if s["slide_text"].strip() or s["fragments"]]

    if len(sys.argv) >= 3:
        out_path = sys.argv[2]
    else:
        out_path = slides_path.replace("slides.html", "narration/slides_data.json")

    import os
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(slides, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(slides)} slides → {out_path}")
    total_frags = sum(len(s["fragments"]) for s in slides)
    print(f"Total fragments: {total_frags}")
    print(f"Total audio files needed: {len(slides) + total_frags}")


if __name__ == "__main__":
    main()
