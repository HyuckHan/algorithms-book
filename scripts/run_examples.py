#!/usr/bin/env python3
"""Compile and run the C/Java/Python reference code for a lecture.

Captures real stdout from each language (never remembered/typed output, per
AGENTS.md principle 2) into figures/NN-*/out-<name>.txt for inclusion in the
chapter, and checks that all three implementations pass their own internal
assertions.

Two kinds of checks live here:

1. Per-algorithm (ALGORITHM_CONFIG): for an algorithm with its own from-scratch
   C/Java/Python demo (ADR-004 -- e.g. Selection Sort, 1.3.1), compiles/runs
   all three on the *same* example input and verifies their outputs agree
   after normalization (each demo's own print format can differ; this
   extracts the sequence of integers from stdout and compares that sequence,
   not the raw text).
2. Legacy lecture03 checks (LECTURE_CONFIG): the pre-existing
   FruitSorting.java/qsort_examples.c comparator-safety demos (copied
   unchanged from lecture-notes/code/lecture03) and the still-combined
   sorting.py/comparator_demo.py runs. Honest scope note: FruitSorting.java
   and qsort_examples.c use *different* example data from each other, so a
   byte-for-byte stdout diff between C and Java is not meaningful there --
   see the comments below.
"""
import argparse
import re
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

# Per-algorithm C/Java/Python demos with a shared example input, one from-scratch
# algorithm each (see chapters/03-sorting.qmd's per-section panel-tabsets).
ALGORITHM_CONFIG = {
    "03": {
        "dir": "03-sorting",
        "algorithms": {
            "selection-sort": {
                "c": {"file": "selection_sort.c", "bin": "selection_sort"},
                "java": {"file": "SelectionSort.java", "class": "SelectionSort"},
                "python": {"file": "selection_sort_demo.py"},
            },
        },
    },
}


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


def compile_and_run_c(c_dir, build_dir, source_file, bin_name):
    c_file = c_dir / source_file
    bin_path = build_dir / bin_name
    compile_result = run(["gcc", "-Wall", "-std=c17", "-o", str(bin_path), str(c_file)])
    if compile_result.returncode != 0:
        return False, "gcc -Wall failed:\n" + compile_result.stdout
    if compile_result.stdout.strip():
        return False, "gcc -Wall produced warnings:\n" + compile_result.stdout
    run_result = run([str(bin_path)])
    return run_result.returncode == 0, run_result.stdout


def compile_and_run_java(java_dir, build_dir, source_file, class_name):
    java_file = java_dir / source_file
    compile_result = run(["javac", "-d", str(build_dir), str(java_file)])
    if compile_result.returncode != 0:
        return False, "javac failed:\n" + compile_result.stdout
    run_result = run(["java", "-cp", str(build_dir), class_name])
    return run_result.returncode == 0, run_result.stdout


def run_python_file(python_dir, filename):
    src = python_dir / filename
    run_result = run(["python3", str(src)], cwd=str(python_dir))
    return run_result.returncode == 0, run_result.stdout


def normalize_numbers(text):
    """Extract the sequence of integers from stdout, ignoring surrounding
    format (brackets, spacing, labels) -- each language's demo prints in its
    own idiom, so this is the "same algorithm, same input" comparison, not a
    byte-diff."""
    return re.findall(r"-?\d+", text)


