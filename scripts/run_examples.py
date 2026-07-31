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
2. Legacy per-lecture checks (LECTURE_CONFIG, currently only lecture03): the
   pre-existing FruitSorting.java/qsort_examples.c comparator-safety demos
   (copied unchanged from lecture-notes/code/lecture03) and the
   still-combined sorting.py/comparator_demo.py runs. Honest scope note:
   FruitSorting.java and qsort_examples.c use *different* example data from
   each other, so a byte-for-byte stdout diff between C and Java is not
   meaningful there -- see the comments below. Lectures with no such legacy
   demo (e.g. lecture01, which only ever had ALGORITHM_CONFIG entries) skip
   this section entirely.
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
            "bubble-sort": {
                "c": {"file": "bubble_sort.c", "bin": "bubble_sort"},
                "java": {"file": "BubbleSort.java", "class": "BubbleSort"},
                "python": {"file": "bubble_sort_demo.py"},
            },
            "insertion-sort": {
                "c": {"file": "insertion_sort.c", "bin": "insertion_sort"},
                "java": {"file": "InsertionSort.java", "class": "InsertionSort"},
                "python": {"file": "insertion_sort_demo.py"},
            },
            "merge-sort": {
                "c": {"file": "merge_sort.c", "bin": "merge_sort"},
                "java": {"file": "MergeSort.java", "class": "MergeSort"},
                "python": {"file": "merge_sort_demo.py"},
            },
            "quick-sort": {
                "c": {"file": "quick_sort.c", "bin": "quick_sort"},
                "java": {"file": "QuickSort.java", "class": "QuickSort"},
                "python": {"file": "quick_sort_demo.py"},
            },
            "heap-sort": {
                "c": {"file": "heap_sort.c", "bin": "heap_sort"},
                "java": {"file": "HeapSort.java", "class": "HeapSort"},
                "python": {"file": "heap_sort.py"},
            },
            "counting-sort": {
                "c": {"file": "counting_sort.c", "bin": "counting_sort"},
                "java": {"file": "CountingSort.java", "class": "CountingSort"},
                "python": {"file": "counting_sort.py"},
            },
            "radix-sort": {
                "c": {"file": "radix_sort.c", "bin": "radix_sort"},
                "java": {"file": "RadixSort.java", "class": "RadixSort"},
                "python": {"file": "radix_sort.py"},
            },
        },
    },
    "01": {
        "dir": "01-introduction",
        "algorithms": {
            "maximum": {
                "c": {"file": "maximum.c", "bin": "maximum"},
                "java": {"file": "Maximum.java", "class": "Maximum"},
                "python": {"file": "maximum.py"},
            },
            "linear-search": {
                "c": {"file": "linear_search.c", "bin": "linear_search"},
                "java": {"file": "LinearSearch.java", "class": "LinearSearch"},
                "python": {"file": "linear_search.py"},
            },
            "binary-search": {
                "c": {"file": "binary_search.c", "bin": "binary_search"},
                "java": {"file": "BinarySearch.java", "class": "BinarySearch"},
                "python": {"file": "binary_search.py"},
            },
        },
    },
    "02": {
        "dir": "02-recursion",
        "algorithms": {
            "sum": {
                "c": {"file": "sum.c", "bin": "sum"},
                "java": {"file": "Sum.java", "class": "Sum"},
                "python": {"file": "sum.py"},
            },
            "hanoi": {
                "c": {"file": "hanoi.c", "bin": "hanoi"},
                "java": {"file": "Hanoi.java", "class": "Hanoi"},
                "python": {"file": "hanoi.py"},
            },
            "recursive-binary-search": {
                "c": {"file": "recursive_binary_search.c", "bin": "recursive_binary_search"},
                "java": {"file": "RecursiveBinarySearch.java", "class": "RecursiveBinarySearch"},
                "python": {"file": "recursive_binary_search.py"},
            },
            "maze": {
                "c": {"file": "maze.c", "bin": "maze"},
                "java": {"file": "Maze.java", "class": "Maze"},
                "python": {"file": "maze.py"},
            },
            "power-set": {
                "c": {"file": "power_set.c", "bin": "power_set"},
                "java": {"file": "PowerSet.java", "class": "PowerSet"},
                "python": {"file": "power_set.py"},
            },
        },
    },
    "04": {
        "dir": "04-selection",
        "algorithms": {
            "select-by-sorting": {
                "c": {"file": "select_by_sorting.c", "bin": "select_by_sorting"},
                "java": {"file": "SelectBySorting.java", "class": "SelectBySorting"},
                "python": {"file": "select_by_sorting.py"},
            },
            "fixed-quickselect": {
                "c": {"file": "fixed_quickselect.c", "bin": "fixed_quickselect"},
                "java": {"file": "FixedQuickselect.java", "class": "FixedQuickselect"},
                "python": {"file": "fixed_quickselect.py"},
            },
            "randomized-select": {
                "c": {"file": "randomized_select.c", "bin": "randomized_select"},
                "java": {"file": "RandomizedSelect.java", "class": "RandomizedSelect"},
                "python": {"file": "randomized_select.py"},
            },
            "deterministic-select": {
                "c": {"file": "deterministic_select.c", "bin": "deterministic_select"},
                "java": {"file": "DeterministicSelect.java", "class": "DeterministicSelect"},
                "python": {"file": "deterministic_select.py"},
            },
        },
    },
    "05": {
        "dir": "05-dynamic-programming",
        "algorithms": {
            # One binary/class per source file (fibonacci.c, MinPathSum.java,
            # etc.) prints both algorithms sharing that file (e.g. memo and
            # bottom-up), so both algorithm keys below point at the same
            # compile/run target -- the per-language dict values are
            # identical between the two entries in each pair by design, not
            # duplication error.
            "fib-memo": {
                "c": {"file": "fibonacci.c", "bin": "fibonacci"},
                "java": {"file": "FibonacciDP.java", "class": "FibonacciDP"},
                "python": {"file": "fibonacci.py"},
            },
            "fib-bottom-up": {
                "c": {"file": "fibonacci.c", "bin": "fibonacci"},
                "java": {"file": "FibonacciDP.java", "class": "FibonacciDP"},
                "python": {"file": "fibonacci.py"},
            },
            "min-path-memo": {
                "c": {"file": "min_path_sum.c", "bin": "min_path_sum"},
                "java": {"file": "MinPathSum.java", "class": "MinPathSum"},
                "python": {"file": "min_path_sum.py"},
            },
            "matrix-bottom-up": {
                "c": {"file": "min_path_sum.c", "bin": "min_path_sum"},
                "java": {"file": "MinPathSum.java", "class": "MinPathSum"},
                "python": {"file": "min_path_sum.py"},
            },
            "lcs-bottom-up": {
                "c": {"file": "lcs.c", "bin": "lcs"},
                "java": {"file": "LCS.java", "class": "LCS"},
                "python": {"file": "lcs.py"},
            },
            "max-subarray-brute-force": {
                "c": {"file": "max_subarray.c", "bin": "max_subarray"},
                "java": {"file": "MaximumSubarray.java", "class": "MaximumSubarray"},
                "python": {"file": "max_subarray.py"},
            },
            "max-subarray-kadane": {
                "c": {"file": "max_subarray.c", "bin": "max_subarray"},
                "java": {"file": "MaximumSubarray.java", "class": "MaximumSubarray"},
                "python": {"file": "max_subarray.py"},
            },
        },
    },
    "06": {
        "dir": "06-search-trees",
        "algorithms": {
            "binary-tree": {
                "c": {"file": "binary_tree.c", "bin": "binary_tree"},
                "java": {"file": "BinaryTree.java", "class": "BinaryTree"},
                "python": {"file": "binary_tree.py"},
            },
            "binary-search-tree": {
                "c": {"file": "binary_search_tree.c", "bin": "binary_search_tree"},
                "java": {"file": "BinarySearchTree.java", "class": "BinarySearchTree"},
                "python": {"file": "binary_search_tree.py"},
            },
            "avl-tree": {
                "c": {"file": "avl_tree.c", "bin": "avl_tree"},
                "java": {"file": "AVLTree.java", "class": "AVLTree"},
                "python": {"file": "avl_tree.py"},
            },
            "red-black-tree": {
                "c": {"file": "red_black_tree.c", "bin": "red_black_tree"},
                "java": {"file": "RedBlackTree.java", "class": "RedBlackTree"},
                "python": {"file": "red_black_tree.py"},
            },
            "btree": {
                "c": {"file": "btree.c", "bin": "btree"},
                "java": {"file": "BTree.java", "class": "BTree"},
                "python": {"file": "btree.py"},
            },
        },
    },
    "08": {
        "dir": "08-graphs",
        "algorithms": {
            # gcc (unlike javac) does not auto-discover dependencies, so
            # each C entry lists every .c file the binary needs: the shared
            # graph.c, the algorithm's own library file, and its demo main().
            "bfs": {
                "c": {"files": ["graph.c", "traversal.c", "traversal_demo.c"], "bin": "traversal_demo"},
                "java": {"file": "GraphTraversal.java", "class": "GraphTraversal"},
                "python": {"file": "traversal.py"},
            },
            "dfs": {
                "c": {"files": ["graph.c", "traversal.c", "traversal_demo.c"], "bin": "traversal_demo"},
                "java": {"file": "GraphTraversal.java", "class": "GraphTraversal"},
                "python": {"file": "traversal.py"},
            },
            "dfs-iterative": {
                "c": {"files": ["graph.c", "dfs_iterative.c", "dfs_iterative_demo.c"], "bin": "dfs_iterative_demo"},
                "java": {"file": "DfsIterative.java", "class": "DfsIterative"},
                "python": {"file": "dfs_iterative.py"},
            },
            "topo-kahn": {
                "c": {"files": ["graph.c", "topological_sort.c", "topological_sort_demo.c"], "bin": "topological_sort_demo"},
                "java": {"file": "TopologicalSort.java", "class": "TopologicalSort"},
                "python": {"file": "topological_sort.py"},
            },
            "topo-dfs": {
                "c": {"files": ["graph.c", "topological_sort.c", "topological_sort_demo.c"], "bin": "topological_sort_demo"},
                "java": {"file": "TopologicalSort.java", "class": "TopologicalSort"},
                "python": {"file": "topological_sort.py"},
            },
            "disjoint-set": {
                "c": {"files": ["disjoint_set.c", "disjoint_set_demo.c"], "bin": "disjoint_set_demo"},
                "java": {"file": "DisjointSetDemo.java", "class": "DisjointSetDemo"},
                "python": {"file": "disjoint_set.py"},
            },
            "prim": {
                "c": {"files": ["graph.c", "disjoint_set.c", "mst.c", "mst_demo.c"], "bin": "mst_demo"},
                "java": {"file": "MinimumSpanningTree.java", "class": "MinimumSpanningTree"},
                "python": {"file": "mst.py"},
            },
            "kruskal": {
                "c": {"files": ["graph.c", "disjoint_set.c", "mst.c", "mst_demo.c"], "bin": "mst_demo"},
                "java": {"file": "MinimumSpanningTree.java", "class": "MinimumSpanningTree"},
                "python": {"file": "mst.py"},
            },
            "dijkstra": {
                "c": {"files": ["graph.c", "shortest_paths.c", "shortest_paths_demo.c"], "bin": "shortest_paths_demo"},
                "java": {"file": "ShortestPaths.java", "class": "ShortestPaths"},
                "python": {"file": "shortest_paths.py"},
            },
            "bellman-ford": {
                "c": {"files": ["graph.c", "shortest_paths.c", "shortest_paths_demo.c"], "bin": "shortest_paths_demo"},
                "java": {"file": "ShortestPaths.java", "class": "ShortestPaths"},
                "python": {"file": "shortest_paths.py"},
            },
            "reconstruct-path": {
                "c": {"files": ["graph.c", "shortest_paths.c", "shortest_paths_demo.c"], "bin": "shortest_paths_demo"},
                "java": {"file": "ShortestPaths.java", "class": "ShortestPaths"},
                "python": {"file": "shortest_paths.py"},
            },
            "dag-shortest-paths": {
                "c": {
                    "files": ["graph.c", "topological_sort.c", "shortest_paths.c",
                              "dag_shortest_paths.c", "dag_shortest_paths_demo.c"],
                    "bin": "dag_shortest_paths_demo",
                },
                "java": {"file": "DagShortestPaths.java", "class": "DagShortestPaths"},
                "python": {"file": "dag_shortest_paths.py"},
            },
        },
    },
    "07": {
        "dir": "07-hash-tables",
        "algorithms": {
            "string-hash": {
                "c": {"file": "string_hash.c", "bin": "string_hash"},
                "java": {"file": "StringHash.java", "class": "StringHash"},
                "python": {"file": "string_hash.py"},
            },
            "chained-hash-table": {
                "c": {"file": "chained_hash_table.c", "bin": "chained_hash_table"},
                "java": {"file": "ChainedHashMap.java", "class": "ChainedHashMap"},
                "python": {"file": "chained_hash_table.py"},
            },
            "open-address-hash-table": {
                "c": {"file": "open_address_hash_table.c", "bin": "open_address_hash_table"},
                "java": {"file": "OpenAddressHashMap.java", "class": "OpenAddressHashMap"},
                "python": {"file": "open_address_hash_table.py"},
            },
        },
    },
    # See chapters/09.inventory §(c). All 4 algorithms share one library file
    # per language (string_matching.py/StringMatchers.java/string_matching.c,
    # matching the source's own organization) but each gets its own small
    # demo driver with its own main() -- Java only allows one main() per
    # class, so each demo is its own class (NaiveMatchDemo.java etc.); C
    # mirrors that with its own small demo .c file compiled together with
    # the shared library .c (same multi-file-per-binary pattern as L08's
    # graph.c + algorithm.c + demo.c). Every demo prints only
    # algorithm-result values (matches / lps / shift table entries), never
    # policy-dependent internals, so the printed token sequence matches
    # exactly across all 3 languages.
    "09": {
        "dir": "09-string-matching",
        "algorithms": {
            "naive-match": {
                "c": {"files": ["string_matching.c", "naive_demo.c"], "bin": "naive_demo"},
                "java": {"file": "NaiveMatchDemo.java", "class": "NaiveMatchDemo"},
                "python": {"file": "naive_demo.py"},
            },
            "rabin-karp": {
                "c": {"files": ["string_matching.c", "rabin_karp_demo.c"], "bin": "rabin_karp_demo"},
                "java": {"file": "RabinKarpDemo.java", "class": "RabinKarpDemo"},
                "python": {"file": "rabin_karp_demo.py"},
            },
            "kmp": {
                "c": {"files": ["string_matching.c", "kmp_demo.c"], "bin": "kmp_demo"},
                "java": {"file": "KmpDemo.java", "class": "KmpDemo"},
                "python": {"file": "kmp_demo.py"},
            },
            "horspool": {
                "c": {"files": ["string_matching.c", "horspool_demo.c"], "bin": "horspool_demo"},
                "java": {"file": "HorspoolDemo.java", "class": "HorspoolDemo"},
                "python": {"file": "horspool_demo.py"},
            },
        },
    },
}


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


