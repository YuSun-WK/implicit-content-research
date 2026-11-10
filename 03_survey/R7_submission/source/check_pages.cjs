/* Extract the figure/table pages from the formal PDF; requires poppler-utils. */
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { PDFDocument } = require('pdf-lib');

(async () => {
  const root = path.resolve(__dirname, '..');
  const input = path.join(root, 'Survey_Final_Review.pdf');
  const output = path.join(root, 'Figure_Table_Check_Pages.pdf');
  const pdf = await PDFDocument.load(fs.readFileSync(input));
  const selected = new Set();
  const allText = [];
  const pages = pdf.getPages();
  for (let i = 0; i < pages.length; i++) {
    const text = execFileSync('pdftotext', ['-layout', '-f', String(i + 1), '-l', String(i + 1), input, '-'], { encoding: 'utf8' });
    allText.push(text);
    if ([1, 2, 3, 4, 5].some(n => text.includes(`图${n}｜`))) selected.add(i);
    if ([1, 2, 3, 4, 5, 6, 7].some(n => text.includes(`表${n}｜`))) {
      selected.add(i);
      if (i + 1 < pages.length) selected.add(i + 1);
    }
    if (pages[i].getWidth() > pages[i].getHeight()) selected.add(i);
  }
  const combined = allText.join('\n');
  for (let n = 1; n <= 9; n++) if (!combined.includes(`${n} `)) throw Error(`Missing chapter ${n}`);
  for (let n = 1; n <= 5; n++) if (!combined.includes(`图${n}｜`)) throw Error(`Missing figure ${n}`);
  for (let n = 1; n <= 7; n++) if (!combined.includes(`表${n}｜`)) throw Error(`Missing table ${n}`);
  if (!combined.includes('附录A') || !combined.includes('附录B') || !combined.includes('参考文献')) throw Error('Missing back matter');
  if (/\\(?:mathrm|varnothing|mid)\b|<math/.test(combined)) throw Error('Unrendered mathematical markup');
  if (allText.some(text => text.trim().length < 100)) throw Error('Blank or near-blank page');
  const referenceStart = allText.map((text, i) => /^\s*参考文献\s*$/m.test(text) ? i : -1).filter(i => i >= 0).at(-1);
  if (referenceStart === undefined || referenceStart < pages.length - 10) throw Error('Could not locate final reference heading');
  const referenceText = allText.slice(referenceStart).join('\n');
  const labels = [...referenceText.matchAll(/^\s*\[(\d{1,2})\]/gm)].map(match => Number(match[1]));
  if (labels.length !== 50 || labels.some((number, i) => number !== i + 1)) {
    throw Error('PDF reference labels must occur exactly once in order [1]–[50]; found: ' + labels.join(', '));
  }
  const first = referenceStart + 1;
  const last = pages.length;
  const middle = Math.floor((first + last) / 2);
  const shots = path.join(root, 'reference_page_screenshots');
  fs.mkdirSync(shots, { recursive: true });
  for (const [name, number] of [['First', first], ['Middle', middle], ['Last', last]]) {
    execFileSync('pdftoppm', ['-f', String(number), '-l', String(number), '-singlefile', '-r', '180', '-png', input,
      path.join(shots, `References_${name}_Page`)]);
  }
  fs.writeFileSync(path.join(root, 'R7_Reference_Numbering_QA.md'),
    `# R7 正式 PDF 参考文献编号复核\n\nCI 对实际生成的 ${pages.length} 页 PDF 逐页提取文本。参考文献从第 ${first} 页开始，到第 ${last} 页结束。文末编号 [1]–[50] 按顺序各出现一次；书目 HTML 按原 50 个引文键映射编号。\n\n实际 PDF 页面以 180 dpi 渲染：首 ${first} 页、中 ${middle} 页、尾 ${last} 页，见 \`reference_page_screenshots/\`。这些截图仅用于本次编号复核。\n`, 'utf8');
  console.log(`PDF reference labels PASS: [1]–[50] exactly once, in order, pages ${first}–${last}; screenshots ${first}, ${middle}, ${last}`);
  const book = await PDFDocument.create();
  const ordered = [...selected].sort((a, b) => a - b);
  for (const page of await book.copyPages(pdf, ordered)) book.addPage(page);
  fs.writeFileSync(output, await book.save());
  console.log(`${pages.length} total pages; ${ordered.length} figure/table check pages: ${ordered.map(i => i + 1).join(', ')}`);
})().catch(error => { console.error(error); process.exitCode = 1; });
