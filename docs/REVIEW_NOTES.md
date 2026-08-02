# REVIEW_NOTES — 정독 중 발견 사항 로그

이 문서는 **책 전체를 천천히 정독하면서 발견한 수정 필요 사항을 모으기 위한** 로그다.
발견할 때마다 즉시 고치지 않고 여기 한 줄씩 쌓아뒀다가, 어느 정도 모이면
(예: 한 챕터 정독 완료 시, 또는 10~20개 누적 시) batch로 한꺼번에 처리한다.
개별 수정을 매번 하면 렌더·배포·커밋이 파편화되므로, 모아서 처리하는 것이 목적이다.

## 사용법

- **발견할 때마다** 아래 표에 한 줄 추가한다. 완벽하게 적으려 하지 말고 빠르게 던지듯 적는다.
- **"원하는 방향"이 애매하면 비워둬도 된다** — 나중에 함께 판단한다.
- **종류**는 처리 방식을 가르므로 되도록 채운다:
  - `그림` = SVG/TikZ 소스 수정 (재컴파일 필요, texlive 필요)
  - `내용` = 본문 서술·설명의 정확성/논리 문제 (.qmd 또는 TikZ 내 텍스트)
  - `표현` = 문구 다듬기·일관성 (경미)
  - `코드` = 3언어 구현/출력 관련
- **상태**: `open`(미처리) → `판단중`(방향 논의 필요) → `수정지시됨`(Claude Code에 전달) → `done`(반영·확인 완료)
- **판단이 필요한 항목**(왜 이렇게 됐는지 근거를 먼저 확인해야 하는 것)은 상태를 `판단중`으로 두고 비고에 메모.

## 발견 사항

