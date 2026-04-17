# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

**Learn By Inventing** is an open educational resource published at GitHub Pages that teaches machine learning and CS algorithms through guided invention — learners derive algorithms themselves via stepwise exercises rather than reading explanations. The audience is motivated beginners to intermediate practitioners.

## Content Workflow

Each chapter is split across two locations:

| Path | Purpose |
|------|---------|
| `src/<chapter_name>/raw_prompt.txt` | Author's rough notes and outline |
| `src/<chapter_name>/polished_prompt.txt` | Refined LLM prompt — **use this over `raw_prompt.txt` if it exists** |
| `<chapter_name>/<topic>.ipynb` | Jupyter notebook learners work through (primary deliverable) |
| `<chapter_name>/<topic>.md` | Markdown chapters (used for conceptual/non-coding content) |

When generating or updating a chapter, read `src/<chapter_name>/polished_prompt.txt` first; fall back to `src/<chapter_name>/raw_prompt.txt` only if the polished version is absent.

## Notebook Content Guidelines

Notebooks are the learner-facing artifact. When creating or editing them:

- All content is **Markdown cells** with exercise prompts; learners write code in empty **Code cells** below each exercise.
- Never reveal solutions — guide learners to derive everything themselves.
- Make steps granular: one concrete, self-contained problem per exercise.
- Add helper/plotting utilities as provided Python code (since the learner shouldn't have to fight boilerplate).
- Exercises should build cumulatively toward a final ML concept (impurity → splitting → decision tree; gradient → MSE → linear regression).

## Current Chapters

- `learning_to_count/learning_to_count.md` — number systems, bases, arithmetic (conceptual/Markdown)
- `logarithm/logarithm.md` — logarithms stub
- `gradient_descent/linear_regression_gradient_descent.ipynb` — gradient descent → linear regression
- `decision_tree/decision_tree.ipynb` — impurity → splitting → decision tree fitting
- `convolutions/convolutions.ipynb` — images → convolution (computer vision)

## Building for GitHub Pages

```bash
bash build.sh             # export all notebooks + markdown to HTML
jupyter notebook          # open notebook server for editing
```

`build.sh` runs `jupyter nbconvert --to html` on each notebook and `pandoc` on markdown chapters, producing `.html` files alongside the source files. `index.html` at the repo root is the site landing page and links to these exported files.

No test suite or package manager is configured. Notebooks use standard scientific Python (numpy, matplotlib, pandas).
