#!/usr/bin/env python3
"""Extract TikZ/pgfplots figures from lecture-notes sections into standalone SVGs.

Pipeline (SPEC 4.4): for each lecture, scan lecture-notes/lectureNN/sections/*.tex
for `tikzpicture`/`axis` (pgfplots) blocks, compile each as a standalone document
(lualatex) reusing the lecture's own TikZ styles, convert to SVG with dvisvgm,
and cache by content hash so unchanged figures are not recompiled. Cache misses
compile in parallel (multiprocessing.Pool, see default_worker_count() and
--jobs) -- needed for lectures with many figures (L06 has ~60, by far the
most of any lecture) to keep build time manageable.

`\\only<N>` overlays are flattened to their final state by default. A small,
lecture-specific FIGURE_CONFIG can mark specific figures as "sequence" instead,
rendering one SVG per overlay step (used for the 1-2 pedagogically key figures
per Milestone 1, e.g. the Selection Sort pass trace and the Merge two-pointer
trace) instead of a single flattened image.

NOTE ON THE STANDALONE PREAMBLE: lecture-notes/theme/beamerthemealgorithms.sty
calls `\\usetheme{metropolis}`, `\\setbeamercolor`, etc. -- all beamer-only
commands -- so it cannot be \\usepackage'd into a `standalone`-class document.
Only its `\\definecolor` lines (the actual palette the TikZ styles reference)
are reproduced below; everything else (TikZ styles, Korean font handling via
kotex) comes from `lecture_common_block()`: lectures that keep their
`\\tikzset{...}` in a dedicated `lectureNN/common.tex` (e.g. L03) get it via
`\\input`; lectures that define it inline in `lectureNN.tex`'s own preamble
instead (e.g. L01, which has no common.tex at all) get those tikzset/newcommand
blocks extracted and reproduced literally.
"""
import argparse
import hashlib
import json
import multiprocessing
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LECTURE_NOTES = REPO_ROOT / "lecture-notes"
CACHE_DIR = REPO_ROOT / "figures" / ".cache" / "tikz-build"

TIKZ_RE = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.DOTALL)
AXIS_RE = re.compile(r"\\begin\{axis\}.*?\\end\{axis\}", re.DOTALL)
# \visible<SPEC>{BODY} (cumulative reveal, used by L02's call-stack "push"
# figure) has the exact same single-branch, brace-balanced shape as
# \only<SPEC>{BODY} and the same lo<=target<=hi semantics work for both here
# (we're picking one flattened/sequence target state, not reproducing
# beamer's live progressive-reveal layout), so one regex/one set of
# functions (find_only_blocks/render_only_at) handles both.
ONLY_HEAD_RE = re.compile(r"\\(?:only|visible)<([^>]*)>")
ALT_HEAD_RE = re.compile(r"\\alt<([^>]*)>|alt=<([^>]*)>")

# Per-lecture "whole-picture" macros that expand to a complete
# `\begin{tikzpicture}...\end{tikzpicture}` themselves, defined once in a
# common/*.tex file -- so a usage site in a section file has no literal
# tikzpicture/axis text for TIKZ_RE/AXIS_RE to find at all. L06's
# `\travtree{#1}...{#7}` (common/search_trees.tex) draws a fixed 7-node tree
# with one style-override argument per node; its three animation frames in
# 03_traversal.tex call it several times in a row -- one call per
# *already-resolved* state (not one tikzpicture with `\only` overlays inside
# it) -- and its comparison frame once. Keyed by lecture -> {macro name:
# argument count}.
MACRO_PICTURES = {
    "06": {"travtree": 7},
    # \htrowthirteen{13-value comma list} and \loadgauge{ratio}{label1}{label2}
    # (lecture-notes/common/hash_tables.tex) are the same "macro definition
    # itself contains a full \begin{tikzpicture}" shape as L06's \travtree --
    # a hash-table row / a load-factor bar drawn fresh per call site, not an
    # \only-wrapped span of one shared picture.
    "07": {"htrowthirteen": 1, "loadgauge": 3},
}
FRAME_START_RE = re.compile(r"\\begin\{frame\}")

PREAMBLE = r"""\documentclass[border=4pt]{standalone}
\usepackage{kotex}
\usepackage{xcolor}
%% Palette from lecture-notes/theme/beamerthemealgorithms.sty (colors only --
%% see the module docstring for why the theme itself can't be reused here).
\definecolor{AlgoBlue}{HTML}{102A43}
\definecolor{AlgoBlueTwo}{HTML}{243B53}
\definecolor{AlgoOrange}{HTML}{F08C46}
\definecolor{AlgoGray}{HTML}{627D98}
\definecolor{AlgoLight}{HTML}{F5F7FA}
\definecolor{AlgoRule}{HTML}{D9E2EC}
\definecolor{AlgoOrangeText}{HTML}{B45309}
\definecolor{AlgoGrayText}{HTML}{586F86}
\usepackage{amsmath,amssymb,mathtools}
\usepackage{array}
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usetikzlibrary{arrows.meta,positioning,calc,fit,trees,patterns,decorations.pathreplacing,matrix,shapes.multipart}
%(common_block)s
\begin{document}
%(body)s
\end{document}
"""

