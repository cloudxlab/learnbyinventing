#!/usr/bin/env python3
"""Test runner for neural_networks exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_1_1_step_function():
    from exercises.ex_1_1_step_function import step_function
    assert step_function(3) == 1
    assert step_function(0) == 1
    assert step_function(-0.5) == 0

def test_ex_1_2_sigmoid():
    from exercises.ex_1_2_sigmoid import sigmoid
    assert sigmoid(0) == 0.5
    assert sigmoid(100) > 0.999
    assert sigmoid(-100) < 0.001
    assert abs(sigmoid(2) - 0.8808) < 1e-3

    zs = np.linspace(-8, 8, 100)
    plt.plot(zs, [step_function(z) for z in zs], label="step")
    plt.plot(zs, sigmoid(zs), label="sigmoid")
    plt.legend(); plt.grid(alpha=0.3); plt.title("A step you can slide down")
    plt.show()

def test_ex_1_3_sigmoid_error():
    from exercises.ex_1_3_sigmoid_error import sigmoid_error
    # perfect confidence -> error ~ 0: huge m centered between the groups
    assert sigmoid_error(10, -10 * 166.5, heights, labels) < 1e-6
    # always-unsure model (m=0, c=0 -> everyone 0.5) -> error 0.25
    assert abs(sigmoid_error(0, 0, heights, labels) - 0.25) < 1e-9

def test_ex_1_4_train():
    from exercises.ex_1_4_train import train
    err_before = sigmoid_error(0.12, 0.3, heights, labels)
    m1, c1 = train(0.12, 0.3, heights, labels, learning_rate=0.1, epochs=100)
    err_after = sigmoid_error(m1, c1, heights, labels)
    print(f"error: {err_before:.4f} -> {err_after:.4f}")
    assert err_after > 0.5                        # stuck!

    print("the smoking gun:", sigmoid(0.12 * 171 + 0.3))
    gm, gc = gradients_mc(sigmoid_error, 0.12, 0.3, heights, labels)
    print("gradients:", gm, gc)                   # ~zero: nothing to descend

def test_ex_1_5_classify():
    from exercises.ex_1_5_classify import classify
    preds = np.array([classify(x) for x in centered])
    print("predictions:", preds, "  labels:", labels)
    assert (preds == labels).all()

def test_ex_2_1_compute_graph():
    from exercises.ex_2_1_compute_graph import compute_graph
    assert abs(compute_graph(2, 1, 1, 1, 1, 1, 1) - 2.7616) < 1e-3
    assert abs(compute_graph(-5, 1, 1, 1, 1, 1, 1) - (-2.6555)) < 1e-3

def test_ex_3_3_predict_tax():
    from exercises.ex_3_3_predict_tax import predict_tax
    pipe_pred = np.array([predict_tax(xi) for xi in x])
    pipe_rmse = np.sqrt(np.mean((pipe_pred - y) ** 2))
    print(f"pipeline RMSE: {pipe_rmse:.5f}   (line was {line_rmse:.4f})")
    assert pipe_rmse < line_rmse / 5

def test_ex_3_4_fit_net():
    from exercises.ex_3_4_fit_net import fit_net
    from exercises.ex_3_4_fit_net import net_error
    params = fit_net(net_error, [1.0, 0.0, 1.0, 0.0], x, y, lr=0.5, epochs=5000)
    sig_rmse = np.sqrt(net_error(params, x, y))
    print(f"sigmoid net RMSE: {sig_rmse:.4f}")
    assert sig_rmse < line_rmse
    assert sig_rmse > pipe_rmse

    m_, c_, w1_, w0_ = params
    xs = np.sort(x)
    plt.scatter(x, y, s=12, alpha=0.5)
    plt.plot(xs, w1_ * sigmoid(m_ * xs + c_) + w0_, "r-", lw=2, label="sigmoid net")
    plt.legend(); plt.grid(alpha=0.3)
    plt.title("Better than a line — but it flattens out")
    plt.show()

def test_ex_3_5_relu():
    from exercises.ex_3_5_relu import relu
    from exercises.ex_3_5_relu import relu_error
    params_r = fit_net(relu_error, [1.0, 0.0, 1.0, 0.0], x, y, lr=0.5, epochs=5000)
    relu_rmse = np.sqrt(relu_error(params_r, x, y))
    print(f"relu net RMSE: {relu_rmse:.5f}")
    assert relu_rmse < sig_rmse
    assert relu_rmse < 0.02

    m_, c_, w1_, w0_ = params_r
    xs = np.sort(x)
    plt.scatter(x, y, s=12, alpha=0.5)
    plt.plot(xs, w1_ * relu(m_ * xs + c_) + w0_, "g-", lw=2, label="relu net")
    plt.legend(); plt.grid(alpha=0.3)
    plt.title("One ReLU neuron — the exact shape of the law")
    plt.show()

    print(f"\nfinal standings — line: {line_rmse:.4f}  sigmoid net: {sig_rmse:.4f}"
          f"  relu net: {relu_rmse:.5f}  pipeline: {pipe_rmse:.5f}")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = errors = 0
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {t.__name__}: {e}")
        except Exception as e:
            errors += 1
            print(f"  ERROR {t.__name__}: {type(e).__name__}: {e}")
    total = passed + failed + errors
    print(f"\n{passed}/{total} passed, {failed} failed, {errors} errors")
    sys.exit(0 if failed + errors == 0 else 1)
