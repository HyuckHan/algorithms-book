# ANIMATION_AUDIT — Beamer 오버레이 → 웹북 tabset 변환 전수 감사

이 문서는 `lecture-notes/`(읽기 전용 원본)의 Beamer 오버레이 애니메이션이 웹북 변환에서
그대로 살아남았는지 **발견·기록만** 하기 위한 것이다. 여기서는 아무것도 고치지 않는다 —
실제 tabset 복원은 별도 작업으로 남긴다.

## 요약

- **전체 애니메이션 그림(원본에서 서로 다른 상태가 2개 이상인 TikZ/축/매크로 그림) 수: 89개**
  (10개 강의 전체의 tikzpicture/axis/매크로 그림 221개 중 다중 프레임인 것만).
- 분류: **(A) 완전 붕괴 51건**, **(B) 프레임 누락 1건**, **(C) 프레임 뭉침 11건**,
  **정상 26건**(tabset 23건 + "2단계 전부 표시" 3건).
- **가장 심각한 것**: L07(해시테이블)·L09(문자열 매칭)·L10(상태공간 탐색) **세 강의의 시퀀스
  그림 42개 전부**가 같은 패턴으로 붕괴돼 있다 — `mode: sequence`로 스텝 SVG는 전부
  생성됐지만 qmd에는 **마지막 스텝 1장만** 삽입되고 나머지는 캡션 텍스트로만 서술된다.
  이미 알려진 3건(L02 push, L06 순회, L06 검색 트레이스)보다 규모가 훨씬 크다.
- 두 번째로 심각한 것: L03(정렬)의 트레이스 그림 8개(bubble/insertion/quick-partition/
  heapify/build-heap/heapsort/counting-sort/radix) 전부가 `FIGURE_CONFIG`에
  `mode: sequence`가 없어 **원본 여러 프레임이 SVG 자체가 1장만 생성되는 단계에서 붕괴**됐다
  (L02 push와 동일 원인).
- `\pause`, `\uncover<>`, `\onslide<>`, `\temporal<>`는 `lecture-notes/` 전체에서 **한 건도
  검색되지 않았다** — 이 강의노트는 오버레이를 전부 `\only`/`\alt`/`\visible`/매크로 반복
  호출로만 표현하므로, `extract_tikz.py`가 다루지 않는 오버레이 명령으로 인한 사각지대는 없다.

## 측정 방법

1. `scripts/extract_tikz.py`를 모듈로 임포트해 그 자신의 `find_figures()`/`overlay_steps()`를
   그대로 재사용했다 — 이 파이프라인이 실제로 SVG를 몇 장 만드는지와 정확히 같은 로직으로
   "원본 프레임 수"를 셌다(같은 코드로 세므로 방법론 불일치가 없다).
   - **원본 프레임 수**(`n_src`): 그림(TikZ/axis)이면 `\only<N>`/`\alt<N>` 스펙에 등장하는
     서로 다른 경계값 개수, 매크로 그림(L06 `\travtree`, L07 `\htrowthirteen`/`\loadgauge`)
     이면 같은 프레임 안에서 호출된 횟수.
   - `FIGURE_CONFIG`에 `"mode": "sequence"`가 없는(=flatten) 그림은 원본에 여러 프레임이
     있어도 파이프라인이 **마지막 상태 하나만** 컴파일한다 — 이 단계에서 이미 붕괴되면 (A).
2. **웹북 step SVG 수**: `figures/NN-*/{slug}-step*.svg`를 실제로 세어 파이프라인 설정과
   디스크 상태가 일치하는지 확인했다(전부 일치 — 디스크에 덜 생성된 경우는 없었다, 즉
   이번 감사에서 (B) 유형은 파이프라인 생성 단계가 아니라 다른 원인 하나뿐이었다).
3. **qmd 삽입 수**: 해당 `chapters/NN-*.qmd`에서 `{slug}-stepN.svg` 참조를 정규식으로 세고,
   그 참조들이 `::: {.panel-tabset}` ~ `:::` 안에 있는지 확인했다.
