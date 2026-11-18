import { DestroyRef, ElementRef, afterNextRender, inject, signal } from '@angular/core';

// ---------------------------------------------------------------------------
// Tipos compartidos por los graficos SVG propios (sin librerias externas).
// Los colores se pasan como cadenas CSS (p. ej. 'var(--ion-color-success)') y
// se aplican con [style.fill], de modo que respondan al tema claro/oscuro.
// ---------------------------------------------------------------------------

/** `opacity` admite numeros o `var(--token)` para ajustar la intensidad por tema. */
export interface ChartSeries {
  label: string;
  color: string;
  opacity?: number | string;
}

export interface ChartSegment extends ChartSeries {
  id: string;
  value: number;
}

export interface TooltipRow {
  label: string;
  value: string;
  color?: string;
  opacity?: number | string;
}

export interface TooltipState {
  x: number;
  y: number;
  title: string;
  rows: TooltipRow[];
}

// ---------------------------------------------------------------------------
// Formato es-CO
// ---------------------------------------------------------------------------

export const NBSP = ' ';
export const VACIO = '—';

const nf0 = new Intl.NumberFormat('es-CO', { maximumFractionDigits: 0 });
const nf1 = new Intl.NumberFormat('es-CO', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
const MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];

/** Entero con separador de miles es-CO (1.234). */
export function fmtInt(n: number | null | undefined): string {
  return n == null || !isFinite(n) ? VACIO : nf0.format(n);
}

/** Decimal con un decimal es-CO (1.234,5). */
export function fmtDec(n: number | null | undefined): string {
  return n == null || !isFinite(n) ? VACIO : nf1.format(n);
}

/** Fraccion 0..1 como porcentaje con un decimal (92,5 %). */
export function fmtPct(r: number | null | undefined): string {
  return r == null || !isFinite(r) ? VACIO : `${nf1.format(r * 100)}${NBSP}%`;
}

export function fmtHoras(h: number | null | undefined): string {
  return h == null || !isFinite(h) ? VACIO : `${nf1.format(h)}${NBSP}h`;
}

function parseIso(iso: string): { y: number; m: number; d: number } | null {
  const mt = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso);
  return mt ? { y: +mt[1], m: +mt[2], d: +mt[3] } : null;
}

/** '2026-11-17' -> '17 nov' (sin depender de la zona horaria). */
export function fmtFechaCorta(iso: string): string {
  const p = parseIso(iso);
  return p ? `${p.d} ${MESES[p.m - 1]}` : iso;
}

/** '2026-11-17' -> '17 nov 2026'. */
export function fmtFechaMedia(iso: string): string {
  const p = parseIso(iso);
  return p ? `${p.d} ${MESES[p.m - 1]} ${p.y}` : iso;
}

/** '2026-11-17' -> 'mar, 17 nov 2026'. */
export function fmtFechaLarga(iso: string): string {
  const p = parseIso(iso);
  if (!p) return iso;
  const dia = new Intl.DateTimeFormat('es-CO', { weekday: 'short', timeZone: 'UTC' }).format(
    new Date(Date.UTC(p.y, p.m - 1, p.d)),
  );
  return `${dia}, ${p.d} ${MESES[p.m - 1]} ${p.y}`;
}

/** ISO con hora -> '17 nov 2026, 7:16 p. m.' (hora local del navegador). */
export function fmtFechaHora(iso: string): string {
  const d = new Date(iso);
  if (isNaN(d.getTime())) return iso;
  const hora = new Intl.DateTimeFormat('es-CO', { hour: 'numeric', minute: '2-digit' }).format(d);
  return `${d.getDate()} ${MESES[d.getMonth()]} ${d.getFullYear()}, ${hora}`;
}

/** 'DIRECCION_INCORRECTA' -> 'Direccion incorrecta'; deja intacto el texto libre. */
export function humanizar(texto: string): string {
  if (!texto) return texto;
  if (!/^[A-Z0-9_]+$/.test(texto)) return texto;
  const t = texto.replace(/_/g, ' ').toLowerCase();
  return t.charAt(0).toUpperCase() + t.slice(1);
}

// ---------------------------------------------------------------------------
// Escalas
// ---------------------------------------------------------------------------

/** Escala "bonita" desde 0 con pasos enteros (los datos son conteos). */
export function niceScale(max: number, target = 4): { max: number; ticks: number[] } {
  const m = Math.max(1, isFinite(max) ? max : 1);
  const rough = m / target;
  const mag = Math.pow(10, Math.floor(Math.log10(rough)));
  const res = rough / mag;
  const base = res <= 1 ? 1 : res <= 2 ? 2 : res <= 5 ? 5 : 10;
  const step = Math.max(1, base * mag);
  const top = Math.ceil(m / step) * step;
  const ticks: number[] = [];
  for (let v = 0; v <= top + step / 1e6; v += step) ticks.push(Math.round(v));
  return { max: top, ticks };
}

/** Indices de etiquetas del eje X, repartidos parejo y siempre con el ultimo. */
export function labelIndices(n: number, maxLabels: number): Set<number> {
  const out = new Set<number>();
  if (n <= 0) return out;
  const step = Math.max(1, Math.ceil(n / Math.max(1, maxLabels)));
  for (let i = n - 1; i >= 0; i -= step) out.add(i);
  return out;
}

// ---------------------------------------------------------------------------
// Ancho real del contenedor: el viewBox se arma con el ancho medido para que
// 1 unidad = 1 px y el texto del grafico siga siendo legible en movil.
// ---------------------------------------------------------------------------

/** Debe llamarse en un contexto de inyeccion (inicializador de campo). */
export function observeWidth(initial = 320) {
  const host = inject<ElementRef<HTMLElement>>(ElementRef);
  const destroyRef = inject(DestroyRef);
  const width = signal(initial);

  afterNextRender(() => {
    const el = host.nativeElement;
    const measure = () => {
      const w = Math.floor(el.getBoundingClientRect().width);
      if (w > 0 && w !== width()) width.set(w);
    };
    measure();
    if (typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    destroyRef.onDestroy(() => ro.disconnect());
  });

  return width;
}
