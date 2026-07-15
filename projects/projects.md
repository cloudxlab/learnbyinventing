# Capstone Projects

Everything so far has been guided: small exercises, tests that tell you when
you're right. Real machine-learning work isn't like that — you get a goal, a
pile of data, and no asserts. These projects are that experience. Each one is
open-ended by design; there is no answer key.

**Prerequisites.** The core chapters (especially Gradient Descent, Decision
Trees, Random Forests, Recommender Systems, and Neural Networks). Several
projects use libraries the book deliberately avoided — `scikit-learn`,
`TensorFlow`/`Keras` — because at project scale you should stand on the
industrial versions of the algorithms you have already invented from scratch.

**How to work.** For every project, write your plan as pseudocode *before*
writing code. Then try the reverse experiment: describe the plan to an LLM and
see whether it produces equivalent pseudocode from your prompt — the gaps
between its version and yours are usually the parts of your plan that were
vague.

---

## Project 1 — Explore a Dataset You Care About

Find a dataset that genuinely interests you on
[Kaggle](https://www.kaggle.com/datasets), download it, and load it into a
pandas `DataFrame`. Produce a handful of visualizations that show what is
interesting in the data: distributions, correlations, a few scatter or bar
plots. The deliverable is not the charts — it's one surprising thing you can
say about the data that you couldn't before.

---

## Project 2 — California Housing: an End-to-End ML Project

Welcome to Machine Learning Housing Corp. Your task: predict median house
values in Californian districts from district-level features. The classic
1990 California census dataset is a natural choice (districts with median
income, housing median age, total rooms, population, location), but any
comparable housing dataset works.

The full pipeline expected in a solution:

1. **Split the data** — `valid, test, train = 10% / 20% / 70%`, using
   *stratified* sampling (stratify on a feature that matters for
   representativeness, e.g. median-income bucket).
2. **Descriptive and visual analysis** of the training set. Decide whether to
   drop duplicate or redundant columns.
3. **Convert non-numeric values to numbers.** This is where most of the craft
   lives:
   - Categorical columns (e.g. ocean proximity) → one-hot encoding.
   - Dates → month/year/day/hour/minute, seconds-since-epoch, is-holiday,
     is-weekend, or a season one-hot.
   - Time of day → morning/noon/evening/night buckets, or a cyclic encoding
     like `sin(time * 360 / 24)`.
   - Location → distance to nearest landmark (coastline, railway station),
     city one-hot, or derived weather features.
   - Free text → word-count/TF-IDF encoding, or LLM-based embeddings.
4. **Impute missing values** — drop the row/column, or fill with 0 / mean /
   median / a model — and watch for NaNs that the imputation itself
   introduces.
5. **Normalize** (you know why, after the saturation lesson in the Neural
   Networks chapter).
6. **Train and compare several models** — `SGDRegressor`, an SVM regressor,
   `RandomForestRegressor`, and a small neural network — fitting on
   `X_train, y_train` and evaluating on `X_valid, y_valid`.
7. **Tune** the hyperparameters of the best performer(s).
8. **Ensemble** — if several models perform comparably, average their
   predictions (you saw why averaging works in the Random Forests chapter).
9. **Predict** on the held-out test set exactly once, at the end.

*Unrelated bonus:* work out how HTTPS actually works — what makes it secure,
and what roles hashing and encryption play in the handshake. (Your hashing
invention from the Dictionaries chapter is a surprisingly good starting
point.)

---

## Project 3 — Train Models on Kaggle Datasets with Keras

Pick one Kaggle dataset suited to **regression** and one suited to
**classification**. Build and train a model for each using TensorFlow/Keras's
`Sequential` API. You already know what every layer is doing — `Dense` is
your `fit_net`, the activations are your `sigmoid`/`relu`, the optimizer is
your gradient-descent loop with better footwork.

---

## Project 4 — Stock Price Prediction (Time Series)

Build a model that predicts a company's next closing price from its previous
20 closing prices, using historical daily data (date + close is enough).

1. **Sliding-window transform:** `X[i] = [Close[i], …, Close[i+19]]` →
   `y[i] = Close[i+20]`. With `n` prices you get `n − 20` samples
   (`X: (n−20, 20)`, `y: (n−20,)`).
2. **Time-ordered split** — earlier data for training, later for testing
   (80/20 is reasonable). *Never shuffle.* Ask yourself why before reading
   on: shuffling would let the model train on the future and be tested on
   the past.
3. **Scaling:** fit the scaler on training data only, then apply it to test
   data — fitting on the full dataset leaks future information into training.
4. **Model:** a feed-forward network, e.g. `Dense(64, relu) → Dense(32, relu)
   → Dense(16, relu) → Dense(1, linear)`. No sigmoid/softmax on the output —
   this is regression.
5. **Training:** minimize MSE or MAE with Adam; `epochs=50, batch_size=32,
   validation_split=0.1` is a fair start.
6. **Evaluation:** report at least two of MAE/MSE/RMSE/MAPE on the test set,
   and plot actual vs. predicted prices.
7. **Answer in writing:** What are the shapes of `X` and `y`? Why must the
   split not be shuffled? Which loss did you pick and why? Do the predictions
   track the trend? Is predicting prices from the last 20 prices reliable in
   real life?
8. **Extensions:** use adjusted close; predict percentage return instead of
   price; compare window sizes (5/10/20/50/100); add open/high/low/volume
   features; compare against the naive baseline "tomorrow = today" (it is
   embarrassingly hard to beat); try an LSTM or a 1-D convolution (you know
   what a convolution is now).

---

## Project 5 — NLP: Embeddings and Character-Level Prediction

**5a.** Using the [20 Newsgroups dataset](https://scikit-learn.org/stable/datasets/real_world.html#the-20-newsgroups-text-dataset)
(~20,000 posts across 20 topics, bundled with scikit-learn), build an
embeddings-based representation of the posts and measure how well a simple
classifier on top of it predicts the topic.

**5b — predict the next character.** Take a plain-text corpus (the works of
Shakespeare are traditional):

1. Break it into sliding windows: 50 characters (`X`) → the next character
   (`y`) — the same transform as the stock project, applied to text.
2. One-hot encode each character in `X` (one dimension per character in the
   vocabulary).
3. Turn `y` into integer class ids — the task is now multiclass
   classification: *which character comes next?*
4. Train a network on the mapping.

Sit with what you built in 5b: a next-token predictor. Scaled up — tokens
instead of characters, attention instead of dense layers, the internet
instead of Shakespeare — this is a language model.

---

## Project 6 — Autoencoders and GANs on Faces

**6a.** An autoencoder compresses an image to a small embedding and
reconstructs it. Use one to build semantic manipulations of human faces: take
the embeddings of two faces, interpolate or arithmetically combine them, and
decode the result.

**6b.** Using a GAN — a generator and a discriminator competing — build a
model that generates a human face from random noise. For what's achievable,
see [thispersondoesnotexist.com](https://this-person-does-not-exist.com/en).

---

## Project 7 — Reinforcement Learning: Write a Policy

Take a reinforcement-learning environment that can be reset and stepped,
returning a reward each step (Gymnasium's `CartPole-v1` is the classic), and
a harness `test_policy(policy)` that runs your policy over many episodes and
reports `mean(rewards)`.

Write a `policy` function — mapping the observed state to an action — that
maximizes the mean reward. Try at least two strategies (a hand-coded
heuristic vs. something learned) and compare.

---

## Project 8 — Read a Real GPT

Read through [cloudxlab/GPT-from-scratch](https://github.com/cloudxlab/GPT-from-scratch/tree/master)
and trace how a minimal GPT-style model is implemented end to end:
tokenization, embeddings, attention blocks, and the training loop. Your goal
is to connect each piece to something you built in this book — the attention
scores are the recommender chapter's `uM.T @ uM`, the training loop is your
`fit_net`, the loss landscape is the one you descended in Chapter 15.

---

<footer>
Source on <a href="https://github.com/cloudxlab/learnbyinventing">GitHub</a> &middot; <a href="../index.html">Back to all chapters</a>

&copy; 2026 <a href="https://cloudxlab.com">CloudxLab</a>. All rights reserved.
</footer>
