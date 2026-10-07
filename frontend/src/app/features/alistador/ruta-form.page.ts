import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonItem,
  IonLabel,
  IonInput,
  IonButton,
  IonText,
  IonSpinner,
  IonList,
  IonBadge,
  IonNote,
  IonCheckbox,
} from '@ionic/angular';
import { RutasService } from '../../core/services/rutas.service';
import { ServiciosService } from '../../core/services/servicios.service';
import { Ruta, Servicio } from '../../core/models';
import { estadoColor, extractErrorMessage } from '../../core/utils';

@Component({
  selector: 'app-ruta-form',
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
    IonNote,
    IonCheckbox,
  ],
  template: `
    <div class="ion-padding">
      <h2>Nueva ruta</h2>

      <form (ngSubmit)="crearRuta()" *ngIf="!rutaCreada">
        <ion-item>
          <ion-label position="floating">ID de motorizado</ion-label>
          <ion-input [(ngModel)]="motorizadoId" name="motorizado" type="number" required></ion-input>
        </ion-item>
        <ion-note class="ion-padding-start" color="medium" style="display:block; font-size: 11px;">
          El listado de usuarios solo es accesible por el rol ADMIN; pide el ID numerico del motorizado al
          administrador.
        </ion-note>
        <ion-item>
          <ion-label position="floating">Fecha</ion-label>
          <ion-input [(ngModel)]="fecha" name="fecha" type="date" required></ion-input>
        </ion-item>

        <ion-button expand="block" type="submit" class="ion-margin-top" [disabled]="saving">
          {{ saving ? 'Creando...' : 'Crear ruta' }}
        </ion-button>
      </form>

      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>

      <div *ngIf="rutaCreada">
        <ion-text color="success"><p>Ruta #{{ rutaCreada.id }} creada. Ahora asigna servicios sin ruta:</p></ion-text>

        <ion-spinner *ngIf="loadingServicios"></ion-spinner>

        <ion-list *ngIf="!loadingServicios">
          <ion-item *ngFor="let s of serviciosSinRuta">
            <ion-checkbox slot="start" [(ngModel)]="seleccionados[s.id]" name="sel{{ s.id }}"></ion-checkbox>
            <ion-label>
              <h3>#{{ s.id }} - {{ s.tipo }} - {{ s.zona }}</h3>
              <p>{{ s.direccion_origen || s.direccion_destino }}</p>
            </ion-label>
            <ion-badge slot="end" [color]="colorFor(s.estado)">{{ s.estado }}</ion-badge>
          </ion-item>
        </ion-list>

        <ion-button expand="block" (click)="asignarSeleccionados()" [disabled]="asignando">
          {{ asignando ? 'Asignando...' : 'Asignar seleccionados a la ruta #' + rutaCreada.id }}
        </ion-button>

        <ion-text color="success" *ngIf="asignados.length">
          <p>Asignados: {{ asignados.join(', ') }}</p>
        </ion-text>
      </div>
    </div>
  `,
})
export class RutaFormPage implements OnInit {
  motorizadoId: number | null = null;
  fecha = '';
  saving = false;
  error = '';

  rutaCreada: Ruta | null = null;
  serviciosSinRuta: Servicio[] = [];
  seleccionados: Record<number, boolean> = {};
  loadingServicios = false;
  asignando = false;
  asignados: number[] = [];

  constructor(
    private rutasService: RutasService,
    private serviciosService: ServiciosService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {}

  crearRuta(): void {
    if (!this.motorizadoId || !this.fecha) return;
    this.saving = true;
    this.error = '';
    this.rutasService.create({ motorizado: this.motorizadoId, fecha: this.fecha }).subscribe({
      next: (r) => {
        this.saving = false;
        this.rutaCreada = r;
        this.cargarServiciosSinRuta();
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.saving = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  cargarServiciosSinRuta(): void {
    this.loadingServicios = true;
    this.serviciosService.list().subscribe({
      next: (data) => {
        this.loadingServicios = false;
        this.serviciosSinRuta = data.filter((s) => !s.ruta);
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.loadingServicios = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  colorFor(estado: string): string {
    return estadoColor(estado as any);
  }

  asignarSeleccionados(): void {
    if (!this.rutaCreada) return;
    const ids = Object.keys(this.seleccionados)
      .filter((k) => this.seleccionados[+k])
      .map((k) => +k);
    if (!ids.length) return;

    this.asignando = true;
    this.error = '';
    let pending = ids.length;
    ids.forEach((id) => {
      this.serviciosService.asignarRuta(id, this.rutaCreada!.id).subscribe({
        next: () => {
          this.asignados.push(id);
          pending -= 1;
          if (pending === 0) {
            this.asignando = false;
            this.cargarServiciosSinRuta();
          }
          this.cdr.detectChanges();
        },
        error: (err) => {
          pending -= 1;
          this.error = extractErrorMessage(err);
          if (pending === 0) this.asignando = false;
          this.cdr.detectChanges();
        },
      });
    });
  }
}
