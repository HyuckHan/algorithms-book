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

const domFacts = await page.evaluate(() => {
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

  const scrollWidth = document.documentElement.scrollWidth;
  const clientWidth = document.documentElement.clientWidth;

  return {
    hasRawMath,
    renderedPseudocodeCount,
    unrenderedPseudocodeCount,
    totalImgs: imgs.length,
    brokenImgs,
    missingAltImgs,
    inlineCode,
    codeBlocks,
    horizontalOverflow: scrollWidth > clientWidth + 2,
  };
});

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
}, null, 2));

await browser.close();
