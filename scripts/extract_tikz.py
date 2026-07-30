#!/usr/bin/env python3
"""Extract TikZ/pgfplots figures from lecture-notes sections into standalone SVGs.

Pipeline (SPEC 4.4): for each lecture, scan lecture-notes/lectureNN/sections/*.tex
for `tikzpicture`/`axis` (pgfplots) blocks, compile each as a standalone document
(lualatex) reusing the lecture's own TikZ styles, convert to SVG with dvisvgm,
and cache by content hash so unchanged figures are not recompiled.

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
ALT_HEAD_RE = re.compile(r"\\alt<([^>]*)>")

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
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usetikzlibrary{arrows.meta,positioning,calc,fit,trees,patterns,decorations.pathreplacing,matrix}
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
        ("02_execution.tex", 0): {"slug": "01-call-stack-push"},
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
        ("05_matrix_path.tex", 3): {"slug": "11-matrix-representative-cell"},
        ("05_matrix_path.tex", 4): {"slug": "12-matrix-reconstruction"},
        ("07_lcs.tex", 0): {"slug": "13-lcs-case1"},
        ("07_lcs.tex", 1): {"slug": "14-lcs-call-tree"},
        ("08_lcs_reconstruction.tex", 0): {"slug": "15-lcs-backtrack-trace"},
        ("11_summary_quiz.tex", 0): {"slug": "16-concept-map"},
    },
    # See chapters/08.inventory §2 for the full index-by-index derivation.
    # This lecture has the most sequence traces of any lecture so far (13,
    # 59 SVGs total) -- BFS queue, DFS recursion stack, Kahn zero-heap, DFS
    # topo finish-order, Prim key updates, Kruskal accept/reject, Dijkstra
    # finalized set, and more all need one SVG per overlay step so the
    # trace doesn't collapse to a single flattened final-state image.
    "08": {
        ("01_graph_basics.tex", 0): {"slug": "01-graph-definition"},
        ("02_representation.tex", 0): {"slug": "02-matrix-direction"},
        ("02_representation.tex", 1): {"slug": "03-matrix-to-list", "mode": "sequence"},
        ("03_bfs.tex", 0): {"slug": "04-bfs-graph"},
        ("03_bfs.tex", 1): {"slug": "05-bfs-queue-trace", "mode": "sequence"},
        ("03_bfs.tex", 2): {"slug": "06-bfs-path-reconstruction"},
        ("04_dfs.tex", 0): {"slug": "07-dfs-recursion-trace", "mode": "sequence"},
        ("05_cycle_detection.tex", 0): {"slug": "08-back-edge-animation", "mode": "sequence"},
        ("06_topological_sort.tex", 0): {"slug": "09-kahn-trace", "mode": "sequence"},
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
}


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
    """
    blocks = []
    pos = 0
    while True:
        m = ALT_HEAD_RE.search(text, pos)
        if not m:
            break
        spec = m.group(1)
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


def find_figures(section_path):
    """Yield (index, kind, raw_text) for each tikzpicture/axis block in a section file, in order."""
    text = section_path.read_text(encoding="utf-8")
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
    spans = sorted(tikz_spans + axis_spans, key=lambda s: s[0])
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
    if not pieces:
        raise ValueError(
            "no lecture%s/common.tex and no tikzset/newcommand found in %s -- "
            "figures may rely on styles this script doesn't know how to reproduce"
            % (lecture, main_tex_path)
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


def process_lecture(lecture, check_only, keep_build):
    sections_dir = LECTURE_NOTES / ("lecture%s" % lecture) / "sections"
    common_block = lecture_common_block(lecture)
    out_dir = REPO_ROOT / "figures" / _lecture_slug(lecture)
    config = FIGURE_CONFIG.get(lecture, {})

    manifest = load_manifest(out_dir)
    expected_files = set()
    built, cached, failed = [], [], []

    section_paths = sorted(sections_dir.glob("*.tex"))
    for section_path in section_paths:
        for idx, kind, raw in find_figures(section_path):
            key = (section_path.name, idx)
            cfg = config.get(key, {})
            slug = cfg.get("slug", "%s-%d" % (section_path.stem, idx))
            mode = cfg.get("mode", "flatten")

            steps = overlay_steps(raw)
            if mode == "sequence" and steps:
                targets = [(step, "%s-step%d" % (slug, i + 1)) for i, step in enumerate(steps)]
            else:
                target_state = max(steps) if steps else None
                targets = [(target_state, slug)]
            for target, out_slug in targets:
                body_tex = render_overlay_at(raw, target) if target is not None else raw
                content_hash = sha1(body_tex)
                out_svg = out_dir / ("%s.svg" % out_slug)
                expected_files.add(out_svg.name)

                if manifest.get(out_slug) == content_hash and out_svg.exists():
                    cached.append(out_slug)
                    continue

                if check_only:
                    failed.append((out_slug, "not yet built (hash changed or missing)"))
                    continue

                ok, err = compile_svg_verified(body_tex, common_block, out_svg, out_slug)
                if ok:
                    manifest[out_slug] = content_hash
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
        "05": "05-dynamic-programming", "08": "08-graphs",
    }
    return names.get(lecture, "lecture%s" % lecture)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lecture", default="03", help="lecture number, e.g. 03 (default: 03)")
    parser.add_argument("--check", action="store_true", help="report status without compiling")
    parser.add_argument("--keep-build", action="store_true", help="keep the LaTeX build cache dir for debugging")
    args = parser.parse_args()

    built, cached, failed, expected_files, manifest = process_lecture(args.lecture, args.check, args.keep_build)

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
