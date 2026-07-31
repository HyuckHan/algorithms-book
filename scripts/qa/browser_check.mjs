// Headless-browser half of scripts/qa_check.py (invoked via `node`, not run
// directly). Loads a rendered chapter page and reports the DOM/CSS facts
// qa_check.py can't get from static analysis: how many pseudocode.js blocks
// actually rendered, and the contrast ratio of inline code as the browser
// actually computes it (both are still influenced by JS timing / cascaded
// CSS, so re-deriving them from source alone would not be a real check).
//
// Usage: node browser_check.mjs <url> ; prints one JSON object to stdout.
import { chromium } from "playwright";

function relativeLuminance([r, g, b]) {
  const chan = (c) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  };
  const [R, G, B] = [chan(r), chan(g), chan(b)];
  return 0.2126 * R + 0.7152 * G + 0.0722 * B;
}

function parseRgb(css) {
  const m = css.match(/rgba?\(([^)]+)\)/);
  if (!m) return null;
  const parts = m[1].split(",").map((s) => parseFloat(s.trim()));
  return parts.slice(0, 3);
}

function contrastRatio(fgCss, bgCss) {
  const fg = parseRgb(fgCss);
  const bg = parseRgb(bgCss);
  if (!fg || !bg) return null;
  const L1 = relativeLuminance(fg);
  const L2 = relativeLuminance(bg);
  const [lighter, darker] = L1 > L2 ? [L1, L2] : [L2, L1];
  return (lighter + 0.05) / (darker + 0.05);
}

// Section-scoped checks for algorithms that got their own isolated
// C/Java/Python panel-tabset (ALGORITHM_CONFIG in run_examples.py). Quarto
// wraps each heading's content in <section id="...">, so this looks up the
// section by the heading's slug id and inspects only code inside it -- a
// whole-page check can't tell "3 languages present somewhere on the page"
// from "3 languages present in *this* algorithm's section". This list is
// flat across all lectures (not scoped to whichever page is being checked);
// ids from a different lecture's page just report found:false harmlessly,
// since qa_check.py only reads the entries relevant to its --lecture arg.
const SECTION_CHECKS = [
  "selection-sort", "bubble-sort", "insertion-sort", "merge-sort",
  "quick-sort", "heapsort", "counting-sort", "radix-sort",
  // L01 introduces Linear/Binary Search early but -- matching the lecture's
  // own deferral of complexity until after asymptotic notation -- their
  // code panel-tabset lives later, under a "...의 복잡도" heading (see
  // qa_check.py's SECTION_ID mapping for the same reasoning).
  "maximum의-복잡도", "linear-search의-복잡도", "binary-search의-복잡도",
  // L02's representative algorithms (Sum, Hanoi, Recursive Binary Search,
  // Maze, Power Set) each get their own H2 Part with no further H3 split,
  // so their code panel-tabset lives directly in that Part's own section id.
  "part-b.-재귀의-실행-호출-스택", "part-g.-재귀적으로-문제-설계하기", "part-h.-hanoi",
  "part-i.-미로-탐색maze과-backtracking", "part-k.-멱집합power-set",
  // L04's SelectBySorting gets its own H3 (self-contained), while
  // Quickselect/RandomizedSelect/DeterministicSelect each get a whole H2
  // Part (see qa_check.py's SECTION_ID mapping -- ids confirmed against the
  // actually-rendered chapter, not guessed from the .qmd headings).
  "가장-단순한-해법-selectbysorting", "part-b.-quickselect",
  "part-c.-randomized-selection의-성능",
  "part-d.-deterministic-linear-selection-median-of-medians",
  // L05's four representative algorithms each get their own H3 subsection
  // (see qa_check.py's SECTION_ID mapping -- ids confirmed against the
  // actually-rendered chapter, not guessed from the .qmd headings).
  "tabulation-bottom-up", "matrix-minimum-path-sum",
  "longest-common-subsequence-lcs", "maximum-subarray-kadanes-algorithm",
  // L06's five representative algorithms each get a whole H2 Part to
  // themselves (see qa_check.py's SECTION_ID mapping -- ids confirmed
  // against the actually-rendered chapter, not guessed from the .qmd
  // headings).
  "part-c.-traversal", "part-g.-bst-insert와-delete", "part-i.-avl-tree",
  "part-j.-red-black-tree", "part-k.-b-tree",
  // L08's 12 algorithm slugs collapse into 6 sections (see qa_check.py's
  // SECTION_ID mapping -- ids confirmed against the actually-rendered
  // chapter, not guessed from the .qmd headings).
  "part-c.-bfs", "part-d.-dfs", "part-f.-topological-sort",
  "part-j.-kruskal과-disjoint-set", "part-m.-unweighteddag-shortest-paths",
  "part-o.-bellmanford-algorithm",
  // L07's 3 ALGORITHM_CONFIG entries each get a whole H2 Part to themselves
  // (see qa_check.py's SECTION_ID mapping -- ids confirmed against the
  // actually-rendered chapter, not guessed from the .qmd headings).
  "part-d.-integer와-string-hashing", "part-f.-separate-chaining",
  "part-k.-삭제와-구현",
  // L09's 4 ALGORITHM_CONFIG entries each get a whole H2 Part to themselves
  // (see qa_check.py's SECTION_ID mapping -- ids confirmed against the
  // actually-rendered chapter, not guessed from the .qmd headings).
  "part-b.-naive-matching", "part-g.-rabin-karp-분석과-활용",
  "part-l.-kmp-search", "part-p.-boyer-moore-horspool",
].map((id) => ({ id, languages: ["python", "java", "c"] }));

