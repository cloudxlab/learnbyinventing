# Practice Problems

The main chapters of this book teach by guided invention: you derive each
algorithm yourself, one small step at a time, before the concept is named.
These 47 exercises are a different mode — **drill practice**. Each notebook
gives you one concrete formula or algorithm and asks you to implement it in
Python from scratch. There is no arc or narrative; every notebook stands alone.

**When to use these.** Work through the five groups in order — Expressions,
If/Else, Loops, Functions, Recursion — as you finish the corresponding LBI
chapter, or as warm-ups before the ML chapters. The ML themes (gradient
descent, entropy, neural networks) preview concepts you will invent in full
later; if a problem feels too hard, come back after the relevant chapter.

**How each notebook works.** Read the problem statement. Fill in the starter
cell wherever you see `# TODO`. Run the test cell at the bottom — if it
prints `All tests passed!`, you're done.

---

## 01 — Expressions

*Best done after:* Chapter 3 (Expressions & Functions)

Each problem is a single Python expression. No loops, no conditionals — just
arithmetic, `math.exp`, and one or two variables.

| # | Difficulty | Concept | Open in Colab |
|---|---|---|---|
| 1 | Easy | Mean of three numbers | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/01_expressions/01_easy_mean_of_three.ipynb) |
| 2 | Easy | Z-score for one value | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/01_expressions/02_easy_zscore_single.ipynb) |
| 3 | Easy | Min-max scale one value | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/01_expressions/03_easy_minmax_single.ipynb) |
| 4 | Medium | Euclidean distance (2-D) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/01_expressions/04_medium_euclidean_2d.ipynb) |
| 5 | Medium | Probability of two independent events | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/01_expressions/05_medium_independent_prob.ipynb) |
| 6 | Medium | Squared error for one prediction | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/01_expressions/06_medium_squared_error_single.ipynb) |
| 7 | Medium | Sigmoid activation function | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/01_expressions/07_medium_sigmoid_single.ipynb) |
| 8 | Hard | One term of a covariance sum | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/01_expressions/08_hard_covariance_term.ipynb) |
| 9 | Hard | One gradient descent update step | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/01_expressions/09_hard_gradient_step_single.ipynb) |

---

## 02 — If / Else

*Best done after:* Chapter 4 (If/Else)

Each problem requires a conditional choice — `"A"` vs `"B"`, `"pure"` vs
`"mixed"`, `"train"` vs `"val"` vs `"test"`. Threshold-based decisions are
everywhere in ML.

| # | Difficulty | Concept | Open in Colab |
|---|---|---|---|
| 1 | Easy | Flag a single outlier by z-score | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/02_if_else/01_easy_outlier_flag.ipynb) |
| 2 | Easy | Classify a probability as likely or unlikely | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/02_if_else/02_easy_probability_likely.ipynb) |
| 3 | Easy | Turn a sigmoid output into a class label | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/02_if_else/03_easy_sigmoid_to_class.ipynb) |
| 4 | Medium | Classify one prediction as TP / FP / TN / FN | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/02_if_else/04_medium_confusion_single.ipynb) |
| 5 | Medium | Assign a point to its nearest centroid | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/02_if_else/05_medium_nearest_centroid.ipynb) |
| 6 | Medium | Classify correlation strength and direction | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/02_if_else/06_medium_correlation_strength.ipynb) |
| 7 | Medium | Min-max normalize without dividing by zero | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/02_if_else/07_medium_safe_normalize.ipynb) |
| 8 | Hard | Assign a sample to train / val / test by position | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/02_if_else/08_hard_split_assignment.ipynb) |
| 9 | Hard | Decide whether a tree node is pure | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/02_if_else/09_hard_pure_node.ipynb) |

---

## 03 — Loops

*Best done after:* Chapter 8 (Loops & Arrays)

Each problem asks you to accumulate a result by looping over a list. The
themes run from basic statistics (mean, std dev) up to gradient descent and
entropy — you will invent the full versions of those ideas in Chapters 15 and
21.

