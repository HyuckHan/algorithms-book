# algorithms-book · 제작 사양서 (SPEC)

이 문서는 `HyuckHan/AlgorithmLectureNotes`의 Beamer 강의노트를 **Quarto 웹북**으로
변환·배포하기 위한 **마스터 기술 사양**이다. 저장소 구조·툴체인·변환 파이프라인·품질 게이트·배포를 규정한다.

> **동반 문서(하이브리드 세트):** 이 SPEC은 기술 사양의 진실의 원천이고, 아래가 이를 보완한다.
> `AGENTS.md`(진입점) · `docs/PRODUCT_VISION.md` · `docs/ARCHITECTURE.md` · `docs/CONTENT_MODEL.md`(status 워크플로) ·
> `docs/MIGRATION_STRATEGY.md` · `docs/PER_LECTURE_NOTES.md`(강의별 교정) · `docs/AGENT_WORKFLOW.md` ·
> `docs/MILESTONES.md` · `docs/QUALITY_ASSURANCE.md` · `docs/DECISIONS.md`(ADR). 충돌 시 SPEC과 DECISIONS가 우선한다.

> 이 사양은 로컬 툴체인이 없는 환경에서 작성되었다. Quarto·TeX·dvisvgm이 실제로 설치된
> 로컬(또는 CI)에서 **반드시 렌더 검증**하며 진행한다. "검증되지 않은 산출물을 완성으로 간주하지 않는다."

---

## 0. 한눈에 보는 결정 사항

| 항목 | 결정 |
|---|---|
| 산출물 | Quarto **book** 프로젝트 (HTML 우선, PDF 병행 출력) |
| 저장소 | 신규 **분리** 저장소 `algorithms-book` (Public) |
| 소스 연결 | 강의노트를 **git submodule**로 포함 (`lecture-notes/`) |
| 톤 | **엄밀 유지** (강의노트의 정확성 보존 + 실행 가능한 코드/연습 추가) |
| 언어 | 본문 한국어, 코드/용어 원문 유지 |
| 수식 | LaTeX 그대로 → Quarto MathJax (프로토타입의 MathML 프리렌더 방식도 허용) |
| 의사코드(75개) | 소스(`algorithmic`) → **pseudocode.js** 자동 변환 (실패 시 SVG 폴백) |
| 다이어그램(TikZ 211개, pgfplots 9개) | **standalone 컴파일 → dvisvgm → SVG**, 해시 캐시 |
| 코드 3버전 | C / Java / Python **탭(panel-tabset)**, 실제 소스파일 주입 + CI 검증 |
| 배포 | GitHub Actions → **GitHub Pages** (+ PDF 아티팩트) |

핵심 원칙 세 가지:
1. **손으로 다시 타이핑하지 않는다.** 의사코드·수식·코드·다이어그램은 모두 소스에서 자동 생성한다.
   (프로토타입에서 의사코드를 손으로 HTML에 넣어 줄바꿈이 깨진 문제를 반복하지 않는다.)
2. **출력을 위조하지 않는다.** 코드 실행 결과는 빌드 시점에 실제 실행해 삽입한다.
3. **소스가 진실의 원천이다.** 강의노트가 갱신되면 submodule 포인터만 올려 따라간다.

---

## 1. 소스 인벤토리 (2025 기준, 변할 수 있으니 빌드 시 재확인)

강의 10개. 제목과 규모:

| # | 제목 | 섹션 | TikZ | 의사코드 | pgfplots | Java | C |
|---|---|---|---|---|---|---|---|
| 01 | 알고리즘 입문 · Introduction to Algorithms | 12 | 13 | 5 | 6 | 0 | 0 |
| 02 | 재귀 · Recursion | 13 | 14 | 0 | 0 | 0 | 0 |
| 03 | 정렬 · Sorting | 19 | 18 | 12 | 0 | 1 | 1 |
| 04 | 선택과 순서통계량 · Selection | 15 | 14 | 5 | 0 | 1 | 2 |
| 05 | 동적 계획법 · Dynamic Programming | 12 | 16 | 9 | 0 | 4 | 4 |
| 06 | 검색 트리 · Search Trees | 14 | **55** | 12 | 0 | 6 | 0 |
| 07 | 해시 테이블 · Hash Tables | 17 | 23 | 5 | 3 | 5 | 2 |
| 08 | 그래프 알고리즘 · Graph Algorithms | 18 | 22 | 12 | 0 | 8 | 7 |
| 09 | 문자열 매칭 · String Matching | 20 | 18 | 6 | 0 | 3 | 3 |
| 10 | 상태공간 트리 탐색 · State-Space Tree Search | 16 | 18 | 9 | 0 | 9 | 6 |

