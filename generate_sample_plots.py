"""Generate sample RL learning curve images for the reinforcement_learning chapter."""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "reinforcement_learning", "img")
os.makedirs(OUT_DIR, exist_ok=True)

np.random.seed(42)

def smooth(y, window=50):
    return [np.mean(y[max(0, i - window):i + 1]) for i in range(len(y))]

def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="#fafaf8")
    plt.close(fig)
    print(f"  wrote {path}")


# REINFORCE curve — noisy, gradual improvement
episodes = 1000
base = np.linspace(20, 350, episodes)
noise = np.random.normal(0, 60, episodes)
reinforce_scores = np.clip(base + noise, 10, 500)

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(reinforce_scores, alpha=0.25, color="#c8a96e", linewidth=0.8)
ax.plot(smooth(reinforce_scores), color="#c8a96e", linewidth=2, label="50-episode average")
ax.set_xlabel("Episode", fontsize=10)
ax.set_ylabel("Score", fontsize=10)
ax.set_title("REINFORCE — typical training curve", fontsize=11)
ax.legend(fontsize=9)
ax.set_facecolor("#fafaf8")
fig.patch.set_facecolor("#fafaf8")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
save(fig, "reinforce_curve.png")


# Actor-Critic curve — faster convergence, less variance
base_ac = np.linspace(20, 450, episodes)
noise_ac = np.random.normal(0, 35, episodes)
ac_scores = np.clip(base_ac + noise_ac, 10, 500)

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(ac_scores, alpha=0.25, color="#3a7a3a", linewidth=0.8)
ax.plot(smooth(ac_scores), color="#3a7a3a", linewidth=2, label="50-episode average")
ax.set_xlabel("Episode", fontsize=10)
ax.set_ylabel("Score", fontsize=10)
ax.set_title("Actor-Critic — typical training curve", fontsize=11)
ax.legend(fontsize=9)
ax.set_facecolor("#fafaf8")
fig.patch.set_facecolor("#fafaf8")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
save(fig, "actor_critic_curve.png")


# Random baseline — flat noisy line
random_scores = np.clip(np.random.normal(22, 8, episodes), 8, 60)

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(random_scores, alpha=0.25, color="#888", linewidth=0.8)
ax.plot(smooth(random_scores), color="#888", linewidth=2, label="50-episode average")
ax.set_xlabel("Episode", fontsize=10)
ax.set_ylabel("Score", fontsize=10)
ax.set_title("Random baseline — no learning", fontsize=11)
ax.legend(fontsize=9)
ax.set_facecolor("#fafaf8")
fig.patch.set_facecolor("#fafaf8")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
save(fig, "random_baseline.png")

print("Done.")
