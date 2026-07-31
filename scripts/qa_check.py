#!/usr/bin/env python3
"""Headless quality gates for a rendered chapter (docs/QUALITY_ASSURANCE.md).

Currently implements:
  - Gate 3 (일부): source `algorithmic` block count == rendered pseudocode.js
    block count (".ps-root" elements actually present in the DOM after JS
    runs, not just how many <pre class="pseudocode"> placeholders exist in
    the static HTML -- a block that fails to render client-side must fail
    this gate, not silently pass because the placeholder tag is present).
  - Gate 6 (일부): inline code (`code:not(pre code)`) contrast >= 4.5:1,
    computed from the browser's actual resolved color/background-color
    (not the source SCSS values, which can differ once Bootstrap/Quarto's
    own cascade rules -- e.g. the $code-bg == $gray-100 fallback -- are
    applied). Also covers every distinct syntax-highlighting token color
    (one per Pandoc/Skylighting token class: comment, keyword, string, ...)
    used inside fenced code blocks, against that code block's actual
    background -- a highlight-style chosen for a *different* background
    than $code-block-bg can leave specific token classes (observed:
    comments) under 4.5:1 even when most tokens are fine.
  - Gate 4 (일부): every fenced code block (div.sourceCode, whether a plain
    block or a panel-tabset pane, active or not) must have non-empty
    rendered content. Catches `{.lang include="path"}` code-fence attributes
    that Quarto/Pandoc silently treats as an inert data-include passthrough
    (never actually inlining the file) instead of the working
    `{{< include path >}}` shortcode placed *inside* the fence.
  - Gate 4, section-scoped (SECTION_GATES): for an algorithm with its own
    isolated section (e.g. 1.3.1 Selection Sort's C/Java/Python
    panel-tabset), on top of the page-wide empty-block check above, this
    also verifies -- scoped to *that section's* DOM subtree only -- that all
    3 languages are present and non-empty, that none of another algorithm's
    identifiers (insertion/bubble/merge sort names) leaked into it, and
    (delegating to run_examples.py's own ALGORITHM_CONFIG pass rather than
    re-implementing compilation) that the 3 languages actually
    compiled/ran and their outputs agree.
  - Internal doc-name leak check: fails if the rendered page's visible body
    text contains an internal repo document name (SPEC, PER_LECTURE_NOTES,
    CODE_INVENTORY, DECISIONS.md, etc.) -- a correction belongs in the
    chapter on its own merits, not cited back to the internal tracking doc
    it came from.
  - Leaked-heading-marker check: fails if visible text outside <pre>/<code>
    contains a literal "##" (a `## heading` inside a fenced div, e.g. a
    step-sequence panel-tabset, that lacked a blank line before the next
    block does not parse as Markdown -- it survives as raw text glued onto
    the previous block), or if any `.tab-pane` contains more than one
    `<img>` (the same underlying bug's other symptom: multiple step images
    landing crammed into a single tab instead of one per tab).

Gates 1/2/5/7 from docs/QUALITY_ASSURANCE.md are NOT implemented here yet
(tracked for M2 per docs/MILESTONES.md); this script does not claim to check
them. It also reports raw-math leakage, broken images, missing alt text, and
console/request errors as a side effect of the same page load, since the
browser_check.mjs pass already collects them, but only gates 3, 4, and 6
affect the exit code.

Requires Node.js + the Playwright browser (see scripts/qa/package.json):
    cd scripts/qa && npm install && npx playwright install chromium
If that isn't set up, this script reports exactly that and exits non-zero --
it does not report gates as passed when it could not actually run them.
"""
import argparse
import http.server
import json
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
QA_DIR = REPO_ROOT / "scripts" / "qa"

CONTRAST_MINIMUM = 4.5

LECTURE_CHAPTER = {
    "01": {"lecture_notes_dir": "lecture01", "chapter_html": "chapters/01-introduction.html"},
    "02": {"lecture_notes_dir": "lecture02", "chapter_html": "chapters/02-recursion.html"},
    "03": {"lecture_notes_dir": "lecture03", "chapter_html": "chapters/03-sorting.html"},
    "04": {"lecture_notes_dir": "lecture04", "chapter_html": "chapters/04-selection.html"},
    "05": {"lecture_notes_dir": "lecture05", "chapter_html": "chapters/05-dynamic-programming.html"},
    "06": {"lecture_notes_dir": "lecture06", "chapter_html": "chapters/06-search-trees.html"},
    "07": {"lecture_notes_dir": "lecture07", "chapter_html": "chapters/07-hash-tables.html"},
    "08": {"lecture_notes_dir": "lecture08", "chapter_html": "chapters/08-graphs.html"},
    "09": {"lecture_notes_dir": "lecture09", "chapter_html": "chapters/09-string-matching.html"},
    "10": {"lecture_notes_dir": "lecture10", "chapter_html": "chapters/10-state-space-search.html"},
}

