import { ChangeDetectionStrategy, Component, input } from '@angular/core';

export interface StatItem {
  label: string;
  value: string;
  /** Color del punto semantico (p. ej. ambar para "pendiente"). */
  dot?: string;
}

/** Lista de cifras (valor grande + etiqueta) en una rejilla que se adapta al ancho. */
@Component({
  selector: 'app-stat-list',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <dl>
      @for (s of items(); track s.label) {
        <div>
          <dd>
            @if (s.dot) {
              <i [style.background]="s.dot"></i>
            }
            {{ s.value }}
          </dd>
          <dt>{{ s.label }}</dt>
        </div>
      }
    </dl>
  `,
  styles: [
    `
      dl {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
        gap: 12px;
        margin: 0;
      }
      dd {
        display: flex;
        align-items: center;
        gap: 6px;
        margin: 0;
        font-size: 22px;
        font-weight: 700;
      }
      dt {
        font-size: 12px;
        color: rgba(var(--ion-text-color-rgb), 0.68);
      }
      i {
        flex: none;
        width: 8px;
        height: 8px;
        border-radius: 50%;
      }
    `,
  ],
})
export class StatListComponent {
  readonly items = input.required<StatItem[]>();
}
