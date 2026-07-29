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
    applied).

Gates 1/2/4/5/7 from docs/QUALITY_ASSURANCE.md are NOT implemented here yet
(tracked for M2 per docs/MILESTONES.md); this script does not claim to check
them. It also reports raw-math leakage, broken images, missing alt text, and
console/request errors as a side effect of the same page load, since the
browser_check.mjs pass already collects them, but only gates 3 and 6 affect
the exit code.

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
    "03": {"lecture_notes_dir": "lecture03", "chapter_html": "chapters/03-sorting.html"},
}


def source_algorithmic_count(lecture):
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import convert_pseudocode as cp  # local import: scripts/ is not normally on sys.path

    sections_dir = cp.LECTURE_NOTES / ("lecture%s" % lecture) / "sections"
    count = 0
    for section_path in sorted(sections_dir.glob("*.tex")):
        count += sum(1 for _ in cp.find_algorithmic_blocks(section_path))
    return count


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
