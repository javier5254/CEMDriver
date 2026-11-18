import { ChangeDetectionStrategy, Component, computed, input, signal } from '@angular/core';
import { ChartTooltipComponent } from './chart-tooltip.component';
import {
  ChartSeries,
  TooltipState,
  fmtInt,
  labelIndices,
  niceScale,
  observeWidth,
} from './chart-utils';

export interface StackedDatum {
  key: string;
  /** Etiqueta corta del eje X (p. ej. "17 nov"). */
  label: string;
  /** Titulo largo para el tooltip y la tabla (p. ej. "mar, 17 nov 2026"). */
  title: string;
  /** Un valor por serie, en el mismo orden que `series`. */
  values: number[];
}

const GAP = 2; // separacion de 2 px entre segmentos apilados
const RADIO = 4; // extremo redondeado de 4 px (solo arriba)

/** Path de una columna con las esquinas superiores redondeadas y base recta. */
function colPath(x: number, top: number, w: number, h: number, r: number): string {
  const rr = Math.min(r, w / 2, h);
  const f = (n: number) => +n.toFixed(2);
  if (rr <= 0.5) return `M${f(x)},${f(top)}h${f(w)}v${f(h)}h${f(-w)}Z`;
  return (
    `M${f(x)},${f(top + h)}V${f(top + rr)}Q${f(x)},${f(top)} ${f(x + rr)},${f(top)}` +
    `H${f(x + w - rr)}Q${f(x + w)},${f(top)} ${f(x + w)},${f(top + rr)}V${f(top + h)}Z`
  );
}

