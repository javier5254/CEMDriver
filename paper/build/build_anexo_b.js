// Uso: node build_anexo_b.js  -> ../Anexo_B_Cronograma_Presupuesto_Producto.docx
const fs = require('fs'), path = require('path');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, Header, AlignmentType, PageNumber,
  WidthType, ShadingType, BorderStyle, HeadingLevel, PageOrientation, SectionType, VerticalAlign } = require('docx');
const OUT = path.resolve(__dirname, '..', 'Anexo_B_Cronograma_Presupuesto_Producto.docx');
const FONT = 'Arial', PROSE = 276, SINGLE = 240;

// ---------- utilidades ----------
const MARK = /(\[COMPLETAR:[^\]]*\])/;
function runs(text, o = {}) {
  return String(text).split(MARK).filter(s => s !== '').map(s => new TextRun({
    text: s, font: FONT, size: o.size || 22, bold: o.bold, italics: o.italics, color: o.color,
    highlight: MARK.test(s) ? 'yellow' : undefined,
  }));
}
const P = (text, o = {}) => new Paragraph({
  alignment: o.align || AlignmentType.JUSTIFIED, keepNext: o.keepNext,
  spacing: { line: o.line || PROSE, before: o.before || 0, after: o.after === undefined ? 120 : o.after },
  children: runs(text, o),
});
const H1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, keepNext: true, spacing: { before: 240, after: 160 },
  children: [new TextRun({ text: t, bold: true, size: 26, font: FONT })] });
const H2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, spacing: { before: 200, after: 120 },
  children: [new TextRun({ text: t, bold: true, size: 22, font: FONT })] });
const TL = (n, title) => [
  new Paragraph({ keepNext: true, spacing: { before: 160, after: 0, line: SINGLE }, children: [new TextRun({ text: `Tabla B${n}`, bold: true, size: 22, font: FONT })] }),
  new Paragraph({ keepNext: true, spacing: { before: 0, after: 100, line: SINGLE }, children: [new TextRun({ text: title, italics: true, size: 22, font: FONT })] }),
];
const NOTE = text => P(text, { size: 18, line: SINGLE, after: 160, before: 80 });

const bd = { style: BorderStyle.SINGLE, size: 4, color: '808080' };
const borders = { top: bd, bottom: bd, left: bd, right: bd };
function cell(content, w, o = {}) {
  const lines = Array.isArray(content) ? content : [content];
  return new TableCell({
    width: { size: w, type: WidthType.DXA }, borders, columnSpan: o.span, verticalAlign: VerticalAlign.CENTER,
    margins: { top: 40, bottom: 40, left: o.pad === undefined ? 80 : o.pad, right: o.pad === undefined ? 80 : o.pad },
    shading: o.fill ? { type: ShadingType.CLEAR, color: 'auto', fill: o.fill } : undefined,
    children: lines.map(t => new Paragraph({ alignment: o.align || AlignmentType.LEFT, spacing: { line: SINGLE, before: 0, after: 0 },
      children: runs(t, { size: o.size || 18, bold: o.bold, color: o.color }) })),
  });
}
const ORANGE = 'F4A340', DARK = 'C55A11', HEAD = 'D9D9D9';
const table = (widths, rows) => new Table({
  width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths, rows,
});

// ---------- 1. Cronograma (mismos datos que la Tabla 9 del paper: se lee de secciones/07-cronograma-presupuesto.md) ----------
function range(a, b) { const r = []; for (let i = a; i <= b; i++) r.push(i); return r; }
const MD7 = fs.readFileSync(path.resolve(__dirname, '..', 'secciones', '07-cronograma-presupuesto.md'), 'utf8').split(/\r?\n/);
const t0 = MD7.findIndex(l => l.startsWith('| Actividad |'));
const GR = []; for (let k = t0; k < MD7.length && MD7[k].startsWith('|'); k++) if (!/^\|\s*-/.test(MD7[k])) GR.push(MD7[k].trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim()));
const GW = [4300, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1660];
if (GR[0].length !== GW.length || GW.reduce((x, y) => x + y, 0) !== 12960) throw new Error('columnas del cronograma');
const gantt = table(GW, GR.map((r, ri) => new TableRow({ tableHeader: ri === 0, cantSplit: true, children: r.map((c, i) => {
  const exec = ri > 0 && i >= 1 && i <= 6 && c === 'X';
  return cell(exec ? '' : c, GW[i], { fill: ri === 0 ? HEAD : exec ? ORANGE : undefined, bold: ri === 0,
    align: i >= 1 && i <= 7 ? AlignmentType.CENTER : AlignmentType.LEFT, size: 16 });
}) })));

