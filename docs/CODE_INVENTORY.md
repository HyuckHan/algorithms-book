# CODE_INVENTORY — 강의별 코드 재고 (ADR-004)

`lecture-notes/code/lectureNN/{java,c}/`에 이미 있는 from-scratch 알고리즘 구현과, 강의를 변환할 때
새로 작성해야 할 구현을 강의별로 정리한다. **"Python만 신규"라고 가정하지 말 것** — Java·C도
강의마다 커버리지가 다르다(L06은 C가 전혀 없음, L04는 Java에 한 알고리즘이 빠짐 등).

조사 방법: 각 강의 `sections/*.tex`에서 `\begin{algorithmic}` 블록(있으면 `\Procedure` 이름)을
전수 추출하고, `lecture-notes/code/lectureNN/`의 기존 파일을 함수/클래스 시그니처 단위로 대조했다.
"있음"은 실제 코드를 확인한 것이고, "확인 필요"는 파일은 있으나 해당 알고리즘까지 구현했는지
이 조사에서 직접 확인하지 못한 경우다(강의 변환 착수 시 재확인).

범례: ✅ 있음(재사용) · ✅(파일 내 포함, 아래 비고 참조) · ❌ 신규 작성 필요 · Python은 정책상 전 항목 신규.

## Lecture 01 · 알고리즘 입문

`lecture-notes/code/lecture01/` 없음(코드 자체가 없음).

| 알고리즘 | 소스 | Java | C | Python |
|---|---|---|---|---|
| Maximum | `05_maximum.tex` | ❌ 신규 | ❌ 신규 | ❌ 신규 |
| LinearSearch | `06_linear_search.tex` | ❌ 신규 | ❌ 신규 | ❌ 신규 |
| BinarySearch | `07_binary_search.tex` | ❌ 신규 | ❌ 신규 | ❌ 신규 |

`04_pseudocode.tex`의 if/else·while 예시 2개는 의사코드 표기법 자체를 가르치는 일반 템플릿이며
from-scratch 알고리즘이 아니므로 코드 대상에서 제외.

## Lecture 02 · 재귀

`lecture-notes/code/lecture02/` 없음. **이 강의는 `\begin{algorithmic}`를 전혀 쓰지 않는다** —
알고리즘을 C `\lstlisting` 코드로 슬라이드에 직접 보여준다(아래 "슬라이드 내 C" 열). ADR-004는
이 슬라이드 코드도 "이미 있으면 재사용" 대상으로 본다: 짧고 이미 정확하므로 C 재작성 없이
그대로 `code/`로 옮기고, Java/Python을 새로 맞추면 된다.

| 알고리즘 | 소스 | 슬라이드 내 C | Java | Python |
|---|---|---|---|---|
| Factorial | `04_basic_examples.tex` | ✅ (그대로 재사용 가능) | ❌ 신규 | ❌ 신규 |
| Power ($x^n$) | `04_basic_examples.tex` | ✅ | ❌ 신규 | ❌ 신규 |
| Fibonacci(재귀, naive) | `04_basic_examples.tex` | 없음(재귀식만 제시) | ❌ 신규 | ❌ 신규 |
| String length(재귀) | `04_basic_examples.tex` | ✅ | ❌ 신규 | ❌ 신규 |
| Print reverse | `04_basic_examples.tex` | ✅ | ❌ 신규 | ❌ 신규 |
| Print binary | `04_basic_examples.tex` | ✅ | ❌ 신규 | ❌ 신규 |
| Hanoi | `08_hanoi.tex` | 없음(다이어그램·점화식만) | ❌ 신규 | ❌ 신규 |
| Maze 탐색 | `09_maze.tex` | 확인 필요(lstlisting 2개 존재) | ❌ 신규 | ❌ 신규 |
| Blob(연결 요소) 세기 | `10_blob.tex` | 없음 | ❌ 신규 | ❌ 신규 |
| Power Set | `11_power_set.tex` | 확인 필요(lstlisting 2개 존재) | ❌ 신규 | ❌ 신규 |

