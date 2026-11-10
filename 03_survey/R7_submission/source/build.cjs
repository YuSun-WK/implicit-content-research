/* R7 A4 academic review layout. Scientific text remains in ../R5_full_draft. */
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { execFileSync, spawnSync } = require('node:child_process');
const { marked } = require('marked');
const { chromium } = require('playwright');
const { PDFDocument, StandardFonts, rgb } = require('pdf-lib');

const root = path.resolve(__dirname, '..');
const draft = path.resolve(root, '..', 'R5_full_draft');
const mdPath = path.join(draft, 'Survey_Full_Draft.md');
const source = fs.readFileSync(mdPath, 'utf8').replace(/\r\n/g, '\n');
const tableFiles = fs.readdirSync(path.join(draft, 'tables'));
const refs = source.slice(source.indexOf('# 参考文献'));
const refsFormal = refs.replace(/^# 参考文献\n\n以下50条书目[^\n]*\n\n/, '# 参考文献\n\n')
  .replace(/\[出版入口\]\(https:\/\/doi\.org\/([^)]+)\)/g, 'DOI: $1')
  .replace(/\[出版入口\]\(([^)]+)\)/g, 'URL: $1');
const keys = [...refs.matchAll(/^\d+\. \*\*([^*]+)\*\* —/gm)].map(x => x[1]);
if (keys.length !== 50 || new Set(keys).size !== 50) throw Error('Expected 50 unique manual bibliography keys');
const numbers = new Map(keys.map((key, i) => [key, i + 1]));
function bibliographyHtml() {
  const found = spawnSync('pandoc', ['--version'], {encoding:'utf8', windowsHide:true});
  if (found.error || found.status !== 0) {
    if (process.env.REQUIRE_PANDOC === '1') throw Error('Pandoc with citeproc is required for formal bibliography build');
    console.warn('Pandoc unavailable: using the 50-entry verified R6 manual list for local preview');
    return render(refsFormal, 'refs');
  }
  const input = keys.map(key => '[@' + key + ']').join(String.fromCharCode(10, 10));
  const html = execFileSync('pandoc', ['--citeproc','--bibliography',path.join(draft,'references.bib'),
    '--csl',path.join(__dirname,'numeric.csl'),'-f','markdown','-t','html5'],{input,encoding:'utf8',windowsHide:true});
  const start = html.indexOf('<div id="refs"');
  if (start < 0) throw Error('Pandoc did not produce a bibliography');
  const rendered = html.slice(start);
  if (/csl-(?:left-margin|right-inline)/.test(rendered)) throw Error('Unexpected CSL alignment wrapper');
  const byKey = new Map();
  const entryPattern = /<div\s+id="ref-([^"]+)"\s+class="csl-entry"[^>]*>([\s\S]*?)<\/div>/g;
  for (const [, key, content] of rendered.matchAll(entryPattern)) {
    if (byKey.has(key)) throw Error('Duplicate Pandoc bibliography key: ' + key);
    byKey.set(key, content.trim());
  }
  if (byKey.size !== 50) throw Error('Pandoc bibliography has ' + byKey.size + ' entries, expected 50');
  const entries = keys.map((key, index) => {
    const content = byKey.get(key);
    if (!content) throw Error('Pandoc bibliography missing key: ' + key);
    const number = index + 1;
    return `<div id="ref-${number}" class="csl-entry"><span class="ref-number">[${number}]</span><span class="ref-content">${content}</span></div>`;
  }).join('\n');
  console.log('Pandoc citeproc bibliography: 50 entries, visibly numbered [1]–[50]');
  return '<h1>参考文献</h1><div id="refs" class="csl-bib-body">' + entries + '</div>';
}