| # | 위치 (챕터 · 파일/줄) | 종류 | 발견 내용 | 원하는 방향 | 상태 | 비고 |
|---|---|---|---|---|---|---|
| 1 | L05 `figures/05-dynamic-programming/12-matrix-reconstruction.svg` | 그림 | 화살표가 불명확(clear하지 않음) | 화살표 방향·굵기·대비를 더 선명하게 | open | matrix path 복원 다이어그램 |
| 2 | L05 `figures/05-dynamic-programming/11-matrix-representative-cell.svg` | 그림 | 화살표는 잘 보이나 "chosen" 레이블이 불명확 | chosen 표시(위치/대비/연결선)를 더 명확하게 | open | 화살표 자체는 OK |
| 3 | L09 `figures/09-string-matching/03-numeric-encoding-cad-step2.svg|내용|"원본의 28은 계산 오류" 문구 노출|삭제 — cad=53만 남김|방침확정|[방침] "원본 대비 교정" 노출 전반에 적용. 정독하며 같은 유형(L09 0-based, L10 pick/AP/C구현 "원본 교정", 기타)을 이 아래에 계속 수집|
|4| L02 Part B 01-call-stack-push.svg|그림|Push 최종만 / Pop 단계별 불일치|Push도 단계별(step1~5 신규)|작업 큼: 새 SVG 5개 / ANIMATION_AUDIT.md 참조|
|11|L03 트레이스 그림 8개(bubble/insertion/quick-partition/heapify/build-heap/heapsort/counting-sort/radix-trace)|그림(애니메이션 붕괴)|`FIGURE_CONFIG`에 `mode: sequence`가 없어 원본 여러 프레임이 최종 상태 SVG 1장으로만 컴파일됨(SVG 자체가 1장뿐, qmd 문제 아님)|`mode: sequence` 추가 후 재추출, tabset으로 삽입|open|L02 push(4번)와 동일 원인. 상세는 ANIMATION_AUDIT.md §L03 참조|
|12|L03/L04/L06 시퀀스 그림 8개(selection-trace/merge-pointers/fixed-pivot-trace/randomized-trace/median-of-medians-trace/tree-terminology-trace/insert-trace/degenerate-bst-trace)|그림(애니메이션 붕괴)|스텝 SVG는 전부 생성돼 있으나 qmd에 처음+마지막 2장만 나란히 삽입되고 중간 프레임 누락|나머지 스텝을 tabset으로 복원|done|L06 순회(9번)와 동일 패턴(프레임 뭉침). 8개 전부 단계별 tabset으로 복원 완료(원본 콜아웃/테이블 텍스트를 각 step 캡션으로 재배치). 상세는 ANIMATION_AUDIT.md 참조|
|13|L07/L09/L10 시퀀스 그림 42개(3개 챕터의 시퀀스 그림 전체)|그림(애니메이션 붕괴)|스텝 SVG는 전부 생성돼 있으나 qmd는 마지막 스텝 1장만 삽입, 나머지는 캡션 텍스트로만 서술|각 그림을 tabset으로 복원|open|이번 감사에서 발견된 가장 큰 규모의 패턴 — 챕터 단위 변환 컨벤션 차이로 추정. 상세는 ANIMATION_AUDIT.md 참조|
|14|L07 `26-logical-vs-probing-load-step2.svg`|내용|캡션·fig-alt가 "logical load와 probing load를 나란히 보여주는 게이지"라고 서술하지만 실제 삽입된 step2.svg는 probing gauge 단독 렌더링(logical gauge는 이미지에 없음)|캡션을 실제 이미지 내용에 맞게 수정하거나 두 게이지를 한 그림에 모아 재추출|open|13번과 같은 근본 원인(step1 누락)에서 파생된 캡션-이미지 불일치. ANIMATION_AUDIT.md §L07 참조|
<!--
새 항목 추가 예시 (이 주석은 지우지 말 것):
| 4 | L?? `파일 또는 챕터·줄` | 그림/내용/표현/코드 | 무엇이 문제인지 | 어떻게 됐으면 하는지(비워도 됨) | open | 참고 메모 |
| 5 | L04 Part D "구현" 문단| 내용 | 구현 문단이 코드 첫 함수 _insertion_sort의 역할을 언급 안 해, 개념 설명과 코드가 어긋나 보임|구현 문단에 "각 5-원소 그룹 median을 insertion sort로 뽑으며, 그룹이 상수 크기(5)라 O(1)" 한 문장 추가|Open | 버그 아님, 설명 보강. 값·코드는 정확|
|6| L06 Part D "Java 구현 노트"	표현|표현|size·height 정의가 한 줄에 나란히 있어 우변이 길어져 목차와 겹침(가로 넘침)|두 정의를 별도 display 수식으로 분리|height의 base case h(NIL)=-1은 height 줄에 유지| Open| |
|7|L06 SUCCESSOR 절 그림+캡션|	그림+내용(오류)| (a) 원본은 트리 1개인데 변환 시 3-4 서브트리가 6의 왼쪽에 통합 안 되고 오른쪽에 별도 그림으로 분리됨 (b) succ(6)=7 값 오류|(a) 3-4를 6의 왼쪽 서브트리로 통합해 트리 1개로 복원 (b) succ(6)=15로 교정	변환 오류.|Open| TikZ 소스에서 트리 구조 복원(texlive). 통합 후 succ 값 전체 재검산|
|8|L06 Part G TreeInsert 의사코드 7행|	표현|	return DUPLICATE의 DUPLICATE만 폰트가 다름(다른 sentinel/반환값과 불일치)|	다른 의사코드의 sentinel 반환값(NIL, NOT_FOUND 등)과 같은 폰트로 통일|Open|pseudocode.js 소스에서 \text{}/\texttt{} 감싸기 방식 불일치 추정. 전 챕터 sentinel 리터럴 폰트 일관성 점검|
|9|	L06 순회 Preorder·Inorder·Postorder 그림|	그림(애니메이션 붕괴)|	원본은 방문 순서 애니메이션(A→A,B→...)인데, 변환에서 프레임들이 좌우로 뭉친 정적 그림이 됨. "두 벌 복제"로 보였던 게 실은 프레임 붕괴|	Pop처럼 단계별 tabset으로 복원(방문 순서대로, 현재 강조+방문완료 회색+visited 누적)|done|	L02 push(4번)와 같은 카테고리: Beamer 오버레이 애니메이션→tabset 변환 실패. Pop/Level-order queue는 성공. 파이프라인 불일치. ANIMATION_AUDIT.md 참조 — preorder/inorder/postorder 전부 단계별 tabset(visited 누적 캡션)으로 복원 완료|
|10|	L06 14-search-trace-step*.svg|	그림(애니메이션 붕괴)|	원본은 step1~4 검색 애니메이션인데 웹북엔 step1·step4만 있고 step2·step3 누락. + 왼쪽 상단 주석 폰트도 작음|	누락된 step2·step3 복원해 4단계 tabset으로. 주석 폰트도 키움|open|9번·4번과 같은 애니메이션 붕괴. 정독으로 못 잡는 유형(누락 프레임). → 애니메이션 변환 감사 필요. ANIMATION_AUDIT.md 참조 — 4단계 tabset 복원 완료(step2·3 원본 콜아웃 텍스트로 캡션 작성). 단 "왼쪽 상단 주석 폰트가 작다"는 별도 지적은 이번에 다루지 않음 — 여전히 open|
-->

## 처리 이력

batch로 처리한 항목은 여기에 커밋 해시와 함께 기록한다(추적용).

| 처리일 | 대상 항목(#) | 커밋 | 비고 |
|---|---|---|---|
| — | — | — | 아직 없음 |