def process_algorithms(lecture, code_dir, out_dir, build_dir):
    cfg = ALGORITHM_CONFIG.get(lecture, {}).get("algorithms", {})
    results = {}
    for algo_name, langs in cfg.items():
        algo_results = {}

        ok_c, out_c = compile_and_run_c(code_dir / "c", build_dir, langs["c"]["file"], langs["c"]["bin"])
        algo_results["c"] = (ok_c, out_c)
        (out_dir / ("out-%s-c.txt" % algo_name)).write_text(out_c, encoding="utf-8")

        ok_java, out_java = compile_and_run_java(
            code_dir / "java", build_dir, langs["java"]["file"], langs["java"]["class"]
        )
        algo_results["java"] = (ok_java, out_java)
        (out_dir / ("out-%s-java.txt" % algo_name)).write_text(out_java, encoding="utf-8")

        ok_py, out_py = run_python_file(code_dir / "python", langs["python"]["file"])
        algo_results["python"] = (ok_py, out_py)
        (out_dir / ("out-%s-python.txt" % algo_name)).write_text(out_py, encoding="utf-8")

        all_ok = all(ok for ok, _ in algo_results.values())
        normalized = {lang: normalize_numbers(out) for lang, (ok, out) in algo_results.items()}
        sequences = list(normalized.values())
        outputs_match = all_ok and len(sequences) > 0 and all(s == sequences[0] for s in sequences)

        results[algo_name] = {"per_language": algo_results, "normalized": normalized, "outputs_match": outputs_match}
    return results


def process_lecture(lecture):
    cfg = LECTURE_CONFIG[lecture]
    code_dir = REPO_ROOT / "code" / cfg["dir"]
    out_dir = REPO_ROOT / "figures" / cfg["dir"]
    build_dir = REPO_ROOT / "figures" / ".cache" / "run_examples" / lecture
    build_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    algorithm_results = process_algorithms(lecture, code_dir, out_dir, build_dir)

    results = {}
    ok_c, out_c = compile_and_run_c(code_dir / "c", build_dir, cfg["c_file"], cfg["c_bin"])
    results["c"] = (ok_c, out_c)
    (out_dir / "out-c.txt").write_text(out_c, encoding="utf-8")

    ok_java, out_java = compile_and_run_java(code_dir / "java", build_dir, cfg["java_file"], cfg["java_class"])
    results["java"] = (ok_java, out_java)
    (out_dir / "out-java.txt").write_text(out_java, encoding="utf-8")

    for py_file in cfg["python_files"]:
        ok_py, out_py = run_python_file(code_dir / "python", py_file)
        key = "python-%s" % Path(py_file).stem
        results[key] = (ok_py, out_py)
        (out_dir / ("out-%s.txt" % Path(py_file).stem)).write_text(out_py, encoding="utf-8")

    all_ok = all(ok for ok, _ in results.values())
    all_ok = all_ok and all(r["outputs_match"] for r in algorithm_results.values())

    # Cross-check: the three from-scratch sort functions in sorting.py must
    # agree with each other on the shared example input (printed as their
    # last three non-empty lines: "selection: ...", "insertion: ...", "merge : ...").
    sorting_out = results["python-sorting"][1]
    lines = [l for l in sorting_out.strip().splitlines() if ":" in l]
    sorted_values = [l.split(":", 1)[1].strip() for l in lines[-3:]]
    algorithms_agree = len(set(sorted_values)) == 1
    all_ok = all_ok and algorithms_agree

    return all_ok, results, algorithms_agree, algorithm_results


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lecture", default="03", help="lecture number, e.g. 03 (default: 03)")
    args = parser.parse_args()

    if args.lecture not in LECTURE_CONFIG:
        print("no run_examples config for lecture %s" % args.lecture)
        sys.exit(1)

    all_ok, results, algorithms_agree, algorithm_results = process_lecture(args.lecture)

    print("run_examples.py --lecture %s" % args.lecture)

    for algo_name, r in algorithm_results.items():
        print("  --- %s (per-algorithm, 3-language) ---" % algo_name)
        for lang, (ok, out) in r["per_language"].items():
            status = "PASS" if ok else "FAIL"
            print("  %-20s %s" % (algo_name + "-" + lang, status))
            if not ok:
                print("    " + "\n    ".join(out.splitlines()[-15:]))
        print("  %-20s normalized=%s -> %s"
              % (algo_name + " outputs match", r["normalized"], "PASS" if r["outputs_match"] else "FAIL"))

    print("  --- legacy lecture03 checks ---")
    for key, (ok, out) in results.items():
        status = "PASS" if ok else "FAIL"
        print("  %-20s %s" % (key, status))
        if not ok:
            print("    " + "\n    ".join(out.splitlines()[-15:]))
    print("  selection/insertion/merge agree: %s" % algorithms_agree)

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
