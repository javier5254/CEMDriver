// Uso: node build_anexos.js  -> ../Anexos_CMEDriver.docx
const fs = require('fs'), path = require('path');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, Header, AlignmentType, PageNumber,
  WidthType, ShadingType, BorderStyle, LevelFormat, HeadingLevel, LineRuleType, PageOrientation, SectionType, TableOfContents, TableLayoutType } = D;
const ROOT = path.resolve(__dirname, '..'), ENT = path.resolve(ROOT, '..', 'docs', 'entrega'), IMG = path.join(__dirname, 'img');
const FONT = 'Arial', PROSE = 276, SINGLE = 240;
const TITLE = 'Anexos — CMEDriver: plataforma orientada a API para la gestión de servicios de mensajería';
const FENCE = '`'.repeat(3);

const SUBS = [
  { f: '01-requerimientos.md', t: 'Requerimientos', land: true },
  { f: '02-stack-tecnologico.md', t: 'Stack tecnológico' },
  { f: '03-arquitectura.md', t: 'Arquitectura' },
  { f: '04-mer.md', t: 'Modelo entidad-relación' },
  { f: '05-bpmn.md', t: 'Modelo BPMN' },
  { f: '06-c4.md', t: 'Modelo C4 (niveles 1 a 4)' },
  { f: '07-trazabilidad.md', t: 'Matriz de trazabilidad', land: true },
  { f: '08-limitaciones-y-mejoras.md', t: 'Limitaciones y mejoras' },
  { f: null, t: 'Casos de uso por actor' },
  { f: null, t: 'Mockups de las pantallas', mock: true },
];
const reported = [];
const MAPS = {};
SUBS.forEach((sb, k) => {
  if (!sb.f) return;
  const L = fs.readFileSync(path.join(ENT, sb.f), 'utf8').split(/\r?\n/); let h2 = 0, h3 = 0, fence = false; const mp = {};
  for (const l of L) {
    if (l.startsWith(FENCE)) { fence = !fence; continue; } if (fence) continue;
    const m = l.match(/^(##|###) (.*)$/); if (!m) continue;
    const key = (m[2].match(/^(\d+(?:\.\d+)*|[a-g](?:\.\d+)?)\.?\s/) || [])[1];
    let num; if (m[1] === '##') { h2++; h3 = 0; num = `A.${k + 1}.${h2}`; } else { h3++; num = `A.${k + 1}.${h2}.${h3}`; }
    if (key) mp[key] = num;
  }
  MAPS[k + 1] = mp;
});
const unresolved = [];
const KEY = '([a-g0-9]+(?:\\.[a-g0-9]+)*)';
function fixRefs(t, ctx) {
  t = t.split('(`paper/secciones/03-introduccion.md`, §3.1 a §3.3)').join('(secciones 3.1 a 3.3 del paper)').split('El charter (§5)').join('El charter (sección 5)')
    .split('Problemas del §1 de').join('Problemas del A.1.1 de').split('Problema del §1').join('Problema del A.1.1').split('Problema (§1)').join('Problema (A.1.1)');
  const re = new RegExp('(?<![\\w\\-/.])0([1-8])(?:-[a-z0-9-]+(?:\\.md)?)?|11-manual-distribucion|§' + KEY + '(\\s+de\\s+\\[?0([1-8])-)?', 'g');
  const tail = /(?<![\w\-/.])0[1-8](?:-[a-z0-9-]+(?:\.md)?)?\s+$/;
  let out = '', last = 0, lastDoc = null, lastPos = -999, m;
  while ((m = re.exec(t))) {
    out += t.slice(last, m.index); last = re.lastIndex;
    if (m[1] || !m[0].startsWith('§')) { lastDoc = m[1] ? +m[1] : 99; lastPos = m.index; out += m[0]; continue; }
    const key = m[2];
    let doc = m[4] ? +m[4] : ((lastDoc && m.index - lastPos < 70) ? lastDoc : (ctx.defDoc || ctx.sub));
    if (/^[a-g](\.\d+)?$/.test(key)) doc = 7;
    if (!(MAPS[doc] && MAPS[doc][key]) && key.split('.').length >= 3) for (const d in MAPS) if (MAPS[d][key]) doc = +d;
    let r = MAPS[doc] && MAPS[doc][key];
    if (!r) {
      const parts = key.split('.');
      const par = parts.length > 1 && MAPS[doc] && MAPS[doc][parts.slice(0, -1).join('.')];
      r = par ? `${par}, ítem ${parts[parts.length - 1]}` : null;
    }
    if (!r) { unresolved.push(`${ctx.file}: ${t.slice(Math.max(0, m.index - 60), m.index + 12)} (doc ${doc})`); out += 'sección ' + key + (m[3] || ''); lastDoc = doc; lastPos = m.index; continue; }
    if (tail.test(out)) out = out.replace(tail, '');
    out += r + (m[3] || '');
    lastDoc = doc; lastPos = m.index;
  }
  return out + t.slice(last);
}


// ---------- inline ----------
const base = (o = {}) => ({ font: FONT, size: 22, ...o });
function cleanLinks(t) {
  t = t.replace(/!\[[^\]]*\]\([^)]*\)/g, '');
  t = t.replace(/<(https?:[^>]+)>/g, '$1');
  t = t.replace(/\[([^\]]*)\]\(([^)\s]*)\)/g, (m, a, u) => /^https?:/.test(u) && a !== u ? `${a} (${u})` : a);
  return t.replace(/<br\s*\/?>/g, ' ').replace(/\\\|/g, '|');
}
function zw(t, code) {
  const Z = '​';
  const ins = w => w.replace(/(\/|::|_|-|\.|,)(?=[^\/:_\-.,\s])/g, '$1' + Z);
  return code ? ins(t) : t.split(/(\s+)/).map(w => (w.length > 18 && !/^\s/.test(w)) ? ins(w) : w).join('');
}
function inline(text, o = {}) {
  text = cleanLinks(text);
  const runs = [], re = /\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|\*(.+?)\*|`([^`]+)`|~~(.+?)~~/g;
  let last = 0, m;
  const push = (t, x = {}) => { if (t) runs.push(new TextRun(base({ ...o, ...x, text: o.zw ? zw(t, x.font === 'Consolas') : t }))); };
  while ((m = re.exec(text))) {
    push(text.slice(last, m.index));
    if (m[1] !== undefined) runs.push(...inline(m[1], { ...o, bold: true, italics: true }));
    else if (m[2] !== undefined) runs.push(...inline(m[2], { ...o, bold: true }));
    else if (m[3] !== undefined) runs.push(...inline(m[3], { ...o, italics: true }));
    else if (m[5] !== undefined) runs.push(...inline(m[5], { ...o, strike: true }));
    else push(m[4], { font: 'Consolas', size: Math.max(14, (o.size || 22) - 2) });
    last = re.lastIndex;
  }
  push(text.slice(last));
  return runs;
}
const P = (text, opts = {}, o = {}) => new Paragraph({ children: inline(text, o), ...opts });

// ---------- tablas ----------
function splitRow(l) {
  l = l.trim(); const cells = []; let cur = '', bt = false;
  for (let i = 0; i < l.length; i++) {
    const c = l[i];
    if (c === '\\' && l[i + 1] === '|') { cur += '\\|'; i++; continue; }
    if (c === '`') bt = !bt;
    if (c === '|' && !bt) { cells.push(cur); cur = ''; continue; }
    cur += c;
  }
  cells.push(cur);
  if (cells[0].trim() === '') cells.shift();
  if (cells.length && cells[cells.length - 1].trim() === '') cells.pop();
  return cells.map(c => c.trim());
}
function mdTable(lines, FW, sz) {
  const rows = lines.filter(l => !/^\|\s*:?-/.test(l)).map(splitRow);
  const n = Math.max(...rows.map(r => r.length));
  rows.forEach(r => { while (r.length < n) r.push(''); });
  const wts = [];
  for (let i = 0; i < n; i++) {
    const lens = rows.map(r => cleanLinks(r[i]).replace(/[*`]/g, '').length).sort((a, b) => a - b);
    const avg = lens.reduce((a, b) => a + b, 0) / lens.length, p90 = lens[Math.floor(lens.length * 0.9)] || 1;
    wts.push(Math.max(6, Math.min(70, 0.5 * avg + 0.5 * p90)) + 4);
  }
  const tot = wts.reduce((a, b) => a + b, 0);
  const minw = []; for (let i = 0; i < n; i++) { let lw = 3; for (const r of rows) for (const w of cleanLinks(r[i]).replace(/[*`~]/g, '').split(/\s+/)) if (!/[\/:_]/.test(w)) lw = Math.max(lw, Math.min(w.length, 19)); minw.push(lw * sz * 5.4 + 220); }
  let cw = wts.map((w, i) => Math.max(620, Math.floor(minw[i]), Math.floor(FW * w / tot)));
  { let sum = cw.reduce((a, b) => a + b, 0); if (sum > FW) { // reduce solo lo que excede el mínimo, empezando por las columnas más anchas
      let over = sum - FW; for (let g = 0; g < 400 && over > 0; g++) { const k = cw.indexOf(Math.max(...cw)); const d = Math.min(over, 40); cw[k] -= d; over -= d; }
    } else cw[cw.indexOf(Math.max(...cw))] += FW - sum; }
  const bd = { style: BorderStyle.SINGLE, size: 4, color: '808080' }, borders = { top: bd, bottom: bd, left: bd, right: bd };
  return new Table({
    width: { size: FW, type: WidthType.DXA }, columnWidths: cw, layout: TableLayoutType.FIXED,
    rows: rows.map((r, ri) => new TableRow({ tableHeader: ri === 0, cantSplit: true, children: r.map((c, i) => new TableCell({
      borders, width: { size: cw[i], type: WidthType.DXA },
      shading: ri === 0 ? { fill: 'D9D9D9', type: ShadingType.CLEAR, color: 'auto' } : undefined,
      margins: { top: 30, bottom: 30, left: 80, right: 80 },
      children: [new Paragraph({ alignment: AlignmentType.LEFT, spacing: { line: SINGLE, after: 0 }, children: inline(c, { size: sz, bold: ri === 0, zw: true }) })],
    })) })),
  });
}

