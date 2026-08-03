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
- **batch 그룹**: A=설명보강, B=표현·폰트·수식, C=TikZ 그림수정, D=애니메이션 재생성, E=그림 크기(%width) 조정, H=보류

## 발견 사항 (현재 유효)

| # | 위치 | 종류 | 발견 내용 | 방향 | 상태 | 처리자 | batch |
|---|---|---|---|---|---|---|---|

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
| L05 #2 재수정 — 25 셀 강조(방법 A) | `ce58f0c` | 폰트만 키운 첫 수정(`2a9f15e`)이 불충분하다는 피드백으로 재작업. 25를 `dp dependency`(파랑)에서 `dp current`(주황, 28과 동일 스타일)로 재-스타일링해 "선택된 값→결과" 흐름을 색으로 통일, 31은 비강조 유지. "chosen" 레이블을 화살표 옆에서 25 셀 바로 위로 재배치. 레이블 이동으로 자연폭이 줄어(125.9pt→77.5pt) 기존 20% width에서 ratio 1.32x로 상한 초과 → 19%(1.25x)로 축소 |
| L06 트리 그림 크기 재조정(batch E) | `7aa946a` | batch B·C 재추출(주석 폰트 확대, succ 트리 병합 등)로 자연폭이 커진 그림들의 ratio가 0.55~0.84x까지 떨어져 상한(1.3x) 대비 너무 작아짐. 순회(08·09·10·11) 40%→50%, search/insert-trace(14·17) 55%→80%(짝 통일), delete-case3(20·21) 55%→70%, right-rotation(23·24) 35%→55%/50%, RB-insert(40·41·43) 30~35%→40~50%, B-tree(48·51·52·54·56·57·58·59) 25~60%→40~80% — 총 41개 이미지 태그 조정, SVG 재추출 불필요(width만 변경). 조정 후 전부 0.98~1.13x로 수렴, 이미 1.0~1.3x였던 그림은 그대로 유지 |
| L02 push 애니메이션 복원(#11, batch D) | `b252c8f` | `FIGURE_CONFIG`에 mode:sequence 누락으로 `\visible<2->/<3->` 누적 애니메이션이 최종 상태 1장으로 붕괴. 소스에 명시적 `<1>`이 없어 `overlay_steps()` 경계 탐지가 {2,3}만 잡는 함정 확인 → `process_lecture()`에 "steps" override 메커니즘 신설, `[1,2,3]`으로 실제 3프레임(sum(4)만→+2→+2) 재추출. qmd를 pop과 동일한 3-tab panel-tabset·30% width(ratio 1.26x)로 교체해 push/pop 시각적 대칭 확보 |
| L03 트레이스 8개 애니메이션 복원(#12, batch D) | `236cc5b` | bubble/insertion/quick-partition/heapify/build-heap/heapsort/counting-sort/radix 8개 `FIGURE_CONFIG`에 mode:sequence 추가(전부 소스에 명시적 `<1>` 있어 steps override 불필요). 재추출 결과 4/5/4/4/5/5/4/3 프레임으로 소스와 정확히 일치 확인(각 트레이스의 배열/트리 상태를 알고리즘으로 재검산 — insertion·heapsort·counting-sort·radix 최종 결과가 실제 정렬/카운트 결과와 일치). qmd 8개를 각각 step별 캡션이 있는 panel-tabset으로 교체, 기존 %width 유지(재추출 후에도 ratio 1.13~1.25x로 변동 없음). 부수적으로 05-insertion-trace가 바로 위 05-insertion-cards 이미지와 빈 줄 없이 붙어있어 pandoc이 새 tabset을 별도 블록으로 인식 못하는 문제(quarto의 "stray :::" 경고)를 발견해 빈 줄 추가로 수정 |
| L03 bubble/quick-partition 비교-스텝 누락 보강(#17, batch D) | `6bf7c7c` | #12 복원 직후 발견: 두 트레이스는 원본 소스 자체가 "swap이 일어난 스텝"만 `\only` 프레임으로 그렸고 "비교했지만 swap 안 함"은 프레임 자체가 없었음(진단: 파이프라인 문제(a)가 아니라 원본 저작 단계 누락(b)). bubble 4→5프레임(29-37 무교환 비교 프레임 추가), quick-partition 4→10프레임(j=1..9 스캔 스텝 전부 + 최종 상태, scan pointer j를 처음으로 시각화)으로 `full_override` 전면 재작성. `common/sorting.tex`에 정의돼 있었지만 lecture-notes/ 전체에서 한 번도 쓰이지 않던 `sort compared`(빗금 패턴) 스타일을 "비교만, swap 없음"에 사용해 `sort current`(단색 주황, swap 있음)와 구분. 모든 프레임 값을 알고리즘으로 직접 재검산, 최종 상태는 원본과 정확히 일치 |
| L02 push 재수정 — 5단계·pop과 스택 방향 정렬(#11 재작업) | `4bd0b42` | 첫 복원(`b252c8f`)은 소스 자체의 3-state 배칭(1→3→5개 누적)을 그대로 복원했을 뿐이라 "재귀 호출마다 frame 하나씩"이라는 본문 서술 및 pop의 5단계 페이스와 어긋남. pop의 템플릿(동일 옵션, `\path` 투명 프레이밍 박스로 5단계 내내 캔버스 크기 고정, `(a) at (0,.35)` 바닥 anchor + `above=of` 체이닝)을 그대로 복사해 `full_override`로 5개 `\only<1>-<5>` 상태를 새로 저작 — sum(4) 바닥·sum(0) 정상으로 pop과 방향 일치, 매 단계 새로 쌓인 frame을 주황으로 강조(pop의 반환 frame 강조와 대칭). 자연폭이 pop과 완전히 동일(132.694pt)해져 push step5와 pop step1이 픽셀 단위로 동일하게 렌더됨 확인 |
| L02 binary-search 레이블 겹침 수정(#18, batch C) | `b538e76` | Part G 이진 탐색 트레이스 상단 "A[mid]=...<x" 레이블이 `above=3pt of aN`(셀 상단에서 3pt)로 배치돼 index 행(y=.68)과 거의 같은 높이에서 겹침. 3개 `\only` 블록의 앵커(a3/a5/a4) 오프셋을 16pt로 확대해 index 행과 명확한 간격 확보, 가로 위치·begin/end 레이블·강조·회색 처리는 그대로 |
| L02 Hanoi 큰 원판 이동 단계 추가(#19, batch D) | `a82453a` | n=3 핵심 상태 트레이스가 "초기→첫 재귀 완료→전체 완료" 3단계뿐이라 재귀를 두 부분으로 가르는 "큰 원판 L→R 이동" 단계가 빠짐. 소스에 4번째 상태가 존재하지 않아 `full_override`로 신규 저작(단, 모든 `\draw[disk]` 좌표는 기존 state1·state3의 원판 사각형을 그대로 재사용) — L 빔, M에 작은 2개, R에 큰 원판 1개인 새 3단계 삽입, 기존 "전체 완료"는 4단계로 밀림 |
| L02 미로 backtracking 프레임 분할(#20, batch D) | `57e9549` | step3이 "전진 3칸 + dead end 2칸"을 한 프레임에 압축해 두 갈래가 동시에 orange로 보임. 기존 step3/step4를 그대로 보존한 채(각각 새 step5/step6이 됨) 그 사이에 "(3,2)-(4,2) 막다른 pocket으로 전진"(새 step3)과 "그 pocket을 dead로 표시하며 (2,2)로 되돌아감"(새 step4) 2개 프레임을 추가해 4→6단계로 확장. 매 프레임 orange 경로가 항상 한 줄기만 되도록 재구성, 최종 경로/dead 집합은 원본과 동일 |

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
| 2026-08-02 | L05 #2 재수정 | `ce58f0c` | "chosen" 폰트만 키운 첫 수정이 불충분해 재작업: 25 셀을 28과 같은 주황(`dp current`)으로 강조, 레이블을 25 셀 위로 재배치, width 20%→19%(1.32x→1.25x) |
| 2026-08-02 | L06 그림 크기 재조정 (batch E) | `7aa946a` | 트리 트레이스·rotation·RB-insert·B-tree 41개 이미지 %width 조정(SVG 재추출 없음), 전부 0.98~1.13x로 수렴 |
| 2026-08-02 | L02 #11 (batch D) | `b252c8f` | push mode:sequence 추가 + "steps" override 메커니즘 신설, 3프레임 재추출, pop과 대칭되는 tabset 복원 |
| 2026-08-02 | L03 #12 (batch D) | `236cc5b` | 8개 트레이스 mode:sequence 추가, 4/5/4/4/5/5/4/3 프레임 재추출·검산, 8개 tabset 복원 |
| 2026-08-02 | L03 #17 (batch D) | `6bf7c7c` | bubble/quick-partition 비교-스텝 누락 보강(4→5, 4→10 프레임), `sort compared` 스타일 도입 |
| 2026-08-03 | L02 #11 재작업 | `4bd0b42` | push를 pop과 같은 템플릿으로 재저작(5단계, 방향·강조 일치), 자연폭 pop과 동일화 |
| 2026-08-03 | L02 #18 (batch C) | `b538e76` | binary-search 레이블 offset 3pt→16pt, index 행과 겹침 해소 |
| 2026-08-03 | L02 #19 (batch D) | `a82453a` | Hanoi 트레이스 3→4단계, 큰 원판 이동 프레임 신규 저작 |
| 2026-08-03 | L02 #20 (batch D) | `57e9549` | 미로 backtracking 트레이스 4→6단계, pocket 탐색/dead-end/백트랙 프레임 분리 |

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