4. 판정 규칙:
   - 삽입 수 = 원본 프레임 수, tabset 안 → **정상**.
   - 삽입 수 = 2, 원본 프레임 수 = 2(즉 2장 다 보임, 정보 손실 없음) → **정상**(tabset 대신
     나란히 배치된 것일 뿐, before/after 쌍으로는 유효한 스타일).
   - 웹북 step SVG 수 < 원본 프레임 수 → **(B) 프레임 누락**.
   - 삽입 수 = 1(원본 프레임 수 ≥ 2) → **(A) 완전 붕괴**.
   - 1 < 삽입 수 < 원본 프레임 수 → **(B) 또는 (C)**: 실제로는 전부 "처음+마지막 2장만
     나란히 삽입, tabset 없음"이라는 동일 구조였다. 이미 알려진 두 예시(L06 검색 트레이스=B,
     L06 순회=C)가 구조적으로 동일한데도 사용자가 다르게 분류해 알려주었으므로, **그 두 건은
     알려준 분류를 그대로 유지**하고, 새로 발견한 나머지는 "여러 프레임이 나란히 붙는다"는
     관찰과 일치하는 **(C)**로 분류했다.

## Lecture 01 · Introduction to Algorithms

| 원본 그림 | 원본 프레임 수 | 웹북 step SVG 수 | qmd 삽입 수 | 유형 | 비고 |
|---|---|---|---|---|---|
| `07-linear-search-trace` | 4 | 4 | 4 | 정상 | tabset 확인 |
| `09-binary-search-trace` | 4 | 4 | 4 | 정상 | tabset 확인 |

L01은 애니메이션 그림 2개 모두 정상 변환.

## Lecture 02 · Recursion

| 원본 그림 | 원본 프레임 수 | 웹북 step SVG 수 | qmd 삽입 수 | 유형 | 비고 |
|---|---|---|---|---|---|
| `01-call-stack-push` | 2(추정 3, 아래 참고) | 1 | 1 | **(A) 완전 붕괴** | **기존 REVIEW_NOTES #4**. `FIGURE_CONFIG["02"]`에 `mode: sequence` 없음(바로 아래 pop은 있음). 원본은 `\visible<2->`/`\visible<3->`로 frame이 누적되는 애니메이션인데 최종 상태(모든 frame 쌓인 상태)만 컴파일됨. 주의: `overlay_steps()`는 스펙에 명시된 경계값만 세므로 "아무것도 안 쌓인 최초 상태"(암묵적 1단계)는 소스에 `<1>`이 없어 이 값(2)에 안 잡힌다 — 실제 복원 시 3단계(1: sum(4)만, 2: +2 frame, 3: +2 frame 더)가 되어야 함 |
| `02-call-stack-pop` | 5 | 5 | 5 | 정상 | tabset 확인 |
| `06-binary-search-reduction` | 3 | 3 | 3 | 정상 | tabset 확인 |
| `08-hanoi-n3-states` | 3 | 3 | 3 | 정상 | tabset 확인 |
| `10-maze-trace` | 4 | 4 | 4 | 정상 | tabset 확인 |
| `12-blob-floodfill` | 3 | 3 | 3 | 정상 | tabset 확인 |

## Lecture 03 · Sorting

| 원본 그림 | 원본 프레임 수 | 웹북 step SVG 수 | qmd 삽입 수 | 유형 | 비고 |
|---|---|---|---|---|---|
| `03-selection-trace` | 5 | 5 | 2 | **(C) 프레임 뭉침** | step1+step5만 나란히 삽입, step2~4 누락. tabset 없음 |
| `04-bubble-trace` | 4 | 1 | 1 | **(A) 완전 붕괴** | *신규*. `FIGURE_CONFIG`에 `mode: sequence` 없음. 소스는 `\only<1..4>`로 매 pass마다 배열·swap 인덱스가 바뀌는 실제 4단계 트레이스(01_bubble.tex 11-14행) — 최종 pass 결과만 남음 |
| `05-insertion-trace` | 5 | 1 | 1 | **(A) 완전 붕괴** | *신규*. 위와 동일 원인 |
| `07-merge-pointers` | 4 | 4 | 2 | **(C) 프레임 뭉침** | *신규*. step1+step4만 삽입, step2~3 누락 |
| `08-quick-partition-trace` | 4 | 1 | 1 | **(A) 완전 붕괴** | *신규* |
| `11-heapify-trace` | 4 | 1 | 1 | **(A) 완전 붕괴** | *신규* |
| `12-build-heap-trace` | 5 | 1 | 1 | **(A) 완전 붕괴** | *신규* |
| `13-heapsort-trace` | 5 | 1 | 1 | **(A) 완전 붕괴** | *신규* |
| `14-counting-sort-trace` | 4 | 1 | 1 | **(A) 완전 붕괴** | *신규* |
| `15-radix-trace` | 3 | 1 | 1 | **(A) 완전 붕괴** | *신규* |