# Per-lecture, per-language identifiers for every from-scratch algorithm with
# its own section (used to build each section's "forbidden" list below: every
# OTHER algorithm's identifiers *in that lecture*, since finding them inside
# this algorithm's section means the tabset is showing more than just its
# own code).
ALGO_IDENTIFIERS = {
    "03": {
        "selection-sort": ["selection_sort", "SelectionSort", "selectionSort"],
        "bubble-sort": ["bubble_sort", "BubbleSort", "bubbleSort"],
        "insertion-sort": ["insertion_sort", "InsertionSort", "insertionSort"],
        "merge-sort": ["merge_sort", "MergeSort", "mergeSort"],
        "quick-sort": ["quick_sort", "QuickSort", "quickSort", "partition"],
        "heap-sort": [
            "heap_sort", "HeapSort", "heapSort",
            "max_heapify", "MaxHeapify", "maxHeapify",
            "build_max_heap", "BuildMaxHeap", "buildMaxHeap",
        ],
        "counting-sort": ["counting_sort", "CountingSort", "countingSort"],
        "radix-sort": ["radix_sort", "RadixSort", "radixSort"],
    },
    "01": {
        "maximum": ["maximum", "Maximum"],
        "linear-search": ["linear_search", "LinearSearch", "linearSearch"],
        "binary-search": ["binary_search", "BinarySearch", "binarySearch"],
    },
    "02": {
        "sum": ["sum"],
        "hanoi": ["hanoi", "Hanoi"],
        "recursive-binary-search": ["bsearch"],
        "maze": ["find_path", "findPath"],
        "power-set": ["power_set", "powerSet", "PowerSet"],
    },
    # Part A's SelectBySorting gets its own H3 (L01/L03-style, self-contained,
    # no further split), while Part B/C/D each dedicate a whole H2 Part to one
    # algorithm (Quickselect/RandomizedSelect/DeterministicSelect, L02-style --
    # see SECTION_ID below, ids confirmed against the actually-rendered
    # _book/chapters/04-selection.html, not guessed from the .qmd headings).
    # "partition3" is deliberately excluded: RandomizedSelect and
    # DeterministicSelect each carry their own independent private copy of a
    # 3-way partition helper (matching how lecture-notes/code/lecture04's own
    # canonical C files duplicate it rather than share it) -- that's parallel
    # structure, not cross-algorithm contamination, so listing it as an
    # exclusive identifier for either would false-positive on the other.
    "04": {
        "select-by-sorting": ["select_by_sorting", "selectBySorting", "SelectBySorting"],
        "fixed-quickselect": ["fixed_quickselect", "fixedQuickselect", "FixedQuickselect", "partition"],
        "randomized-select": ["randomized_select", "randomizedSelect", "RandomizedSelect"],
        "deterministic-select": [
            "deterministic_select", "deterministicSelect", "DeterministicSelect",
            "select_range", "selectRange",
        ],
    },
    # L06's five sections each get a whole Part (H2) to themselves (see
    # SECTION_ID below). "inorder"/"contains"/"height" are deliberately
    # excluded -- every one of the five tree types legitimately implements
    # its own inorder traversal and contains/height helper, so listing them
    # here would false-positive as "contamination" between every pair of
    # sections. "rotate_left"/"rotate_right" are similarly excluded: AVL and
    # Red-Black both have their own rotation helper by that name.
    # "transplant"/"Transplant" is excluded too: BST's delete and
    # Red-Black's delete each carry their own independent transplant-style
    # helper (matching how CLRS's own RB-DELETE reuses the TRANSPLANT
    # concept by name) -- parallel structure, not cross-algorithm
    # contamination, confirmed by an actual gate-4 false-positive during
    # this lecture's QA pass.
    "06": {
        "binary-tree": ["BinaryTree", "preorder", "postorder", "levelorder", "levelOrder", "level_order"],
        "binary-search-tree": ["BinarySearchTree", "successor", "predecessor"],
        "avl-tree": ["AVLTree", "rebalance", "avl_insert"],
        "red-black-tree": [
            "RedBlackTree", "insertFixup", "insert_fixup", "deleteFixup", "delete_fixup",
        ],
        "btree": [
            "BTree", "splitChild", "split_child", "borrowPrev", "borrow_prev",
            "borrowNext", "borrow_next",
        ],
    },
    # L05's four representative algorithms each get their own H3 subsection,
    # but (unlike L01-03) that subsection can hold *two* ALGORITHM_CONFIG
    # demos together (e.g. Matrix Path's memo and bottom-up code+output
    # panels both live under the same "Matrix Minimum Path Sum" H3) -- these
    # are code identifiers (function/class names), not the algorithm's
    # display name, so a generic word like "LCS" appearing in Part E's
    # cross-algorithm comparison prose can't false-positive here.
    "05": {
        "fibonacci": [
            "fibMemo", "fibBottomUp", "FibonacciDP", "memoRec",
            "fib_memo", "fib_bottom_up", "memo_rec",
        ],
        "matrix-path": [
            "minPathMemo", "minPathBottomUp", "MinPathSum",
            "min_path_memo", "min_path_bottom_up", "min_path_memo_rec",
        ],
        "lcs": ["lcsBottomUp", "lcs_bottom_up"],
        "max-subarray": [
            "maxSubarrayBruteForce", "maxSubarrayKadane", "MaximumSubarray",
            "max_subarray_brute_force", "max_subarray_kadane",
        ],
    },
    # L08's 12 run_examples.py slugs collapse into 6 sections (each section
    # can hold multiple slugs' code, same reasoning as L05's shared
    # sections) -- keys here are the section-scoped conceptual group, not
    # the individual slug. Identifiers are actual class/function names from
    # the code (not display names like "BFS"/"Dijkstra", which appear as
    # ordinary words throughout this chapter's prose and comparison tables
    # -- word-boundary matching on those would false-positive constantly).
    "08": {
        "bfs": ["graph_bfs", "BFSResult"],
        "dfs": [
            "graph_dfs", "DFSResult", "dfsIterative", "dfs_iterative",
            "graph_dfs_iterative", "DfsIterative",
        ],
        "topological-sort": [
            "TopologicalSort", "graph_topological_kahn", "graph_topological_dfs",
            "topo_dfs", "topo_visit", "topo_kahn",
        ],
        "mst": [
            "MinimumSpanningTree", "graph_prim", "graph_kruskal",
            "DisjointSet", "dsu_init", "dsu_find", "dsu_union",
        ],
        "dag-shortest-paths": [
            "DagShortestPaths", "graph_dag_shortest_paths", "dag_shortest_paths",
        ],
        "shortest-paths": [
            "ShortestPaths", "graph_dijkstra", "graph_bellman_ford",
            "bellmanFord", "bellman_ford", "graph_reconstruct_path",
            "reconstruct_path",
        ],
    },
    # L07's 3 ALGORITHM_CONFIG entries each get their own H2 Part (see
    # SECTION_ID below). "mutable-key-example" (Java-only, no run_examples.py
    # ALGORITHM_CONFIG entry -- see chapters/07.inventory §c) deliberately has
    # no key here since SECTION_GATES/PIPELINE_ALGORITHMS iterate this dict to
    # build the 3-language pipeline gate, and that demo is single-language by
    # design, not a gate omission.
    "07": {
        "string-hash": ["StringHash", "string_hash", "ascii_sum", "asciiSum"],
        "chained-hash-table": [
            "ChainedHashMap", "ChainedHashTable", "chained_hash_table",
            "chain_put", "chain_get", "chain_remove", "bucket_chain", "bucketChain", "chain_bucket",
        ],
        "open-address-hash-table": [
            "OpenAddressHashMap", "OpenAddressHashTable", "open_address_hash_table",
            "open_put", "open_get", "open_remove", "findIndex", "find_index",
        ],
    },
    # L09's 4 ALGORITHM_CONFIG entries each get a whole H2 Part to themselves
    # (see SECTION_ID below). All 4 share one library file per language
    # (string_matching.py/StringMatchers.java/string_matching.c, matching the
    # source's own organization -- see chapters/09.inventory §c), but each
    # snippet include extracts only that algorithm's own marked region, so
    # there is no natural cross-reference between them to exclude (unlike
    # L06's shared inorder/height or L04's partition3).
    "09": {
        "naive-match": ["naive_match", "naiveAll", "sm_naive_all", "NaiveMatchDemo"],
        "rabin-karp": ["rabin_karp", "rabinKarp", "sm_rabin_karp_all", "RabinKarpDemo"],
        "kmp": [
            "build_lps", "buildLps", "sm_build_lps",
            "kmp_search", "kmpSearch", "sm_kmp_all", "KmpDemo",
        ],
        "horspool": [
            "build_horspool_shift", "buildHorspoolShift", "sm_build_horspool_shift",
            "horspool_search", "horspoolSearch", "sm_horspool_all", "HorspoolDemo",
        ],
    },
    # L10's 6 ALGORITHM_CONFIG entries: permutation-combination lives in its
    # own H3 inside Part A; place-n-queens/subset-sum/color-graph-coloring
    # are 3 sibling H3s inside Part B (not nested in each other, so no
    # cross-scoping risk); knapsack-bnb and a-star each live directly under
    # their own whole H2 Part (D and E) with no dedicated H3 (see SECTION_ID
    # below). arithmetic-progression (Java-only, optional/\ssoptional -- see
    # chapters/10.inventory (c)) has no run_examples.py ALGORITHM_CONFIG
    # entry, so it's deliberately excluded here too (same reasoning as L07's
    # mutable-key-example).
    "10": {
        "permutation-combination": [
            "choose_permutation", "choosePermutation", "ChoosePermutation",
            "choose_combination", "chooseCombination", "ChooseCombination",
            "PermutationGenerator", "ss_permutation_count", "ss_combination_count",
        ],
        "place-n-queens": ["solve_n_queens", "NQueensSolver", "ss_n_queens_count"],
        "subset-sum": ["subset_sum", "SubsetSumSolver", "ss_subset_sum_masks"],
        "color-graph-coloring": ["color_graph", "GraphColoringSolver", "ss_color_graph"],
        "knapsack-bnb": ["knapsack_bnb", "KnapsackBranchAndBound", "ss_knapsack_bnb"],
        "a-star": ["a_star_grid", "AStarGrid", "ss_astar_grid"],
    },
}

