import { ChangeDetectionStrategy, Component, input } from '@angular/core';

/** Tarjeta con titulo y subtitulo que envuelve un grafico o una tabla. */
@Component({
  selector: 'app-panel',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <h3>{{ titulo() }}</h3>
    @if (subtitulo()) {
      <p class="st">{{ subtitulo() }}</p>
    }
    <div class="bd"><ng-content /></div>
  `,
  styles: [
    `
      :host {
        display: block;
        min-width: 0;
        padding: 16px;
        border-radius: 14px;
        background: var(--ion-item-background, #fff);
        box-shadow: 0 0 0 1px rgba(var(--ion-text-color-rgb), 0.06);
      }
      h3 {
        margin: 0;
        font-size: 15px;
        font-weight: 600;
      }
      .st {
        margin: 2px 0 0;
        font-size: 12px;
        color: rgba(var(--ion-text-color-rgb), 0.62);
      }
      .bd {
        margin-top: 12px;
      }
    `,
  ],
})
export class PanelComponent {
  readonly titulo = input.required<string>();
  readonly subtitulo = input('');
}
