#!/usr/bin/env python3
"""
Generate exercise placeholder files and test scripts from chapter notebooks.

For each notebook:
  1. Creates <chapter>/exercises/ with one .py stub per coding exercise
  2. Creates <chapter>/test_exercises.py that imports and tests each stub

Usage:
    python generate_exercises.py                # all chapters
    python generate_exercises.py loops_and_array # single chapter
"""
import json
import os
import re
import sys
import textwrap

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

CHAPTERS = {
    "expressions_and_functions": "expressions_and_functions/expressions_and_functions.ipynb",
    "if_else": "if_else/if_else.ipynb",
    "recursion": "recursion/recursion.ipynb",
    "dictionaries": "dictionaries/dictionaries.ipynb",
    "binary_search": "binary_search/binary_search.ipynb",
    "loops_and_array": "loops_and_array/loops_and_array.ipynb",
    "sorting": "sorting/sorting.ipynb",
    "trees_and_heaps": "trees_and_heaps/trees_and_heaps.ipynb",
    "pattern_matching": "pattern_matching/pattern_matching.ipynb",
    "backtracking": "backtracking/backtracking.ipynb",
    "encoder_decoder": "encoder_decoder/encoder_decoder.ipynb",
    "classes_and_objects": "classes_and_objects/classes_and_objects.ipynb",
    "secrets_of_prediction": "secrets_of_prediction/secrets_of_prediction.ipynb",
    "gradient_descent": "gradient_descent/linear_regression_gradient_descent.ipynb",
    "decision_tree": "decision_tree/decision_tree.ipynb",
    "random_forest": "random_forest/random_forest.ipynb",
    "recommender": "recommender/recommender.ipynb",
    "neural_networks": "neural_networks/neural_networks.ipynb",
    "convolutions": "convolutions/convolutions.ipynb",
    "information_theory": "information_theory/information_theory.ipynb",
}


def slugify(name):
    """Convert a function/exercise name to a filename-safe slug."""
    name = re.sub(r'[`\'"()]', '', name)
    name = re.sub(r'[^a-zA-Z0-9]+', '_', name)
    name = name.strip('_').lower()
    return name


def extract_exercise_label(md_src):
    """Extract exercise number and title from a markdown cell."""
    m = re.search(
        r'#+\s*Exercise\s+(\d+)\.(\d+)\s*[—–\-:]\s*(.+?)(?:\n|$)',
        md_src, re.IGNORECASE
    )
    if m:
        return int(m.group(1)), int(m.group(2)), m.group(3).strip()
    return None, None, None


def parse_code_cell(src):
    """
    Split a code cell into definition part and test part.
    Returns: (imports, defs, test_lines)

    Strategy: find where the last def/class block ends.
    Everything after that is test code.
    """
    lines = src.split('\n')
    imports = []

    # First pass: find the end of the last def/class block
    last_def_end = -1
    in_def = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('from '):
            if not in_def:
                imports.append(line)
                continue
        if re.match(r'^(def |class )', stripped):
            in_def = True
            last_def_end = i
        elif in_def:
            if stripped == '' or line.startswith('    ') or line.startswith('\t'):
                last_def_end = i
            else:
                in_def = False

    if last_def_end < 0:
        return imports, [], []

    # Definition lines: from start to last_def_end (inclusive)
    def_section = lines[:last_def_end + 1]
    test_section = lines[last_def_end + 1:]

    # Extract def blocks from the definition section
    defs = []
    current_block = []
    in_def = False
    for line in def_section:
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('from '):
            continue  # already captured
        if re.match(r'^(def |class )', stripped):
            if in_def and current_block:
                defs.append('\n'.join(current_block))
            current_block = [line]
            in_def = True
        elif in_def:
            current_block.append(line)
        # skip non-def top-level lines in definition section
    if current_block:
        defs.append('\n'.join(current_block))

    # Clean test section: only remove trailing print("...: OK") lines
    test_lines = []
    for line in test_section:
        stripped = line.strip()
        if not stripped:
            if test_lines:
                test_lines.append(line)
            continue
        # Only remove the specific "OK" print pattern at top level
        if re.match(r'^print\(.+:\s*OK', stripped):
            continue
        test_lines.append(line)

    # Trim trailing blanks
    while test_lines and not test_lines[-1].strip():
        test_lines.pop()

    # Convert print(func(...))  # expected to assert statements
    converted = []
    for line in test_lines:
        stripped = line.strip()
        m = re.match(
            r'print\((.+?)\)\s*#\s*(.+)$',
            stripped
        )
        if m:
            expr = m.group(1).strip()
            expected = m.group(2).strip()
            # Try to build an assertion if expected looks like a value
            try:
                compile(expected, '<test>', 'eval')
                indent = line[:len(line) - len(line.lstrip())]
                converted.append(f"{indent}assert {expr} == {expected}")
                continue
            except SyntaxError:
                pass
        converted.append(line)
    test_lines = converted

    return imports, defs, test_lines


