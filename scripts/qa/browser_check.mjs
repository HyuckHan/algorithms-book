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
// from "3 languages present in *this* algorithm's section".
const SECTION_CHECKS = [{ id: "selection-sort", languages: ["python", "java", "c"] }];

const url = process.argv[2];
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

const consoleErrors = [];
page.on("console", (msg) => { if (msg.type() === "error") consoleErrors.push(msg.text()); });
page.on("pageerror", (err) => consoleErrors.push(String(err)));
const failedRequests = [];
page.on("response", (res) => { if (res.status() >= 400) failedRequests.push(res.url() + " :: HTTP " + res.status()); });

await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
// Pseudocode rendering races MathJax readiness against an 8s hard timeout
// (see assets/pseudocode/pseudocode-init.html); wait past that plus margin.
await page.waitForTimeout(9000);

const domFacts = await page.evaluate((sectionChecks) => {
  const bodyText = document.body.innerText;
  const hasRawMath = /\$\$|\\Theta|\\Omega|\\log_|\\frac/.test(bodyText);

  const renderedPseudocodeCount = document.querySelectorAll(".ps-root").length;
  const unrenderedPseudocodeCount = document.querySelectorAll("pre.pseudocode").length;

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
    renderedPseudocodeCount,
    unrenderedPseudocodeCount,
    totalImgs: imgs.length,
    brokenImgs,
    missingAltImgs,
    inlineCode,
    codeBlocks,
    codeTokens,
    sectionFacts,
    horizontalOverflow: scrollWidth > clientWidth + 2,
  };
}, SECTION_CHECKS);

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
  renderedPseudocodeCount: domFacts.renderedPseudocodeCount,
  unrenderedPseudocodeCount: domFacts.unrenderedPseudocodeCount,
  totalImgs: domFacts.totalImgs,
  brokenImgs: domFacts.brokenImgs,
  missingAltImgs: domFacts.missingAltImgs,
  horizontalOverflow: domFacts.horizontalOverflow,
  inlineCodeSamples: uniqueInlineCode,
  codeBlocks: domFacts.codeBlocks,
  codeTokenSamples: uniqueTokens,
  sectionFacts: domFacts.sectionFacts,
}, null, 2));

await browser.close();
