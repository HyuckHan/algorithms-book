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

## 다음 강의 추가 시

새 강의를 변환할 때도 이 표 형식으로 이어서 기록한다(`## Lecture NN · 제목` 절 추가). M5에서
한 번에 처리할 때는 이 문서를 입력으로 삼아 "원본 대비 배율" 같은 일관된 규칙(예: 배율 상한
1.3x, 또는 그림 종류별 고정 %width 표)을 정하고 전체 챕터에 적용한다.