L03은 "-trace"라는 이름이 붙은 그림 10개 전부가 온전한 tabset이 아니다 — 2개는 처음/마지막만
보이는 (C), 나머지 8개는 SVG 자체가 최종 상태 1장만 존재하는 (A)다. 이번 감사에서 (A)/(C) 두
유형 모두 이 챕터에 가장 집중돼 있다.

## Lecture 04 · Selection and Order Statistics

| 원본 그림 | 원본 프레임 수 | 웹북 step SVG 수 | qmd 삽입 수 | 유형 | 비고 |
|---|---|---|---|---|---|
| `07-fixed-pivot-trace` | 5 | 5 | 2 | **(C) 프레임 뭉침** | *신규*. step1+step5만 삽입 |
| `08-randomized-trace` | 7 | 7 | 2 | **(C) 프레임 뭉침** | *신규*. step1+step7만 삽입, 중간 5단계 누락(이 챕터에서 가장 많이 누락된 사례) |
| `11-median-of-medians-trace` | 5 | 5 | 2 | **(C) 프레임 뭉침** | *신규*. step1+step5만 삽입 |

## Lecture 05 · Dynamic Programming

| 원본 그림 | 원본 프레임 수 | 웹북 step SVG 수 | qmd 삽입 수 | 유형 | 비고 |
|---|---|---|---|---|---|
| `04-memo-trace` | 4 | 4 | 4 | 정상 | tabset 확인 |
| `05-bottomup-trace` | 3 | 3 | 3 | 정상 | tabset 확인 |
| `10-matrix-row-progression` | 4 | 4 | 4 | 정상 | tabset 확인 |

L05는 애니메이션 그림 3개 모두 정상 변환.

## Lecture 06 · Search Trees

| 원본 그림 | 원본 프레임 수 | 웹북 step SVG 수 | qmd 삽입 수 | 유형 | 비고 |
|---|---|---|---|---|---|
| `02-tree-terminology-trace` | 4 | 4 | 2 | **(C) 프레임 뭉침** | *신규*. step1+step4만 삽입 |
| `08-preorder-trace` | 5 | 5 | 2 | **(C) 프레임 뭉침** | **기존 REVIEW_NOTES #9 "L06 순회"**. 매크로(`\travtree`) 그림이라 `mode` 필드와 무관하게 5장 전부 생성됨 — 붕괴는 순수 qmd 삽입 단계에서 발생 |
| `09-inorder-trace` | 4 | 4 | 2 | **(C) 프레임 뭉침** | #9와 동일 그룹 |
| `10-postorder-trace` | 5 | 5 | 2 | **(C) 프레임 뭉침** | #9와 동일 그룹 |
| `14-search-trace` | 4 | 4 | 2 | **(B) 프레임 누락** | **기존 REVIEW_NOTES #10**. step2·3 누락(사용자 지정 분류 유지). 구조적으로는 위 (C) 항목들과 동일(처음+마지막만 삽입, tabset 없음) |
| `17-insert-trace` | 6 | 6 | 2 | **(C) 프레임 뭉침** | *신규*. step1+step6만 삽입, 중간 4단계 누락 |
| `18-delete-case1-leaf` | 2 | 2 | 2 | 정상 | before/after 2장 다 표시(정보 손실 없음), tabset 대신 나란히 배치 |
| `19-delete-case2-one-child` | 2 | 2 | 2 | 정상 | 위와 동일 |
| `22-degenerate-bst-trace` | 5 | 5 | 2 | **(C) 프레임 뭉침** | *신규*. step1+step5만 삽입 |
| `48-btree-search-trace` | 2 | 2 | 2 | 정상 | before/after 2장 다 표시(정보 손실 없음) |