# Lecture-specific figure metadata: which tikzpicture (by 0-based index within
# its section file, in document order) gets which output slug, and whether it
# should be flattened to a single final-state SVG or rendered as a step
# sequence. Figures not listed default to flatten with an auto-generated slug.
FIGURE_CONFIG = {
    "03": {
        ("01_motivation.tex", 0): {"slug": "01-sorting-roadmap"},
        ("02_sorting_properties.tex", 0): {"slug": "02-stability-demo"},
        ("03_selection.tex", 0): {"slug": "03-selection-trace", "mode": "sequence"},
        ("04_bubble.tex", 0): {"slug": "04-bubble-trace"},
        ("05_insertion.tex", 0): {"slug": "05-insertion-cards"},
        ("05_insertion.tex", 1): {"slug": "05-insertion-trace"},
        ("07_merge_sort.tex", 0): {"slug": "07-merge-divide"},
        ("07_merge_sort.tex", 1): {"slug": "07-merge-pointers", "mode": "sequence"},
        ("07_merge_sort.tex", 2): {"slug": "07-merge-recursion-tree"},
        ("08_quick_sort.tex", 0): {"slug": "08-quick-partition-trace"},
        ("09_lower_bound.tex", 0): {"slug": "09-decision-tree"},
        ("10_heap_basics.tex", 0): {"slug": "10-heap-array-tree"},
        ("11_heapify.tex", 0): {"slug": "11-heapify-trace"},
        ("12_build_heap.tex", 0): {"slug": "12-build-heap-trace"},
        ("13_heap_sort.tex", 0): {"slug": "13-heapsort-trace"},
        ("14_counting_sort.tex", 0): {"slug": "14-counting-sort-trace"},
        ("15_radix_sort.tex", 0): {"slug": "15-radix-trace"},
        ("19_summary_quiz.tex", 0): {"slug": "19-concept-map"},
    },
    "01": {
        ("01_motivation.tex", 0): {"slug": "01-coin-change"},
        ("01_motivation.tex", 1): {"slug": "02-scale-growth"},
        ("02_algorithm_program.tex", 0): {"slug": "03-algorithm-io"},
        ("02_algorithm_program.tex", 1): {"slug": "04-spec-algorithm-program"},
        ("02_algorithm_program.tex", 2): {"slug": "05-design-steps"},
        ("05_maximum.tex", 0): {"slug": "06-maximum-trace"},
        ("06_linear_search.tex", 0): {"slug": "07-linear-search-trace", "mode": "sequence"},
        ("07_binary_search.tex", 0): {"slug": "08-binary-search-sorted"},
        ("07_binary_search.tex", 1): {"slug": "09-binary-search-trace", "mode": "sequence"},
        # pgfplots (nested inside an outer tikzpicture in the source; find_figures()
        # de-duplicates the redundant inner axis span, see its docstring).
        ("09_orders_of_growth.tex", 0): {"slug": "10-growth-curves"},
        ("10_asymptotic_notation.tex", 0): {"slug": "11-bigo-intuition"},
        ("10_asymptotic_notation.tex", 1): {"slug": "12-oh-omega-theta"},
        ("12_summary_quiz.tex", 0): {"slug": "13-concept-map"},
    },
    "02": {
        # docs/REVIEW_NOTES.md #11: source is \visible<2->/\visible<3-> (no
        # explicit <1>), so overlay_steps() only sees boundaries {2,3} --
        # "steps" overrides with the true 3-frame sequence (see the
        # "steps" override comment in process_lecture above).
        ("02_execution.tex", 0): {"slug": "01-call-stack-push", "mode": "sequence", "steps": [1, 2, 3]},
        ("02_execution.tex", 1): {"slug": "02-call-stack-pop", "mode": "sequence"},
        ("04_basic_examples.tex", 0): {"slug": "03-fibonacci-tree"},
        ("05_recurrences.tex", 0): {"slug": "04-recursion-tree"},
        ("06_master_theorem.tex", 0): {"slug": "05-master-theorem-competition"},
        ("07_recursive_thinking.tex", 0): {"slug": "06-binary-search-reduction", "mode": "sequence"},
        ("08_hanoi.tex", 0): {"slug": "07-hanoi-rules"},
        ("08_hanoi.tex", 1): {"slug": "08-hanoi-n3-states", "mode": "sequence"},
        ("08_hanoi.tex", 2): {"slug": "09-hanoi-recursion-tree"},
        ("09_maze.tex", 0): {"slug": "10-maze-trace", "mode": "sequence"},
        ("10_blob.tex", 0): {"slug": "11-blob-neighbors"},
        ("10_blob.tex", 1): {"slug": "12-blob-floodfill", "mode": "sequence"},
        ("11_power_set.tex", 0): {"slug": "13-power-set-tree"},
        ("13_summary_quiz.tex", 0): {"slug": "14-concept-map"},
    },
    # See chapters/05.inventory §2 for the full index-by-index derivation.
    # Three of the sixteen are the DP-table-filling traces the user's L05
    # prompt calls out by name (memoization trace, bottom-up table
    # progression) -- these render as overlay sequences, same as L01/L02's
    # step-by-step search/sort traces, so the trace doesn't collapse to one
    # flattened final-state image. The LCS "table progression" is NOT in this
    # config or in the 16-figure count: it's a bare `\only{...}` around a
    # `tabular`, not a tikzpicture, so TIKZ_RE never matches it -- that trace
    # is hand-authored as three plain Quarto tables in the qmd instead of an
    # SVG sequence (see chapters/05.inventory §2 note).
    "05": {
        ("01_motivation.tex", 0): {"slug": "01-roadmap"},
        ("01_motivation.tex", 1): {"slug": "02-recurrence-memo-tab"},
        ("02_fibonacci.tex", 0): {"slug": "03-fib-call-tree"},
        ("03_memoization_tabulation.tex", 0): {"slug": "04-memo-trace", "mode": "sequence"},
        ("03_memoization_tabulation.tex", 1): {"slug": "05-bottomup-trace", "mode": "sequence"},
        ("06_optimal_substructure.tex", 0): {"slug": "06-greedy-counterexample-local"},
        ("06_optimal_substructure.tex", 1): {"slug": "07-greedy-counterexample-optimal"},
        ("05_matrix_path.tex", 0): {"slug": "08-matrix-dependency"},
        ("05_matrix_path.tex", 1): {"slug": "09-matrix-call-tree"},
        ("05_matrix_path.tex", 2): {"slug": "10-matrix-row-progression", "mode": "sequence"},
        ("05_matrix_path.tex", 3): {"slug": "11-matrix-representative-cell", "text_patch": "matrix_representative_cell_chosen_label"},
        ("05_matrix_path.tex", 4): {"slug": "12-matrix-reconstruction", "patch": "matrix_reconstruction_path_contrast"},
        ("07_lcs.tex", 0): {"slug": "13-lcs-case1"},
        ("07_lcs.tex", 1): {"slug": "14-lcs-call-tree"},
        ("08_lcs_reconstruction.tex", 0): {"slug": "15-lcs-backtrack-trace"},
        ("11_summary_quiz.tex", 0): {"slug": "16-concept-map"},
    },
    # See chapters/04.inventory §2 for the full index-by-index derivation.
    "04": {
        ("01_motivation.tex", 0): {"slug": "01-roadmap"},
        ("02_order_statistics.tex", 0): {"slug": "02-rank-vs-index"},
        ("03_sort_then_select.tex", 0): {"slug": "03-quicksort-vs-quickselect"},
        ("04_quickselect_idea.tex", 0): {"slug": "04-pivot-subarray-rank"},
        ("04_quickselect_idea.tex", 1): {"slug": "05-right-rank-reason"},
        ("05_quickselect_trace.tex", 0): {"slug": "06-common-first-partition"},
        ("05_quickselect_trace.tex", 1): {"slug": "07-fixed-pivot-trace", "mode": "sequence"},
        ("05_quickselect_trace.tex", 2): {"slug": "08-randomized-trace", "mode": "sequence"},
        ("07_quickselect_analysis.tex", 0): {"slug": "09-geometric-series"},
        ("10_group_of_five.tex", 0): {"slug": "10-groups-of-five"},
        ("10_group_of_five.tex", 1): {"slug": "11-median-of-medians-trace", "mode": "sequence"},
        ("11_pivot_guarantee.tex", 0): {"slug": "12-median-half-guarantee"},
        ("11_pivot_guarantee.tex", 1): {"slug": "13-group-three-guarantee"},
        ("14_summary_quiz.tex", 0): {"slug": "14-concept-map"},
    },
    # See chapters/08.inventory §2 for the full index-by-index derivation.
    # This lecture has the most sequence traces of any lecture so far (13,
    # 59 SVGs total) -- BFS queue, DFS recursion stack, Kahn zero-heap, DFS
    # topo finish-order, Prim key updates, Kruskal accept/reject, Dijkstra
    # finalized set, and more all need one SVG per overlay step so the
    # trace doesn't collapse to a single flattened final-state image.
    # See chapters/06.inventory §2 for the full index-by-index derivation.
    # By far the most figure-dense lecture (60 entries / ~72 SVGs) -- see
    # default_worker_count()/--jobs for the parallel compile this needs.
    # Two overlay mechanisms unique to this lecture: 03_traversal.tex's
    # \travtree{}x7 (MACRO_PICTURES above) and the `alt=<N>{style}{style}`
    # tikz-key form (ALT_HEAD_RE) used in 01_tree_basics.tex/11_btree.tex.
    # AVL/RB/B-Tree "before/after" pairs and triples are each a SEPARATE
    # literal tikzpicture (its own \only wraps the *whole* picture, not an
    # \only span inside one shared picture) -- so unlike this dict's usual
    # "mode": "sequence" pattern, each one is its own flatten-mode entry
    # with a descriptive step suffix baked into its own slug.
    "06": {
        ("01_tree_basics.tex", 0): {"slug": "01-rooted-tree-definition"},
        ("01_tree_basics.tex", 1): {"slug": "02-tree-terminology-trace", "mode": "sequence"},
        ("02_binary_tree.tex", 0): {"slug": "03-left-child-example"},
        ("02_binary_tree.tex", 1): {"slug": "04-right-child-example"},
        ("02_binary_tree.tex", 2): {"slug": "05-full-perfect-complete"},
        ("02_binary_tree.tex", 3): {"slug": "06-linked-representation"},
        ("03_traversal.tex", 0): {"slug": "07-traversal-reference-tree"},
        ("03_traversal.tex", 1): {"slug": "08-preorder-trace"},
        ("03_traversal.tex", 2): {"slug": "09-inorder-trace"},
        ("03_traversal.tex", 3): {"slug": "10-postorder-trace"},
        ("03_traversal.tex", 4): {"slug": "11-level-order-reference-tree"},
        ("03_traversal.tex", 5): {"slug": "12-expression-tree"},
        ("06_bst_search.tex", 0): {"slug": "13-fixed-bst-example"},
        ("06_bst_search.tex", 1): {"slug": "14-search-trace", "mode": "sequence", "text_patch": "trace_orienting_annotation_font"},
        ("06_bst_search.tex", 2): {"slug": "15-successor-cases", "mode": "sequence", "full_override": "successor_merged_tree"},
        # Was "16-successor-case2-ancestor-chain": its content is now fully
        # absorbed into idx 2's merged tree above (see the
        # "successor_merged_tree" FULL_BODY_PATCHES comment), so this source
        # tikzpicture no longer gets its own extracted figure at all.
        ("06_bst_search.tex", 3): {"skip": True},
        ("07_bst_insert_delete.tex", 0): {"slug": "17-insert-trace", "mode": "sequence", "text_patch": "trace_orienting_annotation_font"},
        ("07_bst_insert_delete.tex", 1): {"slug": "18-delete-case1-leaf", "mode": "sequence"},
        ("07_bst_insert_delete.tex", 2): {"slug": "19-delete-case2-one-child", "mode": "sequence"},
        ("07_bst_insert_delete.tex", 3): {"slug": "20-delete-case3-successor-setup"},
        ("07_bst_insert_delete.tex", 4): {"slug": "21-delete-case3-final-tree"},
        ("08_balanced_motivation.tex", 0): {"slug": "22-degenerate-bst-trace", "mode": "sequence"},
        ("09_avl.tex", 0): {"slug": "23-right-rotation-before"},
        ("09_avl.tex", 1): {"slug": "24-right-rotation-after"},
        ("09_avl.tex", 2): {"slug": "25-ll-case-before"},
        ("09_avl.tex", 3): {"slug": "26-ll-case-after"},
        ("09_avl.tex", 4): {"slug": "27-rr-case-before"},
        ("09_avl.tex", 5): {"slug": "28-rr-case-after"},
        ("09_avl.tex", 6): {"slug": "29-lr-case-step1"},
        ("09_avl.tex", 7): {"slug": "30-lr-case-step2"},
        ("09_avl.tex", 8): {"slug": "31-lr-case-step3"},
        ("09_avl.tex", 9): {"slug": "32-rl-case-step1"},
        ("09_avl.tex", 10): {"slug": "33-rl-case-step2"},
        ("09_avl.tex", 11): {"slug": "34-rl-case-step3"},
        ("10_red_black.tex", 0): {"slug": "35-nil-sentinel"},
        ("10_red_black.tex", 1): {"slug": "36-invariant-violation-example"},
        ("10_red_black.tex", 2): {"slug": "37-rb-case1-before"},
        ("10_red_black.tex", 3): {"slug": "38-rb-case1-after"},
        ("10_red_black.tex", 4): {"slug": "39-rb-insert-41-38-31-step1"},
        ("10_red_black.tex", 5): {"slug": "40-rb-insert-41-38-31-step2"},
        ("10_red_black.tex", 6): {"slug": "41-rb-insert-41-38-31-step3"},
        ("10_red_black.tex", 7): {"slug": "42-rb-insert-12-before"},
        ("10_red_black.tex", 8): {"slug": "43-rb-insert-12-after"},
        ("10_red_black.tex", 9): {"slug": "44-rb-insert-19-step1"},
        ("10_red_black.tex", 10): {"slug": "45-rb-insert-19-step2"},
        ("10_red_black.tex", 11): {"slug": "46-rb-insert-8-final"},
        ("11_btree.tex", 0): {"slug": "47-multiway-range-invariant"},
        ("11_btree.tex", 1): {"slug": "48-btree-search-trace", "mode": "sequence"},
        ("11_btree.tex", 2): {"slug": "49-btree-insert-step1"},
        ("11_btree.tex", 3): {"slug": "50-btree-insert-step2"},
        ("11_btree.tex", 4): {"slug": "51-btree-insert-step3"},
        ("11_btree.tex", 5): {"slug": "52-btree-insert-step4"},
        ("11_btree.tex", 6): {"slug": "53-btree-insert2-step1"},
        ("11_btree.tex", 7): {"slug": "54-btree-insert2-step2"},
        ("11_btree.tex", 8): {"slug": "55-btree-final-check"},
        ("11_btree.tex", 9): {"slug": "56-btree-borrow-before"},
        ("11_btree.tex", 10): {"slug": "57-btree-borrow-after"},
        ("11_btree.tex", 11): {"slug": "58-btree-merge-before"},
        ("11_btree.tex", 12): {"slug": "59-btree-merge-after"},
        ("13_summary_quiz.tex", 0): {"slug": "60-concept-map"},
    },
    "08": {
        ("01_graph_basics.tex", 0): {"slug": "01-graph-definition"},
        ("02_representation.tex", 0): {"slug": "02-matrix-direction"},
        ("02_representation.tex", 1): {"slug": "03-matrix-to-list", "mode": "sequence"},
        ("03_bfs.tex", 0): {"slug": "04-bfs-graph"},
        # These three are pure text-stack traces (no graph diagram sharing
        # the canvas, unlike Prim/Dijkstra/Kruskal/back-edge, which embed
        # their pq/callout boxes *alongside* a vertex diagram and are left
        # alone) -- the shared common/graph_algorithms.tex `pq`/`callout`
        # styles' inner sep (2mm/3mm) is generous enough that, with nothing
        # else on the canvas to fill, 2-3 short single-line boxes stacked
        # with the source's 1cm-unit vertical spacing render taller than
        # their content needs. TIKZ_PATCH (see below, applied only to these
        # three figures' own copy of the raw body, never to the read-only
        # lecture-notes/ source or the shared style) tightens both the
        # padding and the inter-box gap without touching any other figure.
        ("03_bfs.tex", 1): {"slug": "05-bfs-queue-trace", "mode": "sequence", "patch": "trace_stack"},
        ("03_bfs.tex", 2): {"slug": "06-bfs-path-reconstruction"},
        ("04_dfs.tex", 0): {"slug": "07-dfs-recursion-trace", "mode": "sequence", "patch": "trace_stack"},
        ("05_cycle_detection.tex", 0): {"slug": "08-back-edge-animation", "mode": "sequence"},
        ("06_topological_sort.tex", 0): {"slug": "09-kahn-trace", "mode": "sequence", "patch": "trace_stack"},
        ("06_topological_sort.tex", 1): {"slug": "10-kahn-cycle-detection"},
        ("06_topological_sort.tex", 2): {"slug": "11-dfs-topo-finish-reverse", "mode": "sequence"},
        ("08_cut_property.tex", 0): {"slug": "12-cut-crossing-edge"},
        ("09_prim.tex", 0): {"slug": "13-prim-trace", "mode": "sequence"},
        ("10_kruskal.tex", 0): {"slug": "14-dsu-animation", "mode": "sequence"},
        ("10_kruskal.tex", 1): {"slug": "15-kruskal-trace", "mode": "sequence"},
        ("11_mst_comparison.tex", 0): {"slug": "16-mst-tie-square"},
        ("12_shortest_path_intro.tex", 0): {"slug": "17-relaxation-animation", "mode": "sequence"},
        ("13_unweighted_dag.tex", 0): {"slug": "18-bfs-weighted-counterexample"},
        ("13_unweighted_dag.tex", 1): {"slug": "19-dag-relaxation-trace", "mode": "sequence"},
        ("14_dijkstra.tex", 0): {"slug": "20-dijkstra-trace", "mode": "sequence"},
        ("14_dijkstra.tex", 1): {"slug": "21-dijkstra-negative-counterexample"},
        ("15_bellman_ford.tex", 0): {"slug": "22-bellman-ford-negative-cycle", "mode": "sequence"},
    },
    # See chapters/07.inventory §(e) for the full index-by-index derivation.
    # 01_motivation/12_load_factor/14_implementation/15_comparison/
    # 16_summary_quiz/17_appendix have no tikzpicture/axis/macro figure at
    # all (tables and lstlisting only) and so contribute no keys here.
    # Two `\htrowthirteen`/`\loadgauge` macro-call figures (MACRO_PICTURES
    # above) are interleaved with literal tikzpicture/axis figures in
    # document order within 05_collision/08_linear_probing/11_deletion --
    # find_figures() sorts all three kinds together by source position, so
    # the index below is that combined order, not a per-kind index.
    "07": {
        ("02_hashing_model.tex", 0): {"slug": "01-hash-pipeline", "text_patch": "hash_pipeline_label_overlap"},
        ("02_hashing_model.tex", 1): {"slug": "02-hash-candidate-bucket"},
        ("03_hash_functions.tex", 0): {"slug": "03-distribution-comparison"},
        # \alt=<1..4>{style}{style} on 4 nodes -- a genuine 4-step trace
        # (each alt highlights the node just computed), not a single final
        # state, so this is a sequence like L06's alt-based traces.
        ("04_string_hashing.tex", 0): {"slug": "04-multiplication-trace", "mode": "sequence"},
        ("04_string_hashing.tex", 1): {"slug": "05-prefix-collision"},
        ("05_collision.tex", 0): {"slug": "06-original-integer-table"},  # macro:htrowthirteen
        ("05_collision.tex", 1): {"slug": "07-insert-29-collision-trace", "mode": "sequence"},
        ("05_collision.tex", 2): {"slug": "08-pigeonhole-principle"},
        ("06_chaining.tex", 0): {"slug": "09-chaining-structure"},
        ("06_chaining.tex", 1): {"slug": "10-chaining-insert-trace", "mode": "sequence", "text_patch": "chaining_insert_step1_edge_target"},
        ("06_chaining.tex", 2): {"slug": "11-chaining-search-delete-trace", "mode": "sequence"},
        ("06_chaining.tex", 3): {"slug": "12-chaining-worst-case"},
        # 07_open_addressing.tex: \htlegend (arity-0, three bare-\tikz
        # snippets, no \begin{tikzpicture} at all) is intentionally NOT in
        # MACRO_PICTURES -- its EMPTY/OCCUPIED/DELETED legend duplicates the
        # \begin{description} text right below it in the same frame, so it's
        # covered by prose instead of a rendered figure (chapters/07.inventory §e).
        # \htrowthirteen IS called once in this file though (the "왜 첫
        # Tombstone에 즉시 쓰지 않는가?" example row) -- must not be missed.
        ("07_open_addressing.tex", 0): {"slug": "13-tombstone-reuse-example"},  # macro:htrowthirteen
        ("08_linear_probing.tex", 0): {"slug": "14-linear-trace1-collision", "mode": "sequence"},
        ("08_linear_probing.tex", 1): {"slug": "15-linear-trace2-wraparound", "mode": "sequence", "text_patch": "linear_trace2_wrap_arrow_target"},
        ("08_linear_probing.tex", 2): {"slug": "16-linear-final-table"},  # macro:htrowthirteen
        ("08_linear_probing.tex", 3): {"slug": "17-primary-clustering", "mode": "sequence"},
        ("08_linear_probing.tex", 4): {"slug": "18-linear-probe-cost-curve"},  # pgfplots axis
        ("09_quadratic_probing.tex", 0): {"slug": "19-quadratic-trace-30", "mode": "sequence"},
        ("09_quadratic_probing.tex", 1): {"slug": "20-secondary-clustering"},
        ("10_double_hashing.tex", 0): {"slug": "21-double-hash-probe-trace", "mode": "sequence"},
        ("10_double_hashing.tex", 1): {"slug": "22-double-hash-gcd-failure"},
        ("11_deletion.tex", 0): {"slug": "23-probe-cluster-before-delete"},  # macro:htrowthirteen
        ("11_deletion.tex", 1): {"slug": "24-wrong-deletion-trace", "mode": "sequence"},
        ("11_deletion.tex", 2): {"slug": "25-correct-deletion-tombstone-trace", "mode": "sequence"},
        # \loadgauge{...} called twice in the same frame (logical then
        # probing load) -- group_macro_calls_by_frame groups them into one
        # 2-state figure, same as any other macro-call sequence.
        ("11_deletion.tex", 3): {"slug": "26-logical-vs-probing-load"},  # macro:loadgauge x2
        ("13_rehashing.tex", 0): {"slug": "27-rehash-animation", "mode": "sequence"},
        ("13_rehashing.tex", 1): {"slug": "28-resize-cost-sequence"},
    },
    # See chapters/09.inventory §(e) for the full index-by-index derivation.
    # No MACRO_PICTURES entry needed: \smrow/\smindices/\smshiftrow
    # (lecture-notes/common/string_matching.tex) are \node-drawing helpers
    # used *inside* an existing tikzpicture, not whole-picture macros like
    # L06's \travtree/L07's \htrowthirteen. No pgfplots axis in this lecture
    # either. 01_problem/03_redundancy/10_lps_table/13_kmp_analysis/
    # 17_comparison/18_implementation/19_summary_quiz/20_appendix have no
    # tikzpicture at all (tables/formulas/text only) -- 19_summary_quiz in
    # particular has no concept-map figure in the source (unlike L06/L07),
    # so the web chapter doesn't invent one.
    "09": {
        ("02_naive.tex", 0): {"slug": "01-naive-alignment-trace", "mode": "sequence"},
        ("02_naive.tex", 1): {"slug": "02-naive-worst-case-repeated-prefix", "mode": "sequence"},
        ("04_rabin_karp_intro.tex", 0): {"slug": "03-numeric-encoding-cad", "mode": "sequence"},
        # Static (no \only overlay), unlike its idx0 sibling.
        ("04_rabin_karp_intro.tex", 1): {"slug": "04-hash-equality-insufficient"},
        ("05_rolling_hash.tex", 0): {"slug": "05-rolling-update-derivation", "mode": "sequence"},
        # Static flow diagram (remove -> multiply -> add), no \only overlay.
        ("05_rolling_hash.tex", 1): {"slug": "06-rolling-update-flow"},
        ("06_modular_collision.tex", 0): {"slug": "07-collision-is-candidate", "mode": "sequence"},
        ("07_rabin_karp_analysis.tex", 0): {"slug": "08-candidate-to-valid-hit", "mode": "sequence"},
        ("08_border.tex", 0): {"slug": "09-prefix-lps-discovery", "mode": "sequence"},
        ("09_kmp_idea.tex", 0): {"slug": "10-mismatch-fallback-trace", "mode": "sequence"},
        ("11_kmp_preprocessing.tex", 0): {"slug": "11-lps-construction-trace", "mode": "sequence"},
        ("12_kmp_search.tex", 0): {"slug": "12-kmp-mismatch-recovery-trace", "mode": "sequence"},
        ("12_kmp_search.tex", 1): {"slug": "13-kmp-overlapping-match", "mode": "sequence"},
        ("14_boyer_moore_intro.tex", 0): {"slug": "14-right-to-left-comparison", "mode": "sequence"},
        ("15_bad_character.tex", 0): {"slug": "15-tiger-shift-table", "mode": "sequence"},
        ("15_bad_character.tex", 1): {"slug": "16-absent-character-shift", "mode": "sequence"},
        ("16_horspool.tex", 0): {"slug": "17-rational-repeated-character", "mode": "sequence"},
        ("16_horspool.tex", 1): {"slug": "18-horspool-trace-tiger", "mode": "sequence"},
    },
    # See chapters/10.inventory §(e) for the full index-by-index derivation.
    # No MACRO_PICTURES entry needed: \prunetriangle (lecture-notes/common/
    # state_space.tex) is a \node-drawing helper used inside an existing
    # tikzpicture, same shape as L09's \smrow -- not a whole-picture macro.
    # No pgfplots either. 13_comparison/14_implementation/15_summary_quiz/
    # 16_appendix have no tikzpicture at all (tables/text only) -- no
    # concept-map figure in the source (same as L09), so none is invented.
    "10": {
        ("01_state_space_basics.tex", 0): {"slug": "01-state-space-tree-structure"},
        ("02_exhaustive_search.tex", 0): {"slug": "02-state-space-expansion", "mode": "sequence"},
        ("02_exhaustive_search.tex", 1): {"slug": "03-dfs-bfs-visit-order", "mode": "sequence"},
        ("03_permutation_combination.tex", 0): {"slug": "04-permutation-state-tree", "mode": "sequence"},
        ("04_backtracking.tex", 0): {"slug": "05-apply-undo-symmetry", "mode": "sequence"},
        # 6-step (matches content map's "N-Queens 6단계").
        ("05_n_queens.tex", 0): {"slug": "06-four-queens-board-trace", "mode": "sequence"},
        ("05_n_queens.tex", 1): {"slug": "07-four-queens-partial-tree"},
        ("06_subset_sum.tex", 0): {"slug": "08-subset-sum-include-exclude-tree"},
        ("06_subset_sum.tex", 1): {"slug": "09-subset-sum-trace", "mode": "sequence"},
        # 4-step (matches content map's "coloring 4단계").
        ("07_graph_coloring.tex", 0): {"slug": "10-graph-coloring-trace", "mode": "sequence"},
        ("08_arithmetic_progression.tex", 0): {"slug": "11-arithmetic-progression-trace", "mode": "sequence"},
        ("09_branch_and_bound.tex", 0): {"slug": "12-bound-based-pruning", "mode": "sequence"},
        # 7-step (matches content map's "Knapsack ... 7단계").
        ("10_knapsack_bnb.tex", 0): {"slug": "13-knapsack-best-first-trace", "mode": "sequence"},
        ("10_knapsack_bnb.tex", 1): {"slug": "14-knapsack-state-tree"},
        ("11_search_orders.tex", 0): {"slug": "15-frontier-policy-animation", "mode": "sequence"},
        ("12_a_star.tex", 0): {"slug": "16-astar-grid-heuristic"},
        # 6-step (matches content map's "A* OPEN/CLOSED 6단계").
        ("12_a_star.tex", 1): {"slug": "17-astar-open-closed-trace", "mode": "sequence"},
        # 3-step (matches content map's "path reconstruction 3단계").
        ("12_a_star.tex", 2): {"slug": "18-astar-path-reconstruction", "mode": "sequence"},
    },
}

