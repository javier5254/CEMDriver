import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import {
  IonList,
  IonItem,
  IonLabel,
  IonBadge,
  IonIcon,
  IonSpinner,
  IonText,
  IonButton,
} from '@ionic/angular';
import { ServiciosService } from '../../core/services/servicios.service';
import { Servicio } from '../../core/models';
import { estadoColor, extractErrorMessage } from '../../core/utils';

@Component({
  selector: 'app-motorizado-servicios-list',
  standalone: true,
  imports: [CommonModule, RouterLink, IonList, IonItem, IonLabel, IonBadge, IonIcon, IonSpinner, IonText, IonButton],
  template: `
    <div class="ion-padding">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2>Mis servicios</h2>
        <ion-button size="small" fill="clear" (click)="fetch()">
          <ion-icon slot="icon-only" name="refresh-outline"></ion-icon>
        </ion-button>
      </div>

      <ion-spinner *ngIf="loading"></ion-spinner>
      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>
      <ion-text color="medium" *ngIf="!loading && !error && servicios.length === 0">
        <p>No tienes servicios asignados.</p>
      </ion-text>

      <ion-list *ngIf="!loading && !error">
        <ion-item *ngFor="let s of servicios" [routerLink]="['/motorizado/servicios', s.id]" button>
          <ion-icon
            slot="start"
            [name]="s.tipo === 'ENTREGA' ? 'cube-outline' : 'bicycle-outline'"
            [color]="s.tipo === 'ENTREGA' ? 'primary' : 'tertiary'"
            style="font-size: 28px;"
          ></ion-icon>
          <ion-label>
            <h3>#{{ s.id }} - {{ s.tipo === 'ENTREGA' ? 'Entrega' : 'Recoleccion' }}</h3>
            <p>{{ s.tipo === 'ENTREGA' ? s.direccion_destino : s.direccion_origen }}</p>
            <p>Zona: {{ s.zona }} - Agenda: {{ s.fecha_agenda }}</p>
          </ion-label>
          <ion-badge slot="end" [color]="colorFor(s.estado)">{{ s.estado }}</ion-badge>
        </ion-item>
      </ion-list>
    </div>
  `,
})
export class MotorizadoServiciosListPage implements OnInit {
  servicios: Servicio[] = [];
  loading = false;
  error = '';

  constructor(
    private serviciosService: ServiciosService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.fetch();
  }

  fetch(): void {
    this.loading = true;
    this.error = '';
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
