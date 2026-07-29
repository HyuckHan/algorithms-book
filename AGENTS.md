# AGENTS.md — Claude Code 진입점

이 저장소(algorithms-book)는 `HyuckHan/AlgorithmLectureNotes`의 Beamer 강의노트를
**Quarto 웹북**으로 변환·배포한다. 작업 에이전트는 세션 시작 시 아래를 이 순서로 읽는다.

1. 이 파일(AGENTS.md)
2. `SPEC.md` — 기술 사양(진실의 원천)
3. `docs/AGENT_WORKFLOW.md` — 작업 규칙·보고·커밋·HANDOFF
4. `docs/MILESTONES.md` — 현재 마일스톤과 완료/금지 조건
5. `docs/CONTENT_MODEL.md` — qmd 작성 규약과 status 워크플로
6. 변환 대상 강의의 `lecture-notes/docs/lectureNN_content_map.md`(교정 원장)
7. `docs/PER_LECTURE_NOTES.md` — 강의별 정확성 주의점
8. `docs/CODE_INVENTORY.md` — 강의별 코드 재고(어떤 알고리즘이 Java/C가 이미 있고 무엇을 신규
   작성해야 하는지; ADR-004 — from-scratch 알고리즘은 전 강의 C/Java/Python 3언어 필수)

핵심 원칙(어기지 말 것):
1. 손으로 다시 타이핑하지 않는다 — 의사코드·수식·코드·다이어그램은 소스에서 자동 생성.
2. 출력을 위조하지 않는다 — 코드 실행 결과는 빌드 시 실제 실행해 삽입.
3. 소스가 진실의 원천 — 강의노트는 `lecture-notes/`(submodule). 그 안을 수정하지 않는다.
4. 마일스톤 범위를 넘지 않는다 — 다음 마일스톤을 자동 시작하지 않는다.
5. 검증 없이 status를 verified/published로 올리지 않는다.