**합계: TikZ 211, 의사코드 75, pgfplots 9.** 다이어그램 변환이 가장 큰 작업이며 L06(트리)에 집중돼 있다.

소스 배치:
- `lectureNN/lectureNN.tex` — 메인. `\input{lectureNN/sections/*.tex}` 순서가 곧 챕터 내 절 순서.
- `lectureNN/sections/*.tex` — 실제 내용(frame, tikzpicture, algorithmic).
- `common/*.tex` — 토픽별 공유 매크로/스타일 + `common/pedagogy.tex`(교육 장치, `\algofont` 등).
- `theme/beamerthemealgorithms.sty` — 색·폰트·metropolis 테마.
- `code/lectureNN/{java,c}/` — 참조 구현. **Python은 아직 없음 → 신규 작성 대상.**

테마 색(웹에서 그대로 재사용, 접근성 검증 완료):
```
AlgoBlue #102A43   AlgoBlueTwo #243B53   AlgoLight #F5F7FA   AlgoRule #D9E2EC
AlgoOrange #F08C46 (채우기·강조 배경 전용, 텍스트로 쓰면 대비 2.46:1 → 금지)
AlgoOrangeText #B45309 (강조 텍스트, 5.02:1)   AlgoGrayText #586F86 (보조 텍스트, 5.21:1)
```
웹 본문 강조 텍스트/링크는 **AlgoOrangeText**를 쓴다(AlgoOrange를 텍스트에 쓰지 말 것).

---

## 2. 저장소 구조 & submodule 설정

로컬에서 `algorithms-book`을 clone한 뒤 첫 작업:

```bash
# 강의노트를 소스로 submodule 연결 (경로: lecture-notes/)
git submodule add https://github.com/HyuckHan/AlgorithmLectureNotes.git lecture-notes
git submodule update --init --recursive
```

목표 디렉터리 레이아웃:

```
algorithms-book/
├── SPEC.md                     ← 이 문서
├── _quarto.yml                 ← Quarto book 프로젝트 설정
├── index.qmd                   ← 표지/서문
├── chapters/
│   ├── 01-introduction.qmd
│   ├── 02-recursion.qmd
│   ├── 03-sorting.qmd          ← 파일럿
│   └── … 10-state-space.qmd
├── code/                       ← 3버전 코드(주입 대상)
│   └── 03-sorting/
│       ├── python/sorting.py   ← 신규 작성
│       ├── java/…              ← lecture-notes/code에서 복사 or 심볼릭
│       └── c/…
├── figures/                    ← 자동 생성 SVG (git 커밋; 재현 스크립트 포함)
│   └── 03-sorting/tikz-<hash>.svg …
├── scripts/
│   ├── extract_tikz.py         ← TikZ/pgfplots → SVG 파이프라인
│   ├── convert_pseudocode.py   ← algorithmic → pseudocode.js
│   ├── run_examples.py         ← 코드 실행 결과 캡처
│   └── build.sh                ← 전체 빌드 오케스트레이션
├── assets/
│   ├── theme.scss              ← AlgoBlue/AlgoOrangeText 등 팔레트
│   └── pseudocode/             ← pseudocode.js + css (vendored)
├── lecture-notes/              ← git submodule (읽기 전용 소스)
├── .github/workflows/deploy.yml
├── .gitignore                  ← _book/, .quarto/, /tmp
└── README.md
```

`.gitignore` 최소 항목: `_book/`, `.quarto/`, `figures/.cache/`, `*.aux *.log`.

---

## 3. 툴체인 사전 점검 (첫 단계에서 반드시 확인)

```bash
quarto --version           # >= 1.4
tlmgr --version || which lualatex xelatex   # TeX Live: metropolis 테마·kotex 필요
dvisvgm --version          # TikZ→SVG
python3 --version          # >= 3.10
node --version             # (선택) pseudocode.js 사전변환용
```

부족한 것:
- **metropolis 테마·Noto Sans CJK KR 폰트**가 없으면 standalone TikZ 컴파일이 실패한다.
  강의노트가 실제로 빌드되는 환경을 그대로 쓰는 것이 가장 안전하다(`make -C lecture-notes lectureNN`가 성공하는 환경).
- TeX Live full 또는 최소한 `beamertheme-metropolis`, `kotex`, `pgfplots`, `algorithmicx`, `dvisvgm`.

---

## 4. 변환 파이프라인 (아티팩트별)

### 4.1 챕터 골격 (section → qmd)