function math(expr) {
  const t = s => '<mi>' + s + '</mi>';
  const sub = (s, v) => '<msub>' + t(s) + '<mi>' + v + '</mi></msub>';
  const map = {
    'I,T': '<mrow><mi>I</mi><mo>,</mo><mi>T</mi></mrow>',
    'C': '<mi>C</mi>',
    '\\mathrm{Task}=(X,Y,G,E)': '<mrow><mi mathvariant="normal">Task</mi><mo>=</mo><mo>(</mo>' + ['X','Y','G','E'].map(t).join('<mo>,</mo>') + '<mo>)</mo></mrow>',
    'G(I,T\\mid C)': '<mrow><mi>G</mi><mo>(</mo><mi>I</mi><mo>,</mo><mi>T</mi><mo>∣</mo><mi>C</mi><mo>)</mo></mrow>',
    'G(I,\\varnothing\\mid C)': '<mrow><mi>G</mi><mo>(</mo><mi>I</mi><mo>,</mo><mo>∅</mo><mo>∣</mo><mi>C</mi><mo>)</mo></mrow>',
    'G(\\varnothing,T\\mid C)': '<mrow><mi>G</mi><mo>(</mo><mo>∅</mo><mo>,</mo><mi>T</mi><mo>∣</mo><mi>C</mi><mo>)</mo></mrow>',
    'G_{\\rm in}': sub('G','in'),
    'P_{\\rm in}': sub('P','in'),
    'R_{\\rm beh}': sub('R','beh'),
    'Q_{\\rm out}': sub('Q','out')
  };
  const body = map[expr.trim()];
  if (!body) throw Error('Unmapped formula: ' + expr);
  return '<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline">' + body + '</math>';
}
function transform(text) {
  let s = text.replace(/\] \(figures\//g, '](figures/');
  s = s.replace(/^> R6 最终整合审阅稿.*\n\n/m, '');
  s = s.replace(/\\\((.*?)\\\)/g, (_, expr) => math(expr));
  const tokens = {
    'Task=(X,Y,G,E)': math('\\mathrm{Task}=(X,Y,G,E)'),
    'G_in': math('G_{\\rm in}'), 'P_in': math('P_{\\rm in}'),
    'R_beh': math('R_{\\rm beh}'), 'Q_out': math('Q_{\\rm out}')
  };
  for (const [plain, html] of Object.entries(tokens)) s = s.split(plain).join(html);
  s = s.replace(/\[@([^\]]+)\]/g, (all, inner) => {
    const cited = inner.split(';').map(x => x.trim().replace(/^@/, ''));
    const nums = cited.map(x => numbers.get(x));
    if (nums.some(x => !x)) throw Error('Unknown citation: ' + all);
    return '<span class="citation">' + nums.map(n => '<a href="#ref-' + n + '">[' + n + ']</a>').join('') + '</span>';
  });
  if (/\\(?:mathrm|varnothing|mid|rm)\b|\\\(|\\\)/.test(s)) throw Error('Unrendered math command');
  return s;
}
function insertTables(s) {
  for (let n = 1; n <= 6; n++) {
    const name = tableFiles.find(x => x.startsWith('T' + n + '_'));
    if (!name) throw Error('Missing T' + n);
    const lines = s.split('\n');
    const index = lines.findIndex(x => x.includes('tables/' + name));
    if (index < 0) throw Error('Table T' + n + ' is not linked in the text');
    const table = fs.readFileSync(path.join(draft, 'tables', name), 'utf8').trim()
      .replace(/^# (.*)/, '**$1**');
    lines.splice(index + 1, 0, '', '<div class="table-block" id="table-' + n + '">', '', table, '', '</div>', '');
    s = lines.join('\n');
  }
  return s;
}
function render(s, mode) {
  let html = marked.parse(transform(s), { gfm: true });
  html = html.replace(/&lt;math[\s\S]*?&lt;\/math&gt;/g, x => x.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&amp;/g, '&'));
  html = html.replace(/src="figures\//g, 'src="../R5_full_draft/figures/');
  html = html.replace(/href="tables\/T([1-7])_[^"]+\.md"/g, (_, n) => 'href="#table-' + n + '"');
  html = html.replace(/<p><img([^>]+)><\/p>\s*<p><strong>(图[1-5]｜[^<]+)<\/strong>(.*?)<\/p>/g,
    '<figure><img$1><figcaption><strong>$2</strong>$3</figcaption></figure>');
  if (mode === 'refs') {
    let i = 0;
    html = html.replace(/<li>/g, () => '<li id="ref-' + (++i) + '">');
    if (i !== 50) throw Error('Rendered bibliography has ' + i + ' entries');
    html = html.replace(/<strong>[^<]+<\/strong> — /g, '');
    html = html.replace(/Daum\{\\'e\}/g, 'Daumé');
  }
  if (html.includes('&lt;math')) throw Error('Escaped MathML remains in ' + mode);
  return html;
}
const chapter9 = source.indexOf('# 9 总结与展望');
const appendix = source.indexOf('# 附录A ');
const bibliography = source.indexOf('# 参考文献');
if (!(chapter9 > 0 && appendix > chapter9 && bibliography > appendix)) throw Error('Section anchors missing');
let bodyMd = insertTables(source.slice(0, chapter9));
const middleMd = source.slice(chapter9, appendix);
const appendixMd = source.slice(appendix, bibliography);
const t7file = tableFiles.find(x => x.startsWith('T7_'));
const t7md = fs.readFileSync(path.join(draft, 'tables', t7file), 'utf8');
const css = `
@page { size: A4; margin: 22mm 19mm 21mm 20mm; }
@page landscape { size: A4 landscape; margin: 17mm 17mm 18mm 17mm; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; color: #111; }
body { font-family: "Noto Serif CJK SC", "Source Han Serif SC", "SimSun", "Microsoft YaHei", serif; font-size: 10.5pt; line-height: 1.58; }
h1,h2,h3 { font-family: "Noto Sans CJK SC", "Source Han Sans SC", "Microsoft YaHei", sans-serif; color:#111; break-after: avoid; }
h1 { font-size: 15pt; margin: 16pt 0 9pt; }
h1:first-child { text-align:center; font-size:20pt; margin: 0 0 20pt; }
h2 { font-size: 12pt; margin: 13pt 0 6pt; }
h3 { font-size: 10.5pt; margin: 10pt 0 5pt; }
p { margin: 0 0 7pt; text-align: justify; orphans: 3; widows: 3; }
p:has(strong:first-child) { text-align:left; }
blockquote { margin: 7pt 0; padding-left: 9pt; border-left: 2pt solid #555; }
ul,ol { margin: 5pt 0 8pt; padding-left: 1.7em; }
li { margin: 2pt 0; }
a { color:#111; text-decoration:none; }
.citation { white-space:nowrap; }
math { font-family: "Cambria Math", "STIX Two Math", serif; font-size:1em; }
figure { margin: 11pt auto 14pt; break-inside: avoid; }
figure img { display:block; width:100%; max-height:125mm; object-fit:contain; }
figcaption { margin-top:5pt; font-size:9pt; line-height:1.4; text-align:justify; }
table { width:100%; border-collapse:collapse; font-size:8.3pt; line-height:1.36; margin:7pt 0 11pt; table-layout:auto; }
th,td { border-top:0.6pt solid #333; border-bottom:0.45pt solid #777; padding:3.5pt 4pt; vertical-align:top; overflow-wrap:anywhere; }
th { font-weight:700; background:#f3f3f3; }
tr { break-inside: avoid; }
.table-block > p:first-child { font-size:9pt; font-weight:700; margin-top:10pt; margin-bottom:4pt; break-after:avoid; }
.table-block > p:last-child { font-size:8pt; }
code { font-family:Consolas,monospace; font-size:8.5pt; }
pre { white-space:pre-wrap; overflow-wrap:anywhere; }
.references h1 { text-align:left!important; font-size:15pt!important; break-before:page; }
.references ol { padding-left:2em; }
.references li { padding-left:0.2em; margin-bottom:5pt; text-align:left; font-size:9pt; line-height:1.45; }
.references .csl-entry { display:flex; align-items:flex-start; margin-bottom:5pt; font-size:9pt; line-height:1.45; overflow-wrap:anywhere; break-inside:avoid; }
.references .ref-number { flex:0 0 2.8em; white-space:nowrap; }
.references .ref-content { flex:1; min-width:0; }
.landscape { page:landscape; }
.landscape h1 { text-align:left!important; font-size:14pt!important; margin:0 0 9pt; }
.landscape table { font-size:8.8pt; line-height:1.30; }
.landscape td,.landscape th { padding:3pt 5pt; }

/* R8 per-table readability and page break rules; source figures stay editable SVG. */
.table-block table { table-layout: fixed; font-size:8.6pt; line-height:1.39; }
.table-block th,.table-block td { overflow-wrap:normal; word-break:normal; hyphens:none; }
.table-block thead { display:table-header-group; }
#table-1 table { font-size:8.7pt; }
#table-2 table { font-size:8.5pt; }
#table-3 table { font-size:8.5pt; }
#table-4 table { font-size:8.8pt; }
#table-5 { break-before:page; }
#table-5 table { font-size:8.5pt; }
#table-6 { break-before:page; }
#table-6 table { font-size:8.45pt; line-height:1.40; }
#table-6 h3 { font-size:10.2pt; margin-top:9pt; }
#table-6 h3:nth-of-type(2) { break-before:page; }
.landscape table { table-layout:fixed; font-size:9.0pt; line-height:1.34; }
.landscape th,.landscape td { overflow-wrap:normal; word-break:normal; }
.table-block tr,.landscape tr { break-inside:avoid; }
.table-block th,.table-block td { padding:4.2pt 4.5pt; }
#table-1 th:nth-child(1),#table-1 td:nth-child(1) {width:12%;}
#table-1 th:nth-child(2),#table-1 td:nth-child(2) {width:16%;}
#table-1 th:nth-child(3),#table-1 td:nth-child(3) {width:25%;}
#table-1 th:nth-child(4),#table-1 td:nth-child(4) {width:23%;}
#table-1 th:nth-child(5),#table-1 td:nth-child(5) {width:24%;}
#table-2 th:nth-child(1),#table-2 td:nth-child(1) {width:13%;}
#table-2 th:nth-child(2),#table-2 td:nth-child(2) {width:20%;}
#table-2 th:nth-child(3),#table-2 td:nth-child(3) {width:28%;}
#table-2 th:nth-child(4),#table-2 td:nth-child(4) {width:17%;}
#table-2 th:nth-child(5),#table-2 td:nth-child(5) {width:22%;}
#table-3 th:nth-child(1),#table-3 td:nth-child(1) {width:18%;}
#table-3 th:nth-child(2),#table-3 td:nth-child(2) {width:27%;}
#table-3 th:nth-child(3),#table-3 td:nth-child(3) {width:28%;}
#table-3 th:nth-child(4),#table-3 td:nth-child(4) {width:27%;}
#table-4 th:nth-child(1),#table-4 td:nth-child(1) {width:17%;}
#table-4 th:nth-child(2),#table-4 td:nth-child(2) {width:25%;}
#table-4 th:nth-child(3),#table-4 td:nth-child(3) {width:28%;}
#table-4 th:nth-child(4),#table-4 td:nth-child(4) {width:30%;}
#table-5 th:nth-child(1),#table-5 td:nth-child(1) {width:18%;}
#table-5 th:nth-child(2),#table-5 td:nth-child(2) {width:26%;}
#table-5 th:nth-child(3),#table-5 td:nth-child(3) {width:27%;}
#table-5 th:nth-child(4),#table-5 td:nth-child(4) {width:29%;}
#table-6 th:nth-child(1),#table-6 td:nth-child(1) {width:18%;}
#table-6 th:nth-child(2),#table-6 td:nth-child(2) {width:28%;}
#table-6 th:nth-child(3),#table-6 td:nth-child(3) {width:27%;}
#table-6 th:nth-child(4),#table-6 td:nth-child(4) {width:27%;}
#table-7 th:nth-child(1),#table-7 td:nth-child(1) {width:16%;}
#table-7 th:nth-child(2),#table-7 td:nth-child(2) {width:25%;}
#table-7 th:nth-child(3),#table-7 td:nth-child(3) {width:27%;}
#table-7 th:nth-child(4),#table-7 td:nth-child(4) {width:32%;}
/* R8 final visual-pagination refinement: avoid orphaned table note / last reference. */
.landscape table { font-size:8.75pt; line-height:1.27; margin:5pt 0 5pt; }
.landscape th,.landscape td { padding:2.0pt 4.0pt; }
.landscape #table-7 > p:last-child { font-size:8pt; line-height:1.2; margin:3pt 0; }
.references .csl-entry { font-size:8.9pt; line-height:1.40; margin-bottom:3.5pt; }


`;
function document(html, cls='') { return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>' + css + '</style></head><body class="' + cls + '">' + html + '</body></html>'; }
const parts = [
  { name:'01-body', html:document(render(bodyMd + middleMd, 'body')) },
  { name:'02-table7', html:document('<div id="table-7">' + render(t7md, 't7') + '</div>','landscape') },
  { name:'03-back', html:document(render(appendixMd, 'appendix') + '<section class="references">' + bibliographyHtml() + '</section>') }
];
const tableCount = parts.reduce((n,p) => n + (p.html.match(/<table>/g) || []).length, 0);
const mathCount = parts.reduce((n,p) => n + (p.html.match(/<math /g) || []).length, 0);
// R8: appendix A/B now contain prose instead of two internal-audit tables.
if (tableCount < 10 || mathCount < 10) throw Error('Missing rendered tables or math: ' + tableCount + '/' + mathCount);
async function launch() {
  if (process.env.BROWSER_EXECUTABLE) return chromium.launch({headless:true,executablePath:process.env.BROWSER_EXECUTABLE});
  try { return await chromium.launch({headless:true}); }
  catch { return chromium.launch({headless:true,channel:'msedge'}); }
}
(async () => {
  const browser = await launch();
  const merged = await PDFDocument.create();
  for (const part of parts) {
    const file = path.join(root, '.' + part.name + '.html');
    fs.writeFileSync(file, part.html, 'utf8');
    const page = await browser.newPage();
    await page.goto(pathToFileURL(file).href, {waitUntil:'load'});
    await page.evaluate(() => document.fonts.ready);
    const loaded = await page.locator('img').evaluateAll(xs => xs.every(x => x.complete && x.naturalWidth > 0));
    if (!loaded) throw Error('Figure load failure in ' + part.name);
    const pdf = await page.pdf({format:'A4',landscape:part.name==='02-table7',printBackground:true,
      margin:part.name==='02-table7' ? {top:'17mm',right:'17mm',bottom:'18mm',left:'17mm'} : {top:'22mm',right:'19mm',bottom:'21mm',left:'20mm'}});
    const section = await PDFDocument.load(pdf);
    const pages = await merged.copyPages(section, section.getPageIndices());
    pages.forEach(x => merged.addPage(x));
    console.log(part.name, pages.length, 'pages');
    await page.close();
    fs.unlinkSync(file);
  }
  await browser.close();
  const font = await merged.embedFont(StandardFonts.Helvetica);
  merged.getPages().forEach((page,i) => {
    const {width} = page.getSize();
    const label = String(i+1);
    page.drawText(label,{x:(width-font.widthOfTextAtSize(label,9))/2,y:22,size:9,font,color:rgb(.15,.15,.15)});
  });
  fs.writeFileSync(path.join(root,'Survey_Final_Review.pdf'),await merged.save());
  console.log('Total',merged.getPageCount(),'pages; 5 SVG figures; 7 external tables; 50 references');
})().catch(e=>{console.error(e);process.exit(1)});
