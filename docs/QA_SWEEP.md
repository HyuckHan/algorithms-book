# QA_SWEEP — M5 하드닝 1차: 전체 챕터 QA 스윕 (2026-08-02)

10개 챕터(01~10) 전부가 verified 상태이나, 각각 개별 검토로 통과했을 뿐 챕터 제작 중 진화한
최신 기준으로 전체를 한꺼번에 재점검한 적은 없었다. 이 문서는 그 재점검 결과를 기록한다.
**이 스윕에서는 아무것도 수정하지 않았다** — 발견한 문제는 아래 (A)/(B)/(C) 분류로만 정리했고,
실제 수정은 M5의 별도 작업으로 남긴다.

## 1. `scripts/qa_check.py` 전체 실행 결과

`quarto render` 전체 재실행 후 `python3 scripts/qa_check.py --lecture NN`을 01~10 전부에 대해
실행했다. **10개 챕터 전부 exit 0, 모든 게이트 PASS, side-effect 정보성 경고(raw math·broken
img·missing alt·overflow·console error·failed request)도 전부 0건**이었다.

| Lecture | gate3(pseudocode count) | gate3b(raw \Call/\State 등 매크로 잔재) | 내부 문서명·production 용어 누출 | trace-step 마크업(##·multi-image) | gate6(inline code 대비) | gate6(token 대비) | gate4(빈 코드블록) | gate4(section: lang 존재·contamination 없음·compile/run·output 일치) |
|---|---|---|---|---|---|---|---|---|
| 01 | PASS (5/5) | PASS | PASS | PASS | PASS | PASS | PASS (18) | PASS (3/3 섹션) |
| 02 | PASS (0/0, 의사코드 없음) | PASS | PASS | PASS | PASS | PASS | PASS (30) | PASS (5/5 섹션) |
| 03 | PASS (12/12) | PASS | PASS | PASS | PASS | PASS | PASS (56) | PASS (7/7 섹션) |
| 04 | PASS (4/4) | PASS | PASS | PASS | PASS | PASS | PASS (24) | PASS (3/3 섹션) |
| 05 | PASS (9/9) | PASS | PASS | PASS | PASS | PASS | PASS (34) | PASS (4/4 섹션, 6/6 알고리즘) |
| 06 | PASS (12/12) | PASS | PASS | PASS | PASS | PASS | PASS (30) | PASS (5/5 섹션) |
| 07 | PASS (5/5) | PASS | PASS | PASS | PASS | PASS | PASS (20) | PASS (3/3 섹션) |
| 08 | PASS (12/12) | PASS | PASS | PASS | PASS | PASS | PASS (50) | PASS (6/6 섹션, 12/12 알고리즘) |
| 09 | PASS (6/6) | PASS | PASS | PASS | PASS | PASS | PASS (24) | PASS (4/4 섹션) |
| 10 | PASS (9/9) | PASS | PASS | PASS | PASS | PASS | PASS (38) | PASS (6/6 섹션) |

**qa_check.py 자체의 게이트 커버리지 — 누락 보고(수정하지 않음, 기록만)**

`docs/QUALITY_ASSURANCE.md` §2의 품질 게이트 1~7 기준으로 `scripts/qa_check.py`가 실제로 exit
code에 반영(hard-gate)하는 항목과 그렇지 않은 항목을 대조했다. 스크립트 자신의 모듈 docstring도
"Gates 1/2/5/7 ... NOT implemented here yet"라고 이미 명시하고 있으나, 사용자가 요청한 체크리스트
기준으로 다시 한번 정확히 표로 남긴다.

| # | QUALITY_ASSURANCE.md 게이트 | qa_check.py 구현 상태 |
|---|---|---|
| 1 | 원시 수식(raw math) 미노출 | **하드 게이트 아님.** `hasRawMath`를 계산은 하지만 `[info]`로만 출력 — 발견돼도 exit code에 영향 없음. |
| 2 | 그림 개수 일치(소스 TikZ == 삽입 SVG), 깨진 `<img>` 0, 모든 그림 fig-alt | **미구현.** 소스 `FIGURE_CONFIG`/매니페스트 개수와 렌더된 `<img>` 개수를 비교하는 코드 자체가 없다. `brokenImgs`/`missingAltImgs`는 계산되지만 `[info]`로만 출력, exit code에 영향 없음. |
| 3 | 의사코드 개수·렌더 | **하드 게이트.** `source_algorithmic_count()` vs `renderedPseudocodeCount`, 그리고 gate 3b(raw macro 잔재)까지 구현됨. |
| 4 | 코드 3버전 빌드/실행·출력 일치 | **하드 게이트.** 페이지 전체 빈 코드블록 검사 + `SECTION_GATES`로 언어 존재·contamination·compile/run·output 일치까지 구현됨. |
| 5 | 반응형(가로 overflow 0, 링크 깨짐 0, 콘솔 에러 0) | **하드 게이트 아님.** `horizontalOverflow`/`consoleErrors`/`failedRequests` 모두 계산되지만 `[info]`로만 출력. |
| 6 | 접근성(대비 ≥4.5:1, 표 header 존재, 색 외 상태 구분) | **부분 구현.** 대비(inline code + syntax-highlight token)는 하드 게이트로 구현됨. **표 header 존재 여부, 색 외 상태 구분 여부는 아예 검사 코드가 없다**(계산도, info 출력도 없음). |
| 7 | 정확성 보존(content map 교정 미회귀) | 처음부터 "리뷰 체크리스트로 검사"라고 문서화됨 — 자동화 대상이 아니며 자동 회귀 검사가 존재하지 않는다. |

이 문서가 다루는 범위는 "게이트가 이미 하드 게이트로 잡는 것"이 아니라 "게이트가 못 잡는 것"이므로,
위 표의 미구현 항목(1/2/5/6의 표 header·색 구분/7)에 해당하는 문제는 아래 §2의 수동 grep 스윕으로
별도 확인했다.

## 2. grep 스윕 요약 (게이트로 안 잡히는 항목)

### 2-1. 수식 모드 안의 `\Call` (L05 버그 패턴)

`figures/*/pseudocode-*.qmd` 전체(생성된 pseudocode.js 조각 69개 파일)에서 `\Call`이 `$...$`/
`\(...\)` 안에 남아있는지 정규식으로 재검사했다. **0건.** `hoist_call_out_of_math()`가 10개
챕터 전체에서 정상 작동하고 있음을 재확인했다(L07 5회, L09 2회, L10 1회 등 그동안 발견된 모든
인스턴스가 여전히 올바르게 hoist되어 있다).

### 2-2. 장 번호 하드코딩

`chapters/*.qmd` 본문(frontmatter 제외)에서 `숫자+장`(예: 3장, 5장) 및 `Lecture N`/`lecture N`
패턴을 전수 검색했다. **01, 04, 06, 07, 09, 10은 0건 — 클린.** 나머지 4개 챕터에서 다음이 발견됨(전부
현재 순서 기준으로는 **숫자 자체는 정확**하지만, "다른 장은 이름으로 참조" 규칙을 위반):

| 챕터 | 건수 | 위치(줄) | 내용 |
|---|---|---|---|
| 02-recursion.qmd | 3 | 310, 699, 751 | "3장(정렬)의 Merge Sort" 등 — 정렬 장을 "3장"으로 지칭 |
| 03-sorting.qmd | 1 | 491 | "Lecture 8의 Prim·Dijkstra와 Lecture 10의 A\*" — 그래프 장/상태공간 탐색 장을 영문 숫자로 지칭 |
| 05-dynamic-programming.qmd | 5 | 50, 56, 65, 87, 833 | "2장(재귀)", "3장의 분할정복" 등. 56행은 자기 자신을 가리키는 그림 캡션("Lecture 5 Road Map")이라 성격이 다름(교차 참조 아님) |
| 08-graphs.qmd | 18 | 3, 546, 693(제목), 694, 702, 1038(제목), 1039, 1041, 1122(제목), 1123, 1262(제목), 1269, 1396, 1398, 1465, 1468, 1469, 1470 | "3장의 heap", "5장(동적 계획법)", "10장의 A\*" 등 — 정렬/DP/상태공간 탐색 장을 숫자로 반복 지칭. frontmatter `description:` 필드에도 포함(3행) |

08-graphs.qmd가 압도적으로 많다 — MIGRATION_STRATEGY 우선순위상 L08은 5번째로 변환되어(L03→L01→
L02→L05→**L08**→L04→L06→L07→L09→L10), "다른 장은 이름으로 참조" 규칙이 이후 L06/L07 즈음 더
엄격히 굳어지기 전에 작성된 것으로 보인다. 이 규칙이 나중에 확립된 chapter 04/06/07/09/10에는
위반 사례가 전혀 없다는 점이 이 해석을 뒷받침한다.

### 2-3. 내부 문서명·제작 용어 누출 (raw qmd 소스 재검사)

렌더된 페이지 텍스트가 아니라 **raw .qmd 소스**에서 이미지 경로(`![...]`)·include 셔트코드·코드펜스를
제외한 순수 프로즈만 추출해 `SPEC.md`/`PER_LECTURE_NOTES`/`CODE_INVENTORY`/`content_map`/`.inventory`
및 `TikZ`/`SVG`/`pgfplots`/`dvisvgm`/`lualatex`/`tikzpicture`/`\only`/`\visible`/`\alt<`/
`pseudocode.js`/`beamer`를 grep했다. **10개 챕터 전부 0건** — 게이트 결과(내부 문서명/production
jargon PASS)와 일치하며, 소스 수준에서도 누출이 없음을 재확인했다.

### 2-4. 실행 결과 출력의 시점 혼란

`figures/*/out-*.txt` 전체(2줄 이상인 파일 전부, 약 90개)를 육안 검토했다. **모호한 사례 0건.**
L06 B-Tree의 `delete size: 0`(이미 수정됨), L07 open-addressing의 policy-dependent 값(이미
의도적으로 출력에서 제외됨) 등 과거에 발견된 패턴이 재발하지 않았고, 이후 L08~L10에서도 모든
다중 라인 출력이 각 값을 구분하는 명시적 레이블(`bfs order:`/`dfs discover:`, `dijkstra dist:`/
`bellman-ford dist:`, `size after remove:` 등)을 갖추고 있다.

### 2-5. 챕터 간 예고-회수(bridge) 정합성

`title="다리: ..."` 콜아웃 11건 전체를 찾아 각각의 주장 대상 장을 실제로 열어 대조했다.

| # | 위치 | 주장 | 대조 결과 |
|---|---|---|---|
| 1 | 03-sorting.qmd:490 | "Lecture 8의 Prim·Dijkstra와 Lecture 10의 A\*가 이 min-PQ를 다시 쓴다" | 내용은 정확(L08·L10 둘 다 실제로 재사용). §2-2의 장 번호 하드코딩과 동일 인스턴스. |
| 2 | 02-recursion.qmd:309 | "3장(정렬)의 Merge Sort가 Case 2" | L03 Merge Sort가 실제로 $T(n)=2T(n/2)+\Theta(n)$, Case 2, $\Theta(n\log n)$로 서술됨 — 내용 정확, 번호만 하드코딩. |
| 3 | 04-selection.qmd:76 | "정렬 장의 partition을 그대로 쓴다" | L03 Quick Sort가 partition 후 양쪽 재귀함을 확인 — 정확, 이름 참조로 이미 준수. |
| 4 | 04-selection.qmd:198 | "재귀 장의 재귀식 분석 도구를 다시 쓴다" | L02에 반복대치·재귀 트리 도구가 실제로 존재 — 정확. |
| 5 | 06-search-trees.qmd:116 | "정렬 장의 heap array representation" | L03에 $parent(i)=\lfloor i/2\rfloor$ 1-based array 표현이 실제로 존재 — 정확. |
| 6 | 06-search-trees.qmd:387 | "재귀 장에서 다룬 'worst-case를 만드는 입력' 논증과 같은 방식" | **약한 불일치 가능성.** L02에서 "특정 입력 순서가 재귀를 최악으로 만든다"는 논증의 명확한 대응 사례를 찾지 못했다(L02의 worst 언급은 이진 탐색의 $\Theta(\log n)$ 상한, 미로의 $O(RC)$ 등 입력 의존적 degenerate case가 아님). 이 논증 패턴은 오히려 L03의 Quick Sort 정렬된 입력 worst-case($\Theta(n^2)$, 이미 정렬/역정렬된 배열)에 더 가깝다 — 콜아웃 제목("재귀식 분석") 자체는 L02 소재가 맞지만, 본문의 구체적 비유 대상은 재확인이 필요하다. |
| 7 | 07-hash-tables.qmd:60 | "검색 트리 장의 dynamic set 비교" | L06 Part E에 hash table 행을 포함한 비교표가 실제로 존재 — 정확. |
| 8 | 07-hash-tables.qmd:145 | "선택 장의 RandomizedSelect처럼 expected는 probability model이 필요" | L04가 실제로 "평균 입력이 아니라 알고리즘 내부 무작위성에 대한 기대값"이라고 서술 — 정확. |
| 9 | 09-string-matching.qmd:212 | "해시 테이블 장의 Horner 다항식 해시" | L07에 동일한 `hash = hash*B + code(c)` Horner 식이 실제로 존재 — 정확. |
| 10 | 10-state-space-search.qmd:428 | "동적 계획법 장의 DP 테이블" | L05가 실제로 겹치는 부분 문제 재사용(memoization/tabulation) 개념을 다룸 — 정확. |
| 11 | 10-state-space-search.qmd:620 | "그래프 장의 heap과 Dijkstra" | L08이 실제로 3장(정렬)의 heap을 재사용한다고 서술하며 $h=0\Rightarrow$ Dijkstra 동치 서술도 L10 본문과 부합 — 정확. |

11건 중 9건은 내용도 정확하고 이름으로도 올바르게 참조했다. 2건(#1, #2)은 내용은 정확하지만
장 번호를 하드코딩했다(§2-2와 동일 인스턴스). 1건(#6)은 콜아웃이 가리키는 구체적 논증이 실제로는
다른 장(L03)의 것일 수 있어 사람이 재확인할 가치가 있다.

## 3. 분류

### (A) 정확성/버그 — M5에서 고칠 대상

1. **장 번호 하드코딩 4건(파일)**, 총 27개 위치 — `02-recursion.qmd`(3곳), `03-sorting.qmd`
   (1곳), `05-dynamic-programming.qmd`(4곳 교차참조 + 1곳 자기참조 캡션), `08-graphs.qmd`
   (18곳, frontmatter description 포함). 전부 §2-2 표에 위치·내용 기록. 숫자 자체는 현재 순서
   기준 정확하지만 "다른 장은 이름으로 참조" 규칙 위반이며, 향후 재편성 시 stale해질 위험이 있다.
2. **06-search-trees.qmd:387의 bridge 콜아웃("재귀 장의 재귀식 분석")** — 본문이 언급하는
   "worst-case를 만드는 입력" 논증의 명확한 대응물이 L02에 없고, 오히려 L03(Quick Sort의
   정렬된 입력 worst-case)에 더 가깝다. 사람이 재확인 후 콜아웃 대상 또는 서술을 조정해야 할
   수 있다.
3. **`scripts/qa_check.py`의 게이트 커버리지 공백** — §1의 표에서 정리한 대로 QUALITY_ASSURANCE.md
   게이트 1(원시 수식)·2(그림 개수/broken img/fig-alt)·5(overflow/console/link)가 하드 게이트로
   구현되어 있지 않고(정보성 출력만 존재하거나 아예 미구현), 게이트 6의 "표 header 존재"·"색 외
   상태 구분"도 전혀 검사되지 않는다. **이번 스윕에서 실제로 이 문제가 발생한 챕터는 0건(모든
   info 출력이 비어 있었다)이지만, 게이트 자체가 없어 향후 회귀를 못 잡을 위험**이 있다. 게이트
   추가는 이 작업의 범위 밖이며 별도 작업으로 남긴다.

### (B) 그림 크기 — 기존 `docs/FIGURE_SIZING.md`로

이번 스윕에서는 그림 크기를 새로 측정하지 않았다. L06~L10은 이미 각 챕터 변환 시점에
`docs/FIGURE_SIZING.md`에 배율표가 기록되어 있다(L06/L07/L09/L10 섹션 존재, M5에서 일괄 처리
예정). 중복 기록하지 않는다.

### (C) 개선 여지(비버그, 참고용)

- 05-dynamic-programming.qmd:56의 "Lecture 5 Road Map" 캡션은 교차 참조가 아니라 자기 챕터를
  가리키는 그림 제목이라 §(A)의 심각도는 아니지만, 다른 챕터들이 그림 캡션에 장 번호를 넣지 않는
  것과 일관성이 떨어진다 — 표현만 다듬으면 되는 수준.
- 이번 스윕으로 확인된 "브리지 11건 중 9건 정확"이라는 높은 정합률은 이 프로젝트의 다리 콜아웃
  관행이 대체로 잘 지켜지고 있음을 보여준다 — M5 수정은 §(A)의 소수 항목에 집중하면 될 것으로
  보인다.
