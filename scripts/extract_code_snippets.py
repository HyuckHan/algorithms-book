#!/usr/bin/env python3
"""Extract marker-delimited algorithm snippets from multi-algorithm source
files, so a chapter section can show *just* that algorithm's code even when
the canonical file (reused per ADR-004 rather than duplicated) also contains
other algorithms.

A source file marks the region to extract with a pair of comments:
    # snippet:selection-sort:start          (Python: '#')
    ...function...
    # snippet:selection-sort:end
    // snippet:selection-sort:start         (Java/C: '//')
    ...
    // snippet:selection-sort:end

For each (source file, snippet name) pair configured below, this writes the
text between the markers (exclusive) to figures/NN-*/snippet-<name>.<ext>,
preserving the original indentation so it's still valid, directly-includable
source. A qmd then does:
    ```{.python}
    {{< include ../figures/03-sorting/snippet-selection-sort.py >}}
    ```
instead of including the whole multi-algorithm file.
"""
import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# (lecture, snippet_name) -> list of (source file relative to code/<dir>/, output extension)
SNIPPET_CONFIG = {
    "03": {
        "dir": "03-sorting",
        "snippets": {
            "selection-sort": [
                ("python/sorting.py", "py"),
                ("java/SelectionSort.java", "java"),
                ("c/selection_sort.c", "c"),
            ],
            "bubble-sort": [
                ("python/sorting.py", "py"),
                ("java/BubbleSort.java", "java"),
                ("c/bubble_sort.c", "c"),
            ],
            "insertion-sort": [
                ("python/sorting.py", "py"),
                ("java/InsertionSort.java", "java"),
                ("c/insertion_sort.c", "c"),
            ],
            "merge-sort": [
                ("python/sorting.py", "py"),
                ("java/MergeSort.java", "java"),
                ("c/merge_sort.c", "c"),
            ],
            "quick-sort": [
                ("python/sorting.py", "py"),
                ("java/QuickSort.java", "java"),
                ("c/quick_sort.c", "c"),
            ],
            "heap-sort": [
                ("python/heap_sort.py", "py"),
                ("java/HeapSort.java", "java"),
                ("c/heap_sort.c", "c"),
            ],
            "counting-sort": [
                ("python/counting_sort.py", "py"),
                ("java/CountingSort.java", "java"),
                ("c/counting_sort.c", "c"),
            ],
            "radix-sort": [
                ("python/radix_sort.py", "py"),
                ("java/RadixSort.java", "java"),
                ("c/radix_sort.c", "c"),
            ],
        },
    },
    "01": {
        "dir": "01-introduction",
        "snippets": {
            "maximum": [
                ("python/maximum.py", "py"),
                ("java/Maximum.java", "java"),
                ("c/maximum.c", "c"),
            ],
            "linear-search": [
                ("python/linear_search.py", "py"),
                ("java/LinearSearch.java", "java"),
                ("c/linear_search.c", "c"),
            ],
            "binary-search": [
                ("python/binary_search.py", "py"),
                ("java/BinarySearch.java", "java"),
                ("c/binary_search.c", "c"),
            ],
        },
    },
    "02": {
        "dir": "02-recursion",
        "snippets": {
            "sum": [
                ("python/sum.py", "py"),
                ("java/Sum.java", "java"),
                ("c/sum.c", "c"),
            ],
            "hanoi": [
                ("python/hanoi.py", "py"),
                ("java/Hanoi.java", "java"),
                ("c/hanoi.c", "c"),
            ],
            "recursive-binary-search": [
                ("python/recursive_binary_search.py", "py"),
                ("java/RecursiveBinarySearch.java", "java"),
                ("c/recursive_binary_search.c", "c"),
            ],
            "maze": [
                ("python/maze.py", "py"),
                ("java/Maze.java", "java"),
                ("c/maze.c", "c"),
            ],
            "power-set": [
                ("python/power_set.py", "py"),
                ("java/PowerSet.java", "java"),
                ("c/power_set.c", "c"),
            ],
        },
    },
    "04": {
        "dir": "04-selection",
        "snippets": {
            "select-by-sorting": [
                ("python/select_by_sorting.py", "py"),
                ("java/SelectBySorting.java", "java"),
                ("c/select_by_sorting.c", "c"),
            ],
            "fixed-quickselect": [
                ("python/fixed_quickselect.py", "py"),
                ("java/FixedQuickselect.java", "java"),
                ("c/fixed_quickselect.c", "c"),
            ],
            "randomized-select": [
                ("python/randomized_select.py", "py"),
                ("java/RandomizedSelect.java", "java"),
                ("c/randomized_select.c", "c"),
            ],
            "deterministic-select": [
                ("python/deterministic_select.py", "py"),
                ("java/DeterministicSelect.java", "java"),
                ("c/deterministic_select.c", "c"),
            ],
        },
    },
    "05": {
        "dir": "05-dynamic-programming",
        "snippets": {
            "fib-memo": [
                ("python/fibonacci.py", "py"),
                ("java/FibonacciDP.java", "java"),
                ("c/fibonacci.c", "c"),
            ],
            "fib-bottom-up": [
                ("python/fibonacci.py", "py"),
                ("java/FibonacciDP.java", "java"),
                ("c/fibonacci.c", "c"),
            ],
            "min-path-memo": [
                ("python/min_path_sum.py", "py"),
                ("java/MinPathSum.java", "java"),
                ("c/min_path_sum.c", "c"),
            ],
            "matrix-bottom-up": [
                ("python/min_path_sum.py", "py"),
                ("java/MinPathSum.java", "java"),
                ("c/min_path_sum.c", "c"),
            ],
            "lcs-bottom-up": [
                ("python/lcs.py", "py"),
                ("java/LCS.java", "java"),
                ("c/lcs.c", "c"),
            ],
            "max-subarray-brute-force": [
                ("python/max_subarray.py", "py"),
                ("java/MaximumSubarray.java", "java"),
                ("c/max_subarray.c", "c"),
            ],
            "max-subarray-kadane": [
                ("python/max_subarray.py", "py"),
                ("java/MaximumSubarray.java", "java"),
                ("c/max_subarray.c", "c"),
            ],
        },
    },
    "06": {
        "dir": "06-search-trees",
        "snippets": {
            "binary-tree": [
                ("python/binary_tree.py", "py"),
                ("java/BinaryTree.java", "java"),
                ("c/binary_tree.c", "c"),
            ],
            "binary-search-tree": [
                ("python/binary_search_tree.py", "py"),
                ("java/BinarySearchTree.java", "java"),
                ("c/binary_search_tree.c", "c"),
            ],
            "avl-tree": [
                ("python/avl_tree.py", "py"),
                ("java/AVLTree.java", "java"),
                ("c/avl_tree.c", "c"),
            ],
            "red-black-tree": [
                ("python/red_black_tree.py", "py"),
                ("java/RedBlackTree.java", "java"),
                ("c/red_black_tree.c", "c"),
            ],
            "btree": [
                ("python/btree.py", "py"),
                ("java/BTree.java", "java"),
                ("c/btree.c", "c"),
            ],
        },
    },
    "08": {
        "dir": "08-graphs",
        "snippets": {
            "bfs": [
                ("python/traversal.py", "py"),
                ("java/GraphTraversal.java", "java"),
                ("c/traversal.c", "c"),
            ],
            "dfs": [
                ("python/traversal.py", "py"),
                ("java/GraphTraversal.java", "java"),
                ("c/traversal.c", "c"),
            ],
            "dfs-iterative": [
                ("python/dfs_iterative.py", "py"),
                ("java/DfsIterative.java", "java"),
                ("c/dfs_iterative.c", "c"),
            ],
            "topo-kahn": [
                ("python/topological_sort.py", "py"),
                ("java/TopologicalSort.java", "java"),
                ("c/topological_sort.c", "c"),
            ],
            "topo-dfs": [
                ("python/topological_sort.py", "py"),
                ("java/TopologicalSort.java", "java"),
                ("c/topological_sort.c", "c"),
            ],
            "disjoint-set": [
                ("python/disjoint_set.py", "py"),
                ("java/DisjointSet.java", "java"),
                ("c/disjoint_set.c", "c"),
            ],
            "prim": [
                ("python/mst.py", "py"),
                ("java/MinimumSpanningTree.java", "java"),
                ("c/mst.c", "c"),
            ],
            "kruskal": [
                ("python/mst.py", "py"),
                ("java/MinimumSpanningTree.java", "java"),
                ("c/mst.c", "c"),
            ],
            "dijkstra": [
                ("python/shortest_paths.py", "py"),
                ("java/ShortestPaths.java", "java"),
                ("c/shortest_paths.c", "c"),
            ],
            "bellman-ford": [
                ("python/shortest_paths.py", "py"),
                ("java/ShortestPaths.java", "java"),
                ("c/shortest_paths.c", "c"),
            ],
            "reconstruct-path": [
                ("python/shortest_paths.py", "py"),
                ("java/ShortestPaths.java", "java"),
                ("c/shortest_paths.c", "c"),
            ],
            "dag-shortest-paths": [
                ("python/dag_shortest_paths.py", "py"),
                ("java/DagShortestPaths.java", "java"),
                ("c/dag_shortest_paths.c", "c"),
            ],
        },
    },
    "07": {
        "dir": "07-hash-tables",
        "snippets": {
            "string-hash": [
                ("python/string_hash.py", "py"),
                ("java/StringHash.java", "java"),
                ("c/string_hash.c", "c"),
            ],
            "chained-hash-table": [
                ("python/chained_hash_table.py", "py"),
                ("java/ChainedHashMap.java", "java"),
                ("c/chained_hash_table.c", "c"),
            ],
            "open-address-hash-table": [
                ("python/open_address_hash_table.py", "py"),
                ("java/OpenAddressHashMap.java", "java"),
                ("c/open_address_hash_table.c", "c"),
            ],
            # Java-only: the mutable-key hazard is a java.util.HashMap
            # contract failure (equals/hashCode-relevant field mutated while
            # the key is in the table) -- source material and CODE_INVENTORY
            # only ever show this in Java, not C/Python (see chapters/07.inventory).
            "mutable-key-example": [
                ("java/MutableKeyExample.java", "java"),
            ],
        },
    },
    # See chapters/09.inventory §(c). All 4 algorithms live in ONE shared
    # library file per language (string_matching.py/StringMatchers.java/
    # string_matching.c), matching how the source itself is organized --
    # each snippet extracts just that algorithm's marked region, same as
    # L03's sorting.py packing multiple sorts with separate markers.
    "09": {
        "dir": "09-string-matching",
        "snippets": {
            "naive-match": [
                ("python/string_matching.py", "py"),
                ("java/StringMatchers.java", "java"),
                ("c/string_matching.c", "c"),
            ],
            "rabin-karp": [
                ("python/string_matching.py", "py"),
                ("java/StringMatchers.java", "java"),
                ("c/string_matching.c", "c"),
            ],
            "kmp": [
                ("python/string_matching.py", "py"),
                ("java/StringMatchers.java", "java"),
                ("c/string_matching.c", "c"),
            ],
            "horspool": [
                ("python/string_matching.py", "py"),
                ("java/StringMatchers.java", "java"),
                ("c/string_matching.c", "c"),
            ],
        },
    },
    # See chapters/10.inventory §(c). All 6 core algorithms live in ONE
    # shared library file per language (state_space_search.py; C is split
    # into per-algorithm files matching lecture-notes/code/lecture10/c's own
    # file layout; Java is split into per-algorithm Solver classes matching
    # lecture-notes/code/lecture10/java's own layout). graph-coloring's C
    # file is new (the source has none -- see chapters/10.inventory (c)),
    # and permutation.c's ss_combination_count is also new (the source only
    # ported ChoosePermutation to C, not ChooseCombination).
    "10": {
        "dir": "10-state-space-search",
        "snippets": {
            "permutation-combination": [
                ("python/state_space_search.py", "py"),
                ("java/PermutationGenerator.java", "java"),
                ("c/permutation.c", "c"),
            ],
            "place-n-queens": [
                ("python/state_space_search.py", "py"),
                ("java/NQueensSolver.java", "java"),
                ("c/n_queens.c", "c"),
            ],
            "subset-sum": [
                ("python/state_space_search.py", "py"),
                ("java/SubsetSumSolver.java", "java"),
                ("c/subset_sum.c", "c"),
            ],
            "color-graph-coloring": [
                ("python/state_space_search.py", "py"),
                ("java/GraphColoringSolver.java", "java"),
                ("c/graph_coloring.c", "c"),
            ],
            "knapsack-bnb": [
                ("python/state_space_search.py", "py"),
                ("java/KnapsackBranchAndBound.java", "java"),
                ("c/knapsack_bnb.c", "c"),
            ],
            "a-star": [
                ("python/state_space_search.py", "py"),
                ("java/AStarGrid.java", "java"),
                ("c/a_star_grid.c", "c"),
            ],
            # Java-only, optional (\ssoptional) supplementary example -- the
            # source has no C port either (see chapters/10.inventory (c)),
            # and this isn't one of the 6 core algorithms in ALGORITHM_CONFIG
            # (no 3-language cross-check needed), same treatment as L07's
            # mutable-key-example.
            "arithmetic-progression": [
                ("java/ArithmeticProgressionSearch.java", "java"),
            ],
        },
    },
}


