import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import {
  IonList,
  IonItem,
  IonLabel,
  IonBadge,
  IonButton,
  IonIcon,
  IonSpinner,
  IonText,
} from '@ionic/angular';
import { ServiciosService } from '../../core/services/servicios.service';
import { Servicio } from '../../core/models';
import { estadoColor, extractErrorMessage } from '../../core/utils';

@Component({
  selector: 'app-cliente-servicios-list',
  standalone: true,
  imports: [CommonModule, RouterLink, IonList, IonItem, IonLabel, IonBadge, IonButton, IonIcon, IonSpinner, IonText],
  template: `
    <div class="ion-padding">
      <h2>Mis servicios</h2>

      <ion-spinner *ngIf="loading"></ion-spinner>
      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>
      <ion-text color="medium" *ngIf="!loading && !error && servicios.length === 0">
        <p>Aun no tienes servicios. Prueba planificar una recoleccion.</p>
      </ion-text>

      <ion-list *ngIf="!loading && !error">
        <ion-item *ngFor="let s of servicios">
          <ion-label>
            <h3>#{{ s.id }} - {{ s.tipo === 'ENTREGA' ? 'Entrega' : 'Recoleccion' }}</h3>
            <p>{{ s.direccion_origen || s.direccion_destino }} - Zona: {{ s.zona }}</p>
            <p>Agenda: {{ s.fecha_agenda }}</p>
          </ion-label>
          <ion-badge slot="end" [color]="colorFor(s.estado)">{{ s.estado }}</ion-badge>
          <ion-button slot="end" fill="clear" size="small" [routerLink]="['/cliente/servicios', s.id, 'tracking']">
            <ion-icon slot="icon-only" name="map-outline"></ion-icon>
          </ion-button>
          <ion-button slot="end" fill="clear" size="small" [routerLink]="['/cliente/servicios', s.id, 'chat']">
            <ion-icon slot="icon-only" name="chatbubble-outline"></ion-icon>
          </ion-button>
        </ion-item>
      </ion-list>
    </div>
  `,
})
export class ClienteServiciosListPage implements OnInit {
  servicios: Servicio[] = [];
  loading = false;
  error = '';

  constructor(
    private serviciosService: ServiciosService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.loading = true;
    this.serviciosService.list().subscribe({
      next: (data) => {
        this.loading = false;
        this.servicios = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.loading = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  colorFor(estado: string): string {
    return estadoColor(estado as any);
  }
}