# Named per-figure TikZ patches (FIGURE_CONFIG's "patch" key), applied to a
# figure's own raw tikzpicture body -- a build-time text transform on our own
# copy, never an edit to the read-only lecture-notes/ source or to the
# shared common/graph_algorithms.tex tikzset (which would also reshape the
# same styles used by Prim/Dijkstra/Kruskal/Bellman-Ford's diagram-embedded
# pq/callout boxes -- see the "08" FIGURE_CONFIG comment above). Each entry
# is (options-to-merge-into-the-tikzpicture-header, tikzset-override-to-
# insert-right-after-it).
TIKZ_PATCHES = {
    # yscale tightens the 1cm-unit vertical gap the source hardcodes between
    # the 2-3 stacked state-text nodes; .append style shrinks just `inner
    # sep`/`font` on top of the existing pq/callout definitions (draw color,
    # fill, rounded corners, border weight all carry over unchanged).
    "trace_stack": (
        "yscale=0.62",
        "\\tikzset{pq/.append style={inner sep=0.8mm,font=\\footnotesize},"
        "callout/.append style={inner sep=0.8mm,font=\\footnotesize}}",
    ),
    # 05_matrix_path.tex's "최소 경로 Reconstruction" figure
    # ("12-matrix-reconstruction", docs/REVIEW_NOTES.md #1): the path arrows
    # (`dp path` style) are drawn cell-edge-to-cell-edge, and at the source's
    # y=.85cm row spacing (cell height 8mm) that leaves only ~0.5mm of
    # vertical gap for the down-arrows -- barely enough room for anything
    # more than the arrowhead itself, plus `dp path`'s AlgoOrange draw color
    # is the same color as the orange highlight-box border each arrow
    # crosses, so it visually merges into it. `y=1cm` (appended after the
    # figure's own `x=1.15cm,y=.85cm`, pgfkeys last-write-wins) opens the gap
    # to ~2mm, matching the horizontal gap; `dp path` is only ever used in
    # this one figure (grep confirms), so redefining it here doesn't affect
    # anything else -- switched to AlgoBlueTwo, the same directional-arrow
    # color already used by this lecture's `dp edge` style, for contrast
    # against the orange highlight boxes.
    "matrix_reconstruction_path_contrast": (
        "y=1cm",
        "\\tikzset{dp path/.style={-Latex,ultra thick,draw=AlgoBlueTwo}}",
    ),
}
TIKZPICTURE_OPEN_RE = re.compile(r"\\begin\{tikzpicture\}(\[[^\]]*\])?")


