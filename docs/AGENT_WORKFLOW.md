# AGENT_WORKFLOW — Claude Code 작업 규칙

## 1. 목적

Claude Code가 저장소를 안정적으로 수정하도록 읽기 순서·작업 범위·검증·커밋·보고·HANDOFF를 정의한다.

## 2. 세션 시작 시 읽을 것

1. 루트 `AGENTS.md`
2. `SPEC.md`
3. 현재 `docs/MILESTONES.md`의 해당 마일스톤
4. `docs/CONTENT_MODEL.md`, 변환 대상의 `lecture-notes/docs/lectureNN_content_map.md`, `docs/PER_LECTURE_NOTES.md`,
   `docs/CODE_INVENTORY.md`(그 강의의 Java/C 기존 여부·신규 작성 대상 — "Python만 신규"라고 가정하지 말 것)
5. 수정 대상 디렉터리의 기존 코드·스크립트

## 3. 세션 시작 명령

```bash
git status --short
git branch --show-current
git log -5 --oneline
git submodule status
```
작업 트리가 깨끗하지 않으면 기존 변경을 덮어쓰지 않는다. 사용자 변경과 에이전트 변경을 분리한다.

## 4. 작업 방식

- 한 세션은 원칙적으로 **하나의 마일스톤**만. 다음 마일스톤을 선행 구현하지 않는다.
- 요구되지 않은 대규모 refactor·검증 없는 의존성 교체 금지.
- `lecture-notes/`(submodule) 내용을 수정하지 않는다(읽기전용 소스).
- 생성 파일(figures/*.svg 등)과 소스 파일을 혼동한 커밋 금지.
- 공통 기반과 콘텐츠 변환을 같은 거대 커밋에 넣지 않는다. 하나의 커밋 = 하나의 논리적 목적.

## 5. 구현 전 보고 형식

```
Understanding
- 현재 마일스톤 목표
- 읽은 주요 파일
- 변경할 파일 범위
- 보존할 기존 계약

Plan
1. …

Risks
- …
```

## 6. 검증 규칙 (수정 범위에 맞게 반드시 실행, 성공 안 한 걸 성공이라 하지 않음)

```bash
# 빌드
quarto render                 # 또는 quarto render chapters/NN-*.qmd
# 파이프라인
python3 scripts/extract_tikz.py --all --check
python3 scripts/convert_pseudocode.py --all --check
python3 scripts/run_examples.py --lecture NN     # 3언어 출력 일치(수정한 강의 하나)
# 품질 게이트(§QUALITY_ASSURANCE): 헤드리스 검사
python3 scripts/qa_check.py _book/…              # 원시수식 0, 그림 개수 일치, 오버플로 0, 대비, alt
```
명령이 아직 없으면 해당 마일스톤에서 정의하거나 실행 불가 사유를 보고한다.

## 7. 완료 보고 형식

```
Completed        - 구현 내용
Files changed    - path: 목적
Validation       - 명령: 결과(정확히)
Known limitations- 남은 문제
Suggested commit - type(scope): summary
```

## 8. 커밋 정책 (Conventional Commits)

```
chore(scaffold): add Quarto book project skeleton
feat(pipeline): extract TikZ to SVG via dvisvgm with hash cache
feat(pseudocode): convert algorithmic blocks with pseudocode.js
feat(lecture03): publish merge sort chapter (status: review)
test(qa): add headless raw-math and overflow checks
fix(lecture07): distinguish expected and worst-case hash lookup
docs(spec): record ADR for Quarto over Next.js
```
커밋 전:
```bash
git diff --check
git status --short
git diff --stat
```

## 9. 초기 프롬프트 (Milestone 0 시작)

```
You are working in the algorithms-book repository.

Read, in order: AGENTS.md, SPEC.md, docs/AGENT_WORKFLOW.md, docs/MILESTONES.md,
docs/ARCHITECTURE.md, docs/CONTENT_MODEL.md, docs/MIGRATION_STRATEGY.md,
docs/PER_LECTURE_NOTES.md, and the existing scripts/ and _quarto.yml.

Perform only Milestone 0: Baseline & Bootstrap.
- Add HyuckHan/AlgorithmLectureNotes as a git submodule at lecture-notes/.
- Check for quarto, lualatex/xelatex, dvisvgm, javac, gcc, python3 and report versions.
- Confirm `make -C lecture-notes lecture03` (or the deck's build) succeeds in this environment;
  if TeX theme/fonts are missing, report exactly what is missing. Do not hide failures.
- Get `quarto render` to build an (near-empty) book and confirm the Pages deploy workflow runs.
- Do NOT convert lecture content yet. Preserve uncommitted user changes.
End with: completed work, files changed, commands+results, known limitations, suggested commit.
```

## 10. 마일스톤 전환 프롬프트 템플릿

```
Read AGENTS.md, SPEC.md, and docs/* first. Review git status and the previous milestone output.
Perform only Milestone <N>: <name> from docs/MILESTONES.md.
Constraints: stay in scope; do not modify lecture-notes/ submodule content; add/update checks for changed
behavior; run all relevant validations and report exact results; do not set status verified/published
without review evidence; do not begin the next milestone.
Report: completed work, files changed, validation commands+results, known limitations, suggested commit.
```

## 11. HANDOFF (`docs/HANDOFF.md` 유지)

다른 세션/머신에서 이어갈 때 기록: 현재 branch·HEAD, submodule commit, 완료·진행 마일스톤, 변경 파일,
마지막 검증 결과, 알려진 실패, 다음에 실행할 정확한 명령, 다음 프롬프트. HANDOFF는 상태 보고이지
마일스톤 자동 승인 문서가 아니다.
