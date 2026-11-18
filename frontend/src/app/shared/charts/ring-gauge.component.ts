import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';

/** Medidor de anillo para tasas (0..1). El riel es el mismo color a baja opacidad. */
@Component({
  selector: 'app-ring-gauge',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <svg
      [attr.width]="size()"
      [attr.height]="size()"
      [attr.viewBox]="'0 0 ' + size() + ' ' + size()"
      role="img"
      [attr.aria-label]="ariaLabel()"
    >
      <circle
        [attr.cx]="half()"
        [attr.cy]="half()"
        [attr.r]="radius()"
        fill="none"
        [attr.stroke-width]="stroke()"
        [style.stroke]="color()"
        stroke-opacity="0.18"
      />
      @if (dash(); as d) {
        <circle
          [attr.cx]="half()"
          [attr.cy]="half()"
          [attr.r]="radius()"
          fill="none"
          stroke-linecap="round"
          [attr.stroke-width]="stroke()"
          [style.stroke]="color()"
          [attr.stroke-dasharray]="d"
          [attr.transform]="'rotate(-90 ' + half() + ' ' + half() + ')'"
        />
      }
    </svg>
  `,
  styles: [':host{display:inline-flex;flex:none}svg{display:block}'],
})
export class RingGaugeComponent {
  /** Fraccion 0..1; null = sin datos (solo riel). */
  readonly value = input<number | null>(null);
  readonly color = input('var(--ion-color-success)');
  readonly size = input(48);
  readonly stroke = input(6);
  readonly ariaLabel = input('Medidor');

  protected readonly half = computed(() => this.size() / 2);
  protected readonly radius = computed(() => (this.size() - this.stroke()) / 2);
  protected readonly dash = computed(() => {
    const v = this.value();
    if (v == null || !isFinite(v) || v <= 0.002) return '';
    const c = 2 * Math.PI * this.radius();
    return `${(Math.min(1, v) * c).toFixed(2)} ${c.toFixed(2)}`;
  });
}