def apply_tikz_patch(raw, patch_name):
    """Merge TIKZ_PATCHES[patch_name]'s options into the body's own
    `\\begin{tikzpicture}[...]` header (preserving any options already
    there, e.g. an `x=`/`y=` the figure sets itself) and insert its
    style-override `\\tikzset{...}` immediately after."""
    options, style_override = TIKZ_PATCHES[patch_name]

    def repl(m):
        existing = m.group(1)
        merged = "[%s,%s]" % (existing[1:-1], options) if existing else "[%s]" % options
        return "\\begin{tikzpicture}%s\n%s" % (merged, style_override)

    return TIKZPICTURE_OPEN_RE.sub(repl, raw, count=1)


# Named per-figure raw-text patches (FIGURE_CONFIG's "text_patch" key) -- for
# cases TIKZ_PATCHES can't reach because the fix targets a literal option
# baked directly onto one \node (not a shared named style a tikzset override
# could cascade into). Each entry is (regex pattern, replacement), applied
# once to the figure's own raw tikzpicture body -- same build-time-only,
# never-touch-lecture-notes/ contract as TIKZ_PATCHES above.
TEXT_PATCHES = {
    # Shared by 06_bst_search.tex's SEARCH 13 trace ("14-search-trace") and
    # 07_bst_insert_delete.tex's INSERT 12 trace ("17-insert-trace"): both
    # have a top-left orienting annotation ("full BST; inactive subtree는
    # 탐색하지 않음" / "full BST; orange path만 따라감") that hardcodes
    # font=\scriptsize directly on its own \node -- unlike every other
    # label/callout in the same picture (node values, the bottom
    # \node[callout]{...} steps), which all use the ambient default size via
    # no override at all. Drop the override so the annotation matches
    # (docs/REVIEW_NOTES.md #7). Checked every other L06 figure for the same
    # `font=\scriptsize`-on-a-\node anti-pattern (grep across
    # lecture-notes/lecture06/sections/*.tex): the only other hits are
    # 02_binary_tree.tex's tiny 2-node L/R edge-label examples and its
    # perfect/complete-tree asides, which are single-state static figures
    # using \scriptsize deliberately for a one-letter edge label or a short
    # side-note -- not this "orienting caption on a multi-step trace"
    # pattern, so they're left alone. Neither of these two nodes has an
    # \only wrapper, so one patch application covers all overlay steps of
    # its figure (4 steps for search-trace, 6 for insert-trace).
    "trace_orienting_annotation_font": (r"font=\\scriptsize,", ""),
    # 05_matrix_path.tex's "대표 Cell 계산" figure ("11-matrix-representative-
    # cell", docs/REVIEW_NOTES.md #2, redone after the first pass -- a
    # font-size-only bump on the "chosen" label -- still read as unclear:
    # the label sat wedged between the 25 cell and the arrow with nothing
    # marking *which* cell was actually selected. 25 and 31 both use the
    # plain "dp dependency" (blue) style, identical to each other, so
    # min(25,31)=25 wasn't visible in the figure itself -- only inferable
    # from the label text. Two changes: (1) re-style the 25 node from
    # "dp dependency" to "dp current" (same orange fill/border already used
    # for the 28 result cell in this same picture, defined in
    # common/dynamic_programming.tex) so the selected value and the value it
    # produces are visually tied together the same way the 28 highlight
    # already ties itself to "this is the answer"; 31 is left as plain
    # "dp dependency" since it's the rejected candidate. (2) drop the
    # edge-attached label (which forced font size to compete with the arrow
    # for space) and place "chosen" as its own node directly above the 25
    # cell instead -- cell height is 8mm ("dp cell"'s minimum height) so at
    # this picture's y=1cm-per-unit default, the cell's top edge is at
    # y=1.4; anchoring a plain `above` node at (1,1.45) puts the label
    # clear of both the cell and the (1,1)--(1,.45) arrow below it.
    "matrix_representative_cell_chosen_label": [
        (r"\\node\[dp dependency\]at\(1,1\)\{25\}", r"\\node[dp current]at(1,1){25}"),
        (
            r"\\draw\[dp edge\]\(1,1\)--node\[right,font=\\scriptsize\]\{chosen\} \(1,\.45\);",
            r"\\draw[dp edge](1,1)--(1,.45);\n\\node[above,font=\\small]at(1,1.45){chosen};",
        ),
    ],
    # 06_chaining.tex's "Chaining Animation: Insert" figure
    # ("10-chaining-insert-trace", step1 only, docs/REVIEW_NOTES.md #9):
    # step1's edge is drawn to a hardcoded coordinate (1.8,-3) that doesn't
    # actually reach the "10" node (drawn independently at (3,-3)) -- unlike
    # steps 2/3, which correctly connect actual named nodes
    # (`\draw[chain edge](b3)--(a);`). Name the node and connect to it the
    # same way, so "10" no longer looks disconnected/floating.
    "chaining_insert_step1_edge_target": (
        r"\\node\[chain active\]at\(3,-3\)\{10\};\\draw\[chain edge\]\(b3\)--\(1\.8,-3\);",
        r"\\node[chain active](a10)at(3,-3){10};\\draw[chain edge](b3)--(a10);",
    ),
    # 08_linear_probing.tex's "Linear Trace II: Wrap-Around" figure
    # ("15-linear-trace2-wraparound", step3 only, docs/REVIEW_NOTES.md #10):
    # the wrap-around arrow's symmetric `bend left=35` makes it arrive at
    # s0.north at a shallow diagonal, so the arrowhead visually reads as
    # pointing left of slot 0 rather than into it. Explicit out/in angles
    # keep the same departure from s12 but make the arrival near-vertical
    # (in=100, just past straight-up) so the tip lands clearly on slot 0.
    "linear_trace2_wrap_arrow_target": (
        r"to\[bend left=35\]",
        r"to[out=165,in=100]",
    ),
    # 02_hashing_model.tex's "Key -> Hash Code -> Compression -> Bucket"
    # figure ("01-hash-pipeline", docs/REVIEW_NOTES.md #8): the 4 boxes sit
    # only 6mm apart, and the "hash-code function"/"compression function"
    # arrow labels are single-line \scriptsize text wider than that gap, so
    # they overflow sideways into the neighboring boxes ("johin",
    # "codepression"). Widen the horizontal gap and wrap each label onto two
    # shorter lines so it fits within the (now-wider) gap even at narrow
    # webbook column widths.
    "hash_pipeline_label_overlap": [
        (r"node distance=6mm and 6mm", r"node distance=22mm and 6mm"),
        (r"node\[above,font=\\scriptsize\]\{hash-code function\}", r"node[above,font=\\scriptsize,yshift=2.5mm]{\\shortstack{hash-code\\\\function}}"),
        (r"node\[above,font=\\scriptsize\]\{compression function\}", r"node[above,font=\\scriptsize,yshift=2.5mm]{\\shortstack{compression\\\\function}}"),
    ],
}


