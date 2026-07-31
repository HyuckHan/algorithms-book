# FIGURE_SIZING — 그림이 내용보다 커 보이는 사례 기록

이 문서는 **수정하지 않고 기록만** 하기 위한 것이다. 개별 그림 크기를 지금 건드리지 않는다 —
M5(운영 하드닝)에서 전체 챕터를 놓고 일관된 크기 기준으로 일괄 조정하기 위한 자료 수집이다.
예외는 L08의 트레이스 상태 박스처럼 명백하고 verified 직전인 경우뿐이다(이미 처리됨, §L08 참고).

## 측정 방법

각 그림의 SVG 원본 크기(`dvisvgm`이 출력한 pt 단위 width, `1pt≈1.333px`로 환산)와, qmd의
`width="N%"` 지정이 실제 본문 컬럼(약 680px로 가정, 사이드바 있는 데스크톱 레이아웃 기준)에서
얼마로 늘어나는지 계산해 **배율(display px / natural px)**로 정렬했다. 배율이 클수록 원본보다
확대되어 보인다 — 특히 노드 수가 적은(1~3개) 작은 다이어그램이 고정 %width 때문에 크게
확대되는 경향이 있다(L08의 BFS/Kahn/DFS 상태 박스와 같은 근본 원인).

## Lecture 01 · Introduction to Algorithms

배율 ≥1.2x인 항목(본문 컬럼 680px 가정, 실제 뷰포트/테마에 따라 달라질 수 있음):

| 배율 | 파일 | 위치(Part) | 왜 커 보이는가 |
|---|---|---|---|
| 1.56x | `06-maximum-trace.svg` | C(Maximum 찾기) | 배열 하나짜리 짧은 트레이스, 55% width |
| 1.27x | `10-growth-curves.svg` | F(성장 차수(Orders of Growth)) | 곡선 비교 그래프, 60% width |
| 1.25x | `13-concept-map.svg` | H(세 알고리즘의 복잡도와 구현) | 개념 지도 전체, 80% width — 다른 챕터의 개념 지도와 일관성 확인 필요 |

**패턴 요약**: L01은 19개 그림 중 3개만 1.2x를 넘어, 지금까지 측정한 챕터 중 배율 문제가 가장
적다. 대부분의 그림(알고리즘 입출력 설명, Linear/Binary Search 트레이스 등)이 이미 자연폭
350~530px 안팎으로 넉넉해 45~70% width에서도 1.2x 미만으로 안정적이다. 유일한 특이 케이스는
개념 지도(`13-concept-map`, 1.25x)로, L03/L04/L05/L06 등 타 챕터의 개념 지도와 함께 일관된
기준으로 재조정할 필요가 있다.

## Lecture 02 · Recursion

배율 ≥1.2x인 항목(본문 컬럼 680px 가정, 실제 뷰포트/테마에 따라 달라질 수 있음):

| 배율 | 파일 | 위치(Part) | 왜 커 보이는가 |
|---|---|---|---|
| 2.30–2.31x | `01-call-stack-push.svg`, `02-call-stack-pop-step1~5.svg`(6개) | B(재귀의 실행: 호출 스택) | 호출 스택 push/pop 애니메이션 각 프레임 — 스택 프레임 1~2개짜리 아주 작은 다이어그램을 55–60% width로 표시 |
| 1.77x | `12-blob-floodfill-step1~3.svg`(3개) | J(Blob과 Flood Fill) | flood fill 진행 3단계, grid 일부만 강조하는 작은 다이어그램, 55% width |
| 1.52–1.53x | `10-maze-trace-step1~4.svg`(4개) | I(미로 탐색(Maze)과 Backtracking) | 미로 grid 트레이스 4단계, 55% width |
| 1.31x | `04-recursion-tree.svg` | E(점화식과 분석 방법) | 재귀 트리 다이어그램, 65% width |

**패턴 요약**: L02는 27개 그림 중 14개가 1.2x를 넘고, 최대 2.31x(호출 스택 push/pop 프레임)에
달한다. 두드러지는 고유 카테고리는 **호출 스택 프레임 애니메이션**(01/02, 스택 depth 1~2개짜리
초소형 다이어그램)으로, L06 B-Tree/RB-Tree의 "node 1~3개짜리 삽입 초반 단계"와 같은 근본
원인(원본이 작을수록 %width 배율이 커짐)을 공유하는 새로운 하위 사례다. Maze/Flood-fill
트레이스도 grid 일부만 그리는 작은 다이어그램이라 같은 원인을 보인다. 반면 Fibonacci/Hanoi/
Power-set 재귀 트리류(03,09,13)는 원본이 이미 크게 그려져 있어 1.2x를 넘지 않는다 — "재귀
트리"라는 카테고리 자체가 문제가 아니라 개별 다이어그램의 절대 크기가 관건임을 보여준다.

