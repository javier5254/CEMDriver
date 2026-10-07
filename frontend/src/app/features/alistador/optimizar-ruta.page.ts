import { ChangeDetectorRef, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonItem, IonLabel, IonInput, IonButton, IonText, IonSpinner, IonList, IonBadge } from '@ionic/angular';
import {
  OptimizacionService,
  OptimizacionRutaResponse,
} from '../../core/services/optimizacion.service';
import { extractErrorMessage } from '../../core/utils';

@Component({
  selector: 'app-optimizar-ruta',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonItem,
    IonLabel,
    IonInput,
    IonButton,
    IonText,
    IonSpinner,
    IonList,
    IonBadge,
  ],
  template: `
    <div class="ion-padding">
      <h2>Optimizar ruta</h2>
      <p>
        Sugiere un orden de visita eficiente para los servicios ya asignados a una ruta, a partir de
        las direcciones geocodificadas. Es solo una sugerencia: no modifica la ruta ni los servicios.
      </p>

      <ion-item>
        <ion-label position="floating">ID de ruta</ion-label>
        <ion-input
          [(ngModel)]="rutaId"
          name="rutaId"
          type="number"
          (keyup.enter)="optimizar()"
        ></ion-input>
      </ion-item>

      <ion-button expand="block" class="ion-margin-top" [disabled]="loading || !rutaId" (click)="optimizar()">
        {{ loading ? 'Optimizando...' : 'Optimizar ruta' }}
      </ion-button>

      <ion-spinner *ngIf="loading"></ion-spinner>
      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>

      <div *ngIf="resultado && !loading" class="ion-margin-top">
        <ion-text color="success">
          <p>
            Distancia total estimada:
            <strong>{{ resultado.distancia_total_km }} km</strong>
            ({{ resultado.orden_sugerido.length }} parada(s))
          </p>
        </ion-text>

        <ion-list *ngIf="resultado.orden_sugerido.length">
          <ion-item *ngFor="let punto of resultado.orden_sugerido; let i = index">
            <ion-badge slot="start" color="primary">{{ i + 1 }}</ion-badge>
            <ion-label>
              <h3>Servicio #{{ punto.servicio_id }}</h3>
              <p>{{ punto.direccion }}</p>
              <p>{{ punto.lat }}, {{ punto.lng }}</p>
            </ion-label>
          </ion-item>
        </ion-list>

        <ion-text color="medium" *ngIf="!resultado.orden_sugerido.length">
          <p>Ningun servicio de esta ruta pudo geocodificarse.</p>
        </ion-text>

        <div *ngIf="resultado.no_geocodificados.length" class="ion-margin-top">
          <ion-text color="warning">
            <p>No se pudieron geocodificar (quedan fuera del orden sugerido):</p>
          </ion-text>
          <ion-list>
            <ion-item *ngFor="let f of resultado.no_geocodificados">
              <ion-label>
                <h3>Servicio #{{ f.servicio_id }}</h3>
                <p>{{ f.direccion }}</p>
              </ion-label>
            </ion-item>
          </ion-list>
        </div>
      </div>
    </div>
  `,
})
export class OptimizarRutaPage {
  rutaId: number | null = null;
  loading = false;
  error = '';
  resultado: OptimizacionRutaResponse | null = null;

  constructor(
    private optimizacionService: OptimizacionService,
    private cdr: ChangeDetectorRef,
  ) {}

  optimizar(): void {
    if (!this.rutaId) return;
    this.loading = true;
    this.error = '';
    this.resultado = null;
    this.optimizacionService.optimizar(this.rutaId).subscribe({
      next: (data) => {
        this.loading = false;
        this.resultado = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.loading = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }
}