def marker_pattern(name):
    # matches either '#' (Python) or '//' (Java/C) comment style
    start = re.compile(r"^[ \t]*(?:#|//)\s*snippet:%s:start\s*$" % re.escape(name), re.MULTILINE)
    end = re.compile(r"^[ \t]*(?:#|//)\s*snippet:%s:end\s*$" % re.escape(name), re.MULTILINE)
    return start, end


def extract(text, name):
    start_re, end_re = marker_pattern(name)
    start_m = start_re.search(text)
    if not start_m:
        return None, "no 'snippet:%s:start' marker found" % name
    end_m = end_re.search(text, start_m.end())
    if not end_m:
        return None, "no 'snippet:%s:end' marker found after start" % name
    body = text[start_m.end() : end_m.start()]
    # drop exactly one leading/trailing blank line left by the marker lines
    body = body.strip("\n") + "\n"
    return body, None


def process_lecture(lecture, check_only):
    cfg = SNIPPET_CONFIG[lecture]
    code_dir = REPO_ROOT / "code" / cfg["dir"]
    out_dir = REPO_ROOT / "figures" / cfg["dir"]

    written, missing = [], []
    for name, sources in cfg["snippets"].items():
        for rel_path, ext in sources:
            src_path = code_dir / rel_path
            out_path = out_dir / ("snippet-%s.%s" % (name, ext))
            if not src_path.exists():
                missing.append("%s (source missing: %s)" % (out_path.name, src_path))
                continue
            text = src_path.read_text(encoding="utf-8")
            body, err = extract(text, name)
            if err:
                missing.append("%s (%s: %s)" % (out_path.name, src_path, err))
                continue
            if check_only:
                if not out_path.exists() or out_path.read_text(encoding="utf-8") != body:
                    missing.append("%s (stale or missing)" % out_path.name)
                continue
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path.write_text(body, encoding="utf-8")
            written.append(out_path.name)

    return written, missing


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lecture", default="03", help="lecture number, e.g. 03 (default: 03)")
    parser.add_argument("--check", action="store_true", help="report status without writing files")
    args = parser.parse_args()

    if args.lecture not in SNIPPET_CONFIG:
        print("extract_code_snippets.py: no config for lecture %s" % args.lecture)
        sys.exit(1)

    written, missing = process_lecture(args.lecture, args.check)

    print("extract_code_snippets.py --lecture %s%s" % (args.lecture, " --check" if args.check else ""))
    print("  written: %d" % len(written))
    print("  missing/stale: %d" % len(missing))
    for m in missing:
        print("    %s" % m)

    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
