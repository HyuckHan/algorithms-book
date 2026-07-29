# CONTENT_MODEL

Beamer 강의자료를 웹 교재용 **`.qmd`**로 변환할 때의 구조·메타데이터·표기·컴포넌트 규약.

## 1. 콘텐츠 계층

```
Course → Lecture → Chapter/Page → Section → Learning object
```
- **Lecture**: `lecture01`–`lecture10`에 대응.
- **Chapter/Page**: 독립 URL 학습 단위. 한 페이지는 5–15분 분량 기본. 긴 강의는 파트로 분할.
- **Learning object**: 정의·예제·의사코드·추적·퀴즈·시각화.

## 2. 필수 frontmatter (qmd)

```yaml
---
title: "Merge Sort"
description: "정렬된 두 절반을 선형 시간에 합쳐 Θ(n log n)에 도달한다."
lecture: 3
part: 3
order: 7
slug: "merge-sort"
status: "draft"            # draft → review → verified → published
objectives:
  - "분할 정복으로 정렬을 설계한다."
  - "Merge의 선형 시간 결합을 추적한다."
  - "재귀 트리와 Master Theorem로 Θ(n log n)을 유도한다."
prerequisites: ["배열", "재귀", "점화식"]
keywords: ["merge sort", "병합 정렬", "divide and conquer", "stable"]
source:
  lecture: "lecture03"
  content_map: "lecture-notes/docs/lecture03_content_map.md"
  sections: ["lecture-notes/lecture03/sections/07_merge_sort.tex"]
last_verified: "2026-07-28"
---
```

### status 값
`draft`(초안) → `review`(검토 대기) → `verified`(기술·교육 검토 완료) → `published`(공개).
**에이전트는 검증 증거 없이 verified/published로 올리지 않는다.**

## 3. 표준 페이지 구조 (알고리즘 페이지)

모든 요소가 필수는 아니지만 알고리즘 페이지는 동일 흐름을 지향한다:

```
## 🎯 학습목표        (frontmatter objectives에서 자동 표기 가능)
## 문제              입력·출력·전제·실패정책·indexing
## 핵심 아이디어
## 의사코드           pseudocode.js (소스 자동변환)
## 실행 추적          단계 SVG 시퀀스 또는 표
## 왜 맞는가          정확성: intuition | proof-sketch | formal
## 복잡도             조건·비용모델 병기
## 구현              C/Java/Python 탭
## 흔한 실수          content map 교정 항목 연계
## 확인 문제          Checkpoint
## 요약
```

## 4. 알고리즘 설명 템플릿

- **문제 계약**: 입력·출력·전제·실패/예외 정책·indexing convention 명시.
- **의사코드**: content map convention 준수. 언어 문법보다 구조 우선. 변수 역할을 본문 설명.
  loop 범위·종료조건 생략 금지. `NOT_FOUND/NIL/∞` sentinel 의미 정의. **소스에서 자동 변환**(손 타이핑 금지).
- **실행 추적**: 입력·tie-breaking 고정으로 재현 가능. 변하는 상태만 강조. 각 단계가 어느 코드/규칙에
  대응하는지 표시. 최종 결과뿐 아니라 중간 invariant 노출.
- **정확성**: `intuition`/`proof-sketch`/`formal` 중 표기. 도구: loop invariant, 귀납, 구조적 귀납,
  교환 논증, cut/cycle property, optimal substructure, contradiction.
- **복잡도**: 조건·비용모델 필수 병기. 나쁜 예 "Hash search is O(1)." / 좋은 예 "적절한 해시와 통제된
  load factor 가정 시 기대 O(1), 최악 O(n)." 상한 `O`, 하한 `Ω`, tight `Θ`. average/expected/amortized 구분.
  그래프는 표현·자료구조 명시.

## 5. 코드 규칙 (3버전)

- canonical은 `lecture-notes/code/NN/{java,c}`에서 가져온다. Python은 신규 작성(같은 알고리즘·같은 예제 입력).
- 웹에는 파일 **주입**(`include=`)으로 노출. HTML에 코드를 박지 않는다.
- 코드블록에 언어·파일명 표시. 복잡 예제는 실행 명령·예상 결과 제공.
- C/Java의 indexing·API 차이는 본문 명시. 컴파일 안 되는 의사코드를 실제 코드처럼 표시 금지.
- **세 언어의 예제 출력 일치**를 CI에서 검증(§QUALITY_ASSURANCE).

## 6. 수식 규칙

- MathJax(또는 KaTeX) 지원 LaTeX. 기호는 첫 등장 시 정의. 수식만으로 설명하지 않고 문장으로 연결.
- 모바일에서 긴 수식이 깨지지 않게 줄바꿈/블록 고려. **화면에 원시 `$$`·`\Theta`가 노출되면 실패**(품질 게이트).

## 7. 교육 컴포넌트 규약 (Quarto callout/shortcode로 구현)

MDX React 컴포넌트 대신 **Quarto callout과 커스텀 shortcode**로 표현한다(정적·접근성 우수).

| 개념 | 구현 |
|---|---|
| 학습목표 | frontmatter + 페이지 상단 목록 |
| Definition | `::: {.callout-note title="정의"}` |
| Invariant | `::: {.callout-tip title="Loop invariant"}` |
| Mission/Takeaway | 강의노트 `\mission`/`\takeaway`에서 추출 → callout |
| ComplexityTable | 마크다운 표 |
| CommonMistake | `::: {.callout-warning title="흔한 실수"}` — content map 교정 항목 연계 |
| Checkpoint | `::: {.callout-caution collapse="true" title="확인 문제"}` (정답 접힘) |
| Exercise/Solution | shortcode; Solution 기본 접힘. 난이도(basic/intermediate/advanced)·유형(trace/impl/proof/comparison/counterexample) |

남발 금지: Definition은 새 용어 첫 정의에만. Checkpoint는 1–3문항 회상. Solution은 정답보다 논리 설명.

## 8. 용어·언어

본문 한국어 기본. 핵심 전문용어는 첫 등장 시 영문 병기, 이후 한 표기로 일관. 표준 용어는 영문 유지.
동일 개념에 여러 번역어 금지.

## 9. 접근성 작성 규칙

그림에 의미 있는 대체텍스트(`fig-alt`). 색만으로 상태 구분 금지(모양/라벨 병행). 표에 header.
링크 텍스트는 목적 설명. 수식·시각화 핵심 의미를 본문에도 서술. 자동재생 애니메이션 금지.

## 10. 콘텐츠 리뷰 체크리스트 (status를 review→verified로 올리기 전)

- [ ] 학습목표가 관찰 가능한 행동으로 작성됨
- [ ] 입력·출력·전제 명확
- [ ] indexing convention 일관
- [ ] 예제와 의사코드 결과 일치
- [ ] 정확성 설명이 과장되지 않음
- [ ] 복잡도에 조건·비용모델 있음
- [ ] 코드가 실제로 컴파일/실행됨(3버전 출력 일치)
- [ ] 경계·실패 사례 포함
- [ ] content map 교정 사항 반영(§PER_LECTURE_NOTES)
- [ ] 모바일·접근성 통과