각 강의 `lectureNN.tex`의 `\input{...sections/XX_*.tex}` **순서를 그대로** 챕터 절 순서로 삼는다.
Beamer의 frame 단위는 웹에서 의미 없으므로, `\section{...}`을 H2로, frame 제목을 H3로 승격한다.
각 챕터는 아래 교육 스캐폴드를 따른다(강의노트의 mission/invariant/takeaway 매크로에서 자동 추출):

```
# {제목}
## 🎯 미션            ← \mission{...}
## {개념 절}          ← frame들. 아이디어 → 불변식(\begin{block}{... invariant}) → 그림
### 의사코드           ← algorithmic → pseudocode.js
### 복잡도             ← 수식 그대로
### 구현 (C/Java/Python) ← panel-tabset
## 💡 배움 포인트       ← \takeaway/\sortingtakeaway 등 집계
## 🧪 직접 해보기       ← 신규 작성(강의 Quiz/Checkpoint 기반)
```

### 4.2 수식

LaTeX 그대로 Quarto에 넘긴다(`$...$`, `$$...$$`). 강의별 매크로(`\Oh \Om \Th`)는
`_quarto.yml`의 `include-in-header`에 MathJax 매크로로 1회 정의한다:
```
\newcommand{\Oh}{\mathcal O} \newcommand{\Om}{\Omega} \newcommand{\Th}{\Theta}
```
대안: 프로토타입처럼 KaTeX로 **빌드 시 MathML 프리렌더**(네트워크 비의존). 어느 쪽이든
"화면에 원시 `$$`·`\Theta`가 노출되지 않는다"를 품질 게이트로 검증한다(§7).

### 4.3 의사코드 (75개) — 손 타이핑 금지

**기본 경로: pseudocode.js.** 강의노트가 `algpseudocode` 문법으로 작성돼 있어 대부분 그대로 매핑된다.
`scripts/convert_pseudocode.py`가 각 `\begin{algorithmic}...\end{algorithmic}` 블록을 추출해
pseudocode.js가 먹는 `\begin{algorithmic}` 스니펫으로 감싸고, 해당 위치에 삽입한다.
- 매핑 확인 필요 토큰: `\Procedure/\EndProcedure`, `\State`, `\If/\ElsIf/\Else/\EndIf`,
  `\For/\ForAll/\EndFor`, `\While/\EndWhile`, `\Return`, `\Call`, `\gets(←)`, `\textproc`(볼드).
- `\algfont` 등 크기 매크로는 무시(웹은 반응형).
- pseudocode.js 애셋은 `assets/pseudocode/`에 vendoring(네트워크 비의존).

**폴백(문법이 안 맞는 소수 블록): SVG.** §4.4의 standalone 파이프라인으로 그 블록만 이미지화.
파일럿(L03)에서 12개 블록 전부 pseudocode.js로 렌더되는지 먼저 확인하고 전체 확대한다.

### 4.4 다이어그램 (TikZ 211 + pgfplots 9) — 가장 큰 작업

**방식: standalone 컴파일 → dvisvgm → SVG, 콘텐츠 해시로 캐시.** `scripts/extract_tikz.py`:

1. 각 `sections/*.tex`에서 `\begin{tikzpicture}...\end{tikzpicture}`,
   `\begin{axis}...\end{axis}`(pgfplots) 블록을 순서대로 추출.
2. 블록마다 standalone 문서를 생성. **강의노트와 동일한 프리앰블**을 재사용해야
   색·좌표·스타일이 슬라이드와 일치한다:
   ```latex
   \documentclass[border=2pt]{standalone}
   \usepackage{theme/beamerthemealgorithms}   % 색/스타일 (또는 색 정의만 발췌)
   \input{common/pedagogy.tex}
   \usepackage{kotex,amsmath,amssymb,mathtools,tikz,pgfplots}
   \usetikzlibrary{arrows.meta,positioning,calc,fit,trees,patterns,decorations.pathreplacing,matrix}
   \input{lectureNN/common.tex}     % 강의별 tikz 스타일(sort cell, tree node 등)
   \pgfplotsset{compat=1.18}
   \begin{document} <블록> \end{document}
   ```
   컴파일 엔진은 강의노트와 동일하게(lualatex/xelatex). 폰트(Noto Sans CJK KR) 필요.
3. `dvisvgm --pdf --font-format=woff --output=figures/NN/tikz-<hash>.svg`로 SVG 생성.
   `<hash>`는 블록 텍스트의 SHA1 → 내용이 안 바뀌면 재컴파일 생략(캐시).