| # | Difficulty | Concept | Open in Colab |
|---|---|---|---|
| 1 | Easy | Compute the mean with a loop | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/03_loops/01_easy_mean_via_loop.ipynb) |
| 2 | Easy | Sum of squared deviations | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/03_loops/02_easy_sum_sq_dev_loop.ipynb) |
| 3 | Medium | Compute the standard deviation | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/03_loops/03_medium_std_dev_loop.ipynb) |
| 4 | Medium | Find all outliers in a dataset | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/03_loops/04_medium_find_outliers_loop.ipynb) |
| 5 | Medium | Min-max normalize an entire list | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/03_loops/05_medium_minmax_list_loop.ipynb) |
| 6 | Medium | Distances from a query point to a training set | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/03_loops/06_medium_knn_distances_loop.ipynb) |
| 7 | Hard | Build a confusion matrix over a dataset | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/03_loops/07_hard_confusion_matrix_loop.ipynb) |
| 8 | Hard | Compute covariance between two lists | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/03_loops/08_hard_covariance_loop.ipynb) |
| 9 | Hard | Run several iterations of gradient descent | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/03_loops/09_hard_gradient_descent_loop.ipynb) |
| 10 | Hard | Compute the entropy of a list of labels | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/03_loops/10_hard_entropy_loop.ipynb) |

---

## 04 — Functions

*Best done after:* Chapter 3 (Expressions & Functions) and Chapter 8 (Loops & Arrays)

These problems ask you to compose smaller functions into larger ones — the
same building-block pattern the book uses throughout. The capstone notebooks
(regression pipeline, entropy + information gain, sigmoid + perceptron) are
mini-versions of full LBI chapters.

| # | Difficulty | Concept | Open in Colab |
|---|---|---|---|
| 1 | Easy | `mean()` function | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/04_functions/01_easy_mean_function.ipynb) |
| 2 | Easy | `variance()` using `mean()` | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/04_functions/02_easy_variance_function.ipynb) |
| 3 | Easy | `std_dev()` using `variance()` | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/04_functions/03_easy_std_dev_function.ipynb) |
| 4 | Medium | `find_outliers()` from stats functions | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/04_functions/04_medium_find_outliers_function.ipynb) |
| 5 | Medium | Simple k-nearest-neighbors classifier | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/04_functions/05_medium_knn_predict_function.ipynb) |
| 6 | Medium | `precision()`, `recall()`, and `f1_score()` | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/04_functions/06_medium_classification_metrics_functions.ipynb) |
| 7 | Medium | `correlation()` from covariance and std dev | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/04_functions/07_medium_correlation_function.ipynb) |
| 8 | Hard | Linear regression pipeline (`predict`, `mse`, `gradient_descent_fit`) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/04_functions/08_hard_regression_pipeline_functions.ipynb) |
| 9 | Hard | `entropy()` and `information_gain()` | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/04_functions/09_hard_entropy_information_gain_functions.ipynb) |
| 10 | Hard | `sigmoid()` and `perceptron()` | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/04_functions/10_hard_neural_net_functions.ipynb) |

---

## 05 — Recursion

*Best done after:* Chapter 5 (Recursion)

Each problem has a natural recursive structure: a base case and a case that
reduces to a smaller version of itself. The ML themes (learning-rate decay,
tree depth) appear in the Gradient Descent and Decision Tree chapters.

| # | Difficulty | Concept | Open in Colab |
|---|---|---|---|
| 1 | Easy | Recursive sum of a list | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/05_recursion/01_easy_recursive_sum.ipynb) |
| 2 | Easy | Recursive product of a list (geometric mean) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/05_recursion/02_easy_recursive_product.ipynb) |
| 3 | Medium | Recursive sum of squared deviations | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/05_recursion/03_medium_recursive_sum_sq_dev.ipynb) |
| 4 | Medium | Recursive factorial (for counting outcomes) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/05_recursion/04_medium_recursive_factorial.ipynb) |
| 5 | Medium | Binomial coefficient via Pascal's rule | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/05_recursion/05_medium_recursive_n_choose_k.ipynb) |
| 6 | Medium | Binary search over sorted distances | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/05_recursion/06_medium_recursive_binary_search.ipynb) |
| 7 | Hard | Recursive merge sort (to find the median) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/05_recursion/07_hard_recursive_merge_sort.ipynb) |
| 8 | Hard | Recursive learning-rate decay schedule | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/05_recursion/08_hard_recursive_lr_decay.ipynb) |
| 9 | Hard | Recursive depth of a decision tree | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cloudxlab/learnbyinventing/blob/main/practice_problems/05_recursion/09_hard_recursive_tree_depth.ipynb) |

---

<footer>
Source on <a href="https://github.com/cloudxlab/learnbyinventing">GitHub</a> &middot; <a href="../index.html">Back to all chapters</a>

&copy; 2026 <a href="https://cloudxlab.com">CloudxLab</a>. All rights reserved.
</footer>
