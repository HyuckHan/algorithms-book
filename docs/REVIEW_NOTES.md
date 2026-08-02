# REVIEW_NOTES — 정독 중 발견 사항 로그

이 문서는 **책 전체를 정독하며 발견한 수정 필요 사항을 모으는** 로그다. 발견 즉시 고치지 않고
쌓아뒀다가 카테고리별 batch로 처리한다(렌더·배포·커밋 파편화 방지).

> **2026-08-02 재정리**: 번호 중복·주석 매몰로 뒤섞였던 이전 버전을 하나의 유니크 번호 체계로
> 통합했다. 이 문서가 유일한 진실의 원천(source of truth)이다. 이전의 활성/주석 이중 번호는 폐기.

## 사용법

- **종류**가 처리 방식을 가른다:
  - `그림-재컴파일` = TikZ 소스 수정 → SVG 재추출 (texlive 필요)
  - `그림-애니메이션` = mode:sequence 추가·재추출 또는 tabset 삽입
  - `내용` = 본문 서술·정확성 (.qmd 또는 TikZ 내 텍스트)
  - `표현` = 문구·폰트·수식 조판
  - `설명보강` = 본문 문단 추가
- **상태**: `open` → `판단중` → `수정지시됨` → `done`
- **처리자**: `[CC]` Claude Code / `[나]` 사용자 직접 / `[?]` 미정
- **batch 그룹**: A=설명보강, B=표현·폰트·수식, C=TikZ 그림수정, D=애니메이션 재생성, H=보류

## 발견 사항 (현재 유효)

| # | 위치 | 종류 | 발견 내용 | 방향 | 상태 | 처리자 | batch |
|---|---|---|---|---|---|---|---|
| 11 | L02 `01-call-stack-push` | 그림-애니메이션 | mode:sequence 없어 SVG 1장만 생성(원본은 누적 애니메이션). 실제 복원 시 3단계(sum(4)만→+2→+2) | mode:sequence 추가·재추출 후 tabset 삽입 | open | [CC] | D |
| 12 | L03 트레이스 8개(bubble/insertion/quick-partition/heapify/build-heap/heapsort/counting-sort/radix) | 그림-애니메이션 | mode:sequence 없어 각각 최종 SVG 1장만 생성 | mode:sequence 추가·재추출 후 tabset 삽입 | open | [CC] | D |

## 보류 항목 (원본 세심 검토 후 별도 처리 — batch H)

| # | 위치 | 종류 | 발견 내용 | 방향 | 상태 |
|---|---|---|---|---|---|
| H1 | L09 전체 애니메이션 (16건) | 그림-애니메이션 | tabset 복원했다가 revert(`11323f1`). step SVG는 디스크에 유지 | 원본(Codex 신규 서사) 대조 검증 후 재복원 판단 | 보류 |
| H2 | L10 전체 애니메이션 (13건) | 그림-애니메이션 | tabset 복원했다가 revert(`699cafa`). step SVG는 디스크에 유지 | 원본 대조 검증 후 재복원 판단 | 보류 |
| H3 | L09 `03-numeric-encoding-cad` "원본 28 오류" 문구 | 내용 | 원본 교정 노출(웹북 독립성 저해) | 문구 삭제, cad=53만. [방침] "원본 대비 교정" 노출 전반에 적용 — 정독하며 같은 유형(L09 0-based, L10 pick/AP/C구현) 수집 | 보류 |

## 완료 항목 (done — 참고용 보존)