4. qmd의 원래 위치에 `![](../figures/NN/tikz-<hash>.svg){fig-alt="..."}`로 삽입.

**오버레이(`\only<...>`, `\visible<...>`, `handout:N`) 처리:**
- 기본: **최종 상태로 평탄화**한다. `\only<k>`가 여러 개면 마지막(또는 `handout:1`로 표시된) 상태만 남기고
  standalone에서 `\only`를 `\ifnum` 없이 "최종만 출력"하도록 전처리한다.
- 단계 학습이 중요한 그림(정렬 pass, merge 진행, 재귀 트리 등)은 **단계별 SVG 시퀀스**로 뽑아
  세로로 나열하거나 간단한 좌우 슬라이더로 제공(프로토타입의 "pass 사다리"가 이 평탄화의 예).
- 어떤 그림을 시퀀스로 만들지는 챕터 저자 판단. 파일럿에서 정렬 3종·merge를 시퀀스로 시범.

**주의:** L06은 TikZ 55개로 가장 무겁다. 캐시와 병렬 컴파일(`scripts` 내 멀티프로세스)로 빌드시간 관리.

### 4.5 코드 3버전 (C / Java / Python)

- **Java·C:** `lecture-notes/code/lectureNN/{java,c}/`에 이미 존재 → `code/NN-*/`로 복사(또는 빌드 시 참조).
  전량은 아니고 챕터가 다루는 핵심 알고리즘에 해당하는 파일만 노출.
- **Python:** **신규 작성.** `code/NN-*/python/`에 Java/C와 **동일한 알고리즘·동일한 예제 입력**으로 작성.
- 웹 표기는 panel-tabset:
  ````
  ::: {.panel-tabset}
  ## Python
  ```{.python include="../code/03-sorting/python/sorting.py"}
  ```
  ## Java
  ```{.java include="../code/03-sorting/java/FruitSorting.java"}
  ```
  ## C
  ```{.c include="../code/03-sorting/c/qsort_examples.c"}
  ```
  :::
  ````
  `include=`로 **파일에서 주입**한다(HTML에 코드를 박지 않는다).
- **실행 결과 삽입:** `scripts/run_examples.py`가 세 언어를 실제 컴파일·실행(`gcc`, `javac/java`, `python3`)해
  stdout을 `figures/NN/out-<lang>.txt`로 저장 → qmd에 include. **세 언어 출력이 일치**하는지 CI에서 대조.
  (Quarto의 코드셀 실행 기능을 Python에 직접 써도 되지만, 3언어 일관성을 위해 스크립트 캡처를 권장.)
- (선택) Python은 **Pyodide**로 브라우저 내 실행 위젯을 붙일 수 있음. C/Java는 참조·대조용.

---

## 5. `_quarto.yml` (초안 — 로컬에서 검증·조정)

```yaml
project:
  type: book
  output-dir: _book
book:
  title: "알고리즘 · Algorithms"
  author: "Hyuck Han"
  chapters:
    - index.qmd
    - chapters/01-introduction.qmd
    - chapters/02-recursion.qmd
    - chapters/03-sorting.qmd
    - chapters/04-selection.qmd
    - chapters/05-dynamic-programming.qmd
    - chapters/06-search-trees.qmd
    - chapters/07-hash-tables.qmd
    - chapters/08-graphs.qmd
    - chapters/09-string-matching.qmd
    - chapters/10-state-space.qmd
  search: true
  repo-url: https://github.com/HyuckHan/algorithms-book
  page-navigation: true
format:
  html:
    theme: [cosmo, assets/theme.scss]
    toc: true
    code-copy: true
    include-in-header: assets/mathjax-macros.html   # \Oh \Om \Th
    css: assets/pseudocode/pseudocode.css
  pdf:
    documentclass: scrreport
    include-in-header: assets/pdf-preamble.tex       # kotex 등
lang: ko
```

`assets/theme.scss`에 팔레트 반영:
```scss
$primary: #102A43;          // AlgoBlue
$link-color: #B45309;       // AlgoOrangeText (대비 통과)
/* 강조/콜아웃 배경에만 #F08C46 사용, 텍스트엔 금지 */
```

---

## 6. GitHub Actions 배포 (초안)

`.github/workflows/deploy.yml` 요지 (로컬 검증 후 확정):
1. `actions/checkout` **with submodules: recursive**
2. TeX Live 설치(metropolis, kotex, pgfplots, algorithmicx) + `dvisvgm` + Noto Sans CJK KR 폰트
3. JDK, GCC, Python 설치
4. `quarto` 설치
5. `bash scripts/build.sh` — TikZ 추출 → 의사코드 변환 → 코드 실행 캡처 → `quarto render`
6. HTML을 **GitHub Pages**로 배포(`actions/deploy-pages`), PDF는 아티팩트로 업로드
- 캐시: `figures/` SVG 캐시와 TeX 패키지 캐시로 빌드시간 단축.
- `main` push 시 자동 실행.

