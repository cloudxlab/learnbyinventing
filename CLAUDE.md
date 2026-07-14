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
- `expressions_and_functions/expressions_and_functions.ipynb` — digit math, formulas as functions, distance formulas, line predict/fit, numerical derivative
- `if_else/if_else.ipynb` — branching, multi-way comparisons, 1D→2D axis decomposition (point-in-rectangle, rectangle intersection)
- `recursion/recursion.ipynb` — factorial, recursive multiply/power/divide, Euclid's HCF, Tower of Hanoi, Fibonacci + memoization
- `dictionaries/dictionaries.ipynb` — dict basics, word count, top-N words, anagram grouping, expense tracker, invert dict, group_by pattern
- `binary_search/binary_search.ipynb` — binary search on continuous ranges: sqrt, cube root, nth root, log₁₀, log base n; change of base formula
- `loops_and_array/loops_and_array.ipynb` — statistics (min/max/mean/SD/IQR), error metrics (RMSE/MAE/Huber), nearest neighbor (1-D→N-D→custom distance), polynomials, linear equation solver, probability/sampling (softmax/temperature), recursion on nested structures
- `sorting/sorting.ipynb` — bubble/insertion/merge/quick sort, in-place 0/1 partition, counting sort (billion ages), comparison counting → O(n²) vs O(n·log n), timing race
- `trees_and_heaps/trees_and_heaps.ipynb` — expression trees (recursive eval), BST insert/find/in-order/delete, balance problem, scheduler → min-heap (push/pop/heap sort), heapq
- `pattern_matching/pattern_matching.ipynb` — exact match → `?` wildcard → `*` via backtracking (glob), then `re`: dates, credit cards, emails, URL extraction from real server log
- `encoder_decoder/encoder_decoder.ipynb` — label-encoding pipeline from problem.pdf: parse CSV, email→int mapping persisted to file, black-box recommender, decoder, end-to-end verification
- `gradient_descent/linear_regression_gradient_descent.ipynb` — gradient descent → linear regression
- `decision_tree/decision_tree.ipynb` — impurity → splitting → decision tree fitting
- `convolutions/convolutions.ipynb` — images → convolution (computer vision)
- `information_theory/information_theory.ipynb` — prefix-free binary codes, variable-length encoding, avg bits per symbol, Huffman coding (greedy tree construction), Shannon entropy, generalized encode/decode

## Building for GitHub Pages

```bash
bash build.sh             # export all notebooks + markdown to HTML
jupyter notebook          # open notebook server for editing
```

`build.sh` runs `jupyter nbconvert --to html` on each notebook and `pandoc` on markdown chapters, producing `.html` files alongside the source files. `index.html` at the repo root is the site landing page and links to these exported files.

No test suite or package manager is configured. Notebooks use standard scientific Python (numpy, matplotlib, pandas).
