# Compose sigmoid() and perceptron()
# Write your solution below. Run this file to test: python exercises/10_hard_neural_net_functions.py

import math


def sigmoid(x):
    """Provided utility -- already implemented, no need to change."""
    return 1 / (1 + math.exp(-x))


def perceptron(inputs, weights, bias):
    """Return the output of a single neuron: sigmoid(dot(inputs, weights) + bias).

    TODO: implement using sigmoid().
    """
    pass


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    import math


    def ref_sigmoid(x):
        return 1 / (1 + math.exp(-x))


    inputs, weights, bias = [1.0, 2.0, -1.0], [0.5, -0.3, 0.8], 0.1
    expected = ref_sigmoid(sum(i * w for i, w in zip(inputs, weights)) + bias)
    assert math.isclose(perceptron(inputs, weights, bias), expected), \
        f"Expected {expected}, got {perceptron(inputs, weights, bias)}"
    print("PASS")