## Lecture 03 · Sorting

배율 ≥1.2x인 항목(본문 컬럼 680px 가정, 실제 뷰포트/테마에 따라 달라질 수 있음):

| 배율 | 파일 | 위치(Part) | 왜 커 보이는가 |
|---|---|---|---|
| 1.67x | `03-selection-trace-step1/5.svg`, `04-bubble-trace.svg`, `05-insertion-trace.svg`(4개) | B(기본 Comparison Sort) | Selection/Bubble/Insertion 각 정렬의 배열 트레이스, 자연폭 224px 안팎의 작은 다이어그램을 55% width로 표시 — 세 정렬이 같은 스타일이라 배율까지 거의 동일 |
| 1.89x | `07-merge-recursion-tree.svg` | C(Divide-and-Conquer와 비교 하한) | merge sort 재귀 트리, 자연폭이 작아(198px) 55%에도 확대 |
| 1.46x | `05-insertion-cards.svg` | B(기본 Comparison Sort) | 카드 정렬 비유 정적 다이어그램, 45% width |
| 1.44x | `02-stability-demo.svg` | A(정렬 문제와 평가 기준) | stability 설명용 작은 다이어그램, 60% width |
| 1.46x | `15-radix-trace.svg` | E(Key 구조를 이용한 정렬과 실무 API) | radix sort 자리수별 트레이스, 70% width |
| 1.31x | `08-quick-partition-trace.svg` | C(Divide-and-Conquer와 비교 하한) | quick sort partition 트레이스, 70% width |
| 1.22–1.24x | `10-heap-array-tree.svg`, `12-build-heap-trace.svg`, `13-heapsort-trace.svg` | D(Heap과 Heapsort) | heap의 array/tree 이중 표현 및 build-heap/heapsort 트레이스, 55–60% width |

**패턴 요약**: L03은 20개 중 12개가 1.2x를 넘는다. 특유의 카테고리는 **Comparison Sort 배열
트레이스**(Selection/Bubble/Insertion, 자연폭 ~224px, 55% width에서 공통적으로 1.67x)로,
L09의 "문자열 트레이스"와 유사하게 짧은 배열 하나만 그리는 작은 원본이 근본 원인이다.
Merge/Quick/Heap/Radix 트레이스도 정도는 덜하지만 같은 패턴을 반복한다.

## Lecture 04 · Selection and Order Statistics

배율 ≥1.2x인 항목(본문 컬럼 680px 가정, 실제 뷰포트/테마에 따라 달라질 수 있음):

| 배율 | 파일 | 위치(Part) | 왜 커 보이는가 |
|---|---|---|---|
| 1.93x | `10-groups-of-five.svg` | D(Deterministic Linear Selection (Median of Medians)) | 5-원소 group 5개를 묶는 작은 다이어그램, 55% width |
| 1.90x | `13-group-three-guarantee.svg` | D | median 이상 3개 원소 설명용 작은 다이어그램, 55% width |
| 1.70x | `12-median-half-guarantee.svg` | D | median 절반 분할 설명, 55% width |
| 1.41x | `11-median-of-medians-trace-step1.svg` | D | median-of-medians 트레이스 1단계, 60% width |
| 1.34x | `06-common-first-partition.svg` | B(Quickselect) | 공통 첫 partition 다이어그램, 70% width |
| 1.30x | `11-median-of-medians-trace-step5.svg` | D | 같은 트레이스 5단계, 60% width |
| 1.25x | `08-randomized-trace-step7.svg` | B(Quickselect) | randomized quickselect 트레이스 마지막 단계, 65% width |
| 1.24x | `14-concept-map.svg` | E(전략 비교와 요약) | 개념 지도, 80% width |
| 1.23x | `03-quicksort-vs-quickselect.svg` | A(Selection 문제와 Order Statistics) | quicksort vs quickselect 비교 다이어그램, 60% width |
| 1.23x | `05-right-rank-reason.svg` | B(Quickselect) | rank 재계산 설명 다이어그램, 60% width |