# lecture -> algorithm name (matches run_examples.py's ALGORITHM_CONFIG keys)
# -> the rendered <section id="..."> slug Quarto derives from that heading's
# text (mostly identical, except L03 Heapsort's heading has no space/dash).
SECTION_ID = {
    "03": {
        "selection-sort": "selection-sort",
        "bubble-sort": "bubble-sort",
        "insertion-sort": "insertion-sort",
        "merge-sort": "merge-sort",
        "quick-sort": "quick-sort",
        "heap-sort": "heapsort",
        "counting-sort": "counting-sort",
        "radix-sort": "radix-sort",
    },
    # L01 introduces Linear/Binary Search early (Part D: problem, pseudocode,
    # trace) but -- matching the lecture's own deferral of complexity to
    # after asymptotic notation is introduced -- their "구현" panel-tabset
    # lives later, alongside their complexity analysis (Part H), under a
    # "...의 복잡도" heading rather than the intro section's own id.
    "01": {
        "maximum": "maximum의-복잡도",
        "linear-search": "linear-search의-복잡도",
        "binary-search": "binary-search의-복잡도",
    },
    # L02's three representative algorithms each get their own H2 Part (no
    # further H3 split), so the code panel-tabset lives directly in that
    # Part's own section id.
    "02": {
        "sum": "part-b.-재귀의-실행-호출-스택",
        "hanoi": "part-h.-hanoi",
        "recursive-binary-search": "part-g.-재귀적으로-문제-설계하기",
        "maze": "part-i.-미로-탐색maze과-backtracking",
        "power-set": "part-k.-멱집합power-set",
    },
    # Confirmed against the actually-rendered _book/chapters/04-selection.html
    # section ids. Part B/C/D's ids are the whole H2 Part's own id (Quarto
    # nests each Part's H3 subsections -- 실행-추적, 복잡도, etc. -- as child
    # <section> elements inside it), since each Part's single algorithm's
    # code panel lives in one of those H3 subsections rather than in a
    # dedicated per-algorithm H3 of its own (matching L02's whole-Part
    # pattern here, not L01/L03's per-algorithm-H3 pattern).
    "04": {
        "select-by-sorting": "가장-단순한-해법-selectbysorting",
        "fixed-quickselect": "part-b.-quickselect",
        "randomized-select": "part-c.-randomized-selection의-성능",
        "deterministic-select": "part-d.-deterministic-linear-selection-median-of-medians",
    },
    # Confirmed against the actually-rendered _book/chapters/05-dynamic-programming.html
    # H3 ids (Quarto's Korean-safe slugger), not guessed from the .qmd headings.
    "05": {
        "fibonacci": "tabulation-bottom-up",
        "matrix-path": "matrix-minimum-path-sum",
        "lcs": "longest-common-subsequence-lcs",
        "max-subarray": "maximum-subarray-kadanes-algorithm",
    },
    # Confirmed against the actually-rendered _book/chapters/06-search-trees.html
    # section ids -- each of the five representative algorithms gets a whole
    # H2 Part to itself (matching L02/L04's whole-Part pattern), so the id is
    # that Part's own id, not a nested per-algorithm H3.
    "06": {
        "binary-tree": "part-c.-traversal",
        "binary-search-tree": "part-g.-bst-insert와-delete",
        "avl-tree": "part-i.-avl-tree",
        "red-black-tree": "part-j.-red-black-tree",
        "btree": "part-k.-b-tree",
    },
    # Confirmed against the actually-rendered _book/chapters/08-graphs.html
    # H2/H3 ids, not guessed from the .qmd headings.
    "08": {
        "bfs": "part-c.-bfs",
        "dfs": "part-d.-dfs",
        "topological-sort": "part-f.-topological-sort",
        "mst": "part-j.-kruskal과-disjoint-set",
        "dag-shortest-paths": "part-m.-unweighteddag-shortest-paths",
        "shortest-paths": "part-o.-bellmanford-algorithm",
    },
    # Confirmed against the actually-rendered _book/chapters/07-hash-tables.html
    # section ids, not guessed from the .qmd headings. Each of L07's 3
    # ALGORITHM_CONFIG entries gets a whole H2 Part to itself, matching
    # L02/L04/L06's whole-Part pattern (open-address-hash-table's demo lives
    # in Part K, which covers both deletion and the implementation demo
    # together -- see chapters/07-hash-tables.qmd).
    "07": {
        "string-hash": "part-d.-integer와-string-hashing",
        "chained-hash-table": "part-f.-separate-chaining",
        "open-address-hash-table": "part-k.-삭제와-구현",
    },
    # Confirmed against the actually-rendered _book/chapters/09-string-matching.html
    # section ids, not guessed from the .qmd headings. Each of L09's 4
    # ALGORITHM_CONFIG entries gets a whole H2 Part to itself.
    "09": {
        "naive-match": "part-b.-naive-matching",
        "rabin-karp": "part-g.-rabin-karp-분석과-활용",
        "kmp": "part-l.-kmp-search",
        "horspool": "part-p.-boyer-moore-horspool",
    },
    # Confirmed against the actually-rendered _book/chapters/10-state-space-search.html
    # section ids, not guessed from the .qmd headings. permutation-combination/
    # place-n-queens/subset-sum/color-graph-coloring each live in their own H3
    # (the id comes from the heading text, not the algorithm key); knapsack-bnb
    # and a-star have no dedicated H3 and live directly under their own whole
    # H2 Part (matching L02/L04's whole-Part pattern).
    "10": {
        "permutation-combination": "순열과-조합-생성",
        "place-n-queens": "n-queens",
        "subset-sum": "subset-sum",
        "color-graph-coloring": "graph-coloring",
        "knapsack-bnb": "part-d.-01-knapsack-branch-and-bound",
        "a-star": "part-e.-a-search",
    },
}

