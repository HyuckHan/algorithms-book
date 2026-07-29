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

One normalization is applied: `\\Call{name}{args}` occasionally appears
*inside* math delimiters in the source (e.g. `$p\\gets\\Call{Partition}{A,low,high}$`
in 08_quick_sort.tex) even though `\\Call` is pseudocode.js/algorithmicx
markup, not real math -- that fails to parse as math. Such spans are hoisted
out of the surrounding `$...$` (moving only the true math sub-parts back
inside `$...$`), matching how `\\Call` is written everywhere else in the
lecture notes.
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
}


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
    names = {"03": "03-sorting"}
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