// ---------- 2. Presupuesto ----------
const COP = n => '$' + Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
const PROPIOS = 'Recursos propios del estudiante';
// Mismos datos que la diapositiva 14 de la presentacion y la Tabla 10 del paper.
// [categoría, descripción, cantidad, unidad, valor unitario, actividades del cronograma (Tabla B1)]
const R = [
  ['Personal', 'Analista de requisitos: levantamiento y especificación de requerimientos, alcance y objetivos', 40, 'h', 150000, '1'],
  ['Personal', 'Arquitecto de software: stack, arquitectura, MER, BPMN, C4 y diagramas UML', 50, 'h', 150000, '1'],
  ['Personal', 'Diseñador UX/UI: diseño de mockups y flujos de interfaz por rol', 45, 'h', 150000, '1'],
  ['Personal', 'Desarrollador backend: API Django, servicios, tracking, chat, optimización de ruta, API keys y webhooks', 75, 'h', 150000, '1'],
  ['Personal', 'Desarrollador frontend: aplicación Ionic y Angular', 60, 'h', 150000, '1'],
  ['Personal', 'Ingeniero de pruebas (QA): pruebas automatizadas del backend', 40, 'h', 150000, '1'],
  ['Personal', 'Investigador: revisión de literatura y marco teórico', 65, 'h', 150000, '1'],
  ['Personal', 'Redactor académico: redacción y revisión del documento y los anexos', 50, 'h', 150000, '1 y 8'],
  ['Personal', 'Gestor de proyecto: planificación, seguimiento, entregas y sustentación', 20, 'h', 150000, '1 y 8'],
  ['Servicios tecnológicos', 'Servidor en la nube, 2 vCPU y 4 GB (etapa siguiente)', 6, 'meses', 120000, '5'],
  ['Servicios tecnológicos', 'Dominio .com.co (etapa siguiente)', 1, 'año', 75000, '5'],
  ['Servicios tecnológicos', 'Correo transaccional, plan gratuito', 1, 'plan', 0, '5'],
  ['Servicios tecnológicos', 'Certificado TLS (Let’s Encrypt)', 1, 'cert.', 0, '5'],
  ['Servicios tecnológicos', 'Mapas y geocodificación: OpenStreetMap y Nominatim', 1, 'servicio', 0, '1 y 5'],
  ['Transporte y campo', 'Desplazamientos para entrevistas, observación y piloto (etapa siguiente)', 12, 'viajes', 14000, '3 y 6'],
  ['Comunicaciones', 'Plan de datos para las pruebas piloto (etapa siguiente)', 6, 'meses', 50000, '6'],
  ['Materiales', 'Impresión de consentimientos e instrumentos (etapa siguiente)', 60, 'copias', 300, '3 y 6'],
  ['Materiales', 'Papelería y carpetas (etapa siguiente)', 1, 'global', 20000, '3 y 6'],
  ['Difusión y sustentación', 'Impresión y empaste del informe final (etapa siguiente)', 2, 'ejemplares', 40000, '8'],
  ['Equipos y materiales', 'Uso de equipo propio (depreciación estimada)', 1, 'global', 50818, '1 a 8'],
  ['Registro y trámites', 'No se registrará el software ante la DNDA: la protección del derecho de autor nace sin registro', 1, 'global', 0, '8'],
];
const TARGET = 75000000, HRS = R.filter(r => r[0] === 'Personal').reduce((a, r) => a + r[2], 0);
const sub = R.reduce((a, r) => a + r[2] * r[4], 0), imprev = Math.round(sub * 0.10), total = sub + imprev, PCT = '10';
if (total !== TARGET || HRS !== 445 || sub !== 68181818 || imprev !== 6818182) throw new Error('suma incoherente ' + [sub, imprev, total, HRS]);
const cash = R.filter(r => r[0] !== 'Personal').reduce((a, r) => a + r[2] * r[4], 0);
const BW = [1300, 3200, 1000, 1500, 1300, 1060];
const brow = (c, d, q, u, v, act) => new TableRow({ cantSplit: true, children: [
  cell(c, BW[0]), cell([d, `Actividad(es): ${act}`], BW[1]), cell(`${q} ${u}`, BW[2], { align: AlignmentType.CENTER }),
  cell(COP(v), BW[3], { align: AlignmentType.RIGHT }),
  cell(COP(q * v), BW[4], { align: AlignmentType.RIGHT }), cell(PROPIOS, BW[5], { size: 16 })] });
