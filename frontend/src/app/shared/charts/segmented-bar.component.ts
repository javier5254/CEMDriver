import { ChangeDetectionStrategy, Component, computed, input, signal } from '@angular/core';
import { ChartTooltipComponent } from './chart-tooltip.component';
import { ChartSegment, TooltipState, fmtInt, fmtPct, observeWidth } from './chart-utils';

/**
 * Barra segmentada: un todo dividido en partes proporcionales. Alta (28 px,
 * con tooltip y leyenda) para composiciones, o delgada (8 px) como barra de
 * avance. Si `total` supera la suma de las partes, el resto se dibuja como riel.
 */
@Component({
  selector: 'app-segmented-bar',
  standalone: true,
  imports: [ChartTooltipComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @let l = layout();
    <div class="wrap">
      <svg
        [attr.viewBox]="'0 0 ' + l.w + ' ' + height()"
        [attr.height]="height()"
        width="100%"
        role="img"
        [attr.aria-label]="ariaLabel()"
        (pointerdown)="limpiar()"
      >
        @if (l.resto; as r) {
          <rect class="rail" [attr.x]="r.x" y="0" [attr.width]="r.w" [attr.height]="height()" [attr.rx]="l.rx" />
        }
        @for (b of l.blocks; track b.id) {
          <rect
            [attr.x]="b.x"
            y="0"
            [attr.width]="b.w"
            [attr.height]="height()"
            [attr.rx]="l.rx"
            [style.fill]="b.color"
            [style.fill-opacity]="b.opacity"
            [class.dim]="activo() !== '' && activo() !== b.id"
            (pointerenter)="mostrar(b.id)"
            (pointerdown)="mostrar(b.id); $event.stopPropagation()"
            (pointerleave)="salir($event)"
          />
        }
      </svg>
      @if (tip(); as t) {
        <app-chart-tooltip [x]="t.x" [y]="t.y" [bounds]="l.w" [title]="t.title" [rows]="t.rows" />
      }
    </div>
    @if (legend()) {
      <ul class="lg">
        @for (s of segments(); track s.id) {
          <li [class.cero]="s.value <= 0">
            <i [style.background]="s.color" [style.opacity]="s.opacity ?? 1"></i>
            <span class="nm">{{ s.label }}</span>
            <b>{{ fmt(s.value) }}</b>
            <span class="pc">{{ pct(s.value, l.den) }}</span>
          </li>
        }
      </ul>
    }
  `,
  styles: [
    `
      :host {
        display: block;
        width: 100%;
      }
      .wrap {
        position: relative;
      }
      svg {
        display: block;
        overflow: visible;
      }
      .rail {
        fill: rgba(var(--ion-text-color-rgb), 0.12);
      }
      rect {
        transition: opacity 0.12s;
      }
      rect.dim {
        opacity: 0.45;
      }
      .lg {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 2px 20px;
        margin: 12px 0 0;
        padding: 0;
        list-style: none;
        font-size: 13px;
      }
      .lg li {
        display: grid;
        grid-template-columns: 12px minmax(0, 1fr) auto 54px;
        align-items: center;
        gap: 8px;
        padding: 4px 0;
        border-bottom: 1px solid rgba(var(--ion-text-color-rgb), 0.07);
      }
      .lg i {
        width: 12px;
        height: 12px;
        border-radius: 3px;
      }
      .nm {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
      .pc {
        text-align: right;
        color: rgba(var(--ion-text-color-rgb), 0.62);
      }
      .cero {
        color: rgba(var(--ion-text-color-rgb), 0.55);
      }
    `,
  ],
})
export class SegmentedBarComponent {
  readonly segments = input.required<ChartSegment[]>();
  /** Total de referencia; si es mayor que la suma, el resto se muestra como riel. */
  readonly total = input<number | null>(null);
  readonly height = input(28);
  readonly legend = input(true);
  readonly ariaLabel = input('Barra segmentada');

  protected readonly tip = signal<TooltipState | null>(null);
  protected readonly activo = signal('');
  private readonly width = observeWidth(320);

  protected readonly fmt = fmtInt;
  protected pct(v: number, den: number): string {
    return den > 0 ? fmtPct(v / den) : fmtPct(null);
  }

  protected readonly layout = computed(() => {
    const w = this.width();
    const h = this.height();
    const segs = this.segments();
    const suma = segs.reduce((a, s) => a + Math.max(0, s.value), 0);
    const den = Math.max(this.total() ?? 0, suma);
    const rx = h >= 20 ? 4 : h / 2;
    const vis = segs.filter((s) => s.value > 0);
    let cursor = 0;
    const blocks = vis.map((s, i) => {
      const bw = den > 0 ? (s.value / den) * w : 0;
      const x0 = cursor;
      cursor += bw;
      const ini = i === 0 ? 0 : 1; // 1 px por lado = 2 px de separacion
      const fin = i === vis.length - 1 && cursor >= w - 0.5 ? 0 : 1;
      const x = x0 + ini;
      return {
        id: s.id,
        x,
        w: Math.max(2, bw - ini - fin),
        cx: x0 + bw / 2,
        color: s.color,
        opacity: s.opacity ?? 1,
      };
    });
    const resto =
      den <= 0
        ? { x: 0, w }
        : cursor < w - 1
          ? { x: cursor + (vis.length ? 1 : 0), w: w - cursor - (vis.length ? 1 : 0) }
          : null;
    return { w, rx, den, blocks, resto };
  });

  protected mostrar(id: string): void {
    if (this.height() < 20) return;
    const l = this.layout();
    const s = this.segments().find((x) => x.id === id);
    const b = l.blocks.find((x) => x.id === id);
    if (!s || !b) return;
    this.activo.set(id);
    this.tip.set({
      x: b.cx,
      y: 0,
      title: s.label,
      rows: [
        { label: 'Servicios', value: fmtInt(s.value), color: s.color, opacity: s.opacity },
        { label: 'Participación', value: this.pct(s.value, l.den) },
      ],
    });
  }

  protected salir(e: PointerEvent): void {
    if (e.pointerType === 'mouse') this.limpiar();
  }

  protected limpiar(): void {
    this.tip.set(null);
    this.activo.set('');
  }
}
