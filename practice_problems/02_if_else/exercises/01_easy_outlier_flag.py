# Flag a Single Outlier by Z-Score
# Write your solution below. Run this file to test: python exercises/01_easy_outlier_flag.py

z = 3.4
threshold = 3

# TODO: set status to "outlier" if abs(z) > threshold, else "normal"
status = None


# --- Tests (do not modify below this line) ---
if __name__ == '__main__':
    expected = "outlier" if abs(z) > threshold else "normal"
    assert status == expected, f"Expected {expected!r}, got {status!r}"
    print("PASS")