**패턴 요약**: L04는 17개 중 10개가 1.2x를 넘고, 최대 1.93x(`10-groups-of-five`)다. 두드러지는
카테고리는 **Median-of-Medians 설명용 소형 다이어그램**(10,12,13 — group 분할, 절반 보장,
3개 보장을 보여주는 원본이 작은 그림들)으로 Part D에 집중되어 있다. 다른 챕터의 "1~3개짜리
작은 다이어그램" 패턴과 같은 원인이며, 최댓값도 2x 미만에 그쳐 L02/L05/L08만큼 극단적이지는
않다.

## Lecture 05 · Dynamic Programming

배율 ≥1.2x인 항목(본문 컬럼 680px 가정, 실제 뷰포트/테마에 따라 달라질 수 있음):

| 배율 | 파일 | 위치(Part) | 왜 커 보이는가 |
|---|---|---|---|
| 3.09x | `11-matrix-representative-cell.svg` | C(Optimal Substructure와 대표 DP 문제) | matrix path-sum table에서 대표 cell 하나만 확대한 아주 작은 다이어그램(자연폭 121px), 55% width |
| 2.51x | `06-greedy-counterexample-local.svg`, `07-greedy-counterexample-optimal.svg`(2개) | C | greedy가 실패하는 반례를 보여주는 작은 다이어그램 2개(자연폭 122px), 45% width |
| 2.50x | `13-lcs-case1.svg` | C | LCS recurrence case 1만 보여주는 아주 작은 다이어그램(자연폭 95px), 35% width에도 확대 |
| 1.71x | `04-memo-trace-step1~4.svg`, `05-bottomup-trace-step1~3.svg`(7개) | B(Memoization, Tabulation, DP 설계 절차) | Fibonacci memo/bottom-up 계산 과정 트레이스 7단계, 자연폭 ~318px에 80% width로 확대 |
| 1.59–1.60x | `01-roadmap.svg`, `02-recurrence-memo-tab.svg` | A(왜 동적 계획법인가?) | 학습 로드맵과 memo/tabulation 대조 다이어그램, 80–90% width |
| 1.41x | `15-lcs-backtrack-trace.svg` | D(LCS 복원과 Maximum Subarray) | LCS 역추적 트레이스, 90% width |
| 1.29x | `16-concept-map.svg` | E(비교, 요약, Quiz) | 개념 지도, 80% width |
| 1.22–1.24x | `08-matrix-dependency.svg`, `09-matrix-call-tree.svg`, `14-lcs-call-tree.svg` | C | matrix 의존관계 다이어그램, matrix/LCS call tree, 60–65% width |

**패턴 요약**: L05는 24개 중 18개(75%)가 1.2x를 넘어 지금까지 측정한 챕터 중 가장 심각하다 —
최대 3.09x(`11-matrix-representative-cell`). 두드러지는 카테고리는 **DP 테이블에서 대표
cell/case 하나만 떼어 보여주는 초소형 설명 다이어그램**(06/07/11/13, 자연폭 95~122px)으로,
"한 줄 표"·"문자열 트레이스"에 이어 확인되는 "원본이 극도로 작은" 카테고리의 또 다른 사례다.
여기에 더해 memo/bottom-up 트레이스 7단계(04/05)가 80% width 고정으로 일괄 1.71x를 보여,
Part B 전체가 과대 확대 상태다.

## Lecture 06 · Search Trees

배율 ≥1.2x인 항목(본문 컬럼 680px 가정, 실제 뷰포트/테마에 따라 달라질 수 있음):

