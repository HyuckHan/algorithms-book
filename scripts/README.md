# scripts/ (SPEC 4장 파이프라인 — 로컬 툴체인에서 구현·검증)

- extract_tikz.py       : sections/*.tex의 tikzpicture·pgfplots 블록 → standalone 컴파일 → dvisvgm → figures/NN/tikz-<sha1>.svg (해시 캐시). \only 오버레이는 최종상태 평탄화, 일부는 단계 시퀀스.
- convert_pseudocode.py : algorithmic 블록 → pseudocode.js 스니펫 (손 타이핑 금지). 실패 블록만 SVG 폴백.
- run_examples.py       : C/Java/Python 실제 컴파일·실행 → stdout 캡처 → figures/NN/out-<lang>.txt, 3언어 출력 일치 검증.
- build.sh              : extract_tikz → convert_pseudocode → run_examples → quarto render 순서 오케스트레이션.

주의: 이 디렉터리는 사양(SPEC)에 따른 구현 대상이다. 강의노트가 실제로 빌드되는 환경
(metropolis 테마·Noto Sans CJK KR·dvisvgm)에서 만들고 검증할 것.
