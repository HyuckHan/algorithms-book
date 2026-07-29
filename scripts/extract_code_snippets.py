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