| 배율 | 파일 | 위치(Part) | 왜 커 보이는가 |
|---|---|---|---|
| 2.62x | `03-left-child-example.svg`, `04-right-child-example.svg` | B(Binary Tree 형태) | node 2개짜리 아주 작은 다이어그램을 30% width로 표시 — 원본이 워낙 작아 배율이 크다 |
| 2.44x | `15-successor-cases.svg` | F(BST 기본 연산) | case1+case2 설명이 나란히 있어 원본은 작지 않지만 55% width가 과함 |
| 2.32x | `49-btree-insert-step1.svg` | K(B-Tree) | node 1개("10")뿐인 삽입 첫 단계, 20% width에도 크게 확대 |
| 2.27x | `16-successor-case2-ancestor-chain.svg` | F(BST 기본 연산) | 3-node 보조 다이어그램, 30% width |
| 2.10x | `39-rb-insert-41-38-31-step1.svg` | J(Red-Black Tree) | node 2개짜리 삽입 첫 단계, 25% width |
| 2.06x | `32-rl-case-step1.svg` | I(AVL Tree) | RL case 1단계(node 3개), 30% width |
| 2.02x | `29-lr-case-step1.svg` | I(AVL Tree) | LR case 1단계(node 3개), 30% width |
| 2.00x | `01-rooted-tree-definition.svg` | A(Tree와 용어) | 7-node 트리지만 컴팩트하게 그려져 45% width에서 확대됨 |
| 1.58x | `60-concept-map.svg` | 개념 지도 | 개념 지도 전체가 70% width — 다른 챕터의 개념 지도와 일관성 확인 필요 |
| 1.53x | `50-btree-insert-step2.svg` | K(B-Tree) | node 1개("10\|20")뿐인 삽입 2단계, 20% width |
| 1.42–1.46x | `34-rl-case-step3.svg`, `31-lr-case-step3.svg`, `33-rl-case-step2.svg`, `30-lr-case-step2.svg` | I(AVL Tree) | LR/RL case 중간·완료 단계(node 3개), 30% width |
| 1.42x | `06-linked-representation.svg` | B(Binary Tree 형태) | 4-필드 레코드 하나뿐인 다이어그램, 30% width |
| 1.37x | `35-nil-sentinel.svg` | J(Red-Black Tree) | 5-node 다이어그램, 45% width |
| 1.34x | `46-rb-insert-8-final.svg` | J(Red-Black Tree) | 최종 확인 트리(6-node), 55% width |
| 1.23–1.30x | `28-rr-case-after.svg`, `26-ll-case-after.svg`, `27-rr-case-before.svg`, `25-ll-case-before.svg` | I(AVL Tree) | LL/RR case 전/후(node 3개), 30% width |
| 1.26x | `22-degenerate-bst-trace-step1.svg` | H(왜 Balanced Tree인가) | 삽입 1단계(node 1개), 50% width |
| 1.23x | `13-fixed-bst-example.svg` | F(BST 기본 연산) | 12-node 예제지만 55% width에서도 확대됨 |
| 1.23x | `36-invariant-violation-example.svg` | J(Red-Black Tree) | 3-node 위반 예시, 35% width |
| 1.22x | `02-tree-terminology-trace-step1.svg` | A(Tree와 용어) | 트레이스 1단계, 45% width |

**패턴 요약**: (1) node 1~3개짜리 아주 작은 다이어그램(특히 AVL LL/RR/LR/RL 각 단계, RB insert
초반 단계, B-Tree 삽입 초반 단계)이 상대적으로 큰 배율을 보인다 — 원본이 작을수록 같은 %width도
더 크게 확대되기 때문이다(L08에서 이미 확인된 것과 같은 원인). (2) 이 목록의 %width 값들은
"AVL/RB/B-Tree before/after 쌍"처럼 서로 다른 크기의 그림을 나란히 보여줄 때 시각적 균형을
맞추려고 초안 단계에서 대략적으로 정한 값이라, 그림마다 원본 크기 대비 일관된 배율 기준이
적용되지 않았다.

## Lecture 07 · Hash Tables

배율 ≥1.2x인 항목(본문 컬럼 680px 가정, 실제 뷰포트/테마에 따라 달라질 수 있음):

