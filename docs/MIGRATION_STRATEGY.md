# MIGRATION_STRATEGY

## 1. 목표

L01–10 Beamer 자료를 Quarto 웹북으로 변환하되 content map의 교정·재구성을 보존한다.
기계적 TeX→qmd 변환이 아니라 **의미 단위 재편집**이다(슬라이드=압축 발표, 웹=연속 읽기).

## 2. 원천 우선순위 (충돌 시)

1. 검증된 코드·테스트 → 2. content map 교정 정책·convention → 3. 현재 LaTeX 소스 → 4. 원본 PPTX.
에이전트는 충돌을 임의 해결하지 않고 `docs/CONTENT_ISSUES.md`에 기록한다.

## 3. 변환 단계 (강의당)

**A. 인벤토리** — `lectureNN/lectureNN.tex`의 `\input` 순서로 section·frame 제목, 정의·알고리즘·예제·수식,
코드 참조, TikZ/pgfplots, 퀴즈/checkpoint, content map 교정 항목을 수집 → `chapters/NN.inventory.json`.

**B. 웹 목차 설계** — 슬라이드 순서를 복제하지 않고 5–15분 단위로 절 구성. 절마다 slug·제목·학습목표·원본 frame 범위·필요 컴포넌트·코드/그림 의존성·검증 책임 결정.

**C. 텍스트 변환** — bullet을 완결된 문장·단락으로. 발표자가 구두로 잇던 논리 보완. 중복 frame 통합.
`\only` 오버레이는 추적표/탭/스텝/정적 단계로 변환.

**D. 다이어그램 변환** — 우선순위: (1) 강의노트 **TikZ→dvisvgm SVG**(원본 일치), (2) 학습상 중요한 것만 단계 SVG 시퀀스,
(3) 접근 가능한 HTML/CSS, (4) 선별적 인터랙티브. 화면 캡처는 금지(임시도 지양).

**E. 코드 연결** — `code/`가 canonical. 테스트 통과 코드만 노출. 긴 파일은 marker로 일부 추출. 다운로드는 전체 파일.
Python은 신규 작성(§CONTENT_MODEL 5).

**F. 검증** — content map↔페이지 매핑, 수식·알고리즘 결과 검산, 코드 빌드/실행(3버전 출력 일치), 링크·접근성, status 갱신.

## 4. 파이프라인 구현 (scripts/)

- **extract_tikz.py**: 각 `sections/*.tex`의 `tikzpicture`/`axis` 블록 추출 → **강의노트와 동일 프리앰블**의
  `standalone` 문서로 감싸 lualatex 컴파일 → `dvisvgm` → `figures/NN/tikz-<sha1>.svg`. SHA1 캐시. `\only`는 최종상태 평탄화(전처리),
  일부는 상태별로 여러 SVG. L06(55개)는 병렬 컴파일.
- **convert_pseudocode.py**: `algorithmic` 블록 → pseudocode.js 스니펫. 매핑 토큰: `\Procedure/\State/\If/\ElsIf/\Else/\For/\ForAll/\While/\Return/\Call/\gets(←)/\textproc`. 실패 블록만 SVG 폴백. **손 타이핑 금지.**
- **run_examples.py**: C(`gcc -Wall`)·Java(`javac/java`)·Python 실제 컴파일·실행 → stdout 캡처 → `figures/NN/out-<lang>.txt`. **3언어 출력 일치 검증.**
- **build.sh**: extract_tikz → convert_pseudocode → run_examples → `quarto render`.

## 5. 강의별 초점 (정확성 주의점은 §PER_LECTURE_NOTES)

- **L01** 알고리즘/명세/프로그램, 추적, invariant, 선형/이진 탐색, 비용모델, 성장차수, O/Ω/Θ.
- **L02** 재귀 구조, base/progress, call stack, recurrence, recursion tree, 반복 vs 재귀.
- **L03** 단순정렬 3종, merge/quick, heap/heapsort, counting/radix, stability·in-place·adaptive, 비교 하한. (파일럿)
- **L04** rank/order statistic, Quickselect, randomized, 3-way partition, median of medians, 평균/기대/최악.
- **L05** State→Transition→Base→Order→Answer/Reconstruction. Fibonacci, matrix path, LCS, max subarray.
- **L06** 용어, BST, AVL, Red-Black, B-Tree. (TikZ 55 — 병렬·캐시)
- **L07** hash pipeline, collision/duplicate, chaining, open addressing, deletion marker, resizing amortized, expected vs worst, hash flooding.
- **L08** 표현, BFS/DFS, topological sort, MST(Prim/Kruskal), 최단경로(Dijkstra/Bellman–Ford).
- **L09** naive, Rabin–Karp, border/LPS·KMP, Boyer–Moore–Horspool.
- **L10** candidate/feasible/optimal, backtracking, pruning, branch-and-bound, incumbent/bound, permutation/combination.

## 6. 변환 우선순위

파일럿 **L03**(정렬)을 먼저 완성한다 — 의사코드 12·TikZ 18·코드 3버전이 모두 등장해 **파이프라인 전체를 검증**한다.
이후 컴포넌트 재사용·주제 다양성을 고려한 순서:

```
L03(파일럿) → L01 → L02 → L05 → L08 → L04 → L06 → L07 → L09 → L10
```
(웹 구현 우선순위이며 강의 진행 순서를 바꾸지 않는다.)

## 7. 강의 완료 기준

- [ ] 계획된 모든 페이지 생성
- [ ] content map 핵심 항목이 페이지에 매핑(교정 보존)
- [ ] 의사코드·예제 결과 검증
- [ ] 관련 코드 3버전 빌드/실행·출력 일치
- [ ] 최소 1개 형성평가(Checkpoint/Exercise)
- [ ] 강의 요약과 다음 강의 연결(개념 다리 — 강의노트 bridge frame 활용)
- [ ] 모바일·키보드·접근성 통과
- [ ] status `verified` 이상
