# Exercise 4.2 — Valid Dates Only
# Write your solution in this file. Run test_exercises.py to check.

def is_valid_date(s):
    return re.fullmatch(STRICT_DATE, s) is not None