L06은 이번 감사에서 tabset으로 "정상" 판정된 시퀀스 그림이 **0개**다 — 2단계짜리 3건만
"둘 다 보이므로 정상"이고, 나머지 7건은 전부 처음+마지막만 남고 중간이 누락됐다(기존에 알려진
순회·검색 트레이스가 예외가 아니라 이 챕터의 지배적 패턴이었다).

## Lecture 07 · Hash Tables

| 원본 그림 | 원본 프레임 수 | 웹북 step SVG 수 | qmd 삽입 수 | 유형 | 비고 |
|---|---|---|---|---|---|
| `04-multiplication-trace` | 4 | 4 | 1 | **(A) 완전 붕괴** | *신규*. 마지막 step만 삽입, 전체 과정은 캡션 텍스트로만 서술 |
| `07-insert-29-collision-trace` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |
| `10-chaining-insert-trace` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |
| `11-chaining-search-delete-trace` | 4 | 4 | 1 | **(A) 완전 붕괴** | *신규* |
| `14-linear-trace1-collision` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |
| `15-linear-trace2-wraparound` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |
| `17-primary-clustering` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |
| `19-quadratic-trace-30` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |
| `21-double-hash-probe-trace` | 4 | 4 | 1 | **(A) 완전 붕괴** | *신규* |
| `24-wrong-deletion-trace` | 5 | 5 | 1 | **(A) 완전 붕괴** | *신규* |
| `25-correct-deletion-tombstone-trace` | 4 | 4 | 1 | **(A) 완전 붕괴** | *신규* |
| `26-logical-vs-probing-load` | 2(매크로, 각 상태=게이지 1개 단독) | 2 | 1 | **(A) 완전 붕괴** | *신규*. **캡션 불일치 추가 발견**: 삽입된 `step2.svg`의 캡션·fig-alt는 "logical load(0.45)와 probing load(0.70)를 나란히 보여주는 게이지"라고 서술하지만, 실제 `step2.svg`는 `\loadgauge` 두 번째 호출(probing gauge)만 단독 렌더링한 것(SVG 폭이 step1과 다름 — 235pt vs 266pt, 두 게이지가 겹쳐진 게 아니라 서로 다른 단일 게이지). 즉 캡션이 이미지에 없는 내용(logical gauge)을 설명하고 있다 |
| `27-rehash-animation` | 4 | 4 | 1 | **(A) 완전 붕괴** | *신규* |

L07은 시퀀스로 설정된 그림 12개 전부가 (A)다 — 스텝 SVG는 12건 모두 디스크에 전부 존재하는데
(즉 파이프라인은 정상 작동했다), qmd 저작 단계에서 마지막 한 장만 쓰고 나머지를 캡션 서술로
대체하는 방식이 이 챕터 전체에 일관되게 적용됐다.

## Lecture 08 · Graph Algorithms

| 원본 그림 | 원본 프레임 수 | 웹북 step SVG 수 | qmd 삽입 수 | 유형 | 비고 |
|---|---|---|---|---|---|
| `03-matrix-to-list` | 3 | 3 | 3 | 정상 | tabset 확인 |
| `05-bfs-queue-trace` | 7 | 7 | 7 | 정상 | tabset 확인 |
| `07-dfs-recursion-trace` | 6 | 6 | 6 | 정상 | tabset 확인 |
| `08-back-edge-animation` | 2 | 2 | 2 | 정상 | tabset 확인 |
| `09-kahn-trace` | 6 | 6 | 6 | 정상 | tabset 확인 |
| `11-dfs-topo-finish-reverse` | 4 | 4 | 4 | 정상 | tabset 확인 |
| `13-prim-trace` | 6 | 6 | 6 | 정상 | tabset 확인 |
| `14-dsu-animation` | 4 | 4 | 4 | 정상 | tabset 확인 |
| `15-kruskal-trace` | 7 | 7 | 7 | 정상 | tabset 확인 |
| `17-relaxation-animation` | 3 | 3 | 3 | 정상 | tabset 확인 |
| `19-dag-relaxation-trace` | 3 | 3 | 3 | 정상 | tabset 확인 |
| `20-dijkstra-trace` | 6 | 6 | 6 | 정상 | tabset 확인 |
| `22-bellman-ford-negative-cycle` | 2 | 2 | 2 | 정상 | tabset 확인 |