# lecture -> conceptual section name -> list of run_examples.py
# ALGORITHM_CONFIG slugs whose pipeline must pass for that section. Defaults
# to [name] itself (see SECTION_GATES below) for lectures where each section
# holds exactly one ALGORITHM_CONFIG entry (L01-03); L05 sections can hold
# two (e.g. Matrix Path's memo + bottom-up demos share one H3).
PIPELINE_ALGORITHMS = {
    "05": {
        "fibonacci": ["fib-memo", "fib-bottom-up"],
        "matrix-path": ["min-path-memo", "matrix-bottom-up"],
        "lcs": ["lcs-bottom-up"],
        "max-subarray": ["max-subarray-brute-force", "max-subarray-kadane"],
    },
    "08": {
        "bfs": ["bfs"],
        "dfs": ["dfs", "dfs-iterative"],
        "topological-sort": ["topo-kahn", "topo-dfs"],
        "mst": ["prim", "kruskal", "disjoint-set"],
        "dag-shortest-paths": ["dag-shortest-paths"],
        "shortest-paths": ["dijkstra", "bellman-ford", "reconstruct-path"],
    },
}

# lecture -> conceptual section name -> identifiers it's allowed to
# reference despite belonging to another group -- L08's DAG Shortest Paths
# genuinely, intentionally builds on both Topological Sort (calls
# TopologicalSort.kahn/graph_topological_kahn to get the evaluation order)
# and the shared shortest-path infrastructure (reuses ShortestPaths.INF as
# its sentinel) rather than duplicating either, matching the
# DAGShortestPaths pseudocode's own \Call{TopologicalSort}{G}. That's real
# architectural reuse, not copy-paste contamination, so it's an explicit
# exception rather than a reason to weaken the identifiers themselves.
ALLOWED_CROSS_REFERENCES = {
    "08": {
        "dag-shortest-paths": ["TopologicalSort", "graph_topological_kahn", "ShortestPaths"],
    },
}