def compile_and_run_c(c_dir, build_dir, source_files, bin_name):
    """`source_files` is one filename (str) or a list of filenames compiled
    together into one binary -- L08's demos need multiple .c files (e.g.
    graph.c + mst.c + mst_demo.c) since gcc, unlike javac, does not
    auto-discover and compile dependencies on its own."""
    if isinstance(source_files, str):
        source_files = [source_files]
    c_files = [str(c_dir / f) for f in source_files]
    bin_path = build_dir / bin_name
    compile_result = run(["gcc", "-Wall", "-std=c17", "-o", str(bin_path)] + c_files)
    if compile_result.returncode != 0:
        return False, "gcc -Wall failed:\n" + compile_result.stdout
    if compile_result.stdout.strip():
        return False, "gcc -Wall produced warnings:\n" + compile_result.stdout
    run_result = run([str(bin_path)])
    return run_result.returncode == 0, run_result.stdout


def compile_and_run_java(java_dir, build_dir, source_file, class_name):
    # javac's implicit-compilation sourcepath defaults to "." (the *process*
    # cwd), not the compiled file's own directory -- L01-05 never needed
    # cross-file dependencies within one lecture's java/ dir, but L08's
    # Graph.java is shared by nearly every other class there. Running with
    # cwd=java_dir and a bare filename (matching run_python_file's existing
    # cwd=python_dir pattern) makes "." resolve to java_dir, so a class like
    # ShortestPaths.java that references Graph auto-compiles it too instead
    # of failing with "cannot find symbol: class Graph".
    compile_result = run(["javac", "-d", str(build_dir), source_file], cwd=str(java_dir))
    if compile_result.returncode != 0:
        return False, "javac failed:\n" + compile_result.stdout
    run_result = run(["java", "-cp", str(build_dir), class_name])
    return run_result.returncode == 0, run_result.stdout


