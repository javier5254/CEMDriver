import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { SegmentedBarComponent } from '../../shared/charts/segmented-bar.component';
import { ChartSegment } from '../../shared/charts/chart-utils';

export interface FilaMotorizado {
  id: number;
  nombre: string;
  servicios: string;
  cerrados: string;
  novedad: string;
  /** Servicios totales (denominador de la barra de avance). */
  total: number;
  segs: ChartSegment[];
  aria: string;
}

/** Tabla compacta de motorizados con barra de avance de cierres exitosos. */
@Component({
  selector: 'app-motorizados-table',
  standalone: true,
  imports: [SegmentedBarComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <table>
      <colgroup>
        <col style="width: 33%" />
        <col style="width: 25%" />
        <col />
        <col />
        <col />
      </colgroup>
      <thead>
        <tr>
          <th scope="col">Motorizado</th>
          <th scope="col">Avance</th>
          <th scope="col">Servicios</th>
          <th scope="col">Cerrados</th>
          <th scope="col">Novedad</th>
        </tr>
      </thead>
      <tbody>
        @for (m of filas(); track m.id) {
          <tr>
            <th scope="row" [title]="m.nombre">{{ m.nombre }}</th>
            <td>
              <app-segmented-bar [segments]="m.segs" [total]="m.total" [height]="8" [legend]="false" [ariaLabel]="m.aria" />
            </td>
            <td>{{ m.servicios }}</td>
            <td>{{ m.cerrados }}</td>
            <td>{{ m.novedad }}</td>
          </tr>
        }
      </tbody>
    </table>
  `,
  styles: [
    `
      table {
        width: 100%;
        table-layout: fixed;
        border-collapse: collapse;
        font-size: 13px;
      }
      th,
      td {
        padding: 8px 0;
        text-align: right;
        border-top: 1px solid rgba(var(--ion-text-color-rgb), 0.07);
      }
      thead th {
        padding: 0 0 6px;
        border: 0;
        font-size: 11px;
        font-weight: 500;
        color: rgba(var(--ion-text-color-rgb), 0.62);
      }
      th:first-child,
      td:first-child {
        text-align: left;
      }
      tbody th {
        overflow: hidden;
        font-weight: 400;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
      td:nth-child(2) {
        padding: 8px 12px;
      }
    `,
  ],
})
export class MotorizadosTableComponent {
  readonly filas = input.required<FilaMotorizado[]>();
}