# Algorithms with their own isolated C/Java/Python section (panel-tabset),
# per ADR-004 / run_examples.py's ALGORITHM_CONFIG.
SECTION_GATES = {
    lecture: [
        {
            "section_id": SECTION_ID[lecture][algo],
            "algorithms": PIPELINE_ALGORITHMS.get(lecture, {}).get(algo, [algo]),
            "languages": ["python", "java", "c"],
            "forbidden": [
                ident
                for other, idents in ALGO_IDENTIFIERS[lecture].items()
                if other != algo
                for ident in idents
                if ident not in ALLOWED_CROSS_REFERENCES.get(lecture, {}).get(algo, [])
            ],
        }
        for algo in ALGO_IDENTIFIERS[lecture]
    ]
    for lecture in ALGO_IDENTIFIERS
}


def check_algorithm_pipeline(lecture, algo_name):
    """Delegate to run_examples.py's own compile/run/output-match check for
    one ALGORITHM_CONFIG entry, instead of re-implementing gcc/javac/python3
    invocation here."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import run_examples as run_mod  # local import: scripts/ is not normally on sys.path

    cfg = run_mod.ALGORITHM_CONFIG[lecture]
    code_dir = REPO_ROOT / "code" / cfg["dir"]
    out_dir = REPO_ROOT / "figures" / cfg["dir"]
    build_dir = REPO_ROOT / "figures" / ".cache" / "run_examples" / lecture
    build_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    results = run_mod.process_algorithms(lecture, code_dir, out_dir, build_dir)
    return results.get(algo_name)


def source_algorithmic_count(lecture):
    """Expected number of distinct rendered pseudocode.js blocks -- delegates
    to convert_pseudocode.py's own PSEUDOCODE_CONFIG-aware count rather than
    a raw `\\begin{algorithmic}` tally, since merge_algorithmic_bodies can
    fold more than one source block into a single rendered slug (e.g. L04's
    DeterministicSelect, split across two source frames but rendered as one
    continuous listing) -- a raw count would over-count against what the
    page actually renders in that case."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import convert_pseudocode as cp  # local import: scripts/ is not normally on sys.path

    return cp.expected_rendered_count(lecture)


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass  # this is a throwaway server for the QA browser pass, not worth the request-log noise


