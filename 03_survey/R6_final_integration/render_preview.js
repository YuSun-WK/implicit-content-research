/* Render the integrated manuscript with its seven tables and five SVG figures. */
const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const { marked } = require("marked");
const { chromium } = require("playwright");
const { PDFDocument } = require("pdf-lib");

const out = __dirname;
const draftDir = path.join(out, "..", "R5_full_draft");
const manuscript = fs.readFileSync(path.join(draftDir, "Survey_Full_Draft.md"), "utf8");
const figureCount = (manuscript.match(/!\[[^\]]+\]\(figures\/F[1-5]\.svg\)/g) || []).length;
if (figureCount !== 5) throw new Error(`Expected 5 figure embeds; got ${figureCount}`);

const rewritten = manuscript.replace(/\]\((figures\/F[1-5]\.svg|tables\/T[1-7]_[^)]+\.md|references\.bib|Citation_Key_Mapping\.md|Bibliography_Conflicts\.md|R5C_Integration_Audit\.md)\)/g,
  (_, target) => `]\(../R5_full_draft/${target})`);
let tableAppendix = "\n\n# 附表 T1–T7（排版核验）\n\n";
for (let i = 1; i <= 7; i++) {
  const name = fs.readdirSync(path.join(draftDir, "tables")).find(x => x.startsWith(`T${i}_`));
  if (!name) throw new Error(`Missing T${i}`);
  tableAppendix += `\n\n## 附表 T${i}｜${name.slice(3, -3).replaceAll("_", " ")}\n\n`;
  tableAppendix += fs.readFileSync(path.join(draftDir, "tables", name), "utf8") + "\n";
}
const content = marked.parse(rewritten + tableAppendix, { gfm: true });
const html = `<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>广义隐晦信息综述｜R6最终整合预览</title>
<style>
@page { size: A4; margin: 17mm 15mm 18mm; }
* { box-sizing: border-box; }
html { color: #17212c; background: #f2f5f8; }
body { max-width: 980px; margin: 0 auto; padding: 32px 48px; background: white;
  font: 15px/1.72 "Microsoft YaHei", "Noto Sans CJK SC", "SimSun", sans-serif; }
h1 { color: #143954; font-size: 25px; line-height: 1.38; margin: 1.5em 0 .6em; break-after: avoid; }
h1:first-child { margin-top: 0; }
h2 { color: #1d506a; font-size: 19px; margin: 1.4em 0 .55em; break-after: avoid; }
h3 { color: #28556b; font-size: 16px; break-after: avoid; }
p { margin: .65em 0; orphans: 3; widows: 3; }
blockquote { margin: .7em 0 1.2em; padding: .35em .9em; border-left: 3px solid #4e8297; background: #edf5f8; }
a { color: #125e8b; text-decoration: none; overflow-wrap: anywhere; }
img { display: block; max-width: 100%; max-height: 182mm; width: auto; height: auto;
  object-fit: contain; margin: 15px auto; break-inside: avoid; }
table { border-collapse: collapse; width: 100%; table-layout: fixed; margin: 14px 0 22px;
  font-size: 10.2px; line-height: 1.38; break-inside: auto; }
th, td { border: 1px solid #b7c7d0; padding: 5px 6px; vertical-align: top; overflow-wrap: anywhere; }
th { background: #e5f0f5; font-weight: 700; }
tr { break-inside: avoid; }
code, pre { font: 10.5px/1.45 Consolas, monospace; overflow-wrap: anywhere; white-space: pre-wrap; }
pre { padding: 10px; background: #f3f6f8; border: 1px solid #dbe3e8; }
li { margin: .3em 0; }
@media print {
  html { background: white; }
  body { width: auto; max-width: none; padding: 0; margin: 0; font-size: 10.7pt; line-height: 1.56; }
  h1 { font-size: 16pt; } h2 { font-size: 13pt; } h3 { font-size: 11pt; }
  table { font-size: 7.5pt; line-height: 1.3; margin: 8pt 0 12pt; }
  th, td { padding: 3pt 3.5pt; }
  a { color: inherit; }
}
</style></head><body>
${content}
</body></html>`;
const htmlPath = path.join(out, "R6_Final_Preview.html");
const pdfPath = path.join(out, "R6_Final_Preview.pdf");
fs.writeFileSync(htmlPath, html, "utf8");

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", args: ["--disable-gpu"] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 768 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  const layout = await page.evaluate(() => {
    const images = [...document.images].map(x => ({ src: x.getAttribute("src"), loaded: x.complete && x.naturalWidth > 0, width: x.naturalWidth, height: x.naturalHeight }));
    const tables = [...document.querySelectorAll("table")].map(x => ({ rows: x.rows.length, width: Math.round(x.getBoundingClientRect().width), scrollWidth: x.scrollWidth, clientWidth: x.clientWidth }));
    const overflowing = [...document.querySelectorAll("body *")].filter(x => x.scrollWidth > x.clientWidth + 3 && !["PRE", "CODE"].includes(x.tagName)).slice(0, 20).map(x => x.tagName + ":" + x.className);
    return { images, tableCount: tables.length, tables, overflowing, bodyScrollWidth: document.body.scrollWidth, bodyClientWidth: document.body.clientWidth };
  });
  if (layout.images.length !== 5 || layout.images.some(x => !x.loaded)) throw new Error("SVG load failure: " + JSON.stringify(layout.images));
  if (layout.tableCount < 9) throw new Error("Tables missing in preview: " + layout.tableCount);
  if (layout.overflowing.length || layout.bodyScrollWidth > layout.bodyClientWidth + 3) throw new Error("Page overflow: " + JSON.stringify(layout.overflowing));
  await page.emulateMedia({ media: "print" });
  const printOverflow = await page.evaluate(() => [...document.querySelectorAll("table, img, pre")]
    .filter(x => x.scrollWidth > x.clientWidth + 3).map(x => x.tagName));
  if (printOverflow.length) throw new Error("Print overflow: " + JSON.stringify(printOverflow));
  if (process.env.R6_SCREENSHOTS) {
    await page.locator("img").first().screenshot({ path: path.join(out, ".qa_F1.png") });
    await page.locator("table").last().screenshot({ path: path.join(out, ".qa_T7.png") });
  }
  await page.pdf({ path: pdfPath, format: "A4", printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="font-size:8px;color:#657481;width:100%;text-align:center"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: { top: "17mm", bottom: "18mm", left: "15mm", right: "15mm" } });
  const pdf = await PDFDocument.load(fs.readFileSync(pdfPath));
  const count = pdf.getPageCount();
  if (count < 20 || count > 160) throw new Error("Unexpected page count: " + count);
  const a4 = pdf.getPages().every(p => Math.abs(p.getWidth() - 595.28) < 1 && Math.abs(p.getHeight() - 841.89) < 1);
  if (!a4) throw new Error("Non-A4 page found");
  const pdfjsPath = path.join(path.dirname(require.resolve("pdfjs-dist/package.json")), "legacy", "build", "pdf.mjs");
  const pdfjs = await import(pathToFileURL(pdfjsPath).href);
  const doc = await pdfjs.getDocument({ data: new Uint8Array(fs.readFileSync(pdfPath)), useSystemFonts: true }).promise;
  const pageText = [];
  for (let i = 1; i <= doc.numPages; i++) {
    const p = await doc.getPage(i);
    const content = await p.getTextContent();
    pageText.push(content.items.map(x => x.str || "").join(""));
  }
  if (pageText.some(x => x.trim().length < 15)) throw new Error("Blank or near-blank PDF page");
  const pdfText = pageText.join(" ");
  for (const marker of ["广义隐晦信息", "Table G4", "mao2025pragmatic", "spinoso-di-piano-etal-2025-rsa"]) {
    if (!pdfText.includes(marker)) throw new Error("PDF missing marker: " + marker);
  }
  const report = { status: "PASS", pdf_pages: count, pdf_bytes: fs.statSync(pdfPath).size, html_bytes: fs.statSync(htmlPath).size,
    svg_loaded: layout.images.length, rendered_tables: layout.tableCount, html_overflow_elements: layout.overflowing.length,
    print_overflow_elements: printOverflow.length, blank_pdf_pages: 0, all_pages_a4: a4,
    page_size: "A4", source: "Survey_Full_Draft.md + T1–T7 + F1–F5" };
  fs.writeFileSync(path.join(out, "render_validation.json"), JSON.stringify(report, null, 2) + "\n", "utf8");
  console.log(JSON.stringify(report, null, 2));
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