Pages URL: `https://hyuckhan.github.io/algorithms-book/`

---

## 7. 품질 게이트 (챕터별 완료 기준 · CI 자동)

한 챕터는 아래를 **모두** 통과해야 완료로 본다:
1. **원시 수식 미노출**: 렌더된 HTML 텍스트에 `$$`·`\Theta`·`\log_`·`\frac` 등이 보이지 않음.
2. **모든 그림 존재**: 소스의 TikZ/pgfplots 개수 == 챕터에 삽입된 SVG 개수. 깨진 `<img>` 0.
3. **의사코드 렌더**: 소스 `algorithmic` 개수 == pseudocode.js(또는 SVG) 블록 개수. 줄바꿈·들여쓰기 정상.
4. **코드 3버전 빌드/실행**: C `gcc -Wall` 무경고 컴파일, Java `javac` 컴파일, Python 실행 성공.
   세 언어의 예제 stdout 일치.
5. **가로 스크롤 0**(반응형), 링크 깨짐 0, 콘솔 에러 0.
6. **접근성**: 본문 텍스트 대비 ≥ 4.5:1(AlgoOrange를 텍스트로 쓰지 않았는지 검사), 모든 `img`에 `fig-alt`.
헤드리스(Playwright 등)로 1·2·3·5·6을, 빌드 스크립트로 4를 검사한다.

---

## 8. 마일스톤

1. **M0 · 부트스트랩**: submodule 연결, 툴체인 점검, `_quarto.yml`·스크립트 골격, `quarto render` 빈 책 성공, Pages 배포 파이프라인 통과(빈 페이지라도).
2. **M1 · 파일럿(L03 정렬)**: TikZ 18개 SVG화, 의사코드 12개 pseudocode.js화, C/Java/Python 탭 + 실제 출력, 품질 게이트 전부 통과. **여기서 파이프라인을 확정**한다.
3. **M2 · 수평 확대**: 파일럿에서 검증된 파이프라인으로 L01·L02·L04·L05 변환.
4. **M3 · 고밀도 챕터**: L06(TikZ 55), L07~L10. L06에서 캐시·병렬화 튜닝.
5. **M4 · 마감**: 표지/서문, 챕터 간 개념 다리(heap↔PQ 등 — 강의노트에 이미 있는 bridge frame 활용), PDF 출력 정리, 전체 링크·접근성 감사.

각 마일스톤 종료 시 `main`에 병합 → 자동 배포로 실제 사이트 확인.

---

## 9. Claude Code 첫 세션 지시 예시

> "이 저장소를 algorithms-book Quarto 웹북으로 만든다. SPEC.md를 읽고 그대로 따르라.
> 먼저 (1) HyuckHan/AlgorithmLectureNotes를 `lecture-notes/`에 git submodule로 추가하고,
> (2) `quarto`·`lualatex`·`dvisvgm`·`javac`·`gcc`·`python3` 설치 여부를 점검해 보고하라.
> (3) 그다음 M0(빈 책 빌드+Pages 배포 파이프라인)까지 세팅하고,
> (4) M1 파일럿으로 lecture03(정렬)을 SPEC 4장 파이프라인대로 변환하라.
> 의사코드는 소스에서 pseudocode.js로 자동 변환하고(손 타이핑 금지),
> TikZ는 standalone+dvisvgm으로 SVG 추출하고, 코드 3버전은 파일 주입 + 실제 실행 출력으로 넣어라.
> 각 단계는 로컬에서 `quarto render`로 검증하고 §7 품질 게이트를 통과시킨 뒤 커밋하라."

---

## 10. 미확정/확인 필요

- **Pyodide 브라우저 실행 위젯**: Python만 인터랙티브로 붙일지(학습성↑, 복잡도↑) 여부 — M1 이후 결정.
- **단계 시퀀스 그림 범위**: 어떤 TikZ를 애니메이션 대신 단계 SVG 시퀀스로 만들지 — 파일럿에서 표본 정하고 확대.
- **PDF 범위**: 웹과 동일 콘텐츠 전량 PDF인지, 요약 PDF인지.
- **라이선스**: 교재이므로 CC BY 4.0 권장(코드 예제는 MIT 병기 가능). 저장소 생성 시 확정.
