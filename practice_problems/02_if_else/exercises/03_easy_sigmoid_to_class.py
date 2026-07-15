# Turn a Sigmoid Output into a Class Label
# Write your solution below. Run this file to test: python exercises/03_easy_sigmoid_to_class.py

activation = 0.63

# TODO: set predicted_class to 1 if activation >= 0.5, else 0
predicted_class = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    expected = 1 if activation >= 0.5 else 0
    assert predicted_class == expected, f"Expected {expected}, got {predicted_class}"
    print("PASS")