def extract_func_names(def_block):
    """Extract function/class names from a definition block."""
    names = []
    for line in def_block.split('\n'):
        m = re.match(r'def (\w+)', line.strip())
        if m:
            names.append(m.group(1))
        m = re.match(r'class (\w+)', line.strip())
        if m:
            names.append(m.group(1))
    return names


def process_notebook(chapter_name, nb_path):
    """Process a single notebook and generate exercise files + test script."""
    full_path = os.path.join(REPO_ROOT, nb_path)
    chapter_dir = os.path.join(REPO_ROOT, chapter_name)
    exercises_dir = os.path.join(chapter_dir, "exercises")

    with open(full_path) as f:
        nb = json.load(f)

    cells = nb['cells']
    exercises = []
    pending_exercise = None

    for i, cell in enumerate(cells):
        src = ''.join(cell['source'])

        if cell['cell_type'] == 'markdown':
            part, num, title = extract_exercise_label(src)
            if part is not None:
                pending_exercise = {
                    'part': part,
                    'num': num,
                    'title': title,
                    'cell_index': i,
                }

        elif cell['cell_type'] == 'code' and pending_exercise:
            has_stub = ('pass' in src and ('def ' in src or 'class ' in src))
            has_todo = '# replace this' in src.lower() or '# TODO' in src or '# your' in src.lower()

            if has_stub or has_todo:
                imports, defs, test_lines = parse_code_cell(src)
                func_names = []
                for d in defs:
                    func_names.extend(extract_func_names(d))

                if func_names or defs:
                    pending_exercise['imports'] = imports
                    pending_exercise['defs'] = defs
                    pending_exercise['test_lines'] = test_lines
                    pending_exercise['func_names'] = func_names
                    pending_exercise['full_src'] = src
                    exercises.append(pending_exercise)
                    pending_exercise = None

    if not exercises:
        print(f"  WARNING: No exercises found in {nb_path}")
        return []

    os.makedirs(exercises_dir, exist_ok=True)

    # Write __init__.py
    init_path = os.path.join(exercises_dir, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, 'w') as f:
            pass

    generated_files = []
    test_functions = []

    for ex in exercises:
        part = ex['part']
        num = ex['num']
        title = ex['title']
        func_names = ex['func_names']

        # File naming: use first function name, or slugified title
        if func_names:
            primary_name = func_names[0]
        else:
            primary_name = slugify(title)

        filename = f"ex_{part}_{num}_{slugify(primary_name)}.py"
        filepath = os.path.join(exercises_dir, filename)

        # Build exercise file content
        file_lines = [
            f"# Exercise {part}.{num} — {title}",
            f"# Write your solution in this file. Run test_exercises.py to check.",
            "",
        ]

        # Add imports
        for imp in ex['imports']:
            file_lines.append(imp)
        if ex['imports']:
            file_lines.append("")

        # Add function/class stubs
        for d in ex['defs']:
            file_lines.append(d)
            file_lines.append("")

        content = '\n'.join(file_lines).rstrip() + '\n'
        with open(filepath, 'w') as f:
            f.write(content)

        generated_files.append(filename)

        # Build test function
        test_name = f"test_ex_{part}_{num}_{slugify(primary_name)}"
        module_name = filename[:-3]  # strip .py

        import_stmts = []
        for fn in func_names:
            import_stmts.append(f"    from exercises.{module_name} import {fn}")

        test_body = []
        for line in ex.get('test_lines', []):
            if line.strip():
                test_body.append(f"    {line}")
            else:
                test_body.append("")

        if import_stmts and test_body:
            test_fn = f"def {test_name}():\n"
            test_fn += '\n'.join(import_stmts) + '\n'
            test_fn += '\n'.join(test_body)
            test_functions.append(test_fn)
        elif import_stmts:
            test_fn = f"def {test_name}():\n"
            test_fn += '\n'.join(import_stmts) + '\n'
            test_fn += f"    assert {func_names[0]} is not None"
            test_functions.append(test_fn)

        ex['filename'] = filename
        ex['module_name'] = module_name

    # Update notebook markdown cells to reference exercise files
    modified = False
    for ex in exercises:
        cell_idx = ex['cell_index']
        cell = cells[cell_idx]
        src = ''.join(cell['source'])
        ref_line = f"\n\n**Write your solution in `exercises/{ex['filename']}`**"
        if f"exercises/{ex['filename']}" not in src:
            cell['source'] = [src + ref_line]
            modified = True

    if modified:
        with open(full_path, 'w') as f:
            json.dump(nb, f, indent=1)
        print(f"    Updated notebook with file references")

    # Write test_exercises.py
    test_path = os.path.join(chapter_dir, "test_exercises.py")
    test_content = f'''#!/usr/bin/env python3
"""Test runner for {chapter_name} exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

'''
    test_content += '\n\n'.join(test_functions)
    test_content += '''


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
    print(f"\\n{passed}/{total} passed, {failed} failed, {errors} errors")
    sys.exit(0 if failed + errors == 0 else 1)
'''
    with open(test_path, 'w') as f:
        f.write(test_content)

    print(f"  {chapter_name}: {len(exercises)} exercises, {len(test_functions)} tests")
    return exercises