def apply_text_patch(raw, patch_name):
    """Apply TEXT_PATCHES[patch_name] to `raw`: one (pattern, replacement)
    tuple, or a list of them applied in order. Each substitution is applied
    once (count=1) and raises if its pattern isn't found, so a future
    upstream source edit that removes the target text doesn't silently make
    this a no-op."""
    entry = TEXT_PATCHES[patch_name]
    subs = [entry] if isinstance(entry, tuple) else entry
    new_raw = raw
    for pattern, replacement in subs:
        new_raw, count = re.subn(pattern, replacement, new_raw, count=1)
        if count == 0:
            raise ValueError(
                "text patch %r: pattern %r not found in raw body" % (patch_name, pattern)
            )
    return new_raw


# Full-body overrides (FIGURE_CONFIG's "full_override" key) -- for a fix that
# needs genuinely new TikZ content, not a small patch of the existing body.
# The scanned `raw` for that (file, idx) is discarded outright and replaced
# with the string below; still build-time-only, still never touches
# lecture-notes/ (the new content lives entirely in this file).
FULL_BODY_PATCHES = {
    # 06_bst_search.tex's SUCCESSOR Animation frame draws Case 1
    # ("15-successor-cases", idx 2: a 5-node tree {15,6,18,17,20} with 6 as a
    # leaf-looking inactive node) and Case 2 ("16-successor-case2-ancestor-
    # chain", idx 3: a *separate*, disconnected tikzpicture positioned in the
    # other beamer \column, showing only {6,3,4} with an upward active-edge
    # path) as two independent tikzpictures -- fine live, side by side on a
    # slide with spoken narration, but confusing as two disconnected diagrams
    # in a standalone webbook (docs/REVIEW_NOTES.md #5): the reader has no
    # way to see that 3/4 are actually part of the SAME tree hanging off 6's
    # left side. This full-body override merges both into one 7-node tree
    # {3,4,6,15,17,18,20} with two \only<N> overlay states (reusing this
    # file's own st current/st done/st inactive/st active edge styles and
    # child{}/child[missing]{} tree syntax, e.g. from this same file's
    # 13-fixed-bst-example), applied to idx 2 with "mode": "sequence" so it
    # renders as a 2-step tabset (Case 1 / Case 2) instead of a single flat
    # image. idx 3 is left unconfigured (auto-slug, unreferenced in the qmd)
    # since its content is now fully absorbed into idx 2's merged figure.
    #
    # Tree structure (confirmed BST-valid and re-checked against the actual
    # SUCCESSOR algorithm, not just sorted order):
    #   15
    #    |-- 6            (left)
    #    |    `-- 3       (left)
    #    |         `-- 4  (right)
    #    `-- 18           (right)
    #         |-- 17      (left)
    #         `-- 20      (right)
    # succ(15)=17 (min of 15's right subtree), succ(6)=15 (6 is a left child,
    # so its nearest such ancestor is succ -- NOT 7, which isn't even in this
    # tree), succ(4)=6 (4 is a right child of 3, 3 is a left child of 6, so
    # walking up from 4 the first "became a left child" ancestor is 6),
    # succ(20)=NIL (20 is the maximum key, no such ancestor exists).
    "successor_merged_tree": r"""\begin{tikzpicture}[level distance=10mm,level 1/.style={sibling distance=26mm},level 2/.style={sibling distance=16mm}]
\node[st node](n15){15}
 child{node[st node](n6){6}
   child{node[st node](n3){3}
     child[missing]{}
     child{node[st node](n4){4}}
   }
 }
 child{node[st node](n18){18}
   child{node[st node](n17){17}}
   child{node[st node](n20){20}}
 };
\only<1|handout:0>{
\node[st current]at(n15){15};
\node[st inactive]at(n6){6};
\node[st inactive]at(n3){3};
\node[st inactive]at(n4){4};
\node[st done]at(n18){18};
\node[st current]at(n17){17};
}
\only<2|handout:1>{
\node[st inactive]at(n15){15};
\node[st done]at(n6){6};
\node[st node]at(n3){3};
\node[st current]at(n4){4};
\node[st inactive]at(n18){18};
\node[st inactive]at(n17){17};
\node[st inactive]at(n20){20};
\draw[st active edge](n4)--(n3)--(n6);
}
\end{tikzpicture}""",
}


