import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { RingGaugeComponent } from './ring-gauge.component';

/** Tarjeta de indicador: etiqueta, valor, nota y (opcional) anillo para tasas. */
@Component({
  selector: 'app-kpi-tile',
  standalone: true,
  imports: [RingGaugeComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="tx">
      <div class="lb">
        @if (dot()) {
          <i class="dot" [style.background]="dot()"></i>
        }
        {{ label() }}
      </div>
      <div class="v">{{ value() }}</div>
      <div class="h">{{ hint() }}</div>
    </div>
    @if (ring() !== undefined) {
      <app-ring-gauge [value]="ring() ?? null" [color]="ringColor()" [ariaLabel]="label()" />
    }
  `,
  styles: [
    `
      :host {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 8px;
        min-width: 0;
        padding: 14px;
        border-radius: 14px;
        background: var(--ion-item-background, #fff);
        box-shadow: 0 0 0 1px rgba(var(--ion-text-color-rgb), 0.06);
      }
      .tx {
        min-width: 0;
      }
      .lb {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        color: rgba(var(--ion-text-color-rgb), 0.68);
      }
      .dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
      }
      .v {
        margin: 4px 0 2px;
        font-size: 28px;
        font-weight: 700;
        line-height: 1.15;
        letter-spacing: -0.01em;
      }
      .h {
        font-size: 12px;
        line-height: 1.3;
        color: rgba(var(--ion-text-color-rgb), 0.62);
      }
    `,
  ],
})
export class KpiTileComponent {
  readonly label = input.required<string>();
  readonly value = input.required<string>();
  readonly hint = input('');
  /** Color del punto semantico junto a la etiqueta. */
  readonly dot = input('');
  /** Fraccion 0..1 del anillo; `undefined` oculta el anillo, `null` lo muestra sin datos. */
  readonly ring = input<number | null | undefined>(undefined);
  readonly ringColor = input('var(--ion-color-success)');
}