| 배율 | 파일 | 위치(Part) | 왜 커 보이는가 |
|---|---|---|---|
| 1.98x | `08-pigeonhole-principle.svg` | E(Collision) | key 4개·bucket 3개짜리 작은 다이어그램, 60% width |
| 1.79x | `22-double-hash-gcd-failure.svg` | J(Double Hashing) | 12-slot 중 3칸만 강조하는 가는 한 줄 다이어그램, 90% width |
| 1.70x | `27-rehash-animation-step4.svg` | M(Resize/Rehashing) | rehash 최종 상태(작은 텍스트 위주), 90% width |
| 1.60x | `23-probe-cluster-before-delete.svg`, `16-linear-final-table.svg`, `13-tombstone-reuse-example.svg`, `06-original-integer-table.svg` | K/H/G/E | `\htrowthirteen` 매크로로 그린 13-slot 한 줄짜리 표 — 가로로 얇고 세로로 짧은 원본이 90% width에서 크게 확대됨(공통 원인) |
| 1.51–1.55x | `15-linear-trace2-wraparound-step3.svg`, `14-linear-trace1-collision-step3.svg`, `07-insert-29-collision-trace-step3.svg`, `25-correct-deletion-tombstone-trace-step4.svg`, `24-wrong-deletion-trace-step5.svg`, `21-double-hash-probe-trace-step4.svg`, `19-quadratic-trace-30-step3.svg` | E/H/I/J/K | 13-slot 한 줄 트레이스의 각 스텝, 90% width — 위와 같은 원인 |
| 1.50x | `26-logical-vs-probing-load-step2.svg` | K(삭제) | `\loadgauge` 매크로로 그린 가는 막대 게이지, 70% width |
| 1.33x | `03-distribution-comparison.svg` | C(Hash Function 설계) | 막대그래프 두 개가 세로로 나열된 다이어그램, 70% width |
| 1.32x | `20-secondary-clustering.svg` | I(Quadratic Probing) | key 3개짜리 작은 다이어그램, 60% width |
| 1.22x | `17-primary-clustering-step3.svg`, `28-resize-cost-sequence.svg`, `18-linear-probe-cost-curve.svg` | H/M/H | primary clustering 트레이스, resize cost 막대그래프, PGFPlots 곡선 — 각각 70%/60%/70% width |

**패턴 요약**: L06/L08에서 이미 확인된 "원본이 작을수록 같은 %width도 더 크게 확대된다"는 원인이 여기서도 반복되지만, L07 특유의 원인이 하나 추가된다 — `\htrowthirteen`/`\loadgauge` 매크로(`lecture-notes/common/hash_tables.tex`)로 그리는 **가로로 얇고 세로로 짧은 "한 줄" 다이어그램**(13-slot 표, load gauge)이 이 목록의 절반 가까이를 차지한다. 이런 다이어그램은 폭은 있지만 높이가 아주 작아 %width 기준 배율 계산 자체가 다른 종류(정사각형에 가까운 tree/graph 다이어그램)와 시각적으로 다르게 느껴질 수 있다 — M5 일괄 조정 시 "한 줄 표" 종류를 별도 카테고리로 다룰지 검토할 가치가 있다.

## Lecture 08 · Graph Algorithms

**L08 재검증**: 상단 "측정 방법" 절 위에 "L08의 트레이스 상태 박스처럼 명백하고 verified
직전인 경우뿐이다(이미 처리됨)"이라고 기록되어 있었으나, 이번에 68개 전체를 재측정한 결과
**여전히 56개(82%)가 1.2x 이상이고 최대 3.66x**로, 추가 조정이 필요하다. 과거에 처리된 것은
BFS 큐 트레이스(`05-bfs-queue-trace-step2/6/7`)와 DFS 재귀 트레이스(`07-dfs-recursion-
trace-step2~6`)의 **일부 중간 단계**뿐이었던 것으로 보이며, 같은 트레이스의 최소 자연폭
단계(`step1`)와 Prim/Kruskal/Dijkstra/Bellman-Ford/DSU/relaxation 등 Part I~O의 알고리즘
트레이스 전체는 손대지 않은 채 남아 있다. 즉 "L08은 기처리로 1.3x 이하 확인"이라고 볼 수
**없으며**, 다음 표의 항목들은 이번 M5 일괄 조정에 포함해야 한다.

배율 ≥1.2x인 항목(본문 컬럼 680px 가정, 실제 뷰포트/테마에 따라 달라질 수 있음):