def apply_full_body_patch(patch_name):
    return FULL_BODY_PATCHES[patch_name]


def find_brace_block(text, open_pos):
    """Given the index of a '{' in text, return (start, end) of the matching '}'.

    `end` is exclusive (one past the closing brace), so text[open_pos:end]
    is the full "{...}" span including both braces.
    """
    assert text[open_pos] == "{"
    depth = 0
    i = open_pos
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return open_pos, i + 1
        i += 1
    raise ValueError("unbalanced braces starting at %d" % open_pos)


def find_only_blocks(text):
    """Find top-level \\only<SPEC>{BODY} or \\visible<SPEC>{BODY} occurrences,
    brace-balanced (ONLY_HEAD_RE matches either keyword).

    Returns a list of (start, end, spec, body) with `end` exclusive. Does not
    recurse into BODY (none of the lecture-notes figures nest \\only/\\visible
    inside another, and none in this repository need it).
    """
    blocks = []
    pos = 0
    while True:
        m = ONLY_HEAD_RE.search(text, pos)
        if not m:
            break
        spec = m.group(1)
        brace_start = m.end()
        if brace_start >= len(text) or text[brace_start] != "{":
            pos = m.end()
            continue
        _, brace_end = find_brace_block(text, brace_start)
        body = text[brace_start + 1 : brace_end - 1]
        blocks.append((m.start(), brace_end, spec, body))
        pos = brace_end
    return blocks


def parse_spec(spec):
    """Parse a beamer overlay spec ("3", "1-3", "2-", "-3") to an (lo, hi) range.

    A spec may carry a trailing "|handout:N" mode-conditional override (e.g.
    "4-|handout:1", used throughout L01's Linear/Binary Search overlay
    figures) that picks a different overlay number specifically for
    handout-mode PDFs. These SVGs are for the web, not a handout PDF, so
    only the base spec before "|" is used.
    """
    spec = spec.split("|", 1)[0].strip()
    if "-" in spec:
        lo_s, hi_s = spec.split("-", 1)
        lo = int(lo_s) if lo_s else float("-inf")
        hi = int(hi_s) if hi_s else float("inf")
        return lo, hi
    n = int(spec)
    return n, n


def render_only_at(text, target):
    """Render `text` with every \\only<SPEC>{BODY} resolved for overlay `target`:
    BODY survives if target is inside SPEC's range, otherwise it is dropped.
    """
    blocks = find_only_blocks(text)
    result = text
    for start, end, spec, body in reversed(blocks):
        lo, hi = parse_spec(spec)
        replacement = body if lo <= target <= hi else ""
        result = result[:start] + replacement + result[end:]
    return result


def find_alt_blocks(text):
    """Find top-level \\alt<SPEC>{TRUE-BODY}{FALSE-BODY} occurrences, brace-balanced
    (used by L01's Binary Search trace to grey out discarded cells from overlay 2
    onward -- \\alt has no `\\only`-style single-branch equivalent, so it needs its
    own extraction/resolution, mirroring find_only_blocks/render_only_at above).

    Also matches the `alt=<SPEC>{TRUE-STYLE}{FALSE-STYLE}` *tikz key* form (no
    backslash) L06 uses inside `\\node[...,alt=<N>{st current}{st done}]`
    style lists (e.g. 01_tree_basics.tex, 11_btree.tex) -- syntactically the
    same SPEC-then-two-braces shape, just triggered by a bare `alt=` key
    rather than the `\\alt` command, and resolved the same way: replacing the
    whole `alt=<...>{...}{...}` span with the chosen branch's bare style name
    leaves a valid `[...,st current]`-style option list, since TikZ styles
    happily cascade.
    """
    blocks = []
    pos = 0
    while True:
        m = ALT_HEAD_RE.search(text, pos)
        if not m:
            break
        spec = m.group(1) if m.group(1) is not None else m.group(2)
        true_start = m.end()
        if true_start >= len(text) or text[true_start] != "{":
            pos = m.end()
            continue
        _, true_end = find_brace_block(text, true_start)
        false_start = true_end
        if false_start >= len(text) or text[false_start] != "{":
            pos = m.end()
            continue
        _, false_end = find_brace_block(text, false_start)
        true_body = text[true_start + 1 : true_end - 1]
        false_body = text[false_start + 1 : false_end - 1]
        blocks.append((m.start(), false_end, spec, true_body, false_body))
        pos = false_end
    return blocks


def render_alt_at(text, target):
    """Render `text` with every \\alt<SPEC>{TRUE}{FALSE} resolved for overlay
    `target`: TRUE survives if target is inside SPEC's range, else FALSE."""
    blocks = find_alt_blocks(text)
    result = text
    for start, end, spec, true_body, false_body in reversed(blocks):
        lo, hi = parse_spec(spec)
        replacement = true_body if lo <= target <= hi else false_body
        result = result[:start] + replacement + result[end:]
    return result


NODE_OVERLAY_RE = re.compile(r"\\node<([^>]*)>")


def normalize_node_overlay_shorthand(text):
    """`\\node<SPEC>[options]{content};` is beamer-tikz's per-node overlay
    shorthand (equivalent to wrapping the whole node command in
    `\\only<SPEC>{...}`), used by L06's 01_tree_basics.tex -- but that
    beamer/tikz overlay integration isn't loaded in the `standalone`-class
    documents this script compiles (no beamer document class), so the bare
    `<SPEC>` right after `\\node` is invalid syntax there and throws a fatal
    LaTeX error. Rewrite each occurrence to the equivalent
    `\\only<SPEC>{\\node...;}` up front, so the normal find_only_blocks/
    render_only_at pass handles it exactly like any other conditional
    content. A brace-balanced scan finds the node command's terminating
    top-level `;` (content can itself contain `{...}` groups)."""
    if "\\node<" not in text:
        return text
    pieces = []
    pos = 0
    for m in NODE_OVERLAY_RE.finditer(text):
        if m.start() < pos:
            continue  # already consumed as part of a previous match's body
        pieces.append(text[pos:m.start()])
        spec = m.group(1)
        i = m.end()
        depth = 0
        while i < len(text):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            elif text[i] == ";" and depth == 0:
                i += 1
                break
            i += 1
        node_cmd = "\\node" + text[m.end():i]
        pieces.append("\\only<%s>{%s}" % (spec, node_cmd))
        pos = i
    pieces.append(text[pos:])
    return "".join(pieces)


def render_overlay_at(text, target):
    """Resolve both \\alt<...>{...}{...} and \\only<...>{...} for overlay `target`."""
    text = render_alt_at(text, target)
    text = render_only_at(text, target)
    return text


def overlay_steps(text):
    """All distinct overlay numbers referenced by \\only<...>/\\alt<...> in `text`,
    sorted."""
    steps = set()
    for _, _, spec, _ in find_only_blocks(text):
        lo, hi = parse_spec(spec)
        if lo != float("-inf"):
            steps.add(lo)
        if hi != float("inf"):
            steps.add(hi)
    for _, _, spec, _, _ in find_alt_blocks(text):
        lo, hi = parse_spec(spec)
        if lo != float("-inf"):
            steps.add(lo)
        if hi != float("inf"):
            steps.add(hi)
    return sorted(steps)


