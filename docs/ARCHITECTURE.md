# ARCHITECTURE

## 1. 저장소 구조 (분리 저장소 + submodule)

웹북은 강의노트와 **분리된** 저장소 `algorithms-book`에 둔다. 강의노트는 읽기전용 소스로
git submodule로 포함한다.

```
algorithms-book/
├── AGENTS.md                 # 에이전트 진입점
├── SPEC.md                   # 기술 사양(진실의 원천)
├── docs/                     # 거버넌스 문서(이 세트)
├── _quarto.yml               # Quarto book 프로젝트
├── index.qmd
├── chapters/03-sorting.qmd … # 강의당 1 챕터
├── code/03-sorting/{python,java,c}/   # 3버전 코드(주입 대상)
├── figures/03-sorting/*.svg  # 자동 생성 SVG(커밋; 재현 스크립트 포함)
├── scripts/                  # extract_tikz / convert_pseudocode / run_examples / build.sh
├── assets/                   # theme.scss, mathjax-macros, pseudocode.js(vendored)
├── lecture-notes/            # git submodule → HyuckHan/AlgorithmLectureNotes (읽기전용)
├── .github/workflows/deploy.yml
└── .gitignore                # _book/ .quarto/ figures/.cache/
```

submodule:
```bash
git submodule add https://github.com/HyuckHan/AlgorithmLectureNotes.git lecture-notes
git submodule update --init --recursive
```

## 2. 기술 스택 — Quarto

| 역할 | 선택 | 비고 |
|---|---|---|
| 정적 사이트/책 | **Quarto (book)** | 목차·검색·교차참조·PDF 동시출력 |
| 수식 | LaTeX → MathJax (또는 KaTeX→MathML 프리렌더) | `\Oh \Om \Th` 매크로 1회 정의 |
| 의사코드 | **pseudocode.js** (vendored) | `algorithmic` 자동 변환, 폴백 SVG |
| 다이어그램 | **standalone LaTeX → dvisvgm → SVG** | TikZ 211·pgfplots 9, 해시 캐시 |
| 코드 탭 | Quarto `panel-tabset` + `include=` | C/Java/Python, CI 실행·출력 일치 |
| 검색 | Quarto 내장(또는 Pagefind) | 정적 |
| 배포 | GitHub Actions → **GitHub Pages** | PDF는 아티팩트 |

선택 기준: 정적 생성, 서버 없이 동작, 마크다운으로 교수자 편집 가능, 코드·수식 안정 표현,
**기존 TeX/TikZ 자산(211개)을 재구현하지 않고 재사용**. React 앱을 새로 만드는 대안은
유지보수 부담과 원본 불일치 위험이 커서 채택하지 않는다(§DECISIONS ADR-001).

## 3. 콘텐츠/프레젠테이션 분리

`.qmd`는 콘텐츠 + frontmatter를 소유한다. 스타일·상호작용은 `assets/`의 SCSS/JS와
Quarto 기능(callout, panel-tabset, figure)이 소유한다. qmd 본문에 임의 HTML 스타일을
박아넣지 않는다(교육 장치는 Quarto callout/shortcode로 표현 — §CONTENT_MODEL).

## 4. URL 구조

```
/                      표지
/chapters/03-sorting   강의 챕터(강의번호로 순서 고정)
```
Quarto book은 챕터=페이지가 기본이다. 강의가 너무 길면 §CONTENT_MODEL의 5–15분 단위로
파트를 나누되, 파일럿(L03)에서 "1강=1챕터(내부 파트 분할)"가 충분한지 먼저 검증한다.

## 5. 빌드 데이터 흐름

```
lecture-notes/ (submodule, 읽기전용)
   ├─ sections/*.tex ─→ scripts/extract_tikz.py ─→ figures/NN/*.svg (해시 캐시)
   ├─ sections/*.tex ─→ scripts/convert_pseudocode.py ─→ pseudocode.js 스니펫
   ├─ code/NN/{java,c} ─┐
   └─ (신규) python/    ─┴→ scripts/run_examples.py ─→ 실제 실행 출력 캡처
                                    ↓
                         chapters/NN-*.qmd (frontmatter + 본문 + 삽입물)
                                    ↓
                              quarto render (HTML + PDF)
                                    ↓
              품질 게이트(§QUALITY_ASSURANCE) → GitHub Pages 배포
```

## 6. 시각화 정책 (SVG 우선, 선별적 인터랙티브)

기본은 **강의노트 TikZ를 dvisvgm으로 SVG 변환**(원본과 픽셀 일치). `\only<>` 오버레이는
(a) 최종 상태로 평탄화, 또는 (b) 학습상 중요한 것만 **단계별 SVG 시퀀스**로 뽑아 세로 나열/슬라이더.
인터랙티브(재생/일시정지/스텝) 위젯은 **파일럿 이후 선별 도입**하며, 없어도 핵심 상태가
이해되도록 정적 SVG를 먼저 완성한다(§DECISIONS ADR-003).

## 7. 배포

- `main` push → GitHub Actions: submodule 체크아웃(recursive) → TeX/dvisvgm/JDK/GCC/Python/Quarto 설치
  → `scripts/build.sh` → `quarto render` → Pages 배포(HTML) + PDF 아티팩트.
- PR 미리보기는 Pages 환경상 제약이 있으니, 필요 시 Netlify/Cloudflare Pages 미리보기 병용 검토.
- LaTeX 빌드(강의노트)와 웹 빌드는 완전히 독립. 웹북이 강의노트 빌드를 건드리지 않는다.

## 8. 보안/개인정보

MVP는 사용자 입력을 저장하지 않는다. 서버측 임의 코드 실행 금지(코드 실행은 빌드시 사전 생성
또는 브라우저 내 Pyodide로 제한). 외부 스크립트 최소화(pseudocode.js·KaTeX는 vendoring).