| 배율 | 파일 | 위치(Part) | 왜 커 보이는가 |
|---|---|---|---|
| 3.66x | `03-matrix-to-list-step2.svg` | B(Graph Representation) | adjacency matrix→list 변환 2단계, 자연폭 130px의 아주 작은 다이어그램을 70% width로 표시 |
| 2.87x | `03-matrix-to-list-step3.svg` | B(Graph Representation) | 같은 변환 3단계, 자연폭 166px |
| 2.95x | `11-dfs-topo-finish-reverse-step1~3.svg`(3개) | F(Topological Sort) | DFS 종료순서 역순 트레이스, 자연폭 161px의 작은 다이어그램을 70% width로 표시 |
| 2.90x | `11-dfs-topo-finish-reverse-step4.svg` | F(Topological Sort) | 같은 트레이스 4단계 |
| 2.61x | `03-matrix-to-list-step1.svg` | B(Graph Representation) | 같은 변환 1단계, 자연폭 183px |
| 2.26x | `05-bfs-queue-trace-step1.svg` | C(BFS) | BFS 큐 트레이스 첫 단계 — 큐에 원소가 1개뿐인 가장 작은 프레임(자연폭 66px), 22% width에도 크게 확대 |
| 1.98x | `17-relaxation-animation-step1.svg` | L(Shortest Paths와 Relaxation) | relaxation 애니메이션 1단계, 자연폭 206px |
| 1.81x | `21-dijkstra-negative-counterexample.svg` | N(Dijkstra Algorithm) | negative edge 반례 다이어그램, 55% width |
| 1.78x | `09-kahn-trace-step1.svg` | F(Topological Sort) | Kahn's algorithm 트레이스 1단계 — in-degree 0 노드가 하나뿐인 초소형 프레임(자연폭 84px) |
| 1.78x | `17-relaxation-animation-step2.svg` | L(Shortest Paths와 Relaxation) | 같은 애니메이션 2단계 |
| 1.76x | `19-dag-relaxation-trace-step1~3.svg`(3개) | M(Unweighted·DAG Shortest Paths) | DAG relaxation 트레이스 3단계, 자연폭 231px |
| 1.71x | `02-matrix-direction.svg` | B(Graph Representation) | 방향 그래프 matrix 표현, 자연폭 159px의 작은 다이어그램을 40% width로 표시 |
| 1.62x | `09-kahn-trace-step2.svg`, `09-kahn-trace-step4.svg` | F(Topological Sort) | Kahn's algorithm 트레이스 2·4단계 |
| 1.53x | `09-kahn-trace-step5.svg` | F(Topological Sort) | 같은 트레이스 5단계 |
| 1.52x | `20-dijkstra-trace-step6.svg` | N(Dijkstra Algorithm) | Dijkstra 트레이스 마지막 단계, 80% width |
| 1.51x | `13-prim-trace-step3.svg`, `13-prim-trace-step6.svg` | I(Prim Algorithm) | Prim MST 트레이스 3·6단계, 80% width |
| 1.48x | `09-kahn-trace-step3.svg` | F(Topological Sort) | Kahn's algorithm 트레이스 3단계 |
| 1.47–1.48x | `13-prim-trace-step1.svg`, `13-prim-trace-step5.svg` | I(Prim Algorithm) | Prim MST 트레이스 1·5단계 |
| 1.46–1.48x | `15-kruskal-trace-step1~6.svg`(6개) | J(Kruskal과 Disjoint Set) | Kruskal MST 트레이스 1~6단계, 자연폭 368~370px에 80% width |
| 1.46x | `04-bfs-graph.svg` | C(BFS) | BFS 대상 그래프 원본, 자연폭 329px에 70% width |
| 1.46x | `17-relaxation-animation-step3.svg` | L(Shortest Paths와 Relaxation) | 같은 애니메이션 3단계 |
| 1.50x | `16-mst-tie-square.svg` | K(MST Correctness와 비교) | MST tie-breaking 설명용 정사각형 다이어그램, 자연폭 182px에 40% width |
| 1.43–1.52x | `20-dijkstra-trace-step1~5.svg`(5개) | N(Dijkstra Algorithm) | Dijkstra 트레이스 1~5단계, 자연폭 358~395px에 80% width |
| 1.42x | `07-dfs-recursion-trace-step1.svg` | D(DFS) | DFS 재귀 트레이스 첫 단계 — 방문 노드 1개뿐인 초소형 프레임(자연폭 106px) |
| 1.37x | `15-kruskal-trace-step7.svg` | J(Kruskal과 Disjoint Set) | Kruskal MST 트레이스 마지막 단계 |
| 1.36x | `22-bellman-ford-negative-cycle-step1/2.svg`(2개) | O(Bellman–Ford Algorithm) | negative cycle 검출 트레이스 2단계, 자연폭 301px에 60% width |
| 1.32x | `12-cut-crossing-edge.svg` | H(Greedy와 Cut Property) | cut property 설명 다이어그램, 55% width |
| 1.30x | `09-kahn-trace-step6.svg` | F(Topological Sort) | Kahn's algorithm 트레이스 마지막 단계 |
| 1.23x | `08-back-edge-animation-step1/2.svg`(2개) | E(DFS 활용과 Cycle Detection) | back edge 발견 애니메이션 2단계, 55% width |
| 1.21x | `14-dsu-animation-step1~4.svg`(4개) | J(Kruskal과 Disjoint Set) | Disjoint Set union 애니메이션 4단계, 자연폭 451px에 80% width — 이 목록에서 배율은 가장 낮지만 여전히 1.2x 초과 |

