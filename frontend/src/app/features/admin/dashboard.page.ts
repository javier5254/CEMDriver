import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  IonGrid,
  IonRow,
  IonCol,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonSpinner,
  IonText,
} from '@ionic/angular';
import { ServiciosService } from '../../core/services/servicios.service';
import { EstadoServicio, Servicio } from '../../core/models';
import { estadoColor, extractErrorMessage } from '../../core/utils';

const ESTADOS: EstadoServicio[] = [
  'CREADO',
  'ASIGNADO',
  'RECIBIDO_CENTRO',
  'EN_TRANSITO',
  'ENTREGADO',
  'RECOLECTADO',
  'NOVEDAD',
  'DEVUELTO',
];

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    IonGrid,
    IonRow,
    IonCol,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
    IonSpinner,
    IonText,
  ],
  template: `
    <div class="ion-padding">
      <h2>Panel de servicios</h2>

      <ion-spinner *ngIf="loading"></ion-spinner>
      <ion-text color="danger" *ngIf="error">
        <p>{{ error }}</p>
      </ion-text>

      <ion-grid *ngIf="!loading && !error">
        <ion-row>
          <ion-col size="6" size-md="3" *ngFor="let e of estados">
            <ion-card [color]="colorFor(e)">
              <ion-card-header>
                <ion-card-title style="font-size: 14px;">{{ e }}</ion-card-title>
              </ion-card-header>
              <ion-card-content style="font-size: 28px; font-weight: bold;">
                {{ counts[e] || 0 }}
              </ion-card-content>
            </ion-card>
          </ion-col>
        </ion-row>
      </ion-grid>

      <p><strong>Total servicios:</strong> {{ total }}</p>
    </div>
  `,
})
export class AdminDashboardPage implements OnInit {
  estados = ESTADOS;
  counts: Partial<Record<EstadoServicio, number>> = {};
  total = 0;
  loading = false;
  error = '';

  constructor(
    private serviciosService: ServiciosService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.loading = true;
    this.serviciosService.list().subscribe({
      next: (servicios: Servicio[]) => {
        this.loading = false;
        this.total = servicios.length;
        const counts: Partial<Record<EstadoServicio, number>> = {};
        for (const s of servicios) {
          counts[s.estado] = (counts[s.estado] || 0) + 1;
        }
        this.counts = counts;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.loading = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  colorFor(estado: EstadoServicio): string {
    return estadoColor(estado);
  }
}
