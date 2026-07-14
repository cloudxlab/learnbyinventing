# Learn By Inventing

Machine Learning &amp; Computer Science — derived, not memorized.

## Preface

I was watching a very popular video on Fourier transformation. I really liked it and understood every step shown in the video but after a few days I forgot everything. I didn't internalize it.

This is when I realized all I wanted was a set of simple stepwise problems that I can do so that I can derive the algorithms by myself — and this way I will never forget.

After teaching about 20 courses on machine learning, I have evolved these exercises.

**Do not read this book. Work with it.** Keep pen & paper and a coding environment handy. Each chapter gives you a sequence of exercises that lead you to re-invent the algorithm yourself.

## Chapters

| # | Chapter | Topics |
|---|---------|--------|
| 1 | [Learning to Count](learning_to_count/learning_to_count.md) | Number systems, bases, arithmetic |
| 2 | [Expressions & Functions](expressions_and_functions/expressions_and_functions.ipynb) | Digit math, formulas, distance, line fitting, numerical derivative |
| 3 | [If-Else](if_else/if_else.ipynb) | Branching, multi-way comparisons, 2D geometry (point-in-rectangle, intersection) |
| 4 | [Recursion](recursion/recursion.ipynb) | Factorial, multiply/power/divide, Euclid's HCF, Tower of Hanoi, Fibonacci + memoization |
| 5 | [Dictionaries](dictionaries/dictionaries.ipynb) | Word counts, top-N, anagram grouping, expense tracker, group-by pattern |
| 6 | [Binary Search & Approximations](binary_search/binary_search.ipynb) | Bisection on continuous ranges: sqrt, nth root, log base n, change of base |
| 7 | [Loops and Arrays](loops_and_array/loops_and_array.ipynb) | Stats (mean/SD/IQR), error metrics (RMSE/MAE/Huber), nearest neighbor, polynomials, softmax |
| 8 | [Sorting](sorting/sorting.ipynb) | Bubble → insertion → merge → quick → counting sort; O(n²) vs O(n·log n) measured |
| 9 | [Trees & Heaps](trees_and_heaps/trees_and_heaps.ipynb) | Expression trees, BST insert/find/delete, scheduler → min-heap |
| 10 | [Pattern Matching](pattern_matching/pattern_matching.ipynb) | Wildcard matcher via backtracking → regex → mining a real server log |
| 11 | [Backtracking](backtracking/backtracking.ipynb) | Systematic enumeration → permutations → validity checks → Sudoku solver |
| 12 | [The Encoder-Decoder Pipeline](encoder_decoder/encoder_decoder.ipynb) | Label encoding, file-based pipeline around a black-box recommender |
| 13 | [Classes & Objects](classes_and_objects/classes_and_objects.ipynb) | Data + behavior, the fit/predict API, inheritance, decision tree as objects, serialization |
| 14 | [The Ancient Secrets of Prediction](secrets_of_prediction/secrets_of_prediction.ipynb) | Vectors & dot product, prediction = solving equations, polynomial fitting, least squares |
| 15 | [Linear Regression & Gradient Descent](gradient_descent/linear_regression_gradient_descent.ipynb) | Gradient descent → linear regression |
| 16 | [Decision Trees](decision_tree/decision_tree.ipynb) | Impurity → splitting → decision tree fitting |
| 17 | [Random Forests](random_forest/random_forest.ipynb) | Variance impurity → regression trees → bootstrap + feature randomness → forest |
| 18 | [Recommender Systems](recommender/recommender.ipynb) | Real ratings data → scaling → cosine similarity → uMᵀuM → recommendations → MapReduce |
| 19 | [Neural Networks](neural_networks/neural_networks.ipynb) | Neurons → saturation lesson → computation graphs → income-tax problem → ReLU |
| 20 | [Convolutions](convolutions/convolutions.ipynb) | Images → convolution (computer vision) |
| 21 | [Information Theory & Compression](information_theory/information_theory.ipynb) | Prefix-free codes → variable-length encoding → Huffman coding → Shannon entropy |
| 22 | [RAG & Agentic AI](rag_and_agents/rag_and_agents.md) | Knowledge gap → search → inventing RAG → tool use → inventing agents |
| 23 | [Capstone Projects](projects/projects.md) | Open-ended end-to-end projects: EDA, housing pipeline, Keras, time series, NLP, GANs, RL |

## How to Use

**Self-paced:** Open any notebook in Jupyter or Colab and work top to bottom. Each blank code cell is yours to fill. Allow 2–4 hours per chapter.

**Classroom / workshop:** One chapter per ~90-minute session. Instructor projects the notebook; learners work in parallel. Natural pause points between exercises.

**ML onboarding:** Chapters 13–23 form a self-contained ML foundations sequence for engineers who can code but are new to ML.

## Running Locally

```bash
jupyter notebook          # open notebook server for editing
bash build.sh             # export all notebooks + markdown to HTML for GitHub Pages
```

## Adding Chapters

1. Write rough notes in `src/<chapter_name>/raw_prompt.txt`
2. Create `<chapter_name>/<topic>.ipynb` following LBI pedagogy:
   - Markdown cells with exercise prompts (never reveal solutions)
   - Empty code cells below each exercise for the learner
   - Exercises build cumulatively toward the final concept
3. Add to `build.sh` and `index.html`
