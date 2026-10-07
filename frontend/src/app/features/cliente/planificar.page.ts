import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlanificarFormComponent } from '../../shared/planificar-form.component';

@Component({
  selector: 'app-planificar',
  standalone: true,
  imports: [CommonModule, PlanificarFormComponent],
  template: `
    <div class="ion-padding">
      <h2>Planificar recoleccion</h2>
      <p style="color: var(--ion-color-medium); font-size: 13px;">
        Elige tu zona y una fecha disponible segun la matriz de cobertura (respeta el leadtime configurado).
      </p>
      <app-planificar-form></app-planificar-form>
    </div>
  `,
})
export class PlanificarPage {}
