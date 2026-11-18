/*
 * Captura la app CMEDriver en funcionamiento (con los datos de la base) y guarda PNG para la presentación.
 *
 * Requisitos: backend en http://localhost:8000 (con `manage.py seed_demo` ejecutado) y frontend en
 * http://localhost:4200 (`npx ng serve`). Necesita puppeteer-core y un Chrome:
 *   PUPPETEER_CORE=<ruta a puppeteer-core>  CHROME_PATH=<chrome.exe>  node capturar.js <carpeta-salida>
 */
const fs = require('fs');
const path = require('path');
const puppeteer = require(process.env.PUPPETEER_CORE || 'puppeteer-core');

const FRONT = process.env.FRONT_URL || 'http://localhost:4200';
const API = process.env.API_URL || 'http://localhost:8000/api';
const CHROME = process.env.CHROME_PATH;
const OUT = path.resolve(process.argv[2] || 'capturas');
fs.mkdirSync(OUT, { recursive: true });

const ESCRITORIO = { width: 1440, height: 900, deviceScaleFactor: 1.5 };
const MOVIL = { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true };
const pausa = (ms) => new Promise((r) => setTimeout(r, ms));

async function login(username, password) {
  const r = await fetch(`${API}/auth/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!r.ok) throw new Error(`login ${username}: ${r.status}`);
  return r.json();
}

async function get(sesion, ruta) {
  const r = await fetch(`${API}${ruta}`, { headers: { Authorization: `Bearer ${sesion.access}` } });
  if (!r.ok) throw new Error(`GET ${ruta}: ${r.status}`);
  return r.json();
}

async function capturar(browser, { nombre, sesion, ruta, viewport, espera = 2500, recorte }) {
  const page = await browser.newPage();
  await page.setViewport(viewport);
  // Ubicación disponible (Bogotá, centro) para que la app no muestre el aviso de permiso denegado
  await browser.defaultBrowserContext().overridePermissions(FRONT, ['geolocation']);
  await page.setGeolocation({ latitude: 4.6486, longitude: -74.0628 });
  await page.evaluateOnNewDocument((s) => {
    try {
      localStorage.setItem('cme_access', s.access);
      localStorage.setItem('cme_refresh', s.refresh);
      localStorage.setItem('cme_user', JSON.stringify(s.user));
    } catch (e) {}
  }, sesion);
  await page.goto(`${FRONT}${ruta}`, { waitUntil: 'networkidle2', timeout: 60000 });
  await pausa(espera);
  const destino = path.join(OUT, `${nombre}.png`);
  await page.screenshot({ path: destino, ...(recorte ? { clip: recorte } : {}) });
  await page.close();
  console.log('capturada', nombre, '->', destino, ruta);
}

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox'] });
  try {
    const admin = await login('admin', 'admin1234');
    const alistador = await login('alistador1', 'alistador1234');
    await capturar(browser, { nombre: 'indicadores-admin', sesion: admin, ruta: '/admin/indicadores', viewport: ESCRITORIO, espera: 3500 });
    await capturar(browser, { nombre: 'admin-dashboard', sesion: admin, ruta: '/admin/dashboard', viewport: ESCRITORIO });
    await capturar(browser, { nombre: 'servicios-alistador', sesion: alistador, ruta: '/alistador/servicios', viewport: ESCRITORIO });

    // Motorizado con un servicio en tránsito
    let moto = null, servMoto = null;
    for (let i = 1; i <= 4 && !servMoto; i++) {
      const s = await login(`demo_moto${i}`, 'demo1234').catch(() => null);
      if (!s) continue;
      const lista = await get(s, '/servicios/');
      const arr = Array.isArray(lista) ? lista : lista.results || [];
      const encontrado = arr.find((x) => x.estado === 'EN_TRANSITO') || arr.find((x) => x.estado === 'ASIGNADO');
      if (encontrado) { moto = s; servMoto = encontrado; }
    }
    if (servMoto) {
      await capturar(browser, { nombre: 'motorizado-servicio', sesion: moto, ruta: `/motorizado/servicios/${servMoto.id}`, viewport: MOVIL });
    } else console.warn('sin servicio para motorizado');

    // Cliente con un servicio en tránsito (mapa) y chat con mensajes
    let cli = null, servCli = null, servChat = null;
    for (let i = 1; i <= 8 && !(servCli && servChat); i++) {
      const s = await login(`demo_cliente${i}`, 'demo1234').catch(() => null);
      if (!s) continue;
      const lista = await get(s, '/servicios/');
      const arr = Array.isArray(lista) ? lista : lista.results || [];
      const tr = arr.find((x) => x.estado === 'EN_TRANSITO');
      if (tr && !servCli) { cli = s; servCli = tr; }
      for (const x of arr) {
        const m = await get(s, `/servicios/${x.id}/mensajes/`).catch(() => []);
        if ((Array.isArray(m) ? m : m.results || []).length >= 3 && !servChat) { servChat = { s, x }; break; }
      }
    }
    if (servCli) await capturar(browser, { nombre: 'cliente-tracking', sesion: cli, ruta: `/cliente/servicios/${servCli.id}/tracking`, viewport: MOVIL, espera: 5000 });
    else console.warn('sin servicio en tránsito para cliente');
    if (servChat) await capturar(browser, { nombre: 'cliente-chat', sesion: servChat.s, ruta: `/cliente/servicios/${servChat.x.id}/chat`, viewport: MOVIL });
    else console.warn('sin chat con mensajes');

    // Swagger (API documentada)
    const page = await browser.newPage();
    await page.setViewport(ESCRITORIO);
    await page.goto(API.replace(/\/api$/, '') + '/api/docs/', { waitUntil: 'networkidle2', timeout: 60000 }).catch((e) => console.warn('swagger:', e.message));
    await pausa(2500);
    await page.screenshot({ path: path.join(OUT, 'swagger.png') });
    await page.close();
    console.log('capturada swagger');
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error(e); process.exit(1); });
