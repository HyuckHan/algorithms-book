# PER_LECTURE_NOTES — 강의별 정확성 주의점

각 강의를 웹으로 변환할 때 **반드시 보존해야 할 교정·convention**. 원장은
`lecture-notes/docs/lectureNN_content_map.md`이며, 변환 시 그 교정 항목을 웹에 그대로 유지한다.
아래는 그 원장에서 뽑은 핵심 요약이다(전체는 각 content map 참조).

## L01 · 알고리즘 입문 / 복잡도
- `O`를 "대략 같다"로 오해하지 않게: **상한**임을 명확히(원본 오개념 교정).
- 비용 모델·case analysis를 결과에 병기. Orders of Growth, O/Ω/Θ 구분.
- pgfplots 성장 곡선 6개 → SVG 변환 대상.

## L02 · 재귀
- Master Theorem은 **표준 case 1·2·3 순서**로, 결과는 Θ로 교정.
- call stack·recurrence·recursion tree 시각화(TikZ 14개) 변환. `\only` 스택 애니메이션은 단계 시퀀스 후보.

## L03 · 정렬 (파일럿)
- **Bubble 함수명 오기 삭제**(잘못 적힌 `selectionSort`), Quick Sort expected time,
  비교 정렬 하한 **`O`→`Ω` 교정**, BUILD-MAX-HEAP **`O(n log n)`→`Θ(n)`**(레벨별 비용 합 증명),
  Java **Comparator `class extends`→interface/functional interface** 교정, C/Java 정수 comparator
  **`a-b` overflow→relational comparison** 교정.
- Merge midpoint는 **overflow-safe** `low+⌊(high-low)/2⌋`.
- Heapsort·Counting Sort는 원본 17장/다장을 **5-state/4-state 애니메이션**으로 축약 → 단계 SVG 시퀀스.

## L04 · 선택과 순서통계량
- `max` recurrence 의미 설명 + **randomized 가정 명시**(직관+수식 2단계).
- BFPRT: 각 항 label, **분수 합 0.9 < 1**, substitution, lower bound 추가해 `Θ(n)`으로 교정.
- 평균/기대/최악 시간 구분. 3-way partition(중복).

## L05 · 동적 계획법
- 원본의 **잘못된 base case, unreachable branch, min/max 혼동, 반환 인덱스, 비교연산자 오류** 교정.
- 공통 템플릿 강제: State → Transition → Base Case → Evaluation Order → Answer/Reconstruction.
- sentinel, rolling state, `dp[m][n]` 인덱싱, equality/type 교정.

## L06 · 검색 트리 (TikZ 55개 — 최다)
- "같은 node 재방문"→**unique simple path**로 교정. full/perfect 혼동 교정, perfect node 공식 convention 명시.
- BST 순회 root 중복 순서→표준 queue 알고리즘. duplicate 정책 `<=`/`>=` 모호성→**distinct-key invariant**.
- height convention, NIL sentinel, **AVL balance factor 부호**, B-Tree minimum degree·I/O 비용 명시.
- TikZ 55개 → 캐시·병렬 컴파일 필수(빌드 시간).

## L07 · 해시 테이블
- prime 규칙, 깨진 곱셈 식 교정. open addressing "추가 공간 없음" 표현 교정.
- hash pipeline, chaining vs open addressing, deletion marker, resizing amortized, **expected vs worst** 구분,
  hash flooding 보안 관점. mutable key 실패 사례.

## L08 · 그래프 알고리즘
- **BFS s/v 혼용** 교정, **representation 없는 복잡도** 교정(표현·자료구조 병기).
- Dijkstra/완화 조건 **`<`→`≤`**로 tie 포함 교정. tie order 재현성.
- MST vs shortest-path tree 구분. zero-weight vs no-edge 구분. Prim/Dijkstra의 PQ=Lecture3 heap 연결.

## L09 · 문자열 매칭
- **1-based→0-based** 교정. valid shift 범위. match/mismatch 뒤 공통 shift를 all-match trace로 명확화.
- Rabin–Karp hash collision **verification 필수**. **LPS convention 통일**(KMP). Horspool shift table.

## L10 · 상태공간 트리 탐색
- **backtracking ≠ DFS**로 명확 구분. **branch-and-bound ≠ backtracking** 구분.
- candidate/feasible/optimal, pruning soundness, incumbent·bound. permutation/combination generation.
- A* min-PQ = Lecture3 heap 연결. 정수 비용·consistent h 정책(overflow/부동소수 주의).

---

## 공통 규칙

- 충돌 시 **원천 우선순위**: (1) 검증된 코드·테스트 → (2) content map 교정 정책·convention →
  (3) 현재 LaTeX 소스 → (4) 원본 PPTX.
- 에이전트는 충돌을 임의 해결하지 않고 `docs/CONTENT_ISSUES.md`에 기록하고 사용자 판단을 구한다.
- content map의 교정을 **되돌리지 않는다**(웹에서 원본 오류를 재도입 금지).