L08은 애니메이션 그림 13개(이 강의에서 가장 많은 시퀀스 수) 전부 정상 — L01/L02/L05와 함께
tabset 변환이 온전한 챕터.

## Lecture 09 · String Matching

| 원본 그림 | 원본 프레임 수 | 웹북 step SVG 수 | qmd 삽입 수 | 유형 | 비고 |
|---|---|---|---|---|---|
| `01-naive-alignment-trace` | 4 | 4 | 1 | **(A) 완전 붕괴** | *신규* |
| `02-naive-worst-case-repeated-prefix` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |
| `03-numeric-encoding-cad` | 2 | 2 | 1 | **(A) 완전 붕괴** | *신규* |
| `05-rolling-update-derivation` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |
| `07-collision-is-candidate` | 2 | 2 | 1 | **(A) 완전 붕괴** | *신규* |
| `08-candidate-to-valid-hit` | 2 | 2 | 1 | **(A) 완전 붕괴** | *신규* |
| `09-prefix-lps-discovery` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |
| `10-mismatch-fallback-trace` | 4 | 4 | 1 | **(A) 완전 붕괴** | *신규* |
| `11-lps-construction-trace` | 6 | 6 | 1 | **(A) 완전 붕괴** | *신규*. 이 챕터에서 가장 긴 원본 시퀀스(6단계)가 1장으로 축소 |
| `12-kmp-mismatch-recovery-trace` | 5 | 5 | 1 | **(A) 완전 붕괴** | *신규* |
| `13-kmp-overlapping-match` | 2 | 2 | 1 | **(A) 완전 붕괴** | *신규* |
| `14-right-to-left-comparison` | 2 | 2 | 1 | **(A) 완전 붕괴** | *신규* |
| `15-tiger-shift-table` | 2 | 2 | 1 | **(A) 완전 붕괴** | *신규* |
| `16-absent-character-shift` | 2 | 2 | 1 | **(A) 완전 붕괴** | *신규* |
| `17-rational-repeated-character` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |
| `18-horspool-trace-tiger` | 4 | 4 | 1 | **(A) 완전 붕괴** | *신규* |

L09는 시퀀스 그림 16개 **전부**가 (A)다 — 이 감사에서 발견된 것 중 L07·L10과 함께 가장 큰
규모의 신규 패턴. (M5 그림 크기 파일럿에서 이미 확인했듯, 이 챕터의 그림들은 모두 최종 스텝
1장 + 서술형 캡션 구조로 작성되어 있었다.)

## Lecture 10 · State-Space Tree Search

| 원본 그림 | 원본 프레임 수 | 웹북 step SVG 수 | qmd 삽입 수 | 유형 | 비고 |
|---|---|---|---|---|---|
| `02-state-space-expansion` | 4 | 4 | 1 | **(A) 완전 붕괴** | *신규* |
| `03-dfs-bfs-visit-order` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |
| `04-permutation-state-tree` | 4 | 4 | 1 | **(A) 완전 붕괴** | *신규* |
| `05-apply-undo-symmetry` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |
| `06-four-queens-board-trace` | 6 | 6 | 1 | **(A) 완전 붕괴** | *신규* |
| `09-subset-sum-trace` | 5 | 5 | 1 | **(A) 완전 붕괴** | *신규* |
| `10-graph-coloring-trace` | 4 | 4 | 1 | **(A) 완전 붕괴** | *신규* |
| `11-arithmetic-progression-trace` | 5 | 5 | 1 | **(A) 완전 붕괴** | *신규* |
| `12-bound-based-pruning` | 4 | 4 | 1 | **(A) 완전 붕괴** | *신규* |
| `13-knapsack-best-first-trace` | 7 | 7 | 1 | **(A) 완전 붕괴** | *신규*. 이 챕터에서 가장 긴 원본 시퀀스(7단계)가 1장으로 축소 |
| `15-frontier-policy-animation` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |
| `17-astar-open-closed-trace` | 6 | 6 | 1 | **(A) 완전 붕괴** | *신규* |
| `18-astar-path-reconstruction` | 3 | 3 | 1 | **(A) 완전 붕괴** | *신규* |

