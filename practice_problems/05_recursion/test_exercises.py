#!/usr/bin/env python3
"""Test runner for practice_problems/05_recursion. Run: python test_exercises.py"""
import subprocess
import sys
import os
import glob

exercises_dir = os.path.join(os.path.dirname(__file__), "exercises")
exercises = sorted(glob.glob(os.path.join(exercises_dir, "*.py")))
exercises = [e for e in exercises if not e.endswith("__init__.py")]

passed = failed = errors = 0
for ex in exercises:
    name = os.path.splitext(os.path.basename(ex))[0]
    try:
        result = subprocess.run(
            [sys.executable, ex],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            passed += 1
            print(f"  PASS  {name}")
        else:
            failed += 1
            err = result.stderr.strip().split("\n")[-1] if result.stderr else "unknown"
            print(f"  FAIL  {name}: {err}")
    except subprocess.TimeoutExpired:
        errors += 1
        print(f"  ERROR {name}: timeout (10s)")
    except Exception as e:
        errors += 1
        print(f"  ERROR {name}: {e}")

total = passed + failed + errors
print(f"\n{passed}/{total} passed, {failed} failed, {errors} errors")
sys.exit(0 if failed + errors == 0 else 1)