def serve_book(book_dir, port):
    handler = lambda *args, **kwargs: _QuietHandler(*args, directory=str(book_dir), **kwargs)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


def run_browser_check(url):
    if shutil.which("node") is None:
        return None, "node is not installed/on PATH"
    node_modules = QA_DIR / "node_modules" / "playwright"
    if not node_modules.exists():
        return None, (
            "scripts/qa/node_modules/playwright is missing -- run "
            "`cd scripts/qa && npm install && npx playwright install chromium` first"
        )
    result = subprocess.run(
        ["node", str(QA_DIR / "browser_check.mjs"), url],
        cwd=str(QA_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=90,
    )
    if result.returncode != 0:
        return None, "browser_check.mjs failed:\n" + result.stderr
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError as e:
        return None, "browser_check.mjs did not print valid JSON: %s\n%s" % (e, result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lecture", default="03", help="lecture number, e.g. 03 (default: 03)")
    parser.add_argument("--book-dir", default="_book", help="rendered Quarto output dir (default: _book)")
    parser.add_argument("--port", type=int, default=8971, help="local port to serve --book-dir on")
    args = parser.parse_args()

    if args.lecture not in LECTURE_CHAPTER:
        print("qa_check.py: no chapter config for lecture %s" % args.lecture)
        sys.exit(1)
    cfg = LECTURE_CHAPTER[args.lecture]

    book_dir = REPO_ROOT / args.book_dir
    chapter_path = book_dir / cfg["chapter_html"]
    if not chapter_path.exists():
        print("qa_check.py: %s does not exist -- run `quarto render` first" % chapter_path)
        sys.exit(1)

    expected = source_algorithmic_count(args.lecture)

    httpd = serve_book(book_dir, args.port)
    try:
        url = "http://127.0.0.1:%d/%s" % (args.port, cfg["chapter_html"])
        facts, err = run_browser_check(url)
    finally:
        httpd.shutdown()

    print("qa_check.py --lecture %s" % args.lecture)

    if err:
        print("  UNABLE TO RUN: %s" % err)
        print("  (not reporting gate 3 / gate 6 as passed -- they did not run)")
        sys.exit(1)

    ok = True

    # Gate 3: source algorithmic count == rendered pseudocode block count.
    rendered = facts["renderedPseudocodeCount"]
    unrendered = facts["unrenderedPseudocodeCount"]
    gate3_pass = rendered == expected and unrendered == 0
    print("  gate 3 (pseudocode block count): source=%d rendered=%d unrendered=%d -> %s"
          % (expected, rendered, unrendered, "PASS" if gate3_pass else "FAIL"))
    ok = ok and gate3_pass

    # Gate 3 (continued): a rendered .ps-root can still show raw, unrendered
    # macro text (e.g. `\Call{name}{args}` left inside a math span, which
    # MathJax doesn't know how to typeset and passes through literally --
    # the L05 bug convert_pseudocode.py's hoist_call_out_of_math exists to
    # prevent). Gate 3 above only counts *whether* a block rendered, not
    # what's inside it, so this is a separate check on the same facts.
    macro_leaks = facts.get("rawPseudocodeMacroLeaks", [])
    macro_leak_ok = len(macro_leaks) == 0
    print("  gate 3 (no raw pseudocode macro leaks in rendered blocks): -> %s"
          % ("PASS" if macro_leak_ok else "FAIL"))
    for leak in macro_leaks:
        print("    LEAK in .ps-root[%d]: %r" % (leak["index"], leak["sample"]))
    ok = ok and macro_leak_ok

    # Internal doc-name / production-jargon leak check: SPEC.md/
    # PER_LECTURE_NOTES.md/etc. must never be cited in reader-facing prose
    # (a correction stands on its own merits; the internal tracking doc it
    # came from is not the reader's business) -- and neither should
    # build-pipeline jargon like TikZ/SVG/pgfplots/`\only` (an author-facing
    # "how this figure was made" note, same failure mode as citing an
    # internal doc). Scoped to the rendered page's visible body text.
    internal_refs = facts.get("internalDocRefs", [])
    internal_ok = len(internal_refs) == 0
    print("  internal doc-name / production jargon references: %s -> %s"
          % (internal_refs if internal_refs else "none", "PASS" if internal_ok else "FAIL"))
    ok = ok and internal_ok

    # Leaked-heading-marker check: a `## heading` immediately followed by
    # another block with no blank line between them in the .qmd source
    # (e.g. inside a step-sequence panel-tabset) doesn't parse as Markdown
    # inside a fenced div -- it survives as literal "## heading" text glued
    # onto the previous block, and any images meant for separate tabs land
    # crammed into one pane instead (exactly what happened to L01's
    # Linear/Binary Search step-sequence tabsets before this gate existed).
    leaked_headings = facts.get("leakedHeadingMarkers", [])
    multi_image_panes = facts.get("multiImageTabPanes", [])
    markup_leak_ok = len(leaked_headings) == 0 and len(multi_image_panes) == 0
    print("  trace figure markup (no leaked ## / no multi-image tab panes): -> %s"
          % ("PASS" if markup_leak_ok else "FAIL"))
    for sample in leaked_headings:
        print("    LEAKED HEADING TEXT: %r" % sample)
    for pane in multi_image_panes:
        print("    MULTI-IMAGE PANE: id=%s imgCount=%d" % (pane["id"], pane["imgCount"]))
    ok = ok and markup_leak_ok

    # Gate 6: inline code contrast >= 4.5:1.
    samples = facts.get("inlineCodeSamples", [])
    if not samples:
        print("  gate 6 (inline code contrast): no inline code found on page -> PASS (vacuous)")
    else:
        gate6_pass = True
        for s in samples:
            c = s.get("contrast")
            status = "PASS" if (c is not None and c >= CONTRAST_MINIMUM) else "FAIL"
            if status == "FAIL":
                gate6_pass = False
            print('  gate 6 (inline code contrast): "%s" color=%s bg=%s contrast=%s -> %s'
                  % (s["text"], s["color"], s["backgroundColor"],
                     ("%.2f:1" % c) if c is not None else "unknown", status))
        ok = ok and gate6_pass

    # Gate 6 (continued): syntax-highlighting token contrast >= 4.5:1, one
    # check per distinct (token class, color, background) combination
    # actually present in the rendered code blocks (Python/Java/C tabs and
    # everything else), including inactive tabset panes.
    token_samples = facts.get("codeTokenSamples", [])
    if not token_samples:
        print("  gate 6 (code token contrast): no syntax-highlighted tokens found -> PASS (vacuous)")
    else:
        gate6b_pass = True
        failing = []
        for t in token_samples:
            c = t.get("contrast")
            if c is None or c < CONTRAST_MINIMUM:
                gate6b_pass = False
                failing.append(t)
        print("  gate 6 (code token contrast): %d distinct token style(s) checked, %d below %.1f:1 -> %s"
              % (len(token_samples), len(failing), CONTRAST_MINIMUM, "PASS" if gate6b_pass else "FAIL"))
        for t in failing:
            c = t.get("contrast")
            print('    LOW CONTRAST: class=%s color=%s bg=%s contrast=%s sample=%r'
                  % (t["cls"], t["color"], t["backgroundColor"],
                     ("%.2f:1" % c) if c is not None else "unknown", t["sample"]))
        ok = ok and gate6b_pass

    # Gate 4: no empty fenced code blocks (the include="path" attribute bug).
    code_blocks = facts.get("codeBlocks", [])
    if not code_blocks:
        print("  gate 4 (empty code blocks): no fenced code blocks found on page -> PASS (vacuous)")
    else:
        empty = [b for b in code_blocks if b["length"] == 0]
        gate4_pass = len(empty) == 0
        print("  gate 4 (empty code blocks): %d code block(s) checked, %d empty -> %s"
              % (len(code_blocks), len(empty), "PASS" if gate4_pass else "FAIL"))
        for b in empty:
            print("    EMPTY: id=%s lang=%s" % (b["id"], b["lang"]))
        ok = ok and gate4_pass

    # Gate 4, section-scoped: presence of all 3 languages, no cross-algorithm
    # contamination, and (via run_examples.py) actual compile/run + output
    # match, all scoped to one algorithm's own section.
    section_facts = {f["id"]: f for f in facts.get("sectionFacts", [])}
    for gate_cfg in SECTION_GATES.get(args.lecture, []):
        sid = gate_cfg["section_id"]
        label = "gate 4 (section #%s)" % sid
        sf = section_facts.get(sid)

        if sf is None or not sf.get("found"):
            print("  %s: section not found on rendered page -> FAIL" % label)
            ok = False
            continue

        missing_langs = [
            lang for lang in gate_cfg["languages"]
            if sf["languages"].get(lang, {}).get("length", 0) == 0
        ]
        langs_pass = len(missing_langs) == 0
        print("  %s: languages=%s missing=%s -> %s"
              % (label, gate_cfg["languages"], missing_langs, "PASS" if langs_pass else "FAIL"))
        ok = ok and langs_pass

        full_text = sf.get("fullText", "")
        # Word-boundary match, not substring: radix sort's own
        # `counting_sort_by_digit` helper legitimately contains
        # "counting_sort" as a substring without being that section's code.
        contamination = [
            term for term in gate_cfg["forbidden"]
            if re.search(r"\b%s\b" % re.escape(term), full_text)
        ]
        contam_pass = len(contamination) == 0
        print("  %s: no other-algorithm code -> %s%s"
              % (label, "PASS" if contam_pass else "FAIL",
                 (" (found: %s)" % contamination) if contamination else ""))
        ok = ok and contam_pass

        for algo_name in gate_cfg["algorithms"]:
            sub_label = "%s [%s]" % (label, algo_name)
            pipeline = check_algorithm_pipeline(args.lecture, algo_name)
            if pipeline is None:
                print("  %s: no run_examples.py ALGORITHM_CONFIG entry for '%s' -> FAIL"
                      % (sub_label, algo_name))
                ok = False
                continue
            compile_run_pass = all(lang_ok for lang_ok, _ in pipeline["per_language"].values())
            print("  %s: compile/run (c/java/python) -> %s" % (sub_label, "PASS" if compile_run_pass else "FAIL"))
            ok = ok and compile_run_pass
            print("  %s: 3-language output match -> %s" % (sub_label, "PASS" if pipeline["outputs_match"] else "FAIL"))
            ok = ok and pipeline["outputs_match"]

    # Side-effect reporting (not gated on yet, see module docstring).
    if facts["hasRawMath"]:
        print("  [info] raw math text detected in rendered page (gate 1 would fail)")
    if facts["brokenImgs"]:
        print("  [info] broken images: %s" % facts["brokenImgs"])
    if facts["missingAltImgs"]:
        print("  [info] images missing alt text: %s" % facts["missingAltImgs"])
    if facts["horizontalOverflow"]:
        print("  [info] horizontal overflow detected")
    if facts["consoleErrors"]:
        print("  [info] console errors: %s" % facts["consoleErrors"])
    if facts["failedRequests"]:
        print("  [info] failed requests: %s" % facts["failedRequests"])

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