| 항목 | 커밋 | 내용 |
|---|---|---|
| L03/L04 프레임 뭉침 5개 | `d8278f8`, `a4f771d` | selection-trace, merge-pointers / fixed-pivot, randomized, median-of-medians tabset 복원 |
| L06 순회·검색·뭉침 | `f69d4b1` | preorder/inorder/postorder, search-trace, tree-terminology, insert-trace, degenerate-bst tabset 복원 |
| L07 시퀀스 12건 + 캡션 | `449e17b` | L07 12개 tabset 복원 + `26-logical-vs-probing-load` 캡션 교정(step1 logical/step2 probing 분리) |
| L04 median-of-medians 설명(#3) | `1d4b4e8` | Part D "구현" 문단에 `_insertion_sort` 역할 설명 문단 추가 |
| L08 애니메이션 설명 3개 + matrix-to-list 해제(#13-16) | `393c05f` | #14 DSU, #15 relaxation, #16 DAG relaxation 문단 추가(애니메이션 유지); #13 03-matrix-to-list tabset 해제(본문 인라인 예시 + Θ(V²)/Θ(V+E) 트레이드오프 문장으로 대체, step SVG는 디스크에 유지) |
| L06 size/height 분리 + DUPLICATE 폰트(#4, #6) | `433e748` | Part D size(x)/height(x)를 별도 display 수식 2개로 분리(목차 겹침 해소); TreeInsert `\texttt{DUPLICATE}` → `$\mathtt{DUPLICATE}$`(NIL/NotFound와 같은 MathJax 경로로 통일, 헤드리스 브라우저로 data-semantic-font="monospace" 일치 확인) |
| L06 search-trace + insert-trace 주석 확대(#7) | `6cf7861`, `976b3fc` | `14-search-trace`·`17-insert-trace` 좌상단 주석의 `font=\scriptsize` 제거. lecture-notes/는 읽기 전용이라 `scripts/extract_tikz.py`에 `text_patch` 메커니즘(TIKZ_PATCHES와 동일한 빌드타임 전용 원칙) 추가, 두 그림이 공유하는 `trace_orienting_annotation_font` 패치 하나로 처리. L06 전체 트레이스 그림(순회 3개·tree-terminology-trace·degenerate-bst-trace 포함)을 전수 확인해 이 패턴은 이 두 그림에만 있음을 확인(나머지는 `callout` 스타일 그대로라 폰트 문제 없음). 재추출 후 calibrated 측정(scriptsize/footnotesize/small/normalsize 384dpi 기준 렌더 비교)으로 두 주석 모두 normalsize로 확인. 자연폭 변화(search 479→509px, insert 511~529→524~556px)에도 기존 55% width에서 ratio 0.67~0.73x로 1.3x 이내 유지(폭 변경 불필요) |
| L06 SUCCESSOR 트리 통합 + succ(6) 교정(#5) | `da08ca1` | 분리돼 있던 두 tikzpicture(Case1 5-node 트리 / Case2 6-3-4 별도 그림)를 `full_override` 메커니즘으로 7-node 트리 하나(2-tab tabset)로 병합. succ(6)=7→15 교정, BST/successor 알고리즘 기준 4개 값 전부 재검산 |
| L05/L07 화살표·레이블 국소 수정(#1,2,8,9,10) | `2a9f15e` | #1 matrix-reconstruction 화살표 간격·색 대비, #2 matrix-representative-cell "chosen" 폰트, #8 hash-pipeline 레이블 겹침(간격+줄바꿈), #9 chaining-insert-trace step1 노드 연결, #10 linear-trace2-wraparound step3 화살표 각도 |

*주: L06 `14-search-trace`·`17-insert-trace`는 애니메이션 tabset(`f69d4b1`)과 주석 폰트(`6cf7861`, `976b3fc`) 모두 done.*

## 처리 이력 (커밋 추적)

| 처리일 | 대상 | 커밋 | 비고 |
|---|---|---|---|
| 2026-08-02 | L03 뭉침 | `d8278f8` | selection-trace, merge-pointers |
| 2026-08-02 | L04 뭉침 | `a4f771d` | fixed-pivot, randomized, median-of-medians |
| 2026-08-02 | L06 순회·검색·뭉침 | `f69d4b1` | 순회 3개, search-trace, tree-terminology, insert-trace, degenerate-bst |
| 2026-08-02 | L07 시퀀스 + 캡션 | `449e17b` | L07 12개 + logical-vs-probing 캡션 |
| 2026-08-02 | L09 복원 | `e960999` | (이후 revert) |
| 2026-08-02 | L10 복원 | `02f4910` | (이후 revert) |
| 2026-08-02 | L09 revert | `11323f1` | reverts `e960999` — 보류(H1). step SVG 유지 |
| 2026-08-02 | L10 revert | `699cafa` | reverts `02f4910` — 보류(H2). step SVG 유지 |
| 2026-08-02 | L04 #3 | `1d4b4e8` | insertion sort 역할 설명 추가 |
| 2026-08-02 | L08 #13-16 | `393c05f` | DSU/relaxation/DAG relaxation 설명 추가 + matrix-to-list tabset 해제 |
| 2026-08-02 | L06 #4, #6 | `433e748` | size/height 수식 분리, DUPLICATE 폰트 통일 |
| 2026-08-02 | L06 #7 | `6cf7861` | search-trace 주석 폰트 확대(text_patch 신설, 4개 SVG 재추출) |
| 2026-08-02 | L06 #7(재진단, 확장) | `976b3fc` | 재진단으로 search-trace 수정이 실제 유효했음(normalsize) 확인 + insert-trace(미수정 상태였음) 동일 패치 적용, 6개 SVG 재추출. L06 전체 트레이스 전수 확인 완료 |
| 2026-08-02 | L06 #5 (batch C) | `da08ca1` | SUCCESSOR 트리 구조 통합(2개 tikzpicture→1개 7-node 트리) + succ(6)=7→15 교정. `FULL_BODY_PATCHES` 메커니즘 신설 |
| 2026-08-02 | L05/L07 #1,2,8,9,10 (batch C) | `2a9f15e` | matrix-reconstruction/representative-cell 화살표·레이블, hash-pipeline 레이블 겹침, chaining-insert-trace step1, linear-trace2-wraparound step3 화살표 수정. `TEXT_PATCHES` 리스트 지원 확장 |

---

## 설명 보강 문단 (#3, #14, #15, #16) — 반영 완료(`1d4b4e8`, `393c05f`), 참고용 보존

애니메이션(tabset)은 진행형이고 값이 정확하므로 **유지**하고, 아래 문단을 지정 위치에 추가한다.
인라인 수식은 `$...$`, 함수·코드명은 백틱. 값·그림·tabset 구조는 변경하지 않는다.

### #3 L04 insertion sort 설명 (Part D "구현" 문단에 삽입)

> 각 5-원소 그룹의 median은 `_insertion_sort`로 그룹을 정렬한 뒤 가운데 원소를 취해 구한다.
> 그룹 크기가 상수(5)이므로 이 정렬은 $O(1)$이고, 그룹이 $\lceil n/5 \rceil$개이므로 전체
> 그룹 정렬 비용은 $\Theta(n)$이다.

*(위 문장을 "구현" 문단에서 `_insertion_sort`가 코드에 처음 등장하기 직전 맥락에 자연스럽게 삽입.)*

### #14 DSU 추가 문단 (DSU Animation tabset 바로 위)

> Kruskal은 간선을 가중치 순으로 훑으며 "이 간선을 넣으면 사이클이 생기는가"를 매번 판정해야
> 한다. 이 판정을 빠르게 해주는 자료구조가 **Disjoint Set Union(DSU)**이다. 각 정점이 속한
> 컴포넌트를 대표원소(root)로 표현하고 두 연산을 제공한다 — `Find(x)`는 $x$가 속한 컴포넌트의
> root를 반환하고, `Union(x, y)`는 두 컴포넌트를 하나로 합친다. 간선 $(u, v)$를 검사할 때
> $Find(u) \ne Find(v)$이면 두 정점이 다른 컴포넌트에 있다는 뜻이므로 사이클 없이 안전하게
> 채택(accept)하고 `Union`으로 합친다. 같으면($Find(u) = Find(v)$) 이미 연결된 컴포넌트라
> 사이클이 생기므로 버린다(reject). 아래 애니메이션은 4개 정점 $\{A\}\{B\}\{C\}\{D\}$가 간선을
> 하나씩 처리하며 컴포넌트가 병합되는 과정을 보여준다.

### #15 relaxation 추가 문단 (relaxation 조건 수식 아래, tabset 위)

> relaxation은 "$u$를 거쳐 $v$로 가는 경로가 지금까지 알던 것보다 짧은가"를 판정하는 연산이다.
> $dist[u] + w(u, v)$가 **candidate**($u$ 경유 새 거리)이고, 이것이 기존 $dist[v]$보다 작으면
> 더 짧은 경로를 찾은 것이므로 $dist[v]$를 갱신하고 $parent[v]$를 $u$로 바꾼다. 아래 애니메이션은
> $dist[u]=4$, $w(u, v)=-2$인 상황을 예로 든다 — candidate는 $4+(-2)=2$이고 기존 $dist[v]=7$보다
> 작으므로, 비교 후 $dist[v]$가 $2$로 갱신된다.

*(선택) Bellman-Ford 복선을 원하면 마지막에: "가중치가 음수여도 relaxation 판정 자체는 동일하게 작동한다." — 단 #16이 음수를 이미 강조하므로 중복 주의.)*

### #16 DAG relaxation 추가 문단 (DAG Relaxation Trace tabset 바로 위)

> DAG(방향 비순환 그래프)에서는 정점을 **topological order**로 나열한 뒤 그 순서대로 한 번씩
> relax하면 최단 거리가 확정된다 — 각 정점을 처리할 때 그 정점으로 들어오는 모든 경로가 이미
> 처리돼 있기 때문이다. 사이클이 없으므로 Dijkstra의 우선순위 큐도, Bellman-Ford의 반복도 필요
> 없다. 아래 예는 topo order `s, a, b, c`를 따른다 — $s$를 relax하면 $d[a]=3$, $d[b]=2$가 되고,
> $a$를 거쳐 $d[c]=3+(-4)=-1$(경로 $s \to a \to c$)이 확정된다. $b$를 거치는 후보 $d[b]+1=3$은
> 이미 확정된 $-1$보다 크므로 갱신하지 않는다. 음수 간선($-4$)이 있어도 topological order 덕분에
> 단 한 번의 pass로 정답을 얻는다.

### 처리 시 주의

- 삽입 위치는 각 문단 제목의 괄호 참조. 독자가 "설명 → 애니메이션 확인" 순서로 읽게.
- 렌더 후 수식이 raw LaTeX로 노출되지 않는지 확인(여기서는 `\Call` 미사용).
- 기존 잘 된 애니메이션 설명(BFS/DFS/Dijkstra trace)의 문체·밀도와 톤 맞춤.

