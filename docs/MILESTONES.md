# MILESTONES

## 공통 실행 규칙

각 마일스톤: (1) 관련 문서·코드 읽기 → (2) 변경 범위 요약 → (3) 구현 → (4) 검증 실행 →
(5) 문서 갱신 → (6) 하나의 논리적 커밋. **명시 범위를 넘어 다음 마일스톤을 자동 시작하지 않는다.**

---

## M0 — Baseline & Bootstrap

**목표** 강의노트 빌드 계약을 보존하고 웹북 기반을 세운다.
**작업**
- `lecture-notes/` submodule 추가(recursive).
- 툴체인 점검: quarto, lualatex/xelatex, dvisvgm, javac, gcc, python3 버전 보고.
- 강의노트 실제 빌드(`make -C lecture-notes lecture03` 등) 성공 여부 확인. metropolis 테마·Noto CJK 폰트 부재 시 정확히 보고.
- `_quarto.yml`·`scripts/` 골격으로 거의 빈 책 `quarto render` 성공.
- GitHub Actions → Pages 배포 파이프라인이 (빈 페이지라도) 통과.
**완료 조건** 성공/실패 빌드가 명확. 웹 작업이 강의노트 빌드를 손상하지 않는 기준 확립. Pages에 무언가 배포됨.
**금지** 강의 콘텐츠 변환, submodule 내용 수정.

---

## M1 — 파일럿: L03 정렬 수직 슬라이스

**목표** L03 한 강을 학생이 쓸 품질로 완성하며 **파이프라인을 확정**한다.
**작업**
- `extract_tikz.py`로 L03 TikZ 18개 → SVG. `\only` 정렬/merge는 단계 시퀀스 표본 제작.
- `convert_pseudocode.py`로 L03 의사코드 12개 → pseudocode.js 렌더(줄바꿈·들여쓰기 정상).
- `code/03-sorting/`에 C/Java(강의노트 복사)+Python(신규) 탭, `run_examples.py`로 실제 출력 삽입·3언어 일치.
- content map(L03) 교정 반영: Bubble 함수명, 하한 O→Ω, BUILD-MAX-HEAP Θ(n), Comparator interface, comparator overflow(§PER_LECTURE_NOTES).
- 챕터 구조(§CONTENT_MODEL 3)·frontmatter·학습목표·Checkpoint.
**완료 조건** §QUALITY_ASSURANCE 품질 게이트 전부 통과. status `review` 이상. content map 매핑표 존재.
**금지** 다른 강의 대량 변환, 미검증 status 상향.

---

## M2 — 파이프라인 안정화 + 거버넌스

**목표** 파일럿에서 검증된 절차를 재사용 가능하게 굳힌다.
**작업**
- frontmatter 스키마 검증(잘못된 lecture/누락 title/중복 slug → 빌드 실패).
- `qa_check.py` 헤드리스 품질 게이트 스크립트 완성.
- 교육 callout/shortcode(Definition/Invariant/CommonMistake/Checkpoint/Exercise/Solution) 정형화.
- `docs/CONTENT_ISSUES.md`, `docs/HANDOFF.md` 초기화.
**완료 조건** 페이지 추가만으로 목차·검색 자동 반영. 스키마·품질 게이트가 CI에서 강제됨.

---

## M3 — 수평 확대 (L01·L02·L05·L08)

**목표** 안정화된 파이프라인으로 4개 강의 변환.
**작업** 강의당 반복: inventory → page map → qmd draft → 그림/코드 통합 → 기술 검토 → 교육 검토 → publish.
강의당 여러 커밋(A: inventory/map, B: 정적 콘텐츠, C: 그림/코드, D: 검증/polish).
**완료 조건** 각 강의 §MIGRATION 7 완료 기준 충족. status `verified` 이상.

---

## M4 — 고밀도 챕터 + 마감 (L04·L06·L07·L09·L10)

**목표** 나머지 변환. **L06(TikZ 55)**에서 캐시·병렬 컴파일 튜닝.
**작업** 위 반복. 표지/서문, 개념 다리(heap↔PQ, Master Theorem 재호명 — 강의노트 bridge frame 활용), 용어집, PDF 출력 정리.
**완료 조건** 전 강의 verified 이상. 전체 링크·접근성 감사 통과. HTML+PDF 배포.

---

## M5 — 운영 하드닝 (선택)

full link check, Lighthouse CI(90+ 목표), axe 접근성, 의존성 audit, 이미지 최적화, print stylesheet,
citation/license 페이지, release tag. (콘텐츠 안정화 후.)

---

## 마일스톤 간 status 규칙
각 챕터는 `draft`로 생성되어 기술+교육 검토 후에만 `verified`로 올라간다. 에이전트는 검토 증거
(검증 명령 결과, content map 매핑) 없이 상향하지 않는다.