**패턴 요약**: L08은 68개 중 56개(82%)가 1.2x를 넘어 L05(75%)보다도 비율이 높고, 절대 배율
최댓값(3.66x)도 이번에 측정한 챕터 중 가장 크다. 세 가지 원인이 겹친다 — (1) L06/L07/L09에서
이미 확인된 "원본이 작을수록 배율이 커진다"는 근본 원인이 `matrix-to-list`, `bfs-queue-
trace-step1`, `kahn-trace`, `dfs-recursion-trace-step1` 같은 **노드/원소 1~2개짜리 트레이스
첫 단계**에서 가장 극단적으로 나타난다(2~3.7x). (2) Prim/Kruskal/Dijkstra/Bellman-Ford/DSU
등 **weighted-graph 알고리즘 트레이스 전 단계가 거의 예외 없이 80% width로 고정**되어 있어,
자연폭이 350~450px로 작지 않은데도 일괄 1.2~1.5x를 보인다 — 이는 "원본이 작아서"가 아니라
"모든 트레이스 시리즈에 같은 큰 %width를 습관적으로 지정한" 별개의 원인이다. (3) 과거
"L08은 기처리"라는 기록과 달리 이번 재측정에서 대다수가 여전히 초과 상태임이 드러나, 해당
기록은 BFS/DFS 트레이스의 **일부 중간 단계**에만 해당하는 좁은 수정이었던 것으로 보인다 —
M5 일괄 조정 시 L08을 다른 미처리 챕터와 동일하게 전체 재조정 대상으로 다뤄야 한다.

## Lecture 09 · String Matching

배율 ≥1.2x인 항목(본문 컬럼 680px 가정, 실제 뷰포트/테마에 따라 달라질 수 있음) — 이 강의는
거의 모든 그림이 이 기준을 넘는다:

| 배율 | 파일 | 위치(Part) | 왜 커 보이는가 |
|---|---|---|---|
| 2.32x | `02-naive-worst-case-repeated-prefix-step3.svg` | B(Naive Matching) | 텍스트 두 줄뿐인 아주 작은 다이어그램, 55% width |
| 1.95x | `01-naive-alignment-trace-step4.svg` | B(Naive Matching) | 7글자 텍스트 행 트레이스, 70% width |
| 1.87x | `05-rolling-update-derivation-step3.svg` | E(Rolling Hash) | 수식 두 줄짜리 작은 다이어그램, 70% width |
| 1.80x | `07-collision-is-candidate-step2.svg` | F(Modular Hash와 Collision) | 텍스트 두 줄짜리 작은 다이어그램, 55% width |
| 1.70x | `08-candidate-to-valid-hit-step2.svg` | G(Rabin-Karp 분석과 활용) | 텍스트 두 줄짜리 작은 다이어그램, 60% width |
| 1.53–1.57x | `15-tiger-shift-table-step2.svg`, `10-mismatch-fallback-trace-step4.svg` | O/I | 작은 텍스트/트레이스 다이어그램, 55–80% width |
| 1.42–1.52x | `03-numeric-encoding-cad-step2.svg`, `06-rolling-update-flow.svg`, `04-hash-equality-insufficient.svg`, `18-horspool-trace-tiger-step4.svg`, `12-kmp-mismatch-recovery-trace-step5.svg` | D/E/D/P/L | 텍스트 위주 또는 7-글자 트레이스, 55–80% width |
| 1.24–1.37x | `09-prefix-lps-discovery-step3.svg`, `16-absent-character-shift-step2.svg`, `17-rational-repeated-character-step3.svg`, `14-right-to-left-comparison-step2.svg`, `11-lps-construction-trace-step6.svg` | H/O/P/N/K | 8글자 이내 텍스트 행 트레이스, 55–70% width |
| 1.20x | `13-kmp-overlapping-match-step2.svg` | L(KMP Search) | 텍스트 두 줄짜리 작은 다이어그램, 55% width |