## Lecture 03 · 정렬 (파일럿, 완료 — 정책 확정 이전)

::: 참고
M1에서 먼저 완료됨. **정책과 불일치하는 알려진 예외**(ADR-004에도 기록): Python
(`code/03-sorting/python/sorting.py`)은 Selection/Insertion/Merge Sort의 from-scratch 구현이고,
C/Java(`code/03-sorting/{c,java}/`)는 `lecture-notes/code/lecture03/`에서 그대로 가져온
Comparator·qsort API 안전성 데모라서 **서로 다른 알고리즘/데이터**를 다룬다. 아래 표는 "정책대로
라면 무엇이 필요한가"를 보여주며, 실제 정합 작업(Bubble/Quick/Heap/Counting의 Java·C from-scratch
구현 추가, 혹은 Selection/Insertion/Merge의 Java·C 추가)은 별도 후속 작업이다.
:::

| 알고리즘 | 소스 | Java | C | Python |
|---|---|---|---|---|
| SelectionSort | `03_selection.tex` | ❌ 신규 | ❌ 신규 | ✅ `sorting.py` |
| BubbleSort | `04_bubble.tex` | ❌ 신규 | ❌ 신규 | ❌ 신규 |
| InsertionSort | `05_insertion.tex` | ❌ 신규 | ❌ 신규 | ✅ `sorting.py` |
| MergeSort / Merge | `07_merge_sort.tex` | ❌ 신규 | ❌ 신규 | ✅ `sorting.py` |
| QuickSort / Partition | `08_quick_sort.tex` | ❌ 신규 | ❌ 신규 | ❌ 신규 |
| MaxHeapify | `11_heapify.tex` | ❌ 신규 | ❌ 신규 | ❌ 신규 |
| BuildMaxHeap | `12_build_heap.tex` | ❌ 신규 | ❌ 신규 | ❌ 신규 |
| HeapSort | `13_heap_sort.tex` | ❌ 신규 | ❌ 신규 | ❌ 신규 |
| CountingSort | `14_counting_sort.tex` | ❌ 신규 | ❌ 신규 | ❌ 신규 |
| (Comparator/qsort API 안전성 데모) | `17_java_sorting.tex`, `18_c_sorting.tex` | ✅ `FruitSorting.java` | ✅ `qsort_examples.c` | ✅ `comparator_demo.py` |

## Lecture 04 · 선택과 순서통계량

`lecture-notes/code/lecture04/{java,c}/` 존재.

| 알고리즘 | 소스 | Java | C | Python |
|---|---|---|---|---|
| SelectBySorting(정렬 후 선택, baseline) | `03_sort_then_select.tex` | ❌ 신규 | ❌ 신규 | ❌ 신규 |
| FixedQuickselect(고정 pivot) | `04_quickselect_idea.tex` | 확인 필요 — `Quickselect.java`가 이 버전인지 RandomizedSelect인지 재확인 | 확인 필요 | ❌ 신규 |
| RandomizedSelect | `08_randomized_select.tex` | ✅ `Quickselect.java`(`select(int[], int, Random)`) | ✅ `quickselect.c`(`quickselect_int`) | ❌ 신규 |
| DeterministicSelect(median-of-medians, group of 5) | `10_group_of_five.tex` | ❌ **Java 없음** (C만 있음) | ✅ `deterministic_select.c` | ❌ 신규 |

## Lecture 05 · 동적 계획법

`lecture-notes/code/lecture05/{java,c}/` 존재 — Java·C 모두 잘 갖춰져 있음, Python만 신규.

