// Uso: node build_seccion6.js -> build/_tmp/seccion6.docx (SOLO la seccion 6; no toca Entrega1/2 ni el Final)
const fs = require('fs'), path = require('path');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, Header, AlignmentType,
  PageNumber, WidthType, ShadingType, BorderStyle, LevelFormat, HeadingLevel, LineRuleType } = D;
const ROOT = path.resolve(__dirname, '..');
const SEC = f => fs.readFileSync(path.join(ROOT, 'secciones', f), 'utf8');
const TITLE = 'CMEDriver: plataforma orientada a API para la gestión, trazabilidad en tiempo real y comunicación directa cliente-mensajero en servicios de mensajería en Colombia';
const FONT = 'Arial';

// ---------- inline ----------
const base = (o = {}) => ({ font: FONT, size: 22, ...o });
function inline(text, o = {}) {
  const runs = [];
  text = text.replace(/`(\[COMPLETAR[^`]*\])`/g, '$1');
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

// ---------- markdown -> docx ----------
const FW = 9360;
function pngSize(f) { const b = fs.readFileSync(f); return [b.readUInt32BE(16), b.readUInt32BE(20)]; }
function mdTable(lines) {
  const rows = lines.filter(l => !/^\|\s*-/.test(l)).map(l => l.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim()));
  const n = rows[0].length;
  const wts = rows[0].map((_, i) => Math.max(8, Math.min(40, Math.max(...rows.map(r => (r[i] || '').length)))) + 6);
  const tot = wts.reduce((a, b) => a + b, 0);
  const cw = wts.map(w => Math.floor(FW * w / tot)); cw[n - 1] += FW - cw.reduce((a, b) => a + b, 0);
  const bd = { style: BorderStyle.SINGLE, size: 4, color: '808080' }, borders = { top: bd, bottom: bd, left: bd, right: bd };
  return new Table({
    width: { size: FW, type: WidthType.DXA }, columnWidths: cw,
    rows: rows.map((r, ri) => new TableRow({ tableHeader: ri === 0, cantSplit: true, children: r.map((c, i) => new TableCell({
      borders, width: { size: cw[i], type: WidthType.DXA },
      shading: ri === 0 ? { fill: 'D9D9D9', type: ShadingType.CLEAR, color: 'auto' } : undefined,
      margins: { top: 30, bottom: 30, left: 90, right: 90 },
      children: [new Paragraph({ alignment: AlignmentType.LEFT, spacing: { line: 240, after: 0 }, children: inline(c, { size: 18, bold: ri === 0 }) })],
    })) })),
  });
}
function convert(md, opts = {}) {
  const out = [], L = md.split(/\r?\n/);
  let i = 0;
  while (i < L.length) {
    const l = L[i];
    if (!l.trim()) { i++; continue; }
    let m;
    if ((m = l.match(/^(#{1,3}) (.*)$/))) {
      const lv = m[1].length;
      out.push(new Paragraph({ heading: [HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3][lv - 1], keepNext: true,
        pageBreakBefore: lv === 1 && !opts.noBreak, children: [new TextRun({ text: m[2] })] }));
      i++; continue;
    }
    if (l.startsWith('|')) { const b = []; while (i < L.length && L[i].startsWith('|')) b.push(L[i++]); out.push(mdTable(b)); out.push(new Paragraph({ spacing: { after: 0, line: 100, lineRule: LineRuleType.EXACT }, children: [] })); continue; }
    if ((m = l.match(/^!\[(.*?)\]\((.*?)\)$/))) {
      const f = path.resolve(ROOT, 'secciones', m[2]); const [w, h] = pngSize(f); const W = Math.min(540, Math.round(283 * w / h));
      out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { line: 240 }, children: [new ImageRun({ type: 'png', data: fs.readFileSync(f), transformation: { width: W, height: Math.round(W * h / w) }, altText: { title: 'Figura', description: m[1], name: 'fig' } })] }));
      i++; continue;
    }
    if (/^(-|\d+\.) /.test(l)) {
      const ord = /^\d+\./.test(l);
      while (i < L.length && /^(-|\d+\.) /.test(L[i])) { out.push(P(L[i].replace(/^(-|\d+\.) /, ''), { numbering: { reference: ord ? 'num' : 'bul', level: 0 } })); i++; }
      continue;
    }
    if (l.startsWith('> ')) { out.push(P(l.slice(2), { indent: { left: 567, right: 567 } })); i++; continue; }
    if (/^\*\*(Tabla|Figura) \d+\*\*$/.test(l)) { out.push(P(l, { alignment: AlignmentType.LEFT, keepNext: true, spacing: { before: 120, after: 0 } })); i++; continue; }
    if (/^\*[^*].*\*$/.test(l) && !l.startsWith('*Nota')) { out.push(P(l, { alignment: AlignmentType.LEFT, keepNext: true, spacing: { after: 60 } })); i++; continue; }
    if (l.startsWith('*Nota.*')) { out.push(P(l, { alignment: AlignmentType.LEFT, spacing: { line: 240, before: 40, after: 140 } }, { size: 20 })); i++; continue; }
    out.push(P(l)); i++;
  }
  return out;
}

const body = [...convert(SEC('06-avance-resultados.md'))];
const H = (sz, extra = {}) => ({ run: { font: FONT, size: sz, bold: true, color: '000000', ...extra }, paragraph: { spacing: { before: 240, after: 120, line: 360 }, alignment: AlignmentType.LEFT } });
const pg = { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } };
const doc = new Document({
  creator: 'Estudiante', title: TITLE,
  styles: {
    default: { document: { run: { font: FONT, size: 22 }, paragraph: { spacing: { line: 360, after: 0 }, alignment: AlignmentType.JUSTIFIED } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, ...H(26), paragraph: { ...H(26).paragraph, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, ...H(24), paragraph: { ...H(24).paragraph, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, ...H(22, { italics: true }), paragraph: { ...H(22).paragraph, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [
    { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
  ] },
  sections: [
    { properties: { page: pg }, children: body },
  ],
});
const outF = path.join(__dirname, '_tmp', 'seccion6.docx');
Packer.toBuffer(doc).then(b => { fs.writeFileSync(outF, b); console.log('ok', outF, b.length); });
