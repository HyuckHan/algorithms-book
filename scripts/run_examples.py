#!/usr/bin/env python3
"""Compile and run the C/Java/Python reference code for a lecture (SPEC 4.5).

Captures real stdout from each language (never remembered/typed output, per
AGENTS.md principle 2) into figures/NN-*/out-<lang>.txt for inclusion in the
chapter, and checks that all three implementations pass their own internal
assertions.

Honest scope note for lecture03 specifically: `code/03-sorting/java/FruitSorting.java`
and `code/03-sorting/c/qsort_examples.c` are copied unchanged from
lecture-notes/code/lecture03 (the read-only source of truth) and demonstrate
comparator/qsort API safety (Comparator chaining; relational, not `a - b`,
comparators) -- they already use *different* example data from each other, so
a byte-for-byte stdout diff between C and Java is not meaningful here. This
script instead verifies the property both share and that
code/03-sorting/python/comparator_demo.py also demonstrates: primitive
extreme-value ordering and stable multi-key ordering with duplicate keys --
and separately verifies that Selection/Insertion/Merge Sort in
code/03-sorting/python/sorting.py agree with each other on the same input
(there is no from-scratch Java/C implementation of those algorithms to diff
against; the Java/C files only exercise the standard-library sort API).
"""
import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

LECTURE_CONFIG = {
    "03": {
        "dir": "03-sorting",
        "c_file": "qsort_examples.c",
        "c_bin": "qsort_examples",
        "java_file": "FruitSorting.java",
        "java_class": "FruitSorting",
        "python_files": ["comparator_demo.py", "sorting.py"],
    },
}


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


def run_c(code_dir, build_dir):
    src = code_dir / "c"
    c_file = src / LECTURE_CONFIG["03"]["c_file"]
    bin_path = build_dir / LECTURE_CONFIG["03"]["c_bin"]
    compile_result = run(["gcc", "-Wall", "-std=c17", "-o", str(bin_path), str(c_file)])
    if compile_result.returncode != 0:
        return False, "gcc -Wall failed:\n" + compile_result.stdout
    if compile_result.stdout.strip():
        return False, "gcc -Wall produced warnings:\n" + compile_result.stdout
    run_result = run([str(bin_path)])
    return run_result.returncode == 0, run_result.stdout


def run_java(code_dir, build_dir):
    src = code_dir / "java"
    java_file = src / LECTURE_CONFIG["03"]["java_file"]
    compile_result = run(["javac", "-d", str(build_dir), str(java_file)])
    if compile_result.returncode != 0:
        return False, "javac failed:\n" + compile_result.stdout
    run_result = run(["java", "-cp", str(build_dir), LECTURE_CONFIG["03"]["java_class"]])
    return run_result.returncode == 0, run_result.stdout


def run_python(code_dir, filename):
    src = code_dir / "python" / filename
    run_result = run(["python3", str(src)])
    return run_result.returncode == 0, run_result.stdout


def process_lecture(lecture):
    cfg = LECTURE_CONFIG[lecture]
    code_dir = REPO_ROOT / "code" / cfg["dir"]
    out_dir = REPO_ROOT / "figures" / cfg["dir"]
    build_dir = REPO_ROOT / "figures" / ".cache" / "run_examples" / lecture
    build_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    ok_c, out_c = run_c(code_dir, build_dir)
    results["c"] = (ok_c, out_c)
    (out_dir / "out-c.txt").write_text(out_c, encoding="utf-8")

    ok_java, out_java = run_java(code_dir, build_dir)
    results["java"] = (ok_java, out_java)
    (out_dir / "out-java.txt").write_text(out_java, encoding="utf-8")

    for py_file in cfg["python_files"]:
        ok_py, out_py = run_python(code_dir, py_file)
        key = "python-%s" % Path(py_file).stem
        results[key] = (ok_py, out_py)
        (out_dir / ("out-%s.txt" % Path(py_file).stem)).write_text(out_py, encoding="utf-8")

    all_ok = all(ok for ok, _ in results.values())

    # Cross-check: the three from-scratch sort functions in sorting.py must
    # agree with each other on the shared example input (printed as their
    # last three non-empty lines: "selection: ...", "insertion: ...", "merge : ...").
    sorting_out = results["python-sorting"][1]
    lines = [l for l in sorting_out.strip().splitlines() if ":" in l]
    sorted_values = [l.split(":", 1)[1].strip() for l in lines[-3:]]
    algorithms_agree = len(set(sorted_values)) == 1
    all_ok = all_ok and algorithms_agree

    return all_ok, results, algorithms_agree


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lecture", default="03", help="lecture number, e.g. 03 (default: 03)")
    args = parser.parse_args()

    if args.lecture not in LECTURE_CONFIG:
        print("no run_examples config for lecture %s" % args.lecture)
        sys.exit(1)

    all_ok, results, algorithms_agree = process_lecture(args.lecture)

    print("run_examples.py --lecture %s" % args.lecture)
    for key, (ok, out) in results.items():
        status = "PASS" if ok else "FAIL"
        print("  %-20s %s" % (key, status))
        if not ok:
            print("    " + "\n    ".join(out.splitlines()[-15:]))
    print("  selection/insertion/merge agree: %s" % algorithms_agree)

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