/** Barras apiladas por categoria (dias) con eje Y, rejilla suave y tooltip. */
@Component({
  selector: 'app-stacked-columns',
  standalone: true,
  imports: [ChartTooltipComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @let l = layout();
    <div class="wrap">
      <svg
        [attr.viewBox]="'0 0 ' + l.w + ' ' + l.h"
        [attr.height]="l.h"
        width="100%"
        role="img"
        [attr.aria-label]="ariaLabel()"
        (pointerdown)="limpiar()"
      >
        @for (t of l.ticks; track t.v) {
          <line class="gr" [class.base]="t.v === 0" [attr.x1]="l.padL" [attr.x2]="l.w - l.padR" [attr.y1]="t.y" [attr.y2]="t.y" />
          <text class="tk" text-anchor="end" dominant-baseline="central" [attr.x]="l.padL - 8" [attr.y]="t.y">{{ t.label }}</text>
        }
        @for (c of l.cols; track c.key) {
          @if (c.i === activo()) {
            <rect class="bd" [attr.x]="c.sx" [attr.y]="l.padT" [attr.width]="c.sw" [attr.height]="l.ih" />
          }
          @for (s of c.segs; track s.k) {
            <path [attr.d]="s.d" [style.fill]="s.color" [style.fill-opacity]="s.opacity" />
          }
        }
        @if (l.pico; as p) {
          <text class="pk" text-anchor="middle" [attr.x]="p.x" [attr.y]="p.y">{{ p.text }}</text>
        }
        @for (x of l.xl; track x.i) {
          <text class="tk" [attr.text-anchor]="x.anchor" [attr.x]="x.x" [attr.y]="l.h - 8">{{ x.text }}</text>
        }
        @for (c of l.cols; track c.key) {
          <rect
            class="hit"
            [attr.x]="c.sx"
            [attr.y]="l.padT"
            [attr.width]="c.sw"
            [attr.height]="l.ih + 8"
            (pointerenter)="mostrar(c.i)"
            (pointerdown)="mostrar(c.i); $event.stopPropagation()"
            (pointerleave)="salir($event)"
          />
        }
      </svg>
      @if (tip(); as t) {
        <app-chart-tooltip [x]="t.x" [y]="t.y" [bounds]="l.w" [title]="t.title" [rows]="t.rows" />
      }
    </div>
    <ul class="lg">
      @for (s of series(); track s.label) {
        <li><i [style.background]="s.color" [style.opacity]="s.opacity ?? 1"></i>{{ s.label }}</li>
      }
    </ul>
    <div class="sr">
      <table>
        <caption>{{ ariaLabel() }}</caption>
        <thead>
          <tr>
            <th scope="col">Día</th>
            @for (s of series(); track s.label) {
              <th scope="col">{{ s.label }}</th>
            }
            <th scope="col">Total</th>
          </tr>
        </thead>
        <tbody>
          @for (d of data(); track d.key) {
            <tr>
              <th scope="row">{{ d.title }}</th>
              @for (v of d.values; track $index) {
                <td>{{ fmt(v) }}</td>
              }
              <td>{{ fmt(suma(d.values)) }}</td>
            </tr>
          }
        </tbody>
      </table>
    </div>
  `,
  styles: [
    `
      :host {
        display: block;
        width: 100%;
        position: relative;
      }
      .wrap {
        position: relative;
      }
      svg {
        display: block;
        overflow: visible;
      }
      .gr {
        stroke: rgba(var(--ion-text-color-rgb), 0.09);
        stroke-width: 1;
      }
      .gr.base {
        stroke: rgba(var(--ion-text-color-rgb), 0.22);
      }
      .tk,
      .pk {
        font-size: 11px;
        fill: rgba(var(--ion-text-color-rgb), 0.62);
      }
      .pk {
        font-weight: 600;
        fill: var(--ion-text-color);
      }
      .bd {
        fill: rgba(var(--ion-text-color-rgb), 0.06);
      }
      .hit {
        fill: transparent;
        cursor: default;
      }
      .lg {
        display: flex;
        flex-wrap: wrap;
        gap: 4px 16px;
        margin: 8px 0 0;
        padding: 0;
        list-style: none;
        font-size: 12px;
        color: rgba(var(--ion-text-color-rgb), 0.78);
      }
      .lg li {
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .lg i {
        width: 10px;
        height: 10px;
        border-radius: 3px;
      }
      .sr {
        position: absolute;
        width: 1px;
        height: 1px;
        margin: -1px;
        overflow: hidden;
        clip: rect(0 0 0 0);
        white-space: nowrap;
      }
    `,
  ],
})
export class StackedColumnsComponent {
  readonly data = input.required<StackedDatum[]>();
  readonly series = input.required<ChartSeries[]>();
  readonly height = input(240);
  readonly ariaLabel = input('Grafico de barras apiladas');

  protected readonly tip = signal<TooltipState | null>(null);
  protected readonly activo = signal(-1);
  private readonly width = observeWidth(560);

  protected readonly fmt = fmtInt;
  protected suma(v: number[]): number {
    return v.reduce((a, b) => a + b, 0);
  }

  protected readonly layout = computed(() => {
    const data = this.data();
    const series = this.series();
    const w = this.width();
    const h = this.height();
    const n = data.length;
    const totals = data.map((d) => d.values.reduce((a, b) => a + b, 0));
    const maxTotal = n ? Math.max(...totals) : 0;
    const sc = niceScale(maxTotal);

    const labels = sc.ticks.map((v) => fmtInt(v));
    const padL = 14 + Math.max(...labels.map((s) => s.length)) * 6.6;
    const padR = 8;
    const padT = 16;
    const padB = 28;
    const iw = Math.max(10, w - padL - padR);
    const ih = h - padT - padB;
    const yOf = (v: number) => padT + ih * (1 - v / sc.max);

    const slot = n ? iw / n : iw;
    const gap = slot >= 8 ? 2 : 1;
    const bw = Math.max(1, Math.min(24, slot - gap));

    const cols = data.map((d, i) => {
      const sx = padL + slot * i;
      const x = sx + (slot - bw) / 2;
      let last = -1;
      d.values.forEach((v, k) => {
        if (v > 0) last = k;
      });
      let cum = 0;
      let primero = true;
      const segs: { k: number; d: string; color: string; opacity: number | string }[] = [];
      d.values.forEach((v, k) => {
        if (v <= 0) return;
        const top = yOf(cum + v);
        const bottom = Math.max(top + 1, yOf(cum) - (primero ? 0 : GAP));
        segs.push({
          k,
          d: colPath(x, top, bw, bottom - top, k === last ? RADIO : 0),
          color: series[k]?.color ?? 'currentColor',
          opacity: series[k]?.opacity ?? 1,
        });
        primero = false;
        cum += v;
      });
      return { key: d.key, i, sx, sw: slot, cx: x + bw / 2, segs };
    });

    const maxLabels = Math.max(2, Math.floor(iw / 58));
    const idx = labelIndices(n, maxLabels);
    const xl = [...idx]
      .sort((a, b) => a - b)
      .map((i) => {
        const cx = padL + slot * i + slot / 2;
        const anchor = cx + 20 > w ? 'end' : cx - 20 < 0 ? 'start' : 'middle';
        const x = anchor === 'end' ? Math.min(cx + 4, w - 1) : anchor === 'start' ? Math.max(cx - 4, 1) : cx;
        return { i, x, anchor, text: data[i].label };
      });

    // Etiqueta selectiva: solo el pico del periodo.
    let pico: { x: number; y: number; text: string } | null = null;
    if (maxTotal > 0) {
      const ip = totals.indexOf(maxTotal);
      const cx = cols[ip].cx;
      pico = {
        x: Math.min(Math.max(cx, padL + 10), w - padR - 10),
        y: yOf(maxTotal) - 5,
        text: fmtInt(maxTotal),
      };
    }

    return {
      w,
      h,
      padL,
      padR,
      padT,
      ih,
      cols,
      xl,
      pico,
      totals,
      yOf,
      ticks: sc.ticks.map((v, i) => ({ v, y: yOf(v), label: labels[i] })),
    };
  });

  protected mostrar(i: number): void {
    const l = this.layout();
    const d = this.data()[i];
    if (!d) return;
    const series = this.series();
    const total = l.totals[i];
    this.activo.set(i);
    this.tip.set({
      x: l.cols[i].cx,
      y: l.yOf(total),
      title: d.title,
      rows: [
        ...d.values.map((v, k) => ({
          label: series[k]?.label ?? '',
          value: fmtInt(v),
          color: series[k]?.color,
          opacity: series[k]?.opacity,
        })),
        { label: 'Total', value: fmtInt(total) },
      ],
    });
  }

  /** El mouse limpia al salir; en tactil el tooltip queda hasta tocar otra zona. */
  protected salir(e: PointerEvent): void {
    if (e.pointerType === 'mouse') this.limpiar();
  }

  protected limpiar(): void {
    this.tip.set(null);
    this.activo.set(-1);
  }
}
