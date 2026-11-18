import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';
import { TooltipRow } from './chart-utils';

/**
 * Tooltip HTML posicionado de forma absoluta dentro del contenedor relativo de
 * un grafico. Solo realza: todos los valores tambien estan en la tabla oculta
 * (lectores de pantalla) o en etiquetas visibles.
 */
@Component({
  selector: 'app-chart-tooltip',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="tip" aria-hidden="true" [class.below]="below()" [style.left.px]="left()" [style.top.px]="y()">
      <div class="tt">{{ title() }}</div>
      @for (r of rows(); track r.label) {
        <div class="tr">
          @if (r.color) {
            <i class="sw" [style.background]="r.color" [style.opacity]="r.opacity ?? 1"></i>
          } @else {
            <i class="sw none"></i>
          }
          <span class="tl">{{ r.label }}</span>
          <b class="tv">{{ r.value }}</b>
        </div>
      }
    </div>
  `,
  styles: [
    `
      .tip {
        position: absolute;
        z-index: 10;
        width: max-content;
        max-width: 220px;
        transform: translate(-50%, calc(-100% - 10px));
        padding: 8px 10px;
        border-radius: 10px;
        font-size: 12px;
        line-height: 1.35;
        color: var(--ion-text-color);
        background: var(--ion-item-background, #fff);
        box-shadow:
          0 0 0 1px rgba(var(--ion-text-color-rgb), 0.12),
          0 6px 20px rgba(0, 0, 0, 0.18);
        pointer-events: none;
        font-variant-numeric: tabular-nums;
      }
      .below {
        transform: translate(-50%, 10px);
      }
      .tt {
        margin-bottom: 4px;
        font-weight: 600;
      }
      .tr {
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .sw {
        flex: none;
        width: 8px;
        height: 8px;
        border-radius: 2px;
      }
      .sw.none {
        background: transparent;
      }
      .tl {
        flex: 1;
        color: rgba(var(--ion-text-color-rgb), 0.7);
      }
      .tv {
        margin-left: 12px;
        font-weight: 600;
      }
    `,
  ],
})
export class ChartTooltipComponent {
  /** Posicion del punto de anclaje en px, relativa al contenedor del grafico. */
  readonly x = input.required<number>();
  readonly y = input.required<number>();
  /** Ancho del contenedor, para que el tooltip no se salga por los lados. */
  readonly bounds = input.required<number>();
  readonly title = input('');
  readonly rows = input<TooltipRow[]>([]);

  protected readonly left = computed(() => {
    const half = 100;
    const b = this.bounds();
    return b <= half * 2 ? b / 2 : Math.min(Math.max(this.x(), half), b - half);
  });
  protected readonly below = computed(() => this.y() < 96);
}
