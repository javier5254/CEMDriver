// Uso: node build_seccion7.js -> build/_tmp/seccion7.docx (secciones 7 Cronograma y 8 Presupuesto, cuerpo para injertar; no toca el Final)
// Fuente: ../secciones/07-cronograma-presupuesto.md. Datos: los de build_anexo_b.js (se verifica que la suma sea exacta).
const fs = require('fs'), path = require('path');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, AlignmentType, WidthType, ShadingType,
  BorderStyle, HeadingLevel, VerticalAlign } = D;
const ROOT = path.resolve(__dirname, '..');
const MD = fs.readFileSync(path.join(ROOT, 'secciones', '07-cronograma-presupuesto.md'), 'utf8');
const FONT = 'Arial', FW = 9360, ORANGE = 'F4A340', DARK = 'C55A11';

// ---------- inline (igual que build_seccion6.js) ----------
const base = (o = {}) => ({ font: FONT, size: 22, ...o });
function inline(text, o = {}) {
  const runs = [];
  const re = /(\[COMPLETAR:[^\]]*\])|\*\*(.+?)\*\*|\*(.+?)\*|`([^`]+)`/g;
  let last = 0, m;
  const push = (t, x = {}) => { if (t) runs.push(new TextRun(base({ ...o, ...x, text: t }))); };
  while ((m = re.exec(text))) {
    push(text.slice(last, m.index));
    if (m[1]) push(m[1], { highlight: 'yellow' });
    else if (m[2] !== undefined) runs.push(...inline(m[2], { ...o, bold: true }));
    else if (m[3] !== undefined) runs.push(...inline(m[3], { ...o, italics: true }));
    else push(m[4], { font: 'Consolas', size: (o.size || 22) - 2 });
    last = re.lastIndex;
  }
  push(text.slice(last));
  return runs;
}
const P = (text, opts = {}, o = {}) => new Paragraph({ children: inline(text, o), ...opts });

// ---------- tablas ----------
const bd = { style: BorderStyle.SINGLE, size: 4, color: '808080' };
const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const parseRows = lines => lines.filter(l => !/^\|\s*-/.test(l)).map(l => l.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim()));
const COP = n => '$' + Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
const money = s => { const m = s.replace(/\*\*/g, '').match(/^\$([\d.]+)/); return m ? Number(m[1].replace(/\./g, '')) : NaN; };

function gantt(rows) {
  const n = rows[0].length, cw = [3160, 560, 560, 560, 560, 560, 560, 840, 2000];
  if (n !== cw.length || cw.reduce((x, y) => x + y, 0) !== FW) throw new Error('columnas del Gantt');
  return new Table({ width: { size: FW, type: WidthType.DXA }, columnWidths: cw, rows: rows.map((r, ri) => new TableRow({
    tableHeader: ri === 0, cantSplit: true, children: r.map((c, i) => {
      const head = ri === 0, exec = !head && i >= 1 && i <= 6 && c === 'X';
      const fill = head ? 'D9D9D9' : exec ? ORANGE : undefined;
      return new TableCell({
        borders: { top: bd, bottom: bd, left: bd, right: bd }, width: { size: cw[i], type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
        shading: fill ? { type: ShadingType.CLEAR, color: 'auto', fill } : undefined, margins: { top: 20, bottom: 20, left: 50, right: 50 },
        children: [new Paragraph({ keepNext: ri < rows.length - 1, alignment: i >= 1 && i <= 7 ? AlignmentType.CENTER : AlignmentType.LEFT,
          spacing: { line: 240, after: 0 }, children: exec ? [] : inline(c, { size: 16, bold: head }) })],
      });
    }),
  })) });
}

function presupuesto(rows) {
  const cw = [1250, 3150, 950, 1900, 1160, 950];
  const al = [AlignmentType.LEFT, AlignmentType.LEFT, AlignmentType.CENTER, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.LEFT];
  // verificacion aritmetica
  let sub = 0, hrs = 0, nR = 0, imprev = NaN, tot = NaN;
  rows.slice(1).forEach(r => {
    const d = r[1].replace(/\*\*/g, '');
    if (/^Subtotal parcial/.test(d)) { if (money(r[4]) !== sub) throw new Error('subtotal ' + sub); return; }
    if (/^Reserva/.test(d)) { imprev = money(r[4]); if (imprev !== Math.round(sub * 0.10)) throw new Error('imprevistos no es 10 %'); return; }
    if (/^TOTAL GENERAL/.test(d)) { tot = money(r[4]); return; }
    nR++; const q = Number(r[2].match(/^(\d+)/)[1]), v = money(r[3]);
    if (/ h$/.test(r[2])) hrs += q;
    if (q * v !== money(r[4])) throw new Error('fila ' + r[1]);
    sub += money(r[4]);
  });
  if (tot !== 75000000 || sub + imprev !== tot || hrs !== 445 || nR !== 21) throw new Error(`suma incoherente ${sub} ${imprev} ${tot} ${hrs} ${nR}`);
  console.log('presupuesto ok: subtotal', COP(sub), 'imprevistos', COP(imprev), 'total', COP(tot), hrs, 'h', nR, 'rubros');
  return new Table({ width: { size: FW, type: WidthType.DXA }, columnWidths: cw, rows: rows.map((r, ri) => {
    const total = /TOTAL GENERAL/.test(r[1]);
    return new TableRow({ tableHeader: ri === 0, cantSplit: true, children: r.map((c, i) => {
      const sigVacia = ri + 1 < rows.length && rows[ri + 1][0] === '';
      const borders = { top: i === 0 && c === '' ? NONE : bd, bottom: i === 0 && sigVacia ? NONE : bd, left: bd, right: bd };
      const fill = ri === 0 ? 'D9D9D9' : total ? 'F2F2F2' : undefined;
      return new TableCell({
        borders, width: { size: cw[i], type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
        shading: fill ? { type: ShadingType.CLEAR, color: 'auto', fill } : undefined, margins: { top: 20, bottom: 20, left: 60, right: 60 },
        children: [new Paragraph({ keepNext: ri < rows.length - 1, alignment: ri === 0 ? AlignmentType.CENTER : al[i], spacing: { line: 240, after: 0 },
          children: inline(c, { size: 16, bold: ri === 0 || (i === 0 && c !== '') }) })],
      });
    }) });
  }) });
}
function mdTable(lines) {
  const rows = parseRows(lines);
  return /^Actividad/.test(rows[0][0]) ? gantt(rows) : presupuesto(rows);
}

// ---------- markdown -> docx ----------
function convert(md) {
  const out = [], L = md.split(/\r?\n/);
  let i = 0;
  while (i < L.length) {
    const l = L[i];
    if (!l.trim()) { i++; continue; }
    let m;
    if ((m = l.match(/^(#{1,3}) (.*)$/))) {
      const lv = m[1].length;
      out.push(new Paragraph({ heading: [HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3][lv - 1], keepNext: true, children: [new TextRun({ text: m[2] })] }));
      i++; continue;
    }
    if (l.startsWith('|')) { const b = []; while (i < L.length && L[i].startsWith('|')) b.push(L[i++]); out.push(mdTable(b)); continue; }
    if (/^\*\*(Tabla|Figura) \d+\*\*$/.test(l)) { out.push(P(l, { alignment: AlignmentType.LEFT, keepNext: true, spacing: { before: 120, after: 0 } })); i++; continue; }
    if (l.startsWith('*Nota.*')) { out.push(P(l, { alignment: AlignmentType.LEFT, spacing: { line: 240, before: 60, after: 140 } }, { size: 18 })); i++; continue; }
    if (/^\*[^*].*\*$/.test(l)) { out.push(P(l, { alignment: AlignmentType.LEFT, keepNext: true, spacing: { after: 60 } })); i++; continue; }
    out.push(P(l)); i++;
  }
  return out;
}

const H = (sz, extra = {}) => ({ run: { font: FONT, size: sz, bold: true, color: '000000', ...extra }, paragraph: { spacing: { before: 240, after: 120, line: 360 }, alignment: AlignmentType.LEFT } });
const doc = new Document({
  creator: 'Estudiante', title: 'Secciones 7 y 8',
  styles: {
    default: { document: { run: { font: FONT, size: 22 }, paragraph: { spacing: { line: 360, after: 0 }, alignment: AlignmentType.JUSTIFIED } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, ...H(26), paragraph: { ...H(26).paragraph, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, ...H(24), paragraph: { ...H(24).paragraph, outlineLevel: 1 } },
    ],
  },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } }, children: convert(MD) }],
});
const outF = path.join(__dirname, '_tmp', 'seccion7.docx');
Packer.toBuffer(doc).then(b => { fs.writeFileSync(outF, b); console.log('ok', outF, b.length); });