def find_macro_calls(text, macro_name, arity):
    """Find every `\\macroname{arg1}...{argN}` call (brace-balanced per
    argument), returning (start, end, full_call_text) tuples in document
    order. A call site with fewer than `arity` brace groups immediately
    following (e.g. a substring match on a longer macro name) is skipped."""
    calls = []
    pattern = re.compile(r"\\%s\b" % re.escape(macro_name))
    pos = 0
    while True:
        m = pattern.search(text, pos)
        if not m:
            break
        end = m.end()
        ok = True
        for _ in range(arity):
            while end < len(text) and text[end].isspace():
                end += 1
            if end >= len(text) or text[end] != "{":
                ok = False
                break
            _, end = find_brace_block(text, end)
        if ok:
            calls.append((m.start(), end, text[m.start():end]))
            pos = end
        else:
            pos = m.end()
    return calls


def group_macro_calls_by_frame(text, calls):
    """Group macro calls (from find_macro_calls) by which `\\begin{frame}`
    block they fall in: consecutive calls in the same frame are one
    animation's already-resolved states (see MACRO_PICTURES docstring), so
    they become one figure/sequence; calls in different frames are
    unrelated figures. Returns a list of (start, end, list_of_raw_calls)."""
    frame_starts = [m.start() for m in FRAME_START_RE.finditer(text)]

    def frame_of(pos):
        lo, hi, ans = 0, len(frame_starts) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if frame_starts[mid] <= pos:
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans

    groups = []
    current_frame = None
    for start, end, raw in calls:
        f = frame_of(start)
        if f != current_frame:
            groups.append({"frame": f, "start": start, "end": end, "raws": []})
            current_frame = f
        groups[-1]["end"] = end
        groups[-1]["raws"].append(raw)
    return [(g["start"], g["end"], g["raws"]) for g in groups]


def find_figures(section_path, lecture=None):
    """Yield (index, kind, raw_text) for each tikzpicture/axis block in a section file, in order.

    `kind` is "tikzpicture"/"axis" with `raw_text` a string, or
    "macro:<name>" (see MACRO_PICTURES) with `raw_text` a *list* of already-
    resolved state strings -- one per call in that macro's frame-group, no
    further `\\only` overlay resolution needed (see
    group_macro_calls_by_frame's docstring).
    """
    text = section_path.read_text(encoding="utf-8")
    text = normalize_node_overlay_shorthand(text)
    tikz_spans = [(m.start(), m.end(), "tikzpicture", m.group(0)) for m in TIKZ_RE.finditer(text)]
    axis_spans = [(m.start(), m.end(), "axis", m.group(0)) for m in AXIS_RE.finditer(text)]
    # pgfplots `axis` blocks are frequently written *inside* an existing
    # `tikzpicture` (observed throughout L01's growth-curve figures, the
    # first lecture with any pgfplots content -- L03 has none). When that's
    # the case the tikzpicture span already contains the whole figure, so
    # keep only that outer span and drop the redundant nested axis span --
    # otherwise the same figure gets compiled twice (once via the outer
    # tikzpicture, once via a synthetic tikzpicture wrapped around just the
    # inner axis) and the figure-count quality gate (QUALITY_ASSURANCE gate
    # 2) no longer matches the source.
    axis_spans = [
        (start, end, kind, raw)
        for (start, end, kind, raw) in axis_spans
        if not any(t_start <= start and end <= t_end for t_start, t_end, _, _ in tikz_spans)
    ]
    macro_spans = []
    for macro_name, arity in MACRO_PICTURES.get(lecture, {}).items():
        calls = find_macro_calls(text, macro_name, arity)
        for start, end, raws in group_macro_calls_by_frame(text, calls):
            macro_spans.append((start, end, "macro:%s" % macro_name, raws))
    spans = sorted(tikz_spans + axis_spans + macro_spans, key=lambda s: s[0])
    # Any remaining (non-nested) axis blocks are bare pgfplots content, which
    # must live inside a tikzpicture in standalone mode; wrap those.
    for idx, (_, _, kind, raw) in enumerate(spans):
        if kind == "axis":
            raw = "\\begin{tikzpicture}\n%s\n\\end{tikzpicture}" % raw
        yield idx, kind, raw


