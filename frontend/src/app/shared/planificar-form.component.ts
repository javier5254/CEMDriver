import { ChangeDetectorRef, Component, EventEmitter, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonItem,
  IonLabel,
  IonInput,
  IonSelect,
  IonSelectOption,
  IonButton,
  IonText,
  IonSpinner,
} from '@ionic/angular';
import { CoberturaService } from '../core/services/cobertura.service';
import { ServiciosService } from '../core/services/servicios.service';
import { Cobertura, Servicio } from '../core/models';
import { extractErrorMessage } from '../core/utils';

/**
 * Formulario reusable de "planificar recoleccion" (RF-17). Usado tanto en la
 * pantalla dedicada del cliente.
 */
@Component({
  selector: 'app-planificar-form',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonItem,
    IonLabel,
    IonInput,
    IonSelect,
    IonSelectOption,
    IonButton,
    IonText,
    IonSpinner,
  ],
  template: `
    <div>
      <ion-item>
        <ion-label>Zona</ion-label>
        <ion-select [(ngModel)]="zona" (ionChange)="onZonaChange()">
          <ion-select-option *ngFor="let z of zonas" [value]="z.zona">{{ z.zona }}</ion-select-option>
        </ion-select>
      </ion-item>

      <ion-item>
        <ion-label position="floating">Direccion de recoleccion</ion-label>
        <ion-input [(ngModel)]="direccionOrigen"></ion-input>
      </ion-item>

      <ion-item>
        <ion-label>Fecha disponible</ion-label>
        <ion-select [(ngModel)]="fechaAgenda" [disabled]="!fechasDisponibles.length">
          <ion-select-option *ngFor="let f of fechasDisponibles" [value]="f">{{ f }}</ion-select-option>
        </ion-select>
      </ion-item>
      <ion-text color="medium" *ngIf="zona && !loadingAgenda && !fechasDisponibles.length">
        <p style="font-size: 12px;">No hay fechas disponibles para esta zona.</p>
      </ion-text>
      <ion-spinner *ngIf="loadingAgenda" name="dots"></ion-spinner>

      <ion-button
        expand="block"
        class="ion-margin-top"
        [disabled]="!zona || !direccionOrigen || !fechaAgenda || saving"
        (click)="submit()"
      >
        {{ saving ? 'Enviando...' : 'Planificar recoleccion' }}
      </ion-button>

      <ion-text color="success" *ngIf="creado"><p>Servicio #{{ creado.id }} creado ({{ creado.estado }}).</p></ion-text>
      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>
    </div>
  `,
})
export class PlanificarFormComponent implements OnInit {
  @Output() creadoEvent = new EventEmitter<Servicio>();

  zonas: Cobertura[] = [];
  zona = '';
  direccionOrigen = '';
  fechasDisponibles: string[] = [];
  fechaAgenda = '';
  loadingAgenda = false;
  saving = false;
  error = '';
  creado: Servicio | null = null;

  constructor(
    private coberturaService: CoberturaService,
    private serviciosService: ServiciosService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.coberturaService.list().subscribe({
      next: (z) => {
        this.zonas = z;
        this.cdr.detectChanges();
      },
      error: () => {},
    });
  }

  onZonaChange(): void {
    this.fechaAgenda = '';
    this.fechasDisponibles = [];
    if (!this.zona) return;
    this.loadingAgenda = true;
    this.coberturaService.agendaDisponible(this.zona).subscribe({
      next: (res) => {
        this.loadingAgenda = false;
        this.fechasDisponibles = res.fechas_disponibles;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.loadingAgenda = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  submit(): void {
    this.saving = true;
    this.error = '';
    this.creado = null;
    this.serviciosService
      .planificar({
        zona: this.zona,
        direccion_origen: this.direccionOrigen,
        fecha_agenda: this.fechaAgenda,
      })
      .subscribe({
        next: (s) => {
          this.saving = false;
          this.creado = s;
          this.creadoEvent.emit(s);
          this.cdr.detectChanges();
        },
        error: (err) => {
          this.saving = false;
          this.error = extractErrorMessage(err);
          this.cdr.detectChanges();
        },
      });
  }
}