**패턴 요약**: L06/L07에서 확인된 "원본이 작을수록 같은 %width도 더 크게 확대된다"는 원인이
이 강의에서 가장 두드러진다 — `\smrow`/`\smindices`/`\smshiftrow`로 그리는 text-character-row
트레이스(예: `C,A,B,A,B,A,C` 7글자)와 `\smhash`/`\smnote` 상자 하나짜리 개념 다이어그램은
원본 크기가 워낙 작아(자연 폭 150~400px) 55~80% width에서 거의 전부 1.2배를 넘는다. 18개
그림 중 17개가 이 기준을 넘는 것은 이 강의 특유의 그림 스타일(짧은 문자열 트레이스가 대부분)
때문으로 보이며, M5 일괄 조정 시 "문자열 트레이스" 종류를 L07의 "한 줄 표"처럼 별도
카테고리로 다룰 필요가 있다.

## Lecture 10 · State-Space Tree Search

배율 ≥1.2x인 항목(본문 컬럼 680px 가정) — 18개 중 17개가 이 기준을 넘는다(L09와 같은 패턴):

| 배율 | 파일 | 위치(Part) | 왜 커 보이는가 |
|---|---|---|---|
| 3.10x | `13-knapsack-best-first-trace-step7.svg` | D(Knapsack B&B) | `\pqview`/`\incbadge` 텍스트 상자 위주 트레이스, 80% width |
| 3.04x | `09-subset-sum-trace-step5.svg` | B(Subset Sum) | 텍스트 두 줄짜리 작은 다이어그램, 70% width |
| 2.86x | `11-arithmetic-progression-trace-step5.svg` | B(AP 선택 심화) | 텍스트 두 줄짜리 작은 다이어그램, 75% width |
| 2.12x | `06-four-queens-board-trace-step6.svg` | B(N-Queens) | 4x4 보드 하나뿐인 작은 다이어그램, 75% width |
| 1.80–1.93x | `14-knapsack-state-tree.svg`, `07-four-queens-partial-tree.svg` | D/B | node 4~5개짜리 작은 트리, 60~70% width |
| 1.85x | `18-astar-path-reconstruction-step3.svg`, `16-astar-grid-heuristic.svg` | E(A*) | 5×7 격자 하나뿐인 다이어그램, 55% width |
| 1.54–1.77x | `02-state-space-expansion-step4.svg`, `12-bound-based-pruning-step4.svg`, `10-graph-coloring-trace-step4.svg`, `04-permutation-state-tree-step4.svg` | A/C/B/A | node 4~7개짜리 작은 트리, 70% width |
| 1.21–1.35x | `05-apply-undo-symmetry-step3.svg`, `01-state-space-tree-structure.svg`, `03-dfs-bfs-visit-order-step3.svg`, `08-subset-sum-include-exclude-tree.svg`, `17-astar-open-closed-trace-step6.svg` | B/A/A/B/E | node 6~7개짜리 다이어그램, 60~70% width |

**패턴 요약**: L09에서 확인된 "원본이 작을수록 같은 %width도 더 크게 확대된다" 패턴이 그대로
반복된다. 이 강의 특유의 원인은 `\ssbox`/`\ssnote`/`\pqview`/`\incbadge`(공유 스타일
`common/state_space.tex`)로 그리는 **텍스트 상자 하나 또는 둘짜리 트레이스**(예: Knapsack PQ
상태, Subset Sum trace, AP trace)가 목록 상위를 차지한다는 점이다 — 이는 L07의 "한 줄 표",
L09의 "문자열 트레이스"에 이어 세 번째로 확인된 "원본 그림 자체가 텍스트 위주라 자연 폭이
아주 작은" 카테고리다. M5 일괄 조정 시 이 세 카테고리(한 줄 표/문자열 트레이스/텍스트 상자
트레이스)를 통합해 다루는 것을 검토한다.

## 다음 강의 추가 시

새 강의를 변환할 때도 이 표 형식으로 이어서 기록한다(`## Lecture NN · 제목` 절 추가). M5에서
한 번에 처리할 때는 이 문서를 입력으로 삼아 "원본 대비 배율" 같은 일관된 규칙(예: 배율 상한
1.3x, 또는 그림 종류별 고정 %width 표)을 정하고 전체 챕터에 적용한다.