// ---------- markdown -> docx ----------
const numbering = [{ reference: 'bul', levels: [0, 1, 2].map(l => ({ level: l, format: LevelFormat.BULLET, text: l === 1 ? '–' : '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540 + 360 * l, hanging: 270 } } } })) }];
let numCount = 0;
function newNum() { const ref = 'n' + (++numCount); numbering.push({ reference: ref, levels: [0, 1, 2].map(l => ({ level: l, format: LevelFormat.DECIMAL, text: `%${l + 1}.`, alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540 + 360 * l, hanging: 360 } } } })) }); return ref; }

// Anonimizacion: la empresa de aplicacion no se nombra en el trabajo (primera mencion por anexo: descripcion generica; luego: la empresa de referencia)
function anonimizar(md) {
  md = md.replace(/Logytech Mobile, empresa multinacional de logística,/g, 'una empresa multinacional de logística, la empresa de referencia,');
  md = md.replace(/Logytech Mobile/, 'una empresa multinacional de logística');
  md = md.replace(/(^|[.!?:]\s+|\*\*\s*)Logytech( Mobile)?/gm, (m, a) => a + 'La empresa de referencia');
  return md.replace(/Logytech( Mobile)?/g, 'la empresa de referencia');
}
function pngSize(f) { const b = fs.readFileSync(f); return [b.readUInt32BE(16), b.readUInt32BE(20)]; }
function imgPara(f, alt, maxW, maxH) {
  const [w, h] = pngSize(f); let W = maxW, H = Math.round(W * h / w);
  if (H > maxH) { H = maxH; W = Math.round(H * w / h); }
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { line: SINGLE, before: 60, after: 120 }, children: [new ImageRun({ type: 'png', data: fs.readFileSync(f), transformation: { width: W, height: H }, altText: { title: 'Figura', description: alt || 'Figura', name: 'fig' } })] });
}
function convert(md, ctx) {
  const { land, sub } = ctx;
md = md.split(/\r?\n/).map(x => { const m = x.match(/^###\s+(\d+\.\d+)\s/); if (m) ctx.defDoc = (sub === 6 && m[1] === '6.2') ? 3 : 0; return x.includes('§') ? fixRefs(x, ctx) : x; }).join('\n');
  const FW = land ? 12960 : 9360, maxW = Math.round(FW / 15), maxH = land ? 430 : 600;
  const out = [], L = md.split(/\r?\n/);
  let i = 0, h2 = 0, h3 = 0, lastImg = -999;
  while (i < L.length) {
    const l = L[i];
    if (l.startsWith(FENCE)) {
      const lang = l.slice(3).trim(), b = []; i++;
      while (i < L.length && !L[i].startsWith(FENCE)) b.push(L[i++]);
      i++;
      if (lang === 'mermaid' && lastImg > -999 && i - lastImg < 400) continue; // PNG equivalente ya incluido
      if (lang === 'mermaid' && ctx.file.startsWith('03') && !ctx.arq) { ctx.arq = 1; out.push(imgPara(path.resolve(ENT, '../diagrams/img/arquitectura-general.png'), 'Arquitectura general', maxW, maxH)); continue; }
      if (lang === 'mermaid' && ctx.file.startsWith('03')) { out.push(imgPara(path.join(IMG, 'despliegue-propuesto.png'), 'Despliegue propuesto', maxW, maxH)); continue; }
      if (lang === 'mermaid') reported.push(`${ctx.file}: bloque mermaid sin PNG (se deja como código)`);
      b.forEach((x, k) => out.push(new Paragraph({ shading: { type: ShadingType.CLEAR, fill: 'F2F2F2', color: 'auto' }, alignment: AlignmentType.LEFT, keepLines: true, keepNext: k < b.length - 1 && k < 30, spacing: { line: SINGLE, after: 0 }, children: [new TextRun({ text: x === '' ? ' ' : x, font: 'Consolas', size: 16 })] })));
      out.push(new Paragraph({ spacing: { after: 100, line: 120, lineRule: LineRuleType.EXACT }, children: [] }));
      continue;
    }
    if (!l.trim() || /^---+$/.test(l.trim())) { i++; continue; }
    let m;
    if ((m = l.match(/^(#{2,4}) (.*)$/))) {
      const lv = m[1].length; const t = m[2].replace(/^\d+(\.\d+)*\.?\s+/, '').replace(ctx.file.startsWith('07') ? /^[a-g](\.\d+)?\.?\s+/ : /^$^/, '').replace(/[*`]/g, '');
      let num = null;
      if (lv === 2) { h2++; h3 = 0; num = `A.${sub}.${h2}`; } else if (lv === 3) { h3++; num = `A.${sub}.${h2}.${h3}`; }
      out.push(new Paragraph({ heading: [null, null, HeadingLevel.HEADING_3, HeadingLevel.HEADING_4, HeadingLevel.HEADING_5][lv], keepNext: true, children: [new TextRun({ text: (num ? num + ' ' : '') + cleanLinks(t) })] }));
      i++; continue;
    }
    if (l.startsWith('|')) { const b = []; while (i < L.length && L[i].startsWith('|')) b.push(L[i++]); out.push(mdTable(b, FW, Math.max(...b.map(x => splitRow(x).length)) >= 6 ? 16 : (land ? 18 : 17))); out.push(new Paragraph({ spacing: { after: 0, line: 120, lineRule: LineRuleType.EXACT }, children: [] })); continue; }
    if ((m = l.match(/^!\[(.*?)\]\((.*?)\)\s*$/))) {
      out.push(imgPara(path.resolve(ENT, m[2]), m[1], maxW, maxH)); lastImg = i; i++; continue;
    }
    if (/^\s*(-|\*|\d+\.) /.test(l)) {
      let ref = null, lastOrd = false;
      while (i < L.length && (/^\s*(-|\*|\d+\.) /.test(L[i]) || (/^\s+\S/.test(L[i]) && !/^\s*\|/.test(L[i])))) {
        const x = L[i], mm = x.match(/^(\s*)(-|\*|\d+\.) (.*)$/);
        if (!mm) { out.push(P(x.trim(), { spacing: { line: PROSE, after: 40 }, indent: { left: 540 }, alignment: AlignmentType.LEFT })); i++; continue; }
        const lvl = Math.min(2, Math.floor(mm[1].length / 2)), ord = /\d/.test(mm[2]);
        if (ord && (!ref || !lastOrd)) ref = newNum();
        lastOrd = ord;
        out.push(P(mm[3], { numbering: { reference: ord ? ref : 'bul', level: lvl }, spacing: { line: PROSE, after: 40 }, alignment: AlignmentType.LEFT }));
        i++;
      }
      continue;
    }
    if (l.startsWith('>')) {
      const b = []; while (i < L.length && L[i].startsWith('>')) b.push(L[i++].replace(/^>\s?/, ''));
      out.push(P(b.filter(x => x.trim()).join(' '), { indent: { left: 400, right: 400 }, spacing: { line: PROSE, before: 60, after: 120 }, border: { left: { style: BorderStyle.SINGLE, size: 12, color: '999999', space: 6 } }, alignment: AlignmentType.LEFT })); continue;
    }
    const b = [l]; i++;
    while (i < L.length && L[i].trim() && !/^(#|\||>|\s*(-|\*|\d+\.) |!\[|---)/.test(L[i]) && !L[i].startsWith(FENCE)) b.push(L[i++]);
    out.push(P(b.join(' '), { spacing: { line: PROSE, after: 120 }, alignment: AlignmentType.LEFT }));
  }
  return out;
}

// ---------- ensamblado ----------
const C = (t, o = {}, sp = {}) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { line: 360, ...sp }, children: inline(t, o) });
const portada = [
  C('UNINPAHU', { bold: true, size: 26 }),
  C('Facultad de Ingeniería y Tecnologías de la Información'),
  C('Programa Ingeniería de Software', {}, { after: 1800 }),
  C(TITLE, { bold: true, size: 30 }, { after: 600, line: 420 }),
  C('Anexo A. Documentación técnica preliminar', { italics: true }, { after: 1600 }),
  C('Autor', { bold: true }),
  C('Javier Esteban Mora Osorio', {}, { after: 300 }),
  C('Docente', { bold: true }),
  C('Luisa Fernanda Loza Muñetón', {}, { after: 1400 }),
  C('Bogotá'),
  C('Noviembre de 2026'),
];
const indice = [
  new Paragraph({ spacing: { before: 240, after: 200 }, children: [new TextRun({ text: 'Contenido', bold: true, size: 28, font: FONT })] }),
  new TableOfContents('Contenido', { hyperlink: true, headingStyleRange: '1-2' }),
];
const portrait = { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } };
const landscape = { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } };
const hdr = () => new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 22 })] })] });

const sections = [{ properties: { page: portrait }, children: portada },
  { properties: { page: { ...portrait, pageNumbers: { start: 1 } }, type: SectionType.NEXT_PAGE }, headers: { default: hdr() }, children: indice }];
SUBS.forEach((s, k) => {
  const sub = k + 1, kids = [];
  if (k === 0) kids.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun('Anexo A. Documentación técnica preliminar')] }));
  kids.push(new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, children: [new TextRun(`A.${sub} ${s.t}`)] }));
  if (s.f) {
    const md = anonimizar(fs.readFileSync(path.join(ENT, s.f), 'utf8')).replace(/^# .*\r?\n/, '');
    kids.push(...convert(md, { land: !!s.land, sub, file: s.f }));
  } else if (s.mock) {
    kids.push(P('Los mockups son diseños de interfaz elaborados antes y durante la implementación como referencia visual. Se incluyen las diez pantallas vigentes. Las pantallas implementadas son las del frontend (`frontend/src/app/app.routes.ts`), cuyas rutas se indican en la tabla siguiente junto con los requerimientos que cada diseño ilustra.', { spacing: { line: PROSE, after: 120 }, alignment: AlignmentType.LEFT }));
    kids.push(new Paragraph({ heading: HeadingLevel.HEADING_3, keepNext: true, children: [new TextRun(`A.${sub}.1 Correspondencia con el frontend`)] }));
    const T = [
      '| Mockup | Rol | Ruta del frontend implementada | RF que ilustra | Estado |',
      '|---|---|---|---|---|',
      '| Main (inicio de sesión) | Todos | `/login` | RF-19 | Implementado |',
      '| ForgotPassword | Todos | `/forgot-password` y `/reset-password` | RF-20 | Implementado |',
      '| AdminDashboard | Administrador | `/admin/dashboard` | RF-03 | Implementado con diferencias menores: el mockup muestra solo las pestañas Dashboard, Usuarios y Cobertura; la aplicación añade API Keys, Webhooks e Indicadores |',
      '| AdminApiKeys | Administrador | `/admin/api-keys` | RF-24, RF-06 | Implementado |',
      '| AdminWebhooks | Administrador | `/admin/webhooks` | RF-25 | Implementado |',
      '| AlistadorCrearServicio | Alistador | `/alistador/servicios/nuevo` | RF-05 | Implementado con diferencias menores: el mockup reúne el formulario y la lista de servicios recientes en una pantalla; en el frontend son rutas separadas (`/alistador/servicios` y `/alistador/servicios/nuevo`) |',
      '| OptimizarRuta | Alistador | `/alistador/optimizar-ruta` | RF-21 | Implementado |',
      '| MotorizadoLista | Motorizado | `/motorizado/servicios` | RF-09 | Implementado con diferencias menores: los contadores Pendientes y Cerrados del mockup no aparecen en la pantalla implementada |',
      '| MotorizadoDetalle | Motorizado | `/motorizado/servicios/:id` | RF-10, RF-11, RF-12, RF-13 | Implementado |',
      '| ClienteTracking | Cliente | `/cliente/servicios/:id/tracking` | RF-15, RF-16, RF-28 | Implementado con diferencias menores: el chat es una pantalla aparte (`/cliente/servicios/:id/chat`), no un panel bajo el mapa |',
    ];
    kids.push(mdTable(T, 9360, 17));
    kids.push(new Paragraph({ spacing: { after: 0, line: 120, lineRule: LineRuleType.EXACT }, children: [] }));
    kids.push(new Paragraph({ heading: HeadingLevel.HEADING_3, keepNext: true, children: [new TextRun(`A.${sub}.2 Pantallas`)] }));
    const FIGS = [
      ['autenticacion', 'Inicio de sesión y restablecimiento de contraseña (RF-19, RF-20)'],
      ['admin-dashboard', 'Administrador: panel de servicios (RF-03)'],
      ['admin-apikeys', 'Administrador: API Keys (RF-24)'],
      ['admin-webhooks', 'Administrador: webhooks (RF-25)'],
      ['alistador-crear', 'Alistador: creación de servicio (RF-05)'],
      ['alistador-optimizar', 'Alistador: optimización de ruta (RF-21)'],
      ['motorizado', 'Motorizado: lista y detalle de servicio (RF-09 a RF-13)'],
      ['cliente-tracking', 'Cliente: seguimiento y chat (RF-15, RF-16, RF-28)'],
    ];
    FIGS.forEach(([n, title], j) => {
      kids.push(P(`**Figura A.${sub}.${j + 1}**`, { keepNext: true, alignment: AlignmentType.LEFT, spacing: { before: 200, after: 0 } }));
      kids.push(P(title, { keepNext: true, alignment: AlignmentType.LEFT, spacing: { after: 60 } }, { italics: true }));
      const img = imgPara(path.resolve(ROOT, 'figuras', `mockup-${n}.png`), title, 600, 560); kids.push(img);
      kids.push(P('*Nota.* Fuente: Elaboración propia.', { alignment: AlignmentType.LEFT, spacing: { line: SINGLE, before: 40, after: 160 } }, { size: 20 }));
    });
  } else {
    const figs = [['Administrador', 'administrador'], ['Alistador', 'alistador'], ['Motorizado', 'motorizado'], ['Cliente', 'cliente']];
    const fcu = path.resolve(ROOT, 'figuras', 'fig-casos-uso.png');
    if (fs.existsSync(fcu)) kids.push(imgPara(fcu, 'Casos de uso', 600, 600));
    else figs.forEach(([n, a], j) => {
      kids.push(new Paragraph({ heading: HeadingLevel.HEADING_3, keepNext: true, children: [new TextRun(`A.${sub}.${j + 1} Casos de uso — ${n}`)] }));
      kids.push(imgPara(path.join(IMG, `cu-${a}.png`), `Casos de uso — ${n}`, 600, 330));
    });
  }
  sections.push({ properties: { page: s.land ? landscape : portrait, type: SectionType.NEXT_PAGE }, headers: { default: hdr() }, children: kids });
});

const H = (sz, extra = {}) => ({ run: { font: FONT, size: sz, bold: true, color: '000000', ...extra }, paragraph: { spacing: { before: 240, after: 120, line: PROSE }, alignment: AlignmentType.LEFT } });
const hs = (n, id, sz, ex) => ({ id, name: 'Heading ' + n, basedOn: 'Normal', next: 'Normal', quickFormat: true, ...H(sz, ex), paragraph: { ...H(sz).paragraph, outlineLevel: n - 1 } });
const doc = new Document({
  creator: 'Javier Esteban Mora Osorio', title: TITLE,
  styles: {
    default: { document: { run: { font: FONT, size: 22 }, paragraph: { spacing: { line: PROSE, after: 0 }, alignment: AlignmentType.LEFT } } },
    paragraphStyles: [hs(1, 'Heading1', 28), hs(2, 'Heading2', 26), hs(3, 'Heading3', 24), hs(4, 'Heading4', 22), hs(5, 'Heading5', 22, { italics: true })],
  },
  numbering: { config: numbering },
  sections,
});
const outF = path.join(ROOT, 'Anexos_CMEDriver.docx');
Packer.toBuffer(doc).then(b => { fs.writeFileSync(outF, b); console.log('ok', outF, b.length); console.log(reported.join('\n')); console.log('sin resolver:', unresolved.join(' | ')); });
