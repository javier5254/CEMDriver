import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';
import { ChartSeries, observeWidth } from './chart-utils';

export interface HBarValue {
  value: number;
  color: string;
  opacity?: number | string;
}

export interface HBarRow {
  id: string;
  label: string;
  /** Valor visible a la derecha de la etiqueta (ya formateado). */
  valueText: string;
  /** Linea secundaria con los valores de cada barra (ya formateada). */
  sub?: string;
  /** Largo del riel de la fila (p. ej. el total de la zona); por defecto, toda la escala. */
  ref?: number;
  /** Una barra por linea; todas comparten la misma escala. */
  bars: HBarValue[];
}

const BAR_H = 8;
const BAR_GAP = 3;

/** Barra horizontal: base recta a la izquierda y extremo derecho redondeado. */
function hPath(w: number, h: number): string {
  const r = Math.min(4, h / 2, w);
  const f = (n: number) => +n.toFixed(2);
  if (w <= 0) return '';
  if (r <= 0.5) return `M0,0H${f(w)}V${h}H0Z`;
  return `M0,0H${f(w - r)}Q${f(w)},0 ${f(w)},${r}V${f(h - r)}Q${f(w)},${h} ${f(w - r)},${h}H0Z`;
}

/**
 * Lista de barras horizontales (zonas, novedades, etc.). Cada fila lleva su
 * etiqueta y valores como texto real (accesible); el SVG solo dibuja las barras.
 */
@Component({
  selector: 'app-hbar-list',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @let l = layout();
    @if (legend().length) {
      <ul class="lg">
        @for (s of legend(); track s.label) {
          <li><i [style.background]="s.color" [style.opacity]="s.opacity ?? 1"></i>{{ s.label }}</li>
        }
      </ul>
    }
    <ol class="rows">
      @for (r of l.rows; track r.id) {
        <li>
          <div class="hd">
            <span class="lb" [title]="r.label">{{ r.label }}</span>
            <b class="vl">{{ r.valueText }}</b>
          </div>
          <svg [attr.viewBox]="'0 0 ' + l.w + ' ' + r.h" [attr.height]="r.h" width="100%" aria-hidden="true">
            @for (b of r.bars; track $index) {
              <g [attr.transform]="'translate(0 ' + b.y + ')'">
                <path class="rail" [attr.d]="b.rail" />
                <path [attr.d]="b.d" [style.fill]="b.color" [style.fill-opacity]="b.opacity" />
              </g>
            }
          </svg>
          @if (r.sub) {
            <div class="sb">{{ r.sub }}</div>
          }
        </li>
      }
    </ol>
  `,
  styles: [
    `
      :host {
        display: block;
        width: 100%;
      }
      .rows {
        margin: 0;
        padding: 0;
        list-style: none;
        display: grid;
        gap: 12px;
      }
      .hd {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 4px;
        font-size: 13px;
      }
      .lb {
        min-width: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
      .vl {
        flex: none;
      }
      svg {
        display: block;
      }
      .rail {
        fill: rgba(var(--ion-text-color-rgb), 0.1);
      }
      .sb {
        margin-top: 3px;
        font-size: 12px;
        color: rgba(var(--ion-text-color-rgb), 0.62);
      }
      .lg {
        display: flex;
        flex-wrap: wrap;
        gap: 4px 16px;
        margin: 0 0 12px;
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
    `,
  ],
})
export class HBarListComponent {
  readonly rows = input.required<HBarRow[]>();
  readonly legend = input<ChartSeries[]>([]);
  private readonly width = observeWidth(320);

  protected readonly layout = computed(() => {
    const w = this.width();
    const rows = this.rows();
    let max = 1;
    for (const r of rows) {
      max = Math.max(max, r.ref ?? 0, ...r.bars.map((b) => b.value));
    }
    const px = (v: number) => (v <= 0 ? 0 : Math.min(w, Math.max(3, (v / max) * w)));
    return {
      w,
      rows: rows.map((r) => {
        const n = r.bars.length;
        return {
          id: r.id,
          label: r.label,
          valueText: r.valueText,
          sub: r.sub,
          h: n * BAR_H + (n - 1) * BAR_GAP,
          bars: r.bars.map((b, i) => ({
            y: i * (BAR_H + BAR_GAP),
            rail: hPath(r.ref != null ? px(r.ref) : w, BAR_H),
            d: hPath(px(b.value), BAR_H),
            color: b.color,
            opacity: b.opacity ?? 1,
          })),
        };
      }),
    };
  });
}
