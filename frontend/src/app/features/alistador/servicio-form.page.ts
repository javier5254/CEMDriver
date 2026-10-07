import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import {
  IonItem,
  IonLabel,
  IonInput,
  IonSelect,
  IonSelectOption,
  IonButton,
  IonText,
  IonNote,
} from '@ionic/angular';
import { ServiciosService } from '../../core/services/servicios.service';
import { CoberturaService } from '../../core/services/cobertura.service';
import { ProductosService } from '../../core/services/productos.service';
import { Cobertura, Producto, TipoServicio } from '../../core/models';
import { extractErrorMessage } from '../../core/utils';

@Component({
  selector: 'app-servicio-form',
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
    IonNote,
  ],
  template: `
    <div class="ion-padding">
      <h2>Nuevo servicio</h2>

      <form (ngSubmit)="save()">
        <ion-item>
          <ion-label>Tipo</ion-label>
          <ion-select [(ngModel)]="model.tipo" name="tipo" required>
            <ion-select-option value="ENTREGA">Entrega</ion-select-option>
            <ion-select-option value="RECOLECCION">Recoleccion</ion-select-option>
          </ion-select>
        </ion-item>

        <ion-item>
          <ion-label position="floating">ID de cliente</ion-label>
          <ion-input [(ngModel)]="model.cliente" name="cliente" type="number" required></ion-input>
        </ion-item>
        <ion-note class="ion-padding-start" color="medium" style="display:block; font-size: 11px;">
          El listado de usuarios solo es accesible por el rol ADMIN (ver desviacion reportada); pide el ID numerico
          del cliente al administrador.
        </ion-note>

        <ion-item>
          <ion-label>Producto (opcional)</ion-label>
          <ion-select [(ngModel)]="model.producto" name="producto">
            <ion-select-option [value]="null">Ninguno</ion-select-option>
            <ion-select-option *ngFor="let p of productos" [value]="p.id">
              {{ p.nombre }} ({{ p.sku }})
            </ion-select-option>
          </ion-select>
        </ion-item>

        <ion-item>
          <ion-label>Zona</ion-label>
          <ion-select [(ngModel)]="model.zona" name="zona" required>
            <ion-select-option *ngFor="let c of zonas" [value]="c.zona">{{ c.zona }}</ion-select-option>
          </ion-select>
        </ion-item>

        <ion-item>
          <ion-label position="floating">Direccion de origen</ion-label>
          <ion-input [(ngModel)]="model.direccion_origen" name="direccion_origen"></ion-input>
        </ion-item>
        <ion-item>
          <ion-label position="floating">Direccion de destino</ion-label>
          <ion-input [(ngModel)]="model.direccion_destino" name="direccion_destino"></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="floating">Fecha de agenda</ion-label>
          <ion-input [(ngModel)]="model.fecha_agenda" name="fecha_agenda" type="date" required></ion-input>
        </ion-item>

        <ion-button expand="block" type="submit" class="ion-margin-top" [disabled]="saving">
          {{ saving ? 'Creando...' : 'Crear servicio' }}
        </ion-button>
      </form>

      <ion-text color="success" *ngIf="success"><p>Servicio #{{ success }} creado correctamente.</p></ion-text>
      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>
    </div>
  `,
})
export class ServicioFormPage implements OnInit {
  model: {
    tipo: TipoServicio;
    cliente: number | null;
    producto: number | null;
    zona: string;
    direccion_origen: string;
    direccion_destino: string;
    fecha_agenda: string;
  } = {
    tipo: 'ENTREGA',
    cliente: null,
    producto: null,
    zona: '',
    direccion_origen: '',
    direccion_destino: '',
    fecha_agenda: '',
  };

  zonas: Cobertura[] = [];
  productos: Producto[] = [];
  saving = false;
  error = '';
  success: number | null = null;

  constructor(
    private serviciosService: ServiciosService,
    private coberturaService: CoberturaService,
    private productosService: ProductosService,
    private router: Router,
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
    this.productosService.list().subscribe({
      next: (p) => {
        this.productos = p;
        this.cdr.detectChanges();
      },
      error: () => {},
    });
  }

  save(): void {
    this.saving = true;
    this.error = '';
    this.success = null;
    this.serviciosService.create(this.model as any).subscribe({
      next: (s) => {
        this.saving = false;
        this.success = s.id;
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