const budgetRows = [
  new TableRow({ tableHeader: true, cantSplit: true, children: ['Categoría', 'Descripción del rubro', 'Cantidad', 'Valor unitario', 'Total', 'Fuente de financiación']
    .map((t, i) => cell(t, BW[i], { fill: HEAD, bold: true, align: AlignmentType.CENTER })) }),
  ...R.map(r => brow(...r)),
  new TableRow({ cantSplit: true, children: [cell(`Subtotal parcial (suma de los ${R.length} rubros)`, BW[0] + BW[1] + BW[2] + BW[3], { span: 4, bold: true }),
    cell(COP(sub), BW[4], { bold: true, align: AlignmentType.RIGHT }), cell(PROPIOS, BW[5], { size: 16 })] }),
  new TableRow({ cantSplit: true, children: [cell('Imprevistos', BW[0]), cell(`Reserva de imprevistos: ${PCT} % del subtotal parcial (reimpresiones, desplazamientos adicionales, ajustes de última hora)`, BW[1] + BW[2] + BW[3], { span: 3 }),
    cell(COP(imprev), BW[4], { align: AlignmentType.RIGHT }), cell(PROPIOS, BW[5], { size: 16 })] }),
  new TableRow({ cantSplit: true, children: [cell('TOTAL GENERAL (subtotal parcial + imprevistos)', BW[0] + BW[1] + BW[2] + BW[3], { span: 4, bold: true, fill: 'F2F2F2' }),
    cell(COP(total), BW[4], { bold: true, align: AlignmentType.RIGHT, fill: 'F2F2F2' }), cell(PROPIOS, BW[5], { size: 16, fill: 'F2F2F2' })] }),
];
const budget = table(BW, budgetRows);