def run_python_file(python_dir, filename):
    src = python_dir / filename
    run_result = run(["python3", str(src)], cwd=str(python_dir))
    return run_result.returncode == 0, run_result.stdout


def normalize_numbers(text):
    """Extract the sequence of integers *and* letter-runs from stdout,
    ignoring surrounding format (brackets, spacing, labels) -- each
    language's demo prints in its own idiom, so this is the "same
    algorithm, same input" comparison, not a byte-diff.

    Letter-runs matter for algorithms whose output is symbolic rather than
    numeric (e.g. Power Set's `{a,b,c}`-style subsets, 1.9.2/2.12): a
    digits-only extraction would reduce that output to an empty sequence
    for all three languages, making the "outputs match" check vacuously
    true -- it would pass even if the three languages printed completely
    different subsets. Print-label words (e.g. "input", "path_exists")
    also get captured, but since every demo in this repo uses the same
    English labels across all three languages by construction, that adds
    signal (catching an accidental label mismatch) without causing false
    negatives.
    """
    return re.findall(r"-?\d+|[a-zA-Z]+", text)


def process_algorithms(lecture, code_dir, out_dir, build_dir):
    cfg = ALGORITHM_CONFIG.get(lecture, {}).get("algorithms", {})
    results = {}
    for algo_name, langs in cfg.items():
        algo_results = {}

        c_source = langs["c"].get("files", langs["c"].get("file"))
        ok_c, out_c = compile_and_run_c(code_dir / "c", build_dir, c_source, langs["c"]["bin"])
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
    legacy_cfg = LECTURE_CONFIG.get(lecture)
    algo_cfg = ALGORITHM_CONFIG.get(lecture, {})
    dir_name = (legacy_cfg or algo_cfg).get("dir")
    if dir_name is None:
        raise ValueError("no ALGORITHM_CONFIG or LECTURE_CONFIG entry for lecture %s" % lecture)

    code_dir = REPO_ROOT / "code" / dir_name
    out_dir = REPO_ROOT / "figures" / dir_name
    build_dir = REPO_ROOT / "figures" / ".cache" / "run_examples" / lecture
    build_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    algorithm_results = process_algorithms(lecture, code_dir, out_dir, build_dir)
    all_ok = all(r["outputs_match"] for r in algorithm_results.values())

    # Lectures with no legacy (pre-ALGORITHM_CONFIG) per-lecture demo -- e.g.
    # L01, which only ever had the per-algorithm Linear/Binary Search demos --
    # skip this whole section; there is nothing "legacy" to cross-check.
    if legacy_cfg is None:
        return all_ok, {}, None, algorithm_results

    cfg = legacy_cfg
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

    all_ok = all_ok and all(ok for ok, _ in results.values())

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

    if args.lecture not in LECTURE_CONFIG and args.lecture not in ALGORITHM_CONFIG:
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

    if results:
        print("  --- legacy lecture%s checks ---" % args.lecture)
        for key, (ok, out) in results.items():
            status = "PASS" if ok else "FAIL"
            print("  %-20s %s" % (key, status))
            if not ok:
                print("    " + "\n    ".join(out.splitlines()[-15:]))
        print("  selection/insertion/merge agree: %s" % algorithms_agree)

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
