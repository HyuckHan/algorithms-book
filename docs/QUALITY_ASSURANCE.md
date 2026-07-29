# QUALITY_ASSURANCE

## 1. 품질 6차원

1. 알고리즘·수학적 정확성  2. 교육적 완결성  3. 코드 실행 가능성
4. 웹 기능·접근성  5. 성능·호환성  6. 회귀 안정성

## 2. 챕터 완료 품질 게이트 (전부 통과해야 status를 올림 · CI 자동)

1. **원시 수식 미노출** — 렌더 HTML 텍스트에 `$$`·`\Theta`·`\log_`·`\frac` 등이 보이지 않음.
2. **그림 개수 일치** — 소스의 TikZ/pgfplots 개수 == 삽입 SVG 개수. 깨진 `<img>` 0. 모든 그림에 `fig-alt`.
3. **의사코드 개수·렌더** — 소스 `algorithmic` 개수 == pseudocode.js/SVG 블록 개수. 줄바꿈·들여쓰기 정상.
4. **코드 3버전 빌드/실행** — 의사코드가 있는 알고리즘은 C/Java/Python 3언어 코드 블록이 모두
   존재하고(렌더된 페이지에 빈 코드블록·빈 탭이 없어야 함 — §ADR-004, `include="path"` 코드펜스
   attribute는 실제로 동작하지 않으니 주의), 세 언어 모두 컴파일·실행되며(C `gcc -Wall` 무경고,
   Java `javac` 성공, Python 실행 성공), **같은 알고리즘의 세 언어 출력이 일치**해야 한다.
5. **반응형** — 가로 스크롤 0(긴 코드는 블록 내부만). 링크 깨짐 0. 콘솔 에러 0.
6. **접근성** — 본문 텍스트 대비 ≥ 4.5:1(AlgoOrange를 텍스트로 쓰지 않았는지 검사), 표 header 존재, 색 외 상태 구분.
7. **정확성 보존** — content map 교정 항목이 되돌려지지 않음(§PER_LECTURE_NOTES 대조).

1·2·3·5·6은 헤드리스(Playwright 등) `scripts/qa_check.py`로 검사. 4는 두 도구로 나눠 검사한다 —
"3언어 코드 블록이 모두 존재(빈 코드블록 아님)"는 `scripts/qa_check.py`(렌더된 페이지의 DOM을 읽어
확인), "컴파일·실행·출력 일치"는 `scripts/run_examples.py`. 7은 리뷰 체크리스트로 검사.

## 3. 검사 도구

- **빌드/링크**: `quarto render` 성공, 내부 링크 검사, frontmatter 스키마 검증.
- **코드**: 3언어 코드 블록 존재(빈 블록 아님) 확인, 컴파일·실행·3언어 출력 diff.
- **웹/접근성**: Playwright 스모크(내비·모바일·오버플로), axe(선택), 대비 계산.
- **성능**: Lighthouse CI(Perf/A11y/BP/SEO 90+ 목표) — M5.
- **회귀**: 핵심 페이지 스냅샷(선택), SVG 캐시 해시로 그림 변경 추적.

## 4. 정확성 검증(수동, review→verified 전)

- 복잡도에 조건·비용모델 병기(과장 없는가).
- 의사코드·예제·코드 출력 상호 일치.
- indexing convention 일관.
- content map 교정 반영(§CONTENT_MODEL 10 체크리스트).

## 5. 브라우저 지원

최신 2개 major의 Chrome·Edge·Firefox·Safari. `prefers-reduced-motion` 존중, 키보드 조작 가능, focus 표시 유지.

## 6. 실패를 숨기지 않는다

에이전트는 통과하지 않은 검사를 통과했다고 보고하지 않는다. 환경 부재로 검사 불가 시(예: 로컬에
metropolis 테마 없음) 그 사실을 정확히 보고하고 status를 올리지 않는다.
