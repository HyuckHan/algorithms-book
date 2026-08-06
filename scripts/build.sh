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

run_if_exists scripts/extract_tikz.py --all        # TikZ/pgfplots → SVG (캐시), 10개 lecture 전부
run_if_exists scripts/convert_pseudocode.py --all  # algorithmic → pseudocode.js, 10개 lecture 전부
run_if_exists scripts/run_examples.py --all        # C/Java/Python 실행 출력 캡처, 10개 lecture 전부
quarto render                                      # 웹북 빌드