L10도 시퀀스 그림 13개 **전부**가 (A) — L07·L09와 정확히 같은 패턴.

## 알려진 3건 확인

| # | 항목 | 이번 감사 결과 |
|---|---|---|
| 4 | L02 `01-call-stack-push` | 목록에 있음 — (A) 완전 붕괴, 위 L02 표에서 상세 재확인(추가로 "실제 3단계여야 하는데 소스 스펙만으론 2단계로 잡힘"이라는 도구 한계도 발견) |
| 9 | L06 `08/09/10-*-trace`(순회) | 목록에 있음 — (C) 프레임 뭉침, 매크로 그림이라 SVG는 전부 생성되고 qmd 삽입만 문제라는 원인까지 확인 |
| 10 | L06 `14-search-trace` | 목록에 있음 — (B)로 유지(구조는 (C)와 동일하지만 사용자 지정 분류를 보존) |

## 신규 발견 요약 (알려진 3건 제외)

- **(A) 완전 붕괴, 파이프라인 단계** — L03 8건(`04-bubble-trace`, `05-insertion-trace`,
  `08-quick-partition-trace`, `11-heapify-trace`, `12-build-heap-trace`, `13-heapsort-trace`,
  `14-counting-sort-trace`, `15-radix-trace`): `FIGURE_CONFIG`에 `mode: sequence` 누락, L02
  push와 동일 원인 — SVG 자체가 최종 상태 1장만 존재.
- **(A) 완전 붕괴, qmd 저작 단계** — L07 12건 + L09 16건 + L10 13건 = **41건**(+ L07의
  `26-logical-vs-probing-load` 1건, 총 42건): 스텝 SVG는 전부 디스크에 존재하지만 qmd가
  마지막 스텝 1장만 삽입. 세 챕터 전체에 걸친 일관된 패턴이라 개별 그림 문제가 아니라
  **챕터 단위 변환 컨벤션의 차이**로 보인다(L01/02/05/06/08은 tabset, L07/09/10은
  "최종 상태 1장 + 서술 캡션"). L07 `26-logical-vs-probing-load`는 추가로 캡션-이미지
  내용 불일치까지 있다.
- **(C) 프레임 뭉침, 신규** — L03 2건(`03-selection-trace`, `07-merge-pointers`), L04 3건
  (`07-fixed-pivot-trace`, `08-randomized-trace`, `11-median-of-medians-trace`), L06 3건
  (`02-tree-terminology-trace`, `17-insert-trace`, `22-degenerate-bst-trace`) = 총 8건:
  스텝 SVG는 전부 존재하지만 qmd는 처음+마지막 2장만 나란히 삽입하고 중간을 누락.

## 감사 범위 밖(참고)

- 순수 텍스트 오버레이(itemize 점진 표시 등)는 이번 감사에서 제외했다(요청 범위: 그림
  애니메이션).
- `\pause`/`\uncover`/`\onslide`/`\temporal`은 강의노트 전체에 사용례가 없어 확인할 대상이
  없었다.
- 사용자가 언급한 "L06 Level-order queue" 정상 사례는 이번 그림-애니메이션 감사 범위에서는
  찾지 못했다 — `FIGURE_CONFIG["06"]`에 level-order용 시퀀스 그림이 없고(`11-level-order-
  reference-tree`는 정적 참조 트리 1장뿐), 큐 상태 변화는 표/텍스트로 서술된 것으로 보인다.
  그림이 아니므로 이 문서의 표 대상이 아니다(필요하면 별도 텍스트-오버레이 감사에서 확인).
