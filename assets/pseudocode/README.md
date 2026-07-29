pseudocode.js 2.4.1 (MIT, SaswatPadhi/pseudocode.js), vendored from the npm
tarball's `build/pseudocode.min.js` / `build/pseudocode.min.css` (SPEC 4.3,
network-independent). `LICENSE` is the upstream license.

The vendored CSS had its `@import url(.../katex.min.css)` line removed: this
project renders pseudocode.js math via the site-wide MathJax setup (already
configured in `_quarto.yml`/`assets/mathjax-macros.html`), not KaTeX, so that
import was an unused external network dependency.

convert_pseudocode.py wraps each `algorithmic` block from the lecture notes
into a `<pre class="pseudocode" data-line-number="true">...</pre>` element;
`assets/pseudocode/pseudocode-init.html` (included via `_quarto.yml`'s
`include-in-header`) calls `pseudocode.renderClass("pseudocode")` on
`DOMContentLoaded`, mirroring the library's own documented MathJax v3
integration (verified against its actual parser source and a Node smoke test
during M1 — see the L03 pseudocode conversion commit).