| 알고리즘 | 소스 | Java | C | Python |
|---|---|---|---|---|
| FibRecursive / FibMemo / FibBottomUp | `02_fibonacci.tex`, `03_memoization_tabulation.tex` | ✅ `FibonacciDP.java` | ✅ `fibonacci.c` | ❌ 신규 |
| MinPath / MinPathMemo(행렬 경로) | `05_matrix_path.tex` | ✅ `MinPathSum.java` | ✅ `min_path_sum.c` | ❌ 신규 |
| LCSLength | `07_lcs.tex` | ✅ `LCS.java` | ✅ `lcs.c` | ❌ 신규 |
| Maximum Subarray(Kadane, informal) | `09_maximum_subarray.tex` | ✅ `MaximumSubarray.java` | ✅ `max_subarray.c` | ❌ 신규 |

## Lecture 06 · 검색 트리

`lecture-notes/code/lecture06/java/` 존재. **C가 전혀 없음** — 이 강의는 C 전체를 신규 작성해야 한다.

| 알고리즘 | 소스 | Java | C | Python |
|---|---|---|---|---|
| Preorder/Inorder/Postorder/LevelOrder 순회 | `03_traversal.tex` | ✅ `BinaryTree.java`/`BinaryTreeDemo.java` | ❌ **신규(강의 전체)** | ❌ 신규 |
| TreeSearch / IterativeTreeSearch / TreeMinimum | `06_bst_search.tex` | ✅ `BinarySearchTree.java` | ❌ 신규 | ❌ 신규 |
| TreeInsert / Transplant(삭제) | `07_bst_insert_delete.tex` | ✅ `BinarySearchTree.java` | ❌ 신규 | ❌ 신규 |
| RotateRight(AVL 회전) | `09_avl.tex` | ✅ `AVLTree.java`(insert/delete 내 균형 로직) | ❌ 신규 | ❌ 신규 |
| BTreeSearch / BTreeInsert | `11_btree.tex` | ✅ `BTree.java` | ❌ 신규 | ❌ 신규 |

::: 비고
Red-Black Tree(`RedBlackTree.java`)는 존재하지만 이 조사에서 뽑은 12개 algorithmic 블록 목록에는
전용 섹션이 없었다 — 강의 변환 시 해당 섹션(있다면)과 다시 대조할 것.
:::

## Lecture 07 · 해시 테이블

`lecture-notes/code/lecture07/{java,c}/` 존재.

| 알고리즘 | 소스 | Java | C | Python |
|---|---|---|---|---|
| StringHash(다항식 해시 함수 자체) | `04_string_hashing.tex` | ❌ **신규**(HashMap 내부에 묻혀 있어 별도 데모 없음) | ❌ 신규 | ❌ 신규 |
| ChainedSearch | `06_chaining.tex` | ✅ `ChainedHashMap.java` | ✅ `chained_hash_table.c` | ❌ 신규 |
| HashSearch / HashPut(open addressing) | `07_open_addressing.tex` | ✅ `OpenAddressHashMap.java` | ✅ `open_address_hash_table.c` | ❌ 신규 |
| HashDelete(tombstone) | `11_deletion.tex` | ✅ `OpenAddressHashMap.java`(`remove`) | 확인 필요 | ❌ 신규 |

## Lecture 08 · 그래프 알고리즘

`lecture-notes/code/lecture08/{java,c}/` 존재 — 커버리지가 가장 좋음.

| 알고리즘 | 소스 | Java | C | Python |
|---|---|---|---|---|
| BFS | `03_bfs.tex` | ✅ `GraphTraversal.java` | ✅ `bfs_dfs.c` | ❌ 신규 |
| DFS | `04_dfs.tex` | ✅ `GraphTraversal.java` | ✅ `bfs_dfs.c` | ❌ 신규 |
| TopoKahn(위상 정렬) | `06_topological_sort.tex` | ✅ `TopologicalSort.java`(`kahn`, `dfs`) | ✅ `topological_sort.c` | ❌ 신규 |
| Prim | `09_prim.tex` | ✅ `MinimumSpanningTree.java` | ✅ `mst.c` | ❌ 신규 |
| Kruskal | `10_kruskal.tex` | ✅ `MinimumSpanningTree.java`(+ `DisjointSet.java`) | ✅ `mst.c`(+ `disjoint_set.c`) | ❌ 신규 |
| DAGShortestPaths(비가중 DAG 최단경로) | `13_unweighted_dag.tex` | ❌ **신규**(`ShortestPaths.java`엔 Dijkstra/Bellman-Ford만 있음) | ❌ 신규 | ❌ 신규 |
| Dijkstra | `14_dijkstra.tex` | ✅ `ShortestPaths.java` | ✅ `shortest_paths.c` | ❌ 신규 |
| BellmanFord | `15_bellman_ford.tex` | ✅ `ShortestPaths.java` | ✅ `shortest_paths.c` | ❌ 신규 |