def process_practice_problems():
    """Process all practice problem notebooks."""
    import glob

    pp_root = os.path.join(REPO_ROOT, "practice_problems")
    folders = sorted(glob.glob(os.path.join(pp_root, "[0-9]*")))
    total = 0

    for folder in folders:
        folder_name = os.path.basename(folder)
        exercises_dir = os.path.join(folder, "exercises")
        os.makedirs(exercises_dir, exist_ok=True)

        init_path = os.path.join(exercises_dir, "__init__.py")
        if not os.path.exists(init_path):
            with open(init_path, 'w') as f:
                pass

        notebooks = sorted(glob.glob(os.path.join(folder, "*.ipynb")))
        exercise_files = []

        for nb_path in notebooks:
            nb_name = os.path.splitext(os.path.basename(nb_path))[0]

            with open(nb_path) as f:
                nb = json.load(f)

            cells = nb['cells']
            # Find code cells
            code_cells = [c for c in cells if c['cell_type'] == 'code']
            if len(code_cells) < 2:
                continue

            # First code cell: exercise stub; Last code cell: tests
            exercise_src = ''.join(code_cells[0]['source'])
            test_src = ''.join(code_cells[-1]['source'])

            # Clean test src: remove "All tests passed!" prints
            test_lines = []
            for line in test_src.split('\n'):
                stripped = line.strip()
                if stripped.startswith('print(') and 'All tests passed' in stripped:
                    continue
                test_lines.append(line)
            test_src_clean = '\n'.join(test_lines).rstrip()

            # Build the exercise file with embedded tests
            # Extract title from first markdown cell
            title = nb_name.replace('_', ' ').title()
            for c in cells:
                if c['cell_type'] == 'markdown':
                    src = ''.join(c['source'])
                    m = re.match(r'#\s*(.+)', src)
                    if m:
                        title = m.group(1).strip()
                    break

            file_content = f"# {title}\n"
            file_content += "# Write your solution below. Run this file to test: "
            file_content += f"python exercises/{nb_name}.py\n\n"
            file_content += exercise_src.rstrip() + "\n"
            file_content += "\n\n# --- Tests (do not modify below this line) ---\n"
            file_content += "if __name__ == '__main__':\n"
            # Indent test code
            for line in test_src_clean.split('\n'):
                if line.strip():
                    file_content += f"    {line}\n"
                else:
                    file_content += "\n"
            file_content += '    print("PASS")\n'

            filepath = os.path.join(exercises_dir, f"{nb_name}.py")
            with open(filepath, 'w') as f:
                f.write(file_content)

            exercise_files.append(nb_name)
            total += 1

            # Update notebook markdown to reference exercise file
            for c in nb['cells']:
                if c['cell_type'] == 'markdown':
                    md_src = ''.join(c['source'])
                    if '### Problem' in md_src or '# ' in md_src:
                        if f"exercises/{nb_name}.py" not in md_src:
                            c['source'] = [md_src + f"\n\n**Write your solution in `exercises/{nb_name}.py`**"]
                            with open(nb_path, 'w') as f:
                                json.dump(nb, f, indent=1)
                        break

        # Write test runner for this folder
        test_path = os.path.join(folder, "test_exercises.py")
        test_content = f'''#!/usr/bin/env python3
"""Test runner for practice_problems/{folder_name}. Run: python test_exercises.py"""
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
            print(f"  PASS  {{name}}")
        else:
            failed += 1
            err = result.stderr.strip().split("\\n")[-1] if result.stderr else "unknown"
            print(f"  FAIL  {{name}}: {{err}}")
    except subprocess.TimeoutExpired:
        errors += 1
        print(f"  ERROR {{name}}: timeout (10s)")
    except Exception as e:
        errors += 1
        print(f"  ERROR {{name}}: {{e}}")

total = passed + failed + errors
print(f"\\n{{passed}}/{{total}} passed, {{failed}} failed, {{errors}} errors")
sys.exit(0 if failed + errors == 0 else 1)
'''
        with open(test_path, 'w') as f:
            f.write(test_content)

        print(f"  practice_problems/{folder_name}: {len(exercise_files)} exercises")

    return total


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None

    if target == "practice_problems":
        print("Processing practice_problems...")
        total = process_practice_problems()
        print(f"\nDone: {total} practice problem exercises")
        return

    if target:
        if target in CHAPTERS:
            chapters = {target: CHAPTERS[target]}
        else:
            print(f"Unknown chapter: {target}")
            print(f"Available: {', '.join(sorted(CHAPTERS.keys()))}, practice_problems")
            sys.exit(1)
    else:
        chapters = CHAPTERS

    all_exercises = {}
    for name, path in sorted(chapters.items()):
        print(f"Processing {name}...")
        exercises = process_notebook(name, path)
        all_exercises[name] = exercises

    total_ex = sum(len(v) for v in all_exercises.values())
    total_ch = len(all_exercises)
    print(f"\nDone: {total_ex} exercises across {total_ch} chapters")

    if not target:
        print("\nProcessing practice_problems...")
        pp_total = process_practice_problems()
        print(f"\nGrand total: {total_ex + pp_total} exercises")


if __name__ == "__main__":
    main()
