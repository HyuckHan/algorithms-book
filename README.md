# algorithms-book

`HyuckHan/AlgorithmLectureNotes`의 Beamer 강의노트를 **Quarto 웹북**으로 변환·배포하는 저장소.
설계는 Quarto 파이프라인(TikZ 자동 SVG 변환·코드 3버전)을 뼈대로, 콘텐츠 거버넌스·에이전트
작업 규율·강의별 정확성 주의점을 결합한 **하이브리드** 사양이다.

## 문서 읽는 순서
1. `AGENTS.md` — 에이전트 진입점(핵심 원칙)
2. `SPEC.md` — 기술 사양(진실의 원천)
3. `docs/PRODUCT_VISION.md` — 목표·독자·범위·성공기준
4. `docs/ARCHITECTURE.md` — Quarto·submodule·빌드 흐름·배포
5. `docs/CONTENT_MODEL.md` — qmd 작성 규약·status 워크플로
6. `docs/MIGRATION_STRATEGY.md` — 변환 단계·파이프라인·강의 순서
7. `docs/PER_LECTURE_NOTES.md` — 강의별 정확성 주의점(교정 원장 요약)
8. `docs/AGENT_WORKFLOW.md` — 작업 규칙·검증·커밋·HANDOFF
9. `docs/MILESTONES.md` — 마일스톤 M0–M5(완료/금지)
10. `docs/QUALITY_ASSURANCE.md` — 품질 게이트·검사
11. `docs/DECISIONS.md` — ADR(왜 Quarto·왜 SVG 변환 등)

## 시작
```bash
git submodule add https://github.com/HyuckHan/AlgorithmLectureNotes.git lecture-notes
git submodule update --init --recursive
# 툴체인: quarto, lualatex/xelatex, dvisvgm, javac, gcc, python3 (SPEC 3장)
bash scripts/build.sh   # extract_tikz → convert_pseudocode → run_examples → quarto render
```
Claude Code로 진행: `AGENTS.md`의 §9 초기 프롬프트로 Milestone 0부터 시작.

## 핵심 원칙
- 손으로 다시 타이핑하지 않는다(소스 자동 생성).
- 출력을 위조하지 않는다(빌드시 실제 실행).
- 소스가 진실의 원천(`lecture-notes/` submodule은 읽기전용).
