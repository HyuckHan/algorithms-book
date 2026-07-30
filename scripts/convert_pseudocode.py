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
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LECTURE_NOTES = REPO_ROOT / "lecture-notes"

ALGORITHMIC_RE = re.compile(r"\\begin\{algorithmic\}(\[[^\]]*\])?(.*?)\\end\{algorithmic\}", re.DOTALL)
MATH_SPAN_RE = re.compile(r"\$([^$]*)\$|\\\(((?:(?!\\\)).)*)\\\)", re.DOTALL)
CALL_RE = re.compile(r"\\Call\{([^{}]*)\}\{([^{}]*)\}")
BARE_TEXT_CMD_RE = re.compile(r"\\text\{[^{}]*\}")
STATEX_RE = re.compile(r"\\Statex\b")
PROCEDURE_HEAD_RE = re.compile(r"\\Procedure\{[^{}]*\}\{[^{}]*\}")
PROCEDURE_NAME_RE = re.compile(r"\\Procedure\{([^{}]*)\}")
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
    "04": {
        ("03_sort_then_select.tex", 0): "select-by-sorting",
        ("04_quickselect_idea.tex", 0): "fixed-quickselect",
        ("08_randomized_select.tex", 0): "randomized-select",
        ("10_group_of_five.tex", 0): "deterministic-select-pivot",
        ("10_group_of_five.tex", 1): "deterministic-select-partition",
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


def find_algorithmic_blocks(section_path):
    text = section_path.read_text(encoding="utf-8")
    for idx, m in enumerate(ALGORITHMIC_RE.finditer(text)):
        yield idx, m.group(2).strip()


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
    names = {
        "01": "01-introduction", "03": "03-sorting", "04": "04-selection",
        "05": "05-dynamic-programming", "08": "08-graphs",
    }
    return names.get(lecture, "lecture%s" % lecture)


def process_lecture(lecture, check_only):
    sections_dir = LECTURE_NOTES / ("lecture%s" % lecture) / "sections"
    out_dir = REPO_ROOT / "figures" / _lecture_slug(lecture)
    config = PSEUDOCODE_CONFIG.get(lecture, {})

    written, unmapped, missing = [], [], []
    manifest = {}

    for section_path in sorted(sections_dir.glob("*.tex")):
        for idx, body in find_algorithmic_blocks(section_path):
            key = (section_path.name, idx)
            slug = config.get(key)
            if slug is None:
                unmapped.append("%s#%d" % (section_path.name, idx))
                continue

            snippet = to_pseudocode_snippet(body)
            manifest[slug] = {"source": section_path.name, "index": idx}
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lecture", default="03", help="lecture number, e.g. 03 (default: 03)")
    parser.add_argument("--check", action="store_true", help="report status without writing files")
    args = parser.parse_args()

    written, unmapped, missing = process_lecture(args.lecture, args.check)

    print("convert_pseudocode.py --lecture %s%s" % (args.lecture, " --check" if args.check else ""))
    print("  written:  %d" % len(written))
    print("  unmapped: %d" % len(unmapped))
    for u in unmapped:
        print("    UNMAPPED %s (add to PSEUDOCODE_CONFIG)" % u)
    if args.check:
        print("  stale/missing: %d" % len(missing))
        for m in missing:
            print("    %s" % m)

    sys.exit(1 if (unmapped or (args.check and missing)) else 0)


if __name__ == "__main__":
    main()
