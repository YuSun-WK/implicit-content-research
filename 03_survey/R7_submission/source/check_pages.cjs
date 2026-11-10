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
    const text = execFileSync('pdftotext', ['-f', String(i + 1), '-l', String(i + 1), input, '-'], { encoding: 'utf8' });
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
  const book = await PDFDocument.create();
  const ordered = [...selected].sort((a, b) => a - b);
  for (const page of await book.copyPages(pdf, ordered)) book.addPage(page);
  fs.writeFileSync(output, await book.save());
  console.log(`${pages.length} total pages; ${ordered.length} figure/table check pages: ${ordered.map(i => i + 1).join(', ')}`);
})().catch(error => { console.error(error); process.exitCode = 1; });