// Internal repo document names (SPEC.md, docs/PER_LECTURE_NOTES.md, etc.)
// must never leak into reader-facing prose -- a correction belongs in the
// chapter on its own merits, not cited back to an internal tracking doc.
// Matched against the rendered page's visible body text with word
// boundaries so e.g. "spec" as an ordinary English word wouldn't false-positive.
const INTERNAL_DOC_PATTERNS = [
  /\bSPEC\b/,
  /\bPER_LECTURE_NOTES\b/,
  /\bCODE_INVENTORY\b/,
  /\bDECISIONS\.md\b/,
  /\bMIGRATION_STRATEGY\b/,
  /\bQUALITY_ASSURANCE\b/,
  /\bCONTENT_MODEL\b/,
  /\bAGENT_WORKFLOW\b/,
  /\bAGENTS\.md\b/,
  /\bMILESTONES\.md\b/,
  // Build-pipeline/production jargon (never meaningful to a reader): this is
  // exactly the class of bug an internal "how this figure was made" note
  // is (found and removed from L05's LCS section -- a callout literally
  // said "TikZ SVG 대신 표로 직접 제시한다"). None of these terms occur
  // anywhere in L01/02/03/05's real rendered body text (checked via
  // page.evaluate(() => document.body.innerText) before adding this list),
  // so this is a zero-false-positive tripwire, not a guess.
  /\bTikZ\b/i,
  /\bSVG\b/,
  /\bpgfplots\b/i,
  /\bdvisvgm\b/i,
  /\blualatex\b/i,
  /\btikzpicture\b/i,
  /\\only\b/,
  /\\visible\b/,
  /\\alt</,
  /pseudocode\.js/i,
];

const url = process.argv[2];
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

const consoleErrors = [];
page.on("console", (msg) => { if (msg.type() === "error") consoleErrors.push(msg.text()); });
page.on("pageerror", (err) => consoleErrors.push(String(err)));
const failedRequests = [];
page.on("response", (res) => { if (res.status() >= 400) failedRequests.push(res.url() + " :: HTTP " + res.status()); });

await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
// Pseudocode rendering races MathJax readiness (8s hard cap) then a
// per-block font warm-up (15s hard cap) before rendering runs (see
// assets/pseudocode/pseudocode-init.html) -- wait past the worst case
// (8s + 15s) plus margin, not just the old single 8s cap, or this check
// can catch the page mid-render on a slow/loaded machine and undercount.
await page.waitForTimeout(25000);