def sha1(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def compile_svg(body_tex, common_block, out_svg, job_name):
    build_dir = CACHE_DIR / job_name
    build_dir.mkdir(parents=True, exist_ok=True)
    job_tex = build_dir / "job.tex"
    job_pdf = build_dir / "job.pdf"
    job_log = build_dir / "job.log"
    job_tex.write_text(PREAMBLE % {"common_block": common_block, "body": body_tex}, encoding="utf-8")

    result = subprocess.run(
        [
            "lualatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-output-directory=%s" % build_dir,
            str(job_tex),
        ],
        cwd=str(LECTURE_NOTES),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0 or not job_pdf.exists():
        return False, job_log.read_text(encoding="utf-8", errors="replace") if job_log.exists() else result.stdout.decode(
            "utf-8", errors="replace"
        )

    # NOTE: `--no-fonts` (glyphs -> SVG <path> outlines) rather than
    # `--font-format=woff` (glyphs -> an embedded webfont referenced by index).
    # dvisvgm 3.6 has a real, reproducible bug in the webfont path: in figures
    # with many preceding glyph-shaping calls in the same document, a later
    # small glyph (observed: dropped inter-word spaces, a "." shrunk to
    # near-invisible) gets embedded with wrong metrics -- confirmed by
    # comparing the PDF (always correct, checked via `pdftoppm`/ImageMagick)
    # against the SVG (wrong) for the *same* PDF, and confirmed the corruption
    # disappears with `--no-fonts` on that same PDF. See the M1 commit message
    # for the investigation. Trade-off: figure text becomes non-selectable
    # vector paths instead of real webfont text -- acceptable for diagrams.
    out_svg.parent.mkdir(parents=True, exist_ok=True)
    svg_result = subprocess.run(
        ["dvisvgm", "--pdf", "--no-fonts", "--output=%s" % out_svg, str(job_pdf)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if svg_result.returncode != 0 or not out_svg.exists():
        return False, svg_result.stdout.decode("utf-8", errors="replace")

    return True, None


# Cheap defense-in-depth on top of the --no-fonts fix above: compile twice and
# require a byte-identical match before accepting the output, in case some
# other rare toolchain glitch (unrelated to the dvisvgm bug above) surfaces.
MAX_RENDER_ATTEMPTS = 3


def compile_svg_verified(body_tex, common_block, out_svg, job_name):
    import collections

    counts = collections.Counter()
    svg_by_hash = {}
    for attempt in range(MAX_RENDER_ATTEMPTS):
        attempt_svg = out_svg.parent / (".attempt-%s.svg" % out_svg.stem)
        ok, err = compile_svg(body_tex, common_block, attempt_svg, "%s-a%d" % (job_name, attempt))
        if not ok:
            return False, err
        data = attempt_svg.read_bytes()
        digest = sha1(data.decode("utf-8", errors="replace"))
        counts[digest] += 1
        svg_by_hash[digest] = data
        if counts[digest] >= 2:
            out_svg.write_bytes(svg_by_hash[digest])
            attempt_svg.unlink(missing_ok=True)
            return True, None
    attempt_svg.unlink(missing_ok=True)
    return False, (
        "render did not stabilize after %d attempts (%d distinct outputs seen) -- "
        "toolchain glyph-shaping glitch, inspect the source block for unusual "
        "glyph sequences" % (MAX_RENDER_ATTEMPTS, len(counts))
    )


def find_macro_block(text, start_kw):
    """Find the first `\\<start_kw>{...}` (brace-balanced) in `text` and return
    its full source span, or None if absent."""
    m = re.search(r"\\%s\s*\{" % re.escape(start_kw), text)
    if not m:
        return None
    brace_start = m.end() - 1
    _, brace_end = find_brace_block(text, brace_start)
    return text[m.start():brace_end]


def find_all_newcommands(text):
    """All `\\newcommand{\\NAME}{...}` spans in `text`, brace-balanced, in order."""
    out = []
    for m in re.finditer(r"\\newcommand\{\\[A-Za-z]+\}\s*\{", text):
        brace_start = m.end() - 1
        _, brace_end = find_brace_block(text, brace_start)
        out.append(text[m.start():brace_end])
    return out


DIRECT_COMMON_INPUT_RE = re.compile(r"\\input\{common/[^}]+\.tex\}")


def lecture_common_block(lecture):
    """The standalone preamble's lecture-specific TikZ-style block.

    L03 (and lectures with the same layout) keep their `\\tikzset{...}` and
    any `\\newcommand`s in a dedicated `lectureNN/common.tex` -- reuse that
    via `\\input`, same as before. L01 has no such file: its tikzset/newcommand
    definitions are inline in `lecture01.tex`'s own preamble instead. Since a
    `standalone`-class document can't \\input a full beamer .tex (it has its
    own \\documentclass/\\begin{document}), extract just the tikzset/newcommand
    blocks and reproduce them literally -- the same reasoning already used
    above for pulling beamerthemealgorithms.sty's color \\definecolors by hand.

    L10 is a third layout: it has no `lecture10/common.tex` at all and inputs
    `common/state_space.tex` (its own dedicated shared style file, not shared
    with any other lecture -- see lecture10_content_map.md's "다른 lecture
    디렉터리의 common.tex를 더 이상 입력하지 않는다") directly in
    `lecture10.tex`'s own preamble instead. Those `\\input{common/...}` lines
    are reproduced verbatim rather than re-extracted: they already resolve
    correctly under this script's `cwd=str(LECTURE_NOTES)` (see
    compile_svg), the same way `\\input{lectureNN/common.tex}` above does.
    """
    common_tex = LECTURE_NOTES / ("lecture%s" % lecture) / "common.tex"
    if common_tex.exists():
        return "\\input{lecture%s/common.tex}" % lecture

    main_tex_path = LECTURE_NOTES / ("lecture%s" % lecture) / ("lecture%s.tex" % lecture)
    main_tex = main_tex_path.read_text(encoding="utf-8")
    preamble = main_tex.split("\\begin{document}", 1)[0]
    pieces = find_all_newcommands(preamble)
    tikzset = find_macro_block(preamble, "tikzset")
    if tikzset:
        pieces.append(tikzset)
    pieces.extend(DIRECT_COMMON_INPUT_RE.findall(preamble))
    if not pieces:
        raise ValueError(
            "no lecture%s/common.tex and no tikzset/newcommand/direct common/ "
            "\\input found in %s -- figures may rely on styles this script "
            "doesn't know how to reproduce" % (lecture, main_tex_path)
        )
    return "\n".join(pieces)


def load_manifest(out_dir):
    manifest_path = out_dir / ".manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return {}


def save_manifest(out_dir, manifest):
    manifest_path = out_dir / ".manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def default_worker_count():
    """Parallel lualatex compile job count: each job is its own process
    invoking lualatex+dvisvgm independently (no shared mutable state --
    compile_svg_verified writes under its own CACHE_DIR/job_name subdir), so
    this only needs to respect available cores/memory, not correctness.
    Capped at 8: lualatex's own memory footprint makes higher parallelism
    prone to thrashing on typical CI/dev machines rather than helping."""
    return max(1, min(os.cpu_count() or 4, 8))


def _compile_job(job):
    body_tex, common_block, out_svg, out_slug = job
    ok, err = compile_svg_verified(body_tex, common_block, out_svg, out_slug)
    return out_slug, ok, err


def process_lecture(lecture, check_only, keep_build, jobs=None):
    """`jobs` parallel lualatex compiles at once for lectures with many
    figures (L06 has ~60 -- see the module docstring's note on caching and
    parallel compilation) -- see default_worker_count() for the default.
    Figure *discovery* and cache-hit checking stay sequential (cheap, and
    order determines each figure's manifest key); only the actual
    lualatex+dvisvgm compile of cache-misses runs in parallel, since each is
    an independent process writing to its own output file."""
    sections_dir = LECTURE_NOTES / ("lecture%s" % lecture) / "sections"
    common_block = lecture_common_block(lecture)
    out_dir = REPO_ROOT / "figures" / _lecture_slug(lecture)
    config = FIGURE_CONFIG.get(lecture, {})

    manifest = load_manifest(out_dir)
    expected_files = set()
    built, cached, failed = [], [], []
    pending = []  # (body_tex, common_block, out_svg, out_slug, content_hash)

    section_paths = sorted(sections_dir.glob("*.tex"))
    for section_path in section_paths:
        for idx, kind, raw in find_figures(section_path, lecture):
            key = (section_path.name, idx)
            cfg = config.get(key, {})
            if cfg.get("skip"):
                # This source tikzpicture/axis/macro-call is intentionally
                # not extracted as its own figure -- e.g. its content has
                # been folded into another figure's "full_override" (see
                # FULL_BODY_PATCHES). Producing no output at all (rather
                # than falling through to an auto-generated, unreferenced
                # slug) keeps figures/ free of orphaned files that would
                # otherwise silently regenerate on every future build.
                continue
            slug = cfg.get("slug", "%s-%d" % (section_path.stem, idx))
            mode = cfg.get("mode", "flatten")
            patch_name = cfg.get("patch")
            text_patch_name = cfg.get("text_patch")
            full_override_name = cfg.get("full_override")

            if kind.startswith("macro:"):
                # Each entry in `raw` (a list) is already one fully-resolved
                # state -- a separate macro call, not an \only overlay of a
                # shared body (see find_figures's docstring) -- so there is
                # no overlay_steps()/render_overlay_at() step here at all.
                bodies = [apply_tikz_patch(b, patch_name) if patch_name else b for b in raw]
                if text_patch_name:
                    bodies = [apply_text_patch(b, text_patch_name) for b in bodies]
                if len(bodies) > 1:
                    targets = [(None, "%s-step%d" % (slug, i + 1), b) for i, b in enumerate(bodies)]
                else:
                    targets = [(None, slug, bodies[0])]
            else:
                if full_override_name:
                    raw = apply_full_body_patch(full_override_name)
                if patch_name:
                    raw = apply_tikz_patch(raw, patch_name)
                if text_patch_name:
                    raw = apply_text_patch(raw, text_patch_name)
                # overlay_steps() only collects \only/\alt/\visible *spec
                # boundaries* -- a cumulative-reveal picture built entirely
                # from \visible<2->/\visible<3-> (no node is ever wrapped in
                # an explicit <1>, since "nothing extra yet" needs no
                # \visible at all) is missing its own first frame from that
                # boundary set (docs/ANIMATION_AUDIT.md's L02 push finding:
                # boundaries {2,3} undercount the true 3-frame sequence
                # {1,2,3}). "steps" lets a FIGURE_CONFIG entry override the
                # detected list with the literal overlay targets to render.
                steps = cfg.get("steps") or overlay_steps(raw)
                if mode == "sequence" and steps:
                    targets = [(step, "%s-step%d" % (slug, i + 1), raw) for i, step in enumerate(steps)]
                else:
                    target_state = max(steps) if steps else None
                    targets = [(target_state, slug, raw)]
            for target, out_slug, target_raw in targets:
                body_tex = render_overlay_at(target_raw, target) if target is not None else target_raw
                content_hash = sha1(body_tex)
                out_svg = out_dir / ("%s.svg" % out_slug)
                expected_files.add(out_svg.name)

                if manifest.get(out_slug) == content_hash and out_svg.exists():
                    cached.append(out_slug)
                    continue

                if check_only:
                    failed.append((out_slug, "not yet built (hash changed or missing)"))
                    continue

                pending.append((body_tex, common_block, out_svg, out_slug, content_hash))

    if not check_only and pending:
        worker_count = min(jobs or default_worker_count(), len(pending))
        jobs_arg = [(b, c, o, s) for b, c, o, s, _ in pending]
        if worker_count > 1:
            with multiprocessing.Pool(worker_count) as pool:
                results = pool.map(_compile_job, jobs_arg)
        else:
            results = [_compile_job(j) for j in jobs_arg]
        hash_by_slug = {out_slug: content_hash for _, _, _, out_slug, content_hash in pending}
        for out_slug, ok, err in results:
            if ok:
                manifest[out_slug] = hash_by_slug[out_slug]
                built.append(out_slug)
            else:
                failed.append((out_slug, err))

    if not check_only:
        save_manifest(out_dir, manifest)
        if not keep_build:
            shutil.rmtree(CACHE_DIR, ignore_errors=True)

    return built, cached, failed, expected_files, manifest


def _lecture_slug(lecture):
    names = {
        "01": "01-introduction", "02": "02-recursion", "03": "03-sorting",
        "04": "04-selection", "05": "05-dynamic-programming", "06": "06-search-trees",
        "07": "07-hash-tables", "08": "08-graphs", "09": "09-string-matching",
        "10": "10-state-space-search",
    }
    return names.get(lecture, "lecture%s" % lecture)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lecture", default="03", help="lecture number, e.g. 03 (default: 03)")
    parser.add_argument("--check", action="store_true", help="report status without compiling")
    parser.add_argument("--keep-build", action="store_true", help="keep the LaTeX build cache dir for debugging")
    parser.add_argument("--jobs", type=int, default=None,
                         help="parallel lualatex compiles (default: min(cpu_count, 8) -- see default_worker_count())")
    args = parser.parse_args()

    built, cached, failed, expected_files, manifest = process_lecture(
        args.lecture, args.check, args.keep_build, jobs=args.jobs
    )

    print("extract_tikz.py --lecture %s%s" % (args.lecture, " --check" if args.check else ""))
    print("  built:  %d" % len(built))
    print("  cached: %d" % len(cached))
    print("  failed: %d" % len(failed))
    for slug, err in failed:
        print("  FAIL %s:" % slug)
        print("    " + "\n    ".join((err or "").splitlines()[-15:]))

    if args.check:
        out_dir = REPO_ROOT / "figures" / _lecture_slug(args.lecture)
        on_disk = {p.name for p in out_dir.glob("*.svg")} if out_dir.exists() else set()
        missing = expected_files - on_disk
        if missing:
            print("  missing on disk: %s" % ", ".join(sorted(missing)))
            failed = failed or [(m, "missing") for m in missing]

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
