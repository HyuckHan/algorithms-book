#!/usr/bin/env bash
# 오케스트레이션 (SPEC 4·6장). M1에서 각 파이프라인 스크립트가 추가되면 자동으로 활성화된다.
# M0(현재)는 스크립트가 아직 없으므로 건너뛰고 quarto render만 검증한다.
set -euo pipefail

run_if_exists() {
  local script="$1"
  shift
  if [ -f "$script" ]; then
    python3 "$script" "$@"
  else
    echo "skip: $script not implemented yet (see docs/MILESTONES.md)"
  fi
}

run_if_exists scripts/extract_tikz.py --all          # TikZ/pgfplots → SVG (캐시), 10개 lecture 전부
run_if_exists scripts/convert_pseudocode.py --all    # algorithmic → pseudocode.js, 10개 lecture 전부
run_if_exists scripts/run_examples.py --all          # C/Java/Python 실행 출력 캡처, 10개 lecture 전부
run_if_exists scripts/extract_code_snippets.py --all # code/의 snippet 마커 구간 → figures/*/snippet-*, 10개 lecture 전부(quarto render보다 먼저)

# 신선도 게이트: 위 네 스크립트가 실제로 산출물을 다시 써도 커밋된 내용과
# 달라지는 파일이 없어야 한다. 하나라도 달라지면 그 산출물이 소스(lecture-notes
# 서브모듈 또는 code/)보다 뒤처진 채로 커밋됐다는 뜻이다.
if [ -n "$(git status --short figures/)" ]; then
  echo "빌드 신선도 게이트 실패: figures/ 아래 다음 파일이 파이프라인 재실행으로 바뀌었습니다."
  git status --short figures/
  echo
  echo "원인: 커밋된 산출물이 소스와 어긋납니다(예: lecture-notes 서브모듈이나 code/가"
  echo "바뀐 뒤 파이프라인을 다시 돌려 커밋하지 않은 경우)."
  echo "조치: 로컬에서 위 스크립트들을 --all 로 실행하고, 그 결과(위에 나열된 파일)를 커밋하십시오."
  exit 1
fi

quarto render                                        # 웹북 빌드