const domFacts = await page.evaluate(({ sectionChecks, internalDocPatternSources }) => {
  const bodyText = document.body.innerText;
  const hasRawMath = /\$\$|\\Theta|\\Omega|\\log_|\\frac/.test(bodyText);
  const internalDocRefs = internalDocPatternSources.filter((src) => new RegExp(src).test(bodyText));

  const renderedPseudocodeCount = document.querySelectorAll(".ps-root").length;
  const unrenderedPseudocodeCount = document.querySelectorAll("pre.pseudocode").length;

  // Raw pseudocode-macro leak check: a `.ps-root` is "rendered" in the sense
  // that pseudocode.js produced *some* DOM for it (renderedPseudocodeCount
  // above counts that), but a `\Call{name}{args}` (or similarly-shaped
  // algorithmicx macro) left *inside* a `$...$`/`\(...\)` math span survives
  // convert_pseudocode.py's hoist unfixed, MathJax doesn't know the `\Call`
  // macro, and rather than throwing it typesets the literal control-word
  // text -- so the block "renders" (a .ps-root exists) but shows raw LaTeX
  // like "\Call{Partition}{A, p, r}" to the reader instead of formatted
  // pseudocode (exactly the L05 bug convert_pseudocode.py's
  // hoist_call_out_of_math was written to prevent). Gate 3 above only counts
  // *whether* a .ps-root exists, not what's inside it, so it cannot catch
  // this on its own -- scan each rendered block's own text for a literal
  // backslash-macro name that should never survive to visible output.
  const RAW_MACRO_NAMES = [
    "Call", "Procedure", "EndProcedure", "Require", "Ensure", "Input", "Output",
    "State", "Statex", "Return", "If", "ElsIf", "Else", "EndIf",
    "For", "ForAll", "EndFor", "While", "EndWhile", "gets", "Comment",
  ];
  const RAW_MACRO_RE = new RegExp("\\\\(?:" + RAW_MACRO_NAMES.join("|") + ")\\b");
  const rawPseudocodeMacroLeaks = Array.from(document.querySelectorAll(".ps-root"))
    .map((el, i) => ({ index: i, text: el.textContent }))
    .filter((r) => RAW_MACRO_RE.test(r.text))
    .map((r) => ({ index: r.index, sample: r.text.slice(0, 120) }));

  // A `## heading` immediately followed by another block (e.g. an image)
  // with no blank line between them in the .qmd source doesn't get parsed
  // as Markdown at all inside a fenced div -- it survives as literal "##
  // heading" text merged into the previous block's paragraph (observed in
  // 01-introduction.qmd's Linear/Binary Search step-sequence tabsets: only
  // step 1 became a real tab, steps 2-4 leaked in as plain text glued to
  // step 1's image). Scan visible text outside <pre>/<code> (where a
  // literal "##" could legitimately appear, e.g. a C preprocessor sample)
  // for a stray "##" as a general leaked-heading-marker tripwire, and
  // separately flag any tab-pane with more than one <img> -- a case
  // multiple step images landing in a single pane, root symptom of the
  // exact same bug.
  const bodyTextOutsideCode = Array.from(document.body.querySelectorAll("*"))
    .filter((el) => el.children.length === 0 && !el.closest("pre") && !el.closest("code"))
    .map((el) => el.textContent)
    .join(" ");
  const leakedHeadingMarkers = [...bodyTextOutsideCode.matchAll(/.{0,20}##\s?\S+.{0,20}/g)].map((m) => m[0]);
  const multiImageTabPanes = Array.from(document.querySelectorAll(".tab-pane"))
    .map((pane) => ({ id: pane.id, imgCount: pane.querySelectorAll("img").length }))
    .filter((p) => p.imgCount > 1);

  const imgs = Array.from(document.querySelectorAll("img"));
  const brokenImgs = imgs.filter((i) => i.naturalWidth === 0).map((i) => i.getAttribute("src"));
  const missingAltImgs = imgs.filter((i) => !i.getAttribute("alt")).map((i) => i.getAttribute("src"));

  const inlineCodeEls = Array.from(document.querySelectorAll("code")).filter((c) => !c.closest("pre"));
  const inlineCode = inlineCodeEls.map((el) => {
    const cs = getComputedStyle(el);
    return { text: el.textContent.slice(0, 60), color: cs.color, backgroundColor: cs.backgroundColor };
  });

  // Fenced code blocks (Quarto/Pandoc wrap each one in a div.sourceCode,
  // whether or not it's inside a panel-tabset). Use textContent, not
  // innerText: inactive (not-currently-selected) tabset panes are
  // display:none, and innerText returns "" for anything not visible, which
  // would misreport a perfectly-populated-but-inactive tab as empty.
  const codeBlocks = Array.from(document.querySelectorAll("div.sourceCode")).map((div) => {
    const codeEl = div.querySelector("code");
    const text = codeEl ? codeEl.textContent : "";
    return { id: div.id || null, lang: codeEl ? codeEl.className : null, length: text.trim().length };
  });

  // Per-token-class syntax-highlighting colors (Pandoc/Skylighting emits one
  // <span class="TOKENTYPE"> per token: "co" comment, "kw" keyword, "st"
  // string, etc.) against the code block's actual background. A dark
  // highlight-style tuned for a *different* dark background than this
  // project's $code-block-bg can still leave specific token classes
  // (observed: comments) under 4.5:1 even though most tokens are fine --
  // getComputedStyle works on display:none (inactive tabset pane) elements
  // in Chromium, since layout-independent style is still computed, so this
  // covers hidden tabs the same as visible ones.
  function effectiveBackground(el) {
    let node = el;
    while (node) {
      const bg = getComputedStyle(node).backgroundColor;
      const m = bg.match(/rgba?\(([^)]+)\)/);
      if (m) {
        const parts = m[1].split(",").map((s) => parseFloat(s));
        if (parts.length < 4 || parts[3] > 0) return bg;
      }
      node = node.parentElement;
    }
    return "rgb(255, 255, 255)";
  }
  const codeTokens = [];
  document.querySelectorAll("code.sourceCode").forEach((codeEl) => {
    const bg = effectiveBackground(codeEl);
    codeEl.querySelectorAll("span[class]").forEach((span) => {
      if (span.children.length > 0) return; // only leaf token spans
      const text = span.textContent;
      if (!text || !text.trim()) return;
      codeTokens.push({
        cls: span.className,
        color: getComputedStyle(span).color,
        backgroundColor: bg,
        sample: text.slice(0, 30),
      });
    });
  });

  const scrollWidth = document.documentElement.scrollWidth;
  const clientWidth = document.documentElement.clientWidth;

  // Per-section presence + contamination facts. textContent (not
  // innerText) is used deliberately: inactive tabset panes are display:none
  // and must still be inspected, same reasoning as codeBlocks above.
  const sectionFacts = sectionChecks.map((cfg) => {
    const section = document.getElementById(cfg.id);
    if (!section) return { id: cfg.id, found: false };
    const allCode = Array.from(section.querySelectorAll("code"));
    const fullText = allCode.map((el) => el.textContent).join("\n");
    const languages = {};
    cfg.languages.forEach((lang) => {
      const matches = allCode.filter((el) => el.classList.contains(lang));
      const text = matches.map((el) => el.textContent).join("\n");
      languages[lang] = { count: matches.length, length: text.trim().length };
    });
    return { id: cfg.id, found: true, languages, fullText };
  });

  return {
    hasRawMath,
    internalDocRefs,
    renderedPseudocodeCount,
    unrenderedPseudocodeCount,
    rawPseudocodeMacroLeaks,
    totalImgs: imgs.length,
    brokenImgs,
    missingAltImgs,
    inlineCode,
    codeBlocks,
    codeTokens,
    sectionFacts,
    leakedHeadingMarkers,
    multiImageTabPanes,
    horizontalOverflow: scrollWidth > clientWidth + 2,
  };
}, { sectionChecks: SECTION_CHECKS, internalDocPatternSources: INTERNAL_DOC_PATTERNS.map((re) => re.source) });

const inlineCodeWithContrast = domFacts.inlineCode.map((c) => ({
  ...c,
  contrast: contrastRatio(c.color, c.backgroundColor),
}));
// de-duplicate by (color,bg) pair for a compact report -- a page can have
// dozens of inline-code spans that all share the same two computed colors.
const seen = new Set();
const uniqueInlineCode = inlineCodeWithContrast.filter((c) => {
  const key = c.color + "|" + c.backgroundColor;
  if (seen.has(key)) return false;
  seen.add(key);
  return true;
});

// de-duplicate token samples by (class, color, background) -- a single code
// block repeats the same handful of token classes/colors many times.
const seenTokens = new Set();
const uniqueTokens = domFacts.codeTokens
  .map((t) => ({ ...t, contrast: contrastRatio(t.color, t.backgroundColor) }))
  .filter((t) => {
    const key = t.cls + "|" + t.color + "|" + t.backgroundColor;
    if (seenTokens.has(key)) return false;
    seenTokens.add(key);
    return true;
  });

console.log(JSON.stringify({
  url,
  consoleErrors,
  failedRequests,
  hasRawMath: domFacts.hasRawMath,
  internalDocRefs: domFacts.internalDocRefs,
  renderedPseudocodeCount: domFacts.renderedPseudocodeCount,
  unrenderedPseudocodeCount: domFacts.unrenderedPseudocodeCount,
  rawPseudocodeMacroLeaks: domFacts.rawPseudocodeMacroLeaks,
  totalImgs: domFacts.totalImgs,
  brokenImgs: domFacts.brokenImgs,
  missingAltImgs: domFacts.missingAltImgs,
  horizontalOverflow: domFacts.horizontalOverflow,
  inlineCodeSamples: uniqueInlineCode,
  codeBlocks: domFacts.codeBlocks,
  codeTokenSamples: uniqueTokens,
  sectionFacts: domFacts.sectionFacts,
  leakedHeadingMarkers: domFacts.leakedHeadingMarkers,
  multiImageTabPanes: domFacts.multiImageTabPanes,
}, null, 2));

await browser.close();
