# Find All Outliers in a Dataset
# Write your solution below. Run this file to test: python exercises/04_medium_find_outliers_loop.py

data = [12, 15, 14, 10, 100, 13, 11, 16, 9, 14]
mean_value = 21.4
variance = 690.84
std_dev = variance ** 0.5
k = 2

# TODO: loop through data and collect every value whose distance from
# the mean exceeds k * std_dev
outliers = []


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    expected = [x for x in data if abs(x - mean_value) > k * std_dev]
    assert outliers == expected, f"Expected {expected}, got {outliers}"
    print("PASS")