## Lecture 09 · 문자열 매칭

`lecture-notes/code/lecture09/{java,c}/` 존재 — 커버리지 좋음.

| 알고리즘 | 소스 | Java | C | Python |
|---|---|---|---|---|
| NaiveMatch | `02_naive.tex` | ✅ `StringMatchers.java`(`naiveAll`/`naiveFirst`) | ✅ `string_matching.c`(`sm_naive_all`) | ❌ 신규 |
| RabinKarp | `07_rabin_karp_analysis.tex` | ✅ `StringMatchers.java`(`rabinKarpAll`) | 확인 필요(파일 존재, 함수 미확인) | ❌ 신규 |
| BuildLPS / KMPSearch | `11_kmp_preprocessing.tex`, `12_kmp_search.tex` | ✅ `StringMatchers.java`(`buildLps`/`kmpAll`) | 확인 필요 | ❌ 신규 |
| BuildShiftTable / Horspool | `16_horspool.tex` | ✅ `StringMatchers.java`(`buildHorspoolShift`/`horspoolAll`) | 확인 필요 | ❌ 신규 |

## Lecture 10 · 상태공간 트리 탐색

`lecture-notes/code/lecture10/{java,c}/` 존재.

| 알고리즘 | 소스 | Java | C | Python |
|---|---|---|---|---|
| ChoosePermutation / ChooseCombination | `03_permutation_combination.tex` | ✅ `PermutationGenerator.java` | ✅ `permutation.c` | ❌ 신규 |
| Backtrack(일반 골격) | `04_backtracking.tex` | 확인 필요(개념 골격, 구체 사례로 대체될 수 있음) | 확인 필요 | ❌ 신규 |
| Place(N-Queens) | `05_n_queens.tex` | ✅ `NQueensSolver.java` | ✅ `n_queens.c` | ❌ 신규 |
| SubsetSum | `06_subset_sum.tex` | ✅ `SubsetSumSolver.java` | ✅ `subset_sum.c` | ❌ 신규 |
| Color(그래프 색칠) | `07_graph_coloring.tex` | ✅ `GraphColoringSolver.java` | 확인 필요(C 쪽 파일 없음 — 목록에 없음) | ❌ 신규 |
| BranchAndBound(Knapsack) | `09_branch_and_bound.tex` | ✅ `KnapsackBranchAndBound.java` | ✅ `knapsack_bnb.c` | ❌ 신규 |
| AStar / Relax | `12_a_star.tex` | ✅ `AStarGrid.java` | ✅ `a_star_grid.c` | ❌ 신규 |

## 요약: 강의별 C 커버리지 격차

L02(코드 자체 없음, 슬라이드 lstlisting만), L06(Java만 있고 **C 전체 신규**), L10의 GraphColoring
(C 없음)을 제외하면 대부분 강의는 Java·C가 이미 어느 정도 갖춰져 있고 **Python만 전량 신규
작성**이 핵심 작업이다. "확인 필요" 항목은 강의 변환 착수 시 해당 파일을 직접 열어 함수 단위로
재확인할 것 — 이 조사는 함수 시그니처 grep 기반이며 파일 전체를 정독하지는 않았다.
