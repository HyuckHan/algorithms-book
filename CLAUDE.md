# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`algorithms-book` converts the Beamer lecture slides in `HyuckHan/AlgorithmLectureNotes` (included
here as the read-only git submodule `lecture-notes/`) into a Quarto webbook (HTML + PDF). It is a
content-migration/build-pipeline project, not an application: most of the "code" is Quarto config,
Python conversion scripts, and `.qmd` chapter content in Korean.

**Current state (check before assuming otherwise):** the project is at the bootstrap stage. `scripts/build.sh`
and `_quarto.yml` are drafts. The pipeline scripts they reference — `scripts/extract_tikz.py`,
`scripts/convert_pseudocode.py`, `scripts/run_examples.py`, `scripts/qa_check.py` — **do not exist yet**.
`chapters/` is empty. Only `code/03-sorting/python/sorting.py` exists under `code/`. Verify with
`ls scripts/ chapters/` rather than trusting doc descriptions of the finished pipeline.

## Required reading order

This repo governs itself through a stack of docs. Read them in this order before making non-trivial
changes — do not skip to implementation from a single file:

1. `AGENTS.md` — entrypoint, the three non-negotiable principles (see below)
2. `SPEC.md` — master technical spec; **source of truth for the pipeline, ties with `docs/DECISIONS.md` on conflicts**
3. `docs/AGENT_WORKFLOW.md` — session start commands, report format, commit policy (below)
4. `docs/MILESTONES.md` — current milestone and its exact scope/prohibitions
5. `docs/CONTENT_MODEL.md` — `.qmd` frontmatter schema, page structure, status workflow
6. The target lecture's `lecture-notes/docs/lectureNN_content_map.md` and `docs/PER_LECTURE_NOTES.md`
   — per-lecture correctness fixes that must be preserved when converting that lecture
7. `docs/ARCHITECTURE.md`, `docs/MIGRATION_STRATEGY.md`, `docs/QUALITY_ASSURANCE.md`, `docs/DECISIONS.md` (ADRs)
   as needed for the task at hand

## Three principles that override convenience

1. **Never hand-retype.** Pseudocode, formulas, diagrams, and code are generated from
   `lecture-notes/` sources, never typed by hand into `.qmd`. (A past prototype broke line-wrapping
   by hand-pasting pseudocode into HTML — do not repeat that.)
2. **Never fake output.** Code execution results shown in the book must come from actually running
   the C/Java/Python at build time (`scripts/run_examples.py`), not from remembered/typed output.
3. **The submodule is the source of truth and is read-only.** Never edit files under `lecture-notes/`.
   If the lecture notes need a correction, that's tracked via the content map, not a local edit.

## Working within a milestone

Milestones (`docs/MILESTONES.md`, M0–M5) define scope. One Claude Code session = one milestone;
do not start the next milestone unprompted, and do not do large unrequested refactors. Session start:

```bash
git status --short
git branch --show-current
git log -5 --oneline
git submodule status
```

If the working tree isn't clean, don't overwrite existing changes — separate user edits from agent edits.

## Build / validation commands

```bash
# One-time setup
git submodule update --init --recursive

# Toolchain check (required before M0-type work)
quarto --version            # >= 1.4
which lualatex xelatex
dvisvgm --version
python3 --version           # >= 3.10
javac -version; gcc --version

# Full pipeline (draft order — scripts must exist first, see "Current state" above)
bash scripts/build.sh        # extract_tikz -> convert_pseudocode -> run_examples -> quarto render

# Targeted
quarto render                          # or: quarto render chapters/NN-*.qmd
python3 scripts/run_examples.py --lecture NN   # verify C/Java/Python stdout match
python3 scripts/qa_check.py _book/...          # quality gate: raw-math, figure count, overflow, contrast, alt-text
```

Never report a check as passing when it didn't run (e.g. missing local TeX theme/fonts) — report the
exact gap instead per `docs/QUALITY_ASSURANCE.md` §6.

## Architecture: build data flow

```
lecture-notes/ (submodule, read-only)
   sections/*.tex --extract_tikz.py--> figures/NN/*.svg (SHA1-cached)
   sections/*.tex --convert_pseudocode.py--> pseudocode.js snippets
   code/NN/{java,c} + code/NN/python (new) --run_examples.py--> captured stdout, 3-language diff
                              v
                  chapters/NN-*.qmd (frontmatter + body + generated inserts)
                              v
                       quarto render (HTML + PDF)
                              v
              quality gates --> GitHub Pages deploy (.github/workflows/deploy.yml)
```

Key structural facts:
- One lecture (`lecture01`–`lecture10`) maps to one chapter `.qmd`, split into 5–15 min sections.
- Diagrams: TikZ/pgfplots are compiled standalone with the *same preamble as the lecture notes*
  (`theme/beamerthemealgorithms`, `common/pedagogy.tex`, per-lecture `common.tex`) then run through
  `dvisvgm`, never re-implemented in a web framework (ADR-003 in `docs/DECISIONS.md`).
  `\only`/`\visible` overlays are flattened to final state, or pulled into a step SVG sequence when
  the step-by-step state matters pedagogically.
  Pseudocode: `algorithmic` blocks map to pseudocode.js via token mapping (`\Procedure`, `\State`,
  `\If/\ElsIf/\Else`, `\For/\ForAll`, `\While`, `\Return`, `\Call`, `\gets`, `\textproc`); unmapped
  blocks fall back to SVG.
  Code: Java/C come from `lecture-notes/code/lectureNN/`; Python is newly written per lecture with
  the same algorithm and example inputs. Web display uses Quarto `panel-tabset` with `include=` file
  injection — never paste code directly into `.qmd`.
- `.qmd` frontmatter carries a `status` field: `draft -> review -> verified -> published`. Never
  advance status without validation evidence (build/test output, content-map cross-check) — see
  `docs/CONTENT_MODEL.md` §2 for the full schema and `docs/QUALITY_ASSURANCE.md` for the gate list.
- Body text is Korean; code and established technical terms stay in their original language.

## Commit conventions

Conventional Commits, one logical purpose per commit (don't mix pipeline/infra changes with content
changes). Before committing: `git diff --check`, `git status --short`, `git diff --stat`. Example
scopes used in this repo: `chore(scaffold)`, `feat(pipeline)`, `feat(pseudocode)`, `feat(lectureNN)`,
`test(qa)`, `fix(lectureNN)`, `docs(spec)`.

## Report format expected at end of a task

Per `docs/AGENT_WORKFLOW.md`, structure implementation reports as:

```
Completed        - what was implemented
Files changed    - path: purpose
Validation       - command: exact result
Known limitations- what's left
Suggested commit - type(scope): summary
```
