import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
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
  IonSelect,
  IonSelectOption,
} from '@ionic/angular';
import { ServiciosService } from '../../core/services/servicios.service';
import { RutasService } from '../../core/services/rutas.service';
import { Ruta, Servicio } from '../../core/models';
import { estadoColor, extractErrorMessage } from '../../core/utils';

@Component({
  selector: 'app-alistador-servicios-list',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,
    IonList,
    IonItem,
    IonLabel,
    IonBadge,
    IonButton,
    IonIcon,
    IonSpinner,
    IonText,
    IonSelect,
    IonSelectOption,
  ],
  template: `
    <div class="ion-padding">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2>Servicios</h2>
        <ion-button routerLink="/alistador/servicios/nuevo">
          <ion-icon slot="start" name="add-outline"></ion-icon>
          Nuevo servicio
        </ion-button>
      </div>

      <ion-spinner *ngIf="loading"></ion-spinner>
      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>

      <ion-list *ngIf="!loading && !error">
        <ion-item *ngFor="let s of servicios">
          <ion-label>
            <h3>#{{ s.id }} - {{ s.tipo }} - {{ s.zona }}</h3>
            <p>Cliente: {{ s.cliente_detalle?.nombre || s.cliente }}</p>
            <p>{{ s.direccion_origen || s.direccion_destino }} - Agenda: {{ s.fecha_agenda }}</p>
            <p *ngIf="s.ruta">Ruta asignada: #{{ s.ruta }}</p>
          </ion-label>
          <ion-badge slot="end" [color]="colorFor(s.estado)">{{ s.estado }}</ion-badge>

          <div slot="end" style="display:flex; align-items:center; gap:4px;" *ngIf="!s.ruta">
            <ion-select
              [(ngModel)]="assign[s.id]"
              placeholder="Ruta"
              style="min-width: 90px;"
              interface="popover"
            >
              <ion-select-option *ngFor="let r of rutas" [value]="r.id">
                #{{ r.id }} - {{ r.motorizado_detalle?.nombre || r.motorizado }}
              </ion-select-option>
            </ion-select>
            <ion-button size="small" (click)="asignar(s)" [disabled]="!assign[s.id]">Asignar</ion-button>
          </div>
        </ion-item>
      </ion-list>
    </div>
  `,
})
export class ServiciosListPage implements OnInit {
  servicios: Servicio[] = [];
  rutas: Ruta[] = [];
  assign: Record<number, number | null> = {};
  loading = false;
  error = '';

  constructor(
    private serviciosService: ServiciosService,
    private rutasService: RutasService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.fetch();
    this.rutasService.list().subscribe({
      next: (r) => {
        this.rutas = r;
        this.cdr.detectChanges();
      },
      error: () => {},
    });
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

  asignar(s: Servicio): void {
    const rutaId = this.assign[s.id];
    if (!rutaId) return;
    this.serviciosService.asignarRuta(s.id, rutaId).subscribe({
      next: () => this.fetch(),
      error: (err) => {
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }
}
