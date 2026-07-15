# Exercise 5.2 — Three Variables
# Write your solution in this file. Run test_exercises.py to check.

def p(v):
    x, y, z = v
    return (x - 1)**2 + (y - 2)**2 + (z + 3)**2


def q(v):
    x, y, z = v
    return x**2 + 2*y**2 + 3*z**2 - 4*x + 6*z
