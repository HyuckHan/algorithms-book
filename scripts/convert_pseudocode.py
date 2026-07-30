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

Two normalizations are applied, both moving text rather than rewriting it
(neither changes what the pseudocode says, only where pseudocode.js's
stricter-than-algorithmicx grammar needs it to sit):

1. `\\Call{name}{args}` occasionally appears *inside* math delimiters in the
   source (e.g. `$p\\gets\\Call{Partition}{A,low,high}$` in 08_quick_sort.tex)
   even though `\\Call` is pseudocode.js/algorithmicx markup, not real math --
   that fails to parse as math. Such spans are hoisted out of the
   surrounding `$...$` (moving only the true math sub-parts back inside
   `$...$`), matching how `\\Call` is written everywhere else in the lecture
   notes.
2. `\\Require`/`\\Ensure`/`\\Input`/`\\Output` are only valid, per the vendored
   parser, as top-level statements directly inside `\\begin{algorithmic}`,
   not nested inside a `\\Procedure{...}{...}...\\EndProcedure` body -- a
   nested `\\Require` throws `Expected endProcedure but received Require`
   (confirmed directly against the parser; L01's Maximum places `\\Require`
   as the procedure's first body statement, which is valid algorithmicx but
   not valid pseudocode.js, and never came up in L03 since nothing there
   uses `\\Require`/`\\Ensure`). Such statements are hoisted to just before
   the `\\Procedure{...}{...}` call so they parse as a top-level
   precondition/postcondition annotation instead.
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
CALL_IN_MATH_RE = re.compile(r"\$([^${}]*)\\Call\{([^{}]*)\}\{([^{}]*)\}([^${}]*)\$")
PROCEDURE_HEAD_RE = re.compile(r"\\Procedure\{[^{}]*\}\{[^{}]*\}")
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


def hoist_call_out_of_math(body):
    def repl(m):
        before, name, args, after = m.groups()
        out = ("$%s$" % before) if before else ""
        out += "\\Call{%s}{$%s$}" % (name, args)
        if after:
            out += "$%s$" % after
        return out

    return CALL_IN_MATH_RE.sub(repl, body)


def find_algorithmic_blocks(section_path):
    text = section_path.read_text(encoding="utf-8")
    for idx, m in enumerate(ALGORITHMIC_RE.finditer(text)):
        yield idx, m.group(2).strip()


def to_pseudocode_snippet(body):
    body = hoist_call_out_of_math(body)
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
    names = {"01": "01-introduction", "03": "03-sorting", "05": "05-dynamic-programming"}
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