// ---------- contenido ----------
const title = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60, line: SINGLE }, children: [new TextRun({ text: 'UNINPAHU', bold: true, size: 24, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60, line: SINGLE }, children: [new TextRun({ text: 'Programa Ingeniería de Software. Proyecto (Ingeniería de Software), semestre 2026-II', size: 20, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200, after: 60, line: 300 }, children: [new TextRun({ text: 'Anexo B. Cronograma, presupuesto y producto entregable', bold: true, size: 28, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60, line: SINGLE }, children: [new TextRun({ text: 'CMEDriver: plataforma orientada a API para la gestión de servicios de mensajería', italics: true, size: 22, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240, line: SINGLE }, children: [new TextRun({ text: 'Javier Esteban Mora Osorio. Docente: Luisa Fernanda Loza Muñetón. Noviembre de 2026', size: 20, font: FONT })] }),
];

const s1 = [
  H1('1. Cronograma de actividades'),
  P('El cronograma abarca el proyecto completo en dos tramos: el semestre 2026-II, ya ejecutado (el proyecto arrancó hacia el 20 de agosto de 2026, según el estudiante, y llega hasta el 17 de noviembre de 2026, fecha de la Entrega 3), y los seis meses planificados del Trabajo de Grado (M1 a M6), que dependen de la autorización de la organización de referencia y no tienen fechas de calendario porque el estudiante no ha definido su inicio. La Tabla B1 lo presenta como diagrama de Gantt: los periodos del semestre son quincenas (el primero, del 20 al 31 de agosto, y el último, del 1 al 17 de noviembre, son parciales), las actividades 1a a 1f son las ejecutadas y las actividades 2 a 8 son las pendientes. Las duraciones difieren según la complejidad de cada actividad: el diseño de la Entrega 1 y el marco teórico de la Entrega 2 ocuparon dos periodos cada uno, y la construcción del prototipo, la actividad más extensa, cinco periodos.'),
  P('Estado real al 17 de noviembre de 2026: están completados el diseño y la planificación, el análisis y el diseño (requisitos, modelo de datos, UML y mockups), la construcción del prototipo hasta el nivel de prototipo temprano, las 110 pruebas automatizadas del backend y la documentación técnica. La validación de requisitos con usuarios reales, la prueba piloto, el trabajo de campo y el análisis de resultados no se han realizado y quedan para el Trabajo de Grado; no existen datos ni resultados de ellos. La compuerta de inicio del trabajo de campo exige instrumentos validados, autorización de la organización de referencia y entorno de pruebas desplegado.'),
];
const s1b = [
  ...TL(1, 'Cronograma del proyecto: semestre 2026-II (hecho) y seis meses de Trabajo de Grado (pendiente)'), gantt,
  NOTE('Nota. Naranja = periodo de ejecución real (quincenas del semestre 2026-II); M1 a M6 = meses relativos del Trabajo de Grado, sin fechas de calendario. Entrega 1: límite el 6 de septiembre; Entrega 2: 11 de octubre; Entrega 3: 17 de noviembre, antes del corte III del 27 al 30 de noviembre. La numeración de las actividades (1 a 8) es la que usan los rubros del presupuesto (Tabla B2): la actividad 1 agrupa las filas 1a a 1f. El prototipo es temprano y no se ha validado con usuarios reales. Compuerta de inicio de campo: instrumentos validados, autorización de la organización de referencia y entorno de pruebas desplegado. Fuente: Elaboración propia.'),
];
const s1c = [
  H2('1.1 Orden real de ejecución del semestre'),
  P('El prototipo se construyó antes y en paralelo a la redacción del documento, no después de ella. Los primeros archivos del código y de la documentación datan del 11 de septiembre de 2026; el primer commit del repositorio es del 6 de octubre de 2026 y ya incluía el backend Django, el frontend Ionic y la documentación existentes. Entre el 6 y el 16 de octubre se registran 29 commits, que corresponden a la documentación técnica de la entrega (6 de octubre), a la reducción de alcance del 9 de octubre, que retiró el inventario, los pagos y el chatbot junto con la sincronización del paper, y al ensamblaje del documento unificado (13 al 16 de octubre). El historial posterior incluye el panel de indicadores y la ampliación de las pruebas automatizadas a 110. Los periodos de la Tabla B1 se sustentan en el calendario y en estas fechas, no solo en el historial del repositorio, que no conserva commits anteriores al 6 de octubre.'),
  P('Esta secuencia invirtió parcialmente el orden lógico habitual, en el que la metodología y la arquitectura preceden a la implementación: en este proyecto se documentaron en parte a posteriori. El avance de resultados y los anexos (Entrega 3) se elaboraron sobre el prototipo ya existente.'),
  H2('1.2 Trabajo de Grado (siguiente etapa, planificado)'),
  P('Las actividades de validación empírica no forman parte de esta asignatura. La Tabla B1 las presenta como plan en meses relativos (M1 a M6), porque dependen del calendario del programa y de la autorización de una empresa multinacional de logística, organización de referencia del proyecto. Ninguna de estas actividades se ha ejecutado. El trabajo de campo (M4 a M5) no inicia sin instrumentos validados, autorización y entorno de pruebas desplegado; el cierre de brechas críticas (control de acceso, cobertura y migración a PostgreSQL) y el despliegue (M2 a M3) lo preceden.'),
  H2('1.3 Preguntas de verificación'),
  P('1. ¿Todas las etapas están representadas en el cronograma? Sí: la Tabla B1 incluye diseño y planificación, análisis y diseño, construcción, pruebas, documentación y entrega, además de las actividades de validación con usuarios reales, que figuran como trabajo del Trabajo de Grado.'),
  P('2. ¿El orden es lógico? Las dependencias son las siguientes: el protocolo (actividad 2), los instrumentos (actividad 3), el cierre de brechas (actividad 4) y el despliegue (actividad 5) preceden al campo (actividad 6), y el análisis (actividad 7) depende del campo. La excepción en el semestre es que la metodología y la arquitectura se documentaron después de construir parte del prototipo, como se declara en la sección 1.1.'),
  P('3. ¿Es compatible con las fechas de entrega del programa? Sí en el semestre: la Entrega 1 cierra el 6 de septiembre, la Entrega 2 el 11 de octubre y la Entrega 3 el 17 de noviembre, antes del corte III del 27 al 30 de noviembre. Los seis meses del Trabajo de Grado se ajustarán al calendario del programa.'),
];

const s2 = [
  H1('2. Presupuesto'),
  P(`El presupuesto estima los costos del proyecto completo (el diseño y el prototipo ya realizados, más seis meses de Trabajo de Grado) según las categorías de la guía: personal, servicios tecnológicos, transporte y campo, comunicaciones, materiales, difusión y sustentación, equipos y materiales, registro y trámites, e imprevistos (10 % del subtotal parcial). Cada rubro indica la actividad del cronograma (Tabla B1) que lo justifica. Los rubros de servidor, dominio, transporte, datos e impresión corresponden a la etapa siguiente (Trabajo de Grado), cuando el sistema se despliega en un entorno de pruebas y se realiza el trabajo de campo; hasta hoy el prototipo no se ha desplegado. Los servicios gratuitos (correo transaccional en plan gratuito, certificado TLS de Let’s Encrypt y OpenStreetMap/Nominatim) se registran con costo $0. El software no se registrará ante la Dirección Nacional de Derecho de Autor (DNDA), por lo que ese trámite se registra con $0; la protección del derecho de autor nace sin registro.`),
  P(`La categoría de personal valora a $150.000 por hora las ${HRS} horas que el estudiante, integrante único del proyecto, estima haber dedicado en nueve roles; los honorarios son un aporte valorizado con recursos propios y no un desembolso en efectivo, y las horas son una estimación del estudiante. La financiación es de recursos propios del estudiante; la empresa de referencia no aportó recursos al proyecto. Las demás cifras son valores de referencia del estudiante, expresados en pesos colombianos (COP), por confirmar con proveedores.`),
  ...TL(2, 'Presupuesto del proyecto (período previo y Trabajo de Grado), en pesos colombianos'), budget,
  NOTE(`Nota. Cifras de referencia en pesos colombianos (COP), por confirmar con proveedores. Las ${HRS} horas, dedicadas durante el semestre 2026-II, son una estimación del estudiante, quien actúa en varios roles; sus honorarios son un aporte valorizado (recursos propios), no un desembolso en efectivo. El subtotal parcial es la suma de las columnas Total de los ${R.length} rubros (${COP(sub)}); los imprevistos (${COP(imprev)}) son el ${PCT} % del subtotal y el total general es ${COP(total)}. Excluida la valoración del tiempo propio, los gastos de uso y desembolso ascienden a ${COP(cash)} antes de imprevistos. Los rubros de servidor, dominio, transporte, datos e impresión son de la etapa siguiente.`),
  H2('2.1 Preguntas de verificación'),
  P('1. ¿Cada rubro del presupuesto corresponde a una actividad del cronograma? Sí. La descripción de cada rubro cita la actividad (1 a 8) de la Tabla B1 a la que corresponde, y ninguna actividad queda sin costo asociado, incluso cuando el costo es $0.'),
  P(`2. ¿Se incluyeron los imprevistos y existe un plan alternativo? Sí. Se reservaron ${COP(imprev)}, el ${PCT} % del subtotal. Si el presupuesto resultara insuficiente, el plan alternativo consiste en reemplazar la impresión y el empaste por entrega digital, utilizar solo software de código abierto y servicios gratuitos, y emplear un entorno de pruebas local en lugar del servidor en la nube.`),
  P('3. ¿La fuente de financiación es realista y está disponible durante el período del proyecto? Los recursos propios del estudiante cubren los rubros de uso y desembolso, y el costo del personal corresponde a tiempo propio valorizado, sin desembolso. Los valores son de referencia y se confirmarán con proveedores al iniciar la etapa siguiente.'),
];

const s3 = [
  H1('3. Producto entregable'),
  P('El producto entregable de la asignatura es un prototipo funcional temprano de CMEDriver, una plataforma orientada a API para la gestión de servicios de mensajería, acompañado del documento académico y de la documentación técnica de los anexos. El prototipo se compone de un backend Django con seis aplicaciones y doce entidades, y de un frontend Ionic y Angular, e incluye los siguientes módulos: usuarios con roles (administrador, alistador, motorizado y cliente); cobertura y tiempos de entrega; servicios y rutas, con entregas y recolecciones; evidencia de entrega mediante foto y firma; seguimiento por GPS; chat en tiempo real con alcance restringido al cliente dueño del servicio y al motorizado asignado; optimización de ruta mediante la heurística del vecino más cercano; y claves de API con webhooks firmados. Ciento diez pruebas automatizadas del backend verifican estos módulos. El documento académico recoge el problema, los objetivos, el marco teórico, la metodología y el avance de resultados, y los anexos reúnen los requerimientos, el stack tecnológico, la arquitectura, el modelo entidad-relación, el modelo BPMN, el modelo C4, la matriz de trazabilidad, las limitaciones y los casos de uso por actor.'),
  P('El producto se dirige a la empresa de referencia del proyecto, y en particular a sus equipos de operaciones y de tecnología, sujeto a su autorización. Para el equipo de operaciones sirve como modelo de cómo se podrían registrar servicios, evidencias y recorridos en una misma plataforma; para el equipo de tecnología, como referencia de una arquitectura orientada a API con integración mediante claves y webhooks. Apoya decisiones sobre qué módulos conviene validar con usuarios reales y qué integraciones priorizar en el Trabajo de Grado, y aporta a la ingeniería de software un caso documentado de diseño y construcción de una plataforma de gestión de servicios de mensajería con trazabilidad entre necesidades, requerimientos, modelos, código y pruebas. El producto no afirma validación con la operación de la empresa de referencia ni resultados de mejora, porque no existen datos de usuarios reales. Es un prototipo académico: el envío de correo de restablecimiento de contraseña se simula por consola, los usuarios son de prueba, el build nativo de Android no se verificó, y el inventario, los pagos y el chatbot se retiraron del alcance en octubre de 2026.'),
];

const hdr = () => new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 22 })] })] });
const portrait = { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } };
const landscape = { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } };
const doc = new Document({
  creator: 'Javier Esteban Mora Osorio', title: 'Anexo B. Cronograma, presupuesto y producto entregable',
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 26, bold: true }, paragraph: { outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 22, bold: true }, paragraph: { outlineLevel: 1 } },
    ],
  },
  sections: [
    { properties: { page: { ...portrait, pageNumbers: { start: 1 } } }, headers: { default: hdr() }, children: [...title, ...s1] },
    { properties: { page: landscape, type: SectionType.NEXT_PAGE }, headers: { default: hdr() }, children: s1b },
    { properties: { page: portrait, type: SectionType.NEXT_PAGE }, headers: { default: hdr() }, children: [...s1c, ...s2, ...s3] },
  ],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('OK', OUT, 'subtotal', sub, 'imprev', imprev, 'total', total, 'cash', cash); });
