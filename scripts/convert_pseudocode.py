#!/usr/bin/env python3
"""Convert lecture-notes `algorithmic` blocks into pseudocode.js snippets.

Pipeline (SPEC 4.3): scan lecture-notes/lectureNN/sections/*.tex for
`\\begin{algorithmic}...\\end{algorithmic}` blocks and wrap each one as a
`<pre class="pseudocode">` fragment for pseudocode.js to render client-side,
so pseudocode is never hand-retyped into the .qmd.

The `algorithmic` package's `[1]` (enable line numbering) argument is not part
of pseudocode.js's own grammar (line numbers are a `data-line-number`
attribute instead), so it is stripped. Everything else -- `\\Procedure`,
`\\State`, `\\If/\\ElsIf/\\Else/\\EndIf`, `\\For/\\ForAll/\\EndFor`,
`\\While/\\EndWhile`, `\\Return`, `\\Call`, `\\gets`, math in `$...$` -- maps
onto pseudocode.js's grammar unchanged and case-insensitively (verified
directly against the vendored library's Lexer.js/Parser.js and a Node smoke
test during M1, not assumed from memory).

Four normalizations are applied, all moving or renaming text rather than
rewriting it (neither changes what the pseudocode says, only where or as
what pseudocode.js's stricter-than-algorithmicx grammar needs it to appear):

1. `\\Call{name}{args}` occasionally appears *inside* math delimiters in the
   source (e.g. `$p\\gets\\Call{Partition}{A,low,high}$` in 08_quick_sort.tex,
   or `\\(u\\gets\\Call{ExtractMin}{Q}\\)` throughout L08 -- pseudocode.js's
   own lexer treats `$...$` and `\\(...\\)` as equivalent math delimiters,
   so both need the same handling) even though `\\Call` is pseudocode.js/
   algorithmicx markup, not real math -- that fails to parse as math. Such
   spans are hoisted out of the surrounding math (moving only the true math
   sub-parts back into freshly-opened `$...$`), matching how `\\Call` is
   written everywhere else in the lecture notes. A single math span can
   contain more than one `\\Call` (e.g. L05's
   `$memo[n]\\gets\\Call{FibMemo}{n-1,memo}+\\Call{FibMemo}{n-2,memo}$`) --
   each one is hoisted independently, alternating plain-math and bare-`\\Call`
   segments.
2. `\\text{...}` is a math-mode command with no meaning in pseudocode.js's
   non-math grammar (unlike `\\textbf`/`\\textrm`/etc., which its Lexer does
   recognize outside math). One bare occurrence outside any math span
   (`06_topological_sort.tex`'s `\\Call{TopoVisit}{$v$}=\\text{CYCLE}`)
   throws a parse error -- wrapped in `$...$` instead, since `\\text` is
   valid there.
3. `\\Statex` (algorithmicx's un-numbered continuation line) has no entry in
   pseudocode.js's statement grammar at all -- one occurrence
   (`06_topological_sort.tex`) throws `Expected `end` but received
   `Statex``. Renamed to `\\State`, the closest supported equivalent (only
   visible difference: a line-number prefix `\\Statex` omits).
4. `\\Require`/`\\Ensure`/`\\Input`/`\\Output` are only valid, per the vendored
   parser, as top-level statements directly inside `\\begin{algorithmic}`,
   not nested inside a `\\Procedure{...}{...}...\\EndProcedure` body -- a
   nested `\\Require` throws `Expected endProcedure but received Require`
   (confirmed directly against the parser; L01's Maximum places `\\Require`
   as the procedure's first body statement, which is valid algorithmicx but
   not valid pseudocode.js, and never came up in L03 since nothing there
   uses `\\Require`/`\\Ensure`). Such statements are hoisted to just before
   the `\\Procedure{...}{...}` call so they parse as a top-level
   precondition/postcondition annotation instead.
5. `\\Procedure{NAME}{args}`'s NAME cannot contain whitespace at all --
   confirmed directly against the vendored parser with minimal repros: even
   a plain two-English-word name (`\\Procedure{Binary Search}`) throws
   `Expected an atom of close but received ordinary`, and a `~`/NBSP
   stand-in for the space either parses but prints the literal `~` glyph or
   still throws. This never surfaced before L04 because every prior
   lecture's multi-word procedure names were already written concatenated
   in the source (e.g. `BinarySearch`) -- L04's
   `\\Procedure{DeterministicSelect (continued)}` is the first occurrence of
   a documentation qualifier ("this procedure continues from an earlier
   slide") written with a literal space. Squashing whitespace out of just
   the NAME group (never the args group) fixes the parse without changing
   which procedure it is; a name with no whitespace is left untouched, so
   this is a no-op for every already-working lecture.

Separately from those five text-level normalizations, PSEUDOCODE_CONFIG can
map more than one (section file, index) key to the *same* slug -- this marks
a procedure the source splits across multiple frames purely for slide-space
reasons (e.g. L04's `10_group_of_five.tex` has two `\\Procedure{DeterministicSelect...}`
blocks: "Pivot 만들기" builds the pivot, "(continued)" partitions around it
and recurses) as one continuous algorithm rather than two separate ones.
merge_algorithmic_bodies() drops every body's `\\Procedure{...}{...}` header
except the first (a later header would show extra locally-computed
variables, e.g. `M`, as if they were caller-supplied parameters, which they
aren't) and every body's `\\EndProcedure` except the last, then concatenates
them -- so pseudocode.js renders one line-numbered listing that continues
instead of two blocks that both start at line 1 and look like two separate
procedure definitions.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LECTURE_NOTES = REPO_ROOT / "lecture-notes"

# Canonical lecture -> figures/ subdirectory slug mapping. Also the source of
# truth for "all lectures" (--all): sorted(LECTURE_SLUGS.keys()). L02 has no
# algorithmic blocks (0 pseudocode figures), but is listed here anyway so
# --all resolves its out_dir correctly instead of falling back to the wrong
# "lecture02" (process_lecture's PSEUDOCODE_CONFIG.get(lecture, {}) lookup
# below already handles L02 having no config entry -- this dict is only
# about the output directory name).
LECTURE_SLUGS = {
    "01": "01-introduction", "02": "02-recursion", "03": "03-sorting",
    "04": "04-selection", "05": "05-dynamic-programming", "06": "06-search-trees",
    "07": "07-hash-tables", "08": "08-graphs", "09": "09-string-matching",
    "10": "10-state-space-search",
}

ALGORITHMIC_RE = re.compile(r"\\begin\{algorithmic\}(\[[^\]]*\])?(.*?)\\end\{algorithmic\}", re.DOTALL)
MATH_SPAN_RE = re.compile(r"\$([^$]*)\$|\\\(((?:(?!\\\)).)*)\\\)", re.DOTALL)
CALL_RE = re.compile(r"\\Call\{([^{}]*)\}\{([^{}]*)\}")
BARE_TEXT_CMD_RE = re.compile(r"\\text\{[^{}]*\}")
STATEX_RE = re.compile(r"\\Statex\b")
PROCEDURE_HEAD_RE = re.compile(r"\\Procedure\{[^{}]*\}\{[^{}]*\}")
PROCEDURE_NAME_RE = re.compile(r"\\Procedure\{([^{}]*)\}")
PROCEDURE_HEADER_LINE_RE = re.compile(r"^\\Procedure\{[^{}]*\}\{[^{}]*\}\s*\n?")
END_PROCEDURE_TAIL_RE = re.compile(r"\\EndProcedure\s*$")
PRECONDITION_RE = re.compile(r"\\(?:Require|Ensure|Input|Output)\s*\{")

# Lecture-specific slugs, keyed by (section filename, 0-based index of the
# algorithmic block within that file, in document order).
PSEUDOCODE_CONFIG = {
    "03": {
        ("03_selection.tex", 0): "selection-sort",
        ("04_bubble.tex", 0): "bubble-sort",
        ("05_insertion.tex", 0): "insertion-sort",
        ("07_merge_sort.tex", 0): "merge-sort",
        ("07_merge_sort.tex", 1): "merge",
        ("08_quick_sort.tex", 0): "quick-sort",
        ("08_quick_sort.tex", 1): "partition",
        ("11_heapify.tex", 0): "max-heapify-recursive",
        ("11_heapify.tex", 1): "max-heapify-iterative",
        ("12_build_heap.tex", 0): "build-max-heap",
        ("13_heap_sort.tex", 0): "heap-sort",
        ("14_counting_sort.tex", 0): "counting-sort",
    },
    "01": {
        ("04_pseudocode.tex", 0): "pseudocode-if-else",
        ("04_pseudocode.tex", 1): "pseudocode-while",
        ("05_maximum.tex", 0): "maximum",
        ("06_linear_search.tex", 0): "linear-search",
        ("07_binary_search.tex", 0): "binary-search",
    },
    # See chapters/06.inventory §3. Exactly one \Call-in-math occurrence
    # (03_traversal.tex's LevelOrder: "$u\gets\Call{Dequeue}{Q}$") -- the
    # same L05-bug pattern hoist_call_out_of_math already generalizes for;
    # verified by running this script and inspecting the output (no manual
    # edits made). Red-Black Tree has no dedicated \Procedure block in the
    # source at all (insertion/deletion are prose+TikZ only, confirmed by
    # reading every section file) -- there is deliberately no "06" entry
    # for it here.
    "06": {
        ("03_traversal.tex", 0): "preorder",
        ("03_traversal.tex", 1): "inorder",
        ("03_traversal.tex", 2): "postorder",
        ("03_traversal.tex", 3): "level-order",
        ("06_bst_search.tex", 0): "tree-search-recursive",
        ("06_bst_search.tex", 1): "tree-search-iterative",
        ("06_bst_search.tex", 2): "tree-minimum",
        ("07_bst_insert_delete.tex", 0): "tree-insert",
        ("07_bst_insert_delete.tex", 1): "transplant",
        ("09_avl.tex", 0): "rotate-right",
        ("11_btree.tex", 0): "btree-search",
        ("11_btree.tex", 1): "btree-insert",
    },
    # See chapters/05.inventory §1 for the frame titles these came from. The
    # three blocks with no `\Procedure{...}` wrapper in the source (bare
    # `\State`/`\For` loops, presented under a frame title instead) get a
    # slug matching that frame title rather than a source-named procedure.
    "05": {
        ("02_fibonacci.tex", 0): "fib-recursive",
        ("03_memoization_tabulation.tex", 0): "fib-memo",
        ("03_memoization_tabulation.tex", 1): "fib-bottom-up",
        ("05_matrix_path.tex", 0): "min-path",
        ("05_matrix_path.tex", 1): "min-path-memo",
        ("05_matrix_path.tex", 2): "matrix-bottom-up",
        ("07_lcs.tex", 0): "lcs-length",
        ("07_lcs.tex", 1): "lcs-bottom-up",
        ("09_maximum_subarray.tex", 0): "max-subarray-brute-force",
    },
    # See chapters/08.inventory §3. 04_dfs.tex idx0 contains two \Procedure
    # calls (DFS, DFSVisit) inside one \begin{algorithmic} block -- that's
    # still a single pseudocode.js snippet, matching how the source presents
    # them together in one frame.
    # See chapters/04.inventory §3. The first three of \Call-in-math
    # occurrences the L05 bug taught us to watch for live here too --
    # 04_quickselect_idea.tex idx0 and both blocks of 10_group_of_five.tex --
    # hoist_call_out_of_math (generalized during the L08 session) is expected
    # to fix all three without further changes; verified by running this
    # script and inspecting the output (no manual edits made).
    # 10_group_of_five.tex's two \Procedure{DeterministicSelect...} blocks
    # ("Pivot 만들기" then "(continued)") are one continuous algorithm split
    # across two frames for slide-space reasons -- both map to the same
    # slug so merge_algorithmic_bodies() (see module docstring) renders them
    # as a single continuously-numbered listing instead of two blocks that
    # each restart at line 1 and look like two separate procedures.
    "04": {
        ("03_sort_then_select.tex", 0): "select-by-sorting",
        ("04_quickselect_idea.tex", 0): "fixed-quickselect",
        ("08_randomized_select.tex", 0): "randomized-select",
        ("10_group_of_five.tex", 0): "deterministic-select",
        ("10_group_of_five.tex", 1): "deterministic-select",
    },
    "08": {
        ("03_bfs.tex", 0): "bfs",
        ("04_dfs.tex", 0): "dfs",
        ("04_dfs.tex", 1): "dfs-iterative",
        ("05_cycle_detection.tex", 0): "has-cycle-dfs",
        ("06_topological_sort.tex", 0): "topo-kahn",
        ("06_topological_sort.tex", 1): "topo-dfs",
        ("09_prim.tex", 0): "prim",
        ("10_kruskal.tex", 0): "kruskal",
        ("12_shortest_path_intro.tex", 0): "reconstruct-path",
        ("13_unweighted_dag.tex", 0): "dag-shortest-paths",
        ("14_dijkstra.tex", 0): "dijkstra",
        ("15_bellman_ford.tex", 0): "bellman-ford",
    },
    # See chapters/07.inventory §(b). All 5 \Call occurrences in this lecture
    # sit inside `$...$` math in the source (StringHash's \Call{Code}{c},
    # ChainedPut's \Call{ChainedSearch}{...}, HashSearch/HashPut's
    # \Call{Probe}{...}, HashDelete's \Call{FindSlot}{...}) -- the L05 bug
    # pattern hoist_call_out_of_math already generalizes for, exercised here
    # more than in any other lecture so far. No merges needed: every
    # \Procedure block here is already complete on its own (unlike L04's
    # split DeterministicSelect); ChainedPut calling ChainedSearch, and
    # HashSearch/HashPut/HashDelete calling the not-formally-defined
    # Probe/FindSlot, are connected via qmd prose instead (the B-Tree
    # "independent subroutine" pattern), not by merging blocks.
    "07": {
        ("04_string_hashing.tex", 0): "string-hash",
        # ChainedSearch and ChainedPut sit in ONE \begin{algorithmic} block
        # (separated by a bare \Statex, not a second \begin{algorithmic}) --
        # same "two \Procedures, one source block" shape as L08's
        # 04_dfs.tex (DFS/DFSVisit), so this is a single pseudocode.js
        # snippet, not two.
        ("06_chaining.tex", 0): "chained-hash-operations",
        ("07_open_addressing.tex", 0): "hash-search",
        ("07_open_addressing.tex", 1): "hash-put",
        ("11_deletion.tex", 0): "hash-delete",
    },
    # See chapters/09.inventory §(b). 2 of the 3 \Call occurrences sit inside
    # $...$/\(...\) math (KMPSearch's \Call{BuildLPS}{P}, Horspool's
    # \Call{BuildShiftTable}{P}) -- both fixed by hoist_call_out_of_math like
    # every other lecture's instances. The third (RabinKarp's
    # \Call{EqualAt}{$T,P,s$}) is already outside math in the source (only
    # its own args are math-wrapped), so it needs no fix -- EqualAt itself
    # has no \Procedure block at all (named-but-undefined, like L07's
    # Probe/FindSlot), connected via qmd prose instead. BuildLPS and
    # BuildShiftTable, by contrast, ARE each a complete standalone
    # \Procedure elsewhere in this same lecture, so KMPSearch calling
    # BuildLPS and Horspool calling BuildShiftTable are normal complete-to-
    # complete procedure references (no merge, no special handling needed
    # -- same as L06 BST's successor/predecessor or L07's ChainedPut/
    # ChainedSearch).
    "09": {
        ("02_naive.tex", 0): "naive-match",
        ("07_rabin_karp_analysis.tex", 0): "rabin-karp",
        ("11_kmp_preprocessing.tex", 0): "build-lps",
        ("12_kmp_search.tex", 0): "kmp-search",
        ("16_horspool.tex", 0): "build-shift-table",
        ("16_horspool.tex", 1): "horspool-search",
    },
    # See chapters/10.inventory §(b). Only 1 of 13 \Call occurrences sits
    # inside math (04_backtracking.tex's \ForAll{\(decision\in\Call{Candidates}
    # {state}\)}) -- fewest of any lecture so far, still fixed by
    # hoist_call_out_of_math. Backtrack and BranchAndBound are conceptual
    # skeletons only (IsComplete/IsFeasible/Report/Candidates/Apply/
    # IsPromising/Undo and RepresentsFeasibleSolution/IsComplete/Expand/
    # FeasibilityPossible are all named-but-undefined -- the L07 Probe/L09
    # EqualAt pattern, connected via qmd prose to the concrete algorithms
    # that instantiate them, not merged or given their own bodies).
    # AStar calling Relax is a normal complete-to-complete procedure
    # reference (both fully defined in 12_a_star.tex), same shape as L09's
    # KMPSearch/BuildLPS.
    "10": {
        ("03_permutation_combination.tex", 0): "choose-permutation",
        ("03_permutation_combination.tex", 1): "choose-combination",
        ("04_backtracking.tex", 0): "backtrack-skeleton",
        ("05_n_queens.tex", 0): "place-n-queens",
        ("06_subset_sum.tex", 0): "subset-sum",
        ("07_graph_coloring.tex", 0): "color-graph-coloring",
        ("09_branch_and_bound.tex", 0): "branch-and-bound-skeleton",
        ("12_a_star.tex", 0): "a-star",
        ("12_a_star.tex", 1): "relax",
    },
}


def find_brace_block(text, open_pos):
    """Given the index of a '{' in text, return (start, end) of the matching
    '}' (end exclusive one past it), brace-balanced."""
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


def hoist_precondition_before_procedure(body):
    """Move a `\\Require{...}`/`\\Ensure{...}`/`\\Input{...}`/`\\Output{...}`
    that appears as a `\\Procedure{...}{...}` body's first statement to just
    before that `\\Procedure` call, since pseudocode.js only accepts those
    as top-level algorithmic-scope statements (see module docstring)."""
    proc_m = PROCEDURE_HEAD_RE.search(body)
    if not proc_m:
        return body
    pos = proc_m.end()
    while pos < len(body) and body[pos].isspace():
        pos += 1
    pre_m = PRECONDITION_RE.match(body, pos)
    if not pre_m:
        return body
    brace_start = pre_m.end() - 1
    _, brace_end = find_brace_block(body, brace_start)
    precondition = body[pre_m.start():brace_end]
    return body[: proc_m.start()] + precondition + "\n" + body[proc_m.start() : pre_m.start()] + body[brace_end:]


def hoist_calls_from_span(content):
    """Split one math span's inner content (no delimiters) into alternating
    plain-math / bare-`\\Call` pieces, one `\\Call` at a time -- handles any
    number of `\\Call`s in the same span, not just a single one."""
    pieces = []
    pos = 0
    for m in CALL_RE.finditer(content):
        before = content[pos : m.start()]
        if before:
            pieces.append("$%s$" % before)
        pieces.append("\\Call{%s}{$%s$}" % (m.group(1), m.group(2)))
        pos = m.end()
    tail = content[pos:]
    if tail:
        pieces.append("$%s$" % tail)
    return "".join(pieces)


def hoist_call_out_of_math(body):
    """Hoist every `\\Call{...}{...}` out of the math spans it appears in
    (see module docstring point 1) -- covers both `$...$` and `\\(...\\)`
    delimiters (pseudocode.js's own lexer treats them identically) and any
    number of `\\Call`s within one span."""

    def repl(m):
        content = m.group(1) if m.group(1) is not None else m.group(2)
        if "\\Call" not in content:
            return m.group(0)
        return hoist_calls_from_span(content)

    return MATH_SPAN_RE.sub(repl, body)


def wrap_bare_text_commands(body):
    """`\\text{...}` is a math-mode command (valid only inside `$...$`/
    `\\(...\\)`); pseudocode.js's grammar has no non-math meaning for it
    (unlike `\\textbf`/`\\textrm`/etc., which its Lexer does recognize as
    plain text-mode commands -- see the font-cmd token table in the vendored
    library). One occurrence outside any math span
    (`06_topological_sort.tex`'s `\\Call{TopoVisit}{$v$}=\\text{CYCLE}`)
    throws a parse error that, like the `\\Call`-in-math case above, aborts
    pseudocode.js's single uncaught forEach over every block on the page --
    leaving every block *after* the offending one unrendered too. Fix:
    wrap any `\\text{...}` found outside an existing math span in `$...$`,
    leaving `\\text{...}` that's already properly inside math untouched."""
    spans = [m.span() for m in MATH_SPAN_RE.finditer(body)]

    def in_existing_math(pos):
        return any(start <= pos < end for start, end in spans)

    def repl(m):
        return m.group(0) if in_existing_math(m.start()) else "$%s$" % m.group(0)

    return BARE_TEXT_CMD_RE.sub(repl, body)


def squash_procedure_name_whitespace(body):
    """`\\Procedure{NAME}{args}`'s NAME cannot contain whitespace in
    pseudocode.js's grammar at all (see module docstring point 5) -- strip
    whitespace from just the NAME group, leaving the args group untouched."""

    def repl(m):
        return "\\Procedure{%s}" % re.sub(r"\s+", "", m.group(1))

    return PROCEDURE_NAME_RE.sub(repl, body)


def rename_statex_to_state(body):
    """`\\Statex` (algorithmicx's un-numbered continuation-line command) has
    no entry at all in pseudocode.js's statement grammar (only `\\State`/
    `\\Print`/`\\Return` are recognized) -- one occurrence
    (`06_topological_sort.tex`'s `\\Statex outer loop 후 ...`, describing
    what happens after the outer loop closes) throws `Expected `end` but
    received `Statex``. `\\State` is the closest supported equivalent; the
    only visible difference is a line-number prefix `\\Statex` omits, which
    doesn't change what the line says."""
    return STATEX_RE.sub("\\\\State", body)


def merge_algorithmic_bodies(bodies):
    """Merge multiple `\\Procedure{...}{...}...\\EndProcedure` bodies that
    describe one continuous algorithm split across several source frames
    (see module docstring) into a single body: only the first body's
    `\\Procedure` header and only the last body's `\\EndProcedure` survive,
    so the result reads as one procedure instead of several. Bodies are
    stripped of surrounding whitespace before joining so line breaks between
    the merged pieces are consistent regardless of source formatting."""
    parts = []
    for i, raw in enumerate(bodies):
        part = raw.strip()
        if i > 0:
            part = PROCEDURE_HEADER_LINE_RE.sub("", part, count=1).lstrip()
        if i < len(bodies) - 1:
            part = END_PROCEDURE_TAIL_RE.sub("", part).rstrip()
        parts.append(part)
    return "\n".join(parts)


def find_algorithmic_blocks(section_path):
    text = section_path.read_text(encoding="utf-8")
    for idx, m in enumerate(ALGORITHMIC_RE.finditer(text)):
        yield idx, m.group(2).strip()


def expected_rendered_count(lecture):
    """Number of distinct pseudocode.js blocks this lecture's rendered page
    should show: the number of distinct configured PSEUDOCODE_CONFIG slugs,
    not the raw count of `\\begin{algorithmic}` source blocks -- those can
    differ when merge_algorithmic_bodies folds more than one source block
    into a single rendered slug (see module docstring and PSEUDOCODE_CONFIG's
    "04" entry). Used by qa_check.py's gate 3 as the expected baseline."""
    sections_dir = LECTURE_NOTES / ("lecture%s" % lecture) / "sections"
    config = PSEUDOCODE_CONFIG.get(lecture, {})
    slugs = set()
    for section_path in sorted(sections_dir.glob("*.tex")):
        for idx, _ in find_algorithmic_blocks(section_path):
            slug = config.get((section_path.name, idx))
            if slug is not None:
                slugs.add(slug)
    return len(slugs)


def to_pseudocode_snippet(body):
    body = wrap_bare_text_commands(body)
    body = hoist_call_out_of_math(body)
    body = squash_procedure_name_whitespace(body)
    body = rename_statex_to_state(body)
    body = hoist_precondition_before_procedure(body)
    return "\\begin{algorithmic}\n%s\n\\end{algorithmic}" % body


def to_html_fragment(snippet):
    return (
        '```{=html}\n'
        '<pre class="pseudocode" data-line-number="true">\n'
        "%s\n"
        "</pre>\n"
        "```\n" % html.escape(snippet, quote=False)
    )


def _lecture_slug(lecture):
    return LECTURE_SLUGS.get(lecture, "lecture%s" % lecture)


def process_lecture(lecture, check_only):
    sections_dir = LECTURE_NOTES / ("lecture%s" % lecture) / "sections"
    out_dir = REPO_ROOT / "figures" / _lecture_slug(lecture)
    config = PSEUDOCODE_CONFIG.get(lecture, {})

    written, unmapped, missing = [], [], []
    manifest = {}

    # Group by slug (not just iterate block-by-block) so multiple source
    # blocks mapped to the same slug -- one algorithm split across several
    # frames, see PSEUDOCODE_CONFIG's "04" entry and module docstring -- are
    # merged into a single snippet instead of each producing its own file.
    slug_entries = {}
    for section_path in sorted(sections_dir.glob("*.tex")):
        for idx, body in find_algorithmic_blocks(section_path):
            key = (section_path.name, idx)
            slug = config.get(key)
            if slug is None:
                unmapped.append("%s#%d" % (section_path.name, idx))
                continue
            slug_entries.setdefault(slug, []).append((section_path.name, idx, body))

    for slug, entries in slug_entries.items():
        bodies = [body for _, _, body in entries]
        merged_body = bodies[0] if len(bodies) == 1 else merge_algorithmic_bodies(bodies)
        snippet = to_pseudocode_snippet(merged_body)
        manifest[slug] = (
            {"source": entries[0][0], "index": entries[0][1]}
            if len(entries) == 1
            else {"sources": [{"source": s, "index": i} for s, i, _ in entries]}
        )
        out_path = out_dir / ("pseudocode-%s.qmd" % slug)

        if check_only:
            if not out_path.exists() or out_path.read_text(encoding="utf-8") != to_html_fragment(snippet):
                missing.append(slug)
            continue

        out_dir.mkdir(parents=True, exist_ok=True)
        out_path.write_text(to_html_fragment(snippet), encoding="utf-8")
        written.append(slug)

    if not check_only:
        manifest_path = out_dir / ".pseudocode-manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")

    return written, unmapped, missing


def _run_one_lecture(lecture, check_only):
    """Process a single lecture and print its report (same format regardless
    of whether this is the sole --lecture run or one iteration of --all).
    Returns (written, unmapped, missing, failed) where `failed` matches the
    original single-lecture exit-code condition."""
    written, unmapped, missing = process_lecture(lecture, check_only)

    print("convert_pseudocode.py --lecture %s%s" % (lecture, " --check" if check_only else ""))
    print("  written:  %d" % len(written))
    print("  unmapped: %d" % len(unmapped))
    for u in unmapped:
        print("    UNMAPPED %s (add to PSEUDOCODE_CONFIG)" % u)
    if check_only:
        print("  stale/missing: %d" % len(missing))
        for m in missing:
            print("    %s" % m)

    failed = bool(unmapped or (check_only and missing))
    return written, unmapped, missing, failed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lecture", default=None, help="lecture number, e.g. 03")
    parser.add_argument("--all", action="store_true", help="process all lectures 01-10")
    parser.add_argument("--check", action="store_true", help="report status without writing files")
    args = parser.parse_args()

    if not args.lecture and not args.all:
        parser.error("one of --lecture LECTURE or --all is required")
    if args.lecture and args.all:
        parser.error("--lecture and --all are mutually exclusive")

    if not args.all:
        written, unmapped, missing, failed = _run_one_lecture(args.lecture, args.check)
        sys.exit(1 if failed else 0)

    lectures = sorted(LECTURE_SLUGS.keys())
    per_lecture = []
    failed_lectures = []
    for lecture in lectures:
        try:
            written, unmapped, missing, failed = _run_one_lecture(lecture, args.check)
        except Exception as e:
            print("  ERROR processing lecture %s: %s" % (lecture, e))
            written, unmapped, missing, failed = [], [], [], True
        per_lecture.append((lecture, len(written), len(unmapped), len(missing)))
        if failed:
            failed_lectures.append(lecture)
        print()

    total_written = sum(w for _, w, _, _ in per_lecture)
    total_unmapped = sum(u for _, _, u, _ in per_lecture)
    total_missing = sum(m for _, _, _, m in per_lecture)
    print("=== --all summary ===")
    for lecture, written_n, unmapped_n, missing_n in per_lecture:
        print("  %s: written=%d unmapped=%d missing=%d" % (lecture, written_n, unmapped_n, missing_n))
    print("  TOTAL: written=%d unmapped=%d missing=%d" % (total_written, total_unmapped, total_missing))
    if failed_lectures:
        print("  failed lectures: %s" % ", ".join(failed_lectures))

    sys.exit(1 if failed_lectures else 0)


if __name__ == "__main__":
    main()
