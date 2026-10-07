import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonList,
  IonItem,
  IonLabel,
  IonInput,
  IonSelect,
  IonSelectOption,
  IonButton,
  IonIcon,
  IonBadge,
  IonSpinner,
  IonText,
} from '@ionic/angular';
import { ApiKeysService, ApiKey, ApiKeyCreada } from '../../core/services/api-keys.service';
import { UsuariosService } from '../../core/services/usuarios.service';
import { Usuario } from '../../core/models';
import { extractErrorMessage } from '../../core/utils';

@Component({
  selector: 'app-api-keys-list',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonList,
    IonItem,
    IonLabel,
    IonInput,
    IonSelect,
    IonSelectOption,
    IonButton,
    IonIcon,
    IonBadge,
    IonSpinner,
    IonText,
  ],
  template: `
    <div class="ion-padding">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2>API Keys</h2>
        <ion-button (click)="showForm = !showForm">
          <ion-icon slot="start" name="add-outline"></ion-icon>
          Nueva API Key
        </ion-button>
      </div>
      <p>
        Credenciales para que sistemas externos (e-commerce, ERP) creen y consulten servicios
        via API sin un login humano. Cada llave actua en nombre de un usuario ALISTADOR
        existente.
      </p>

      <!-- Banner: la llave cruda solo se muestra una vez, justo despues de crearla. -->
      <div
        *ngIf="llaveCreada"
        style="border: 2px solid var(--ion-color-danger, #eb445a); border-radius: 8px; padding: 12px; margin-bottom: 16px; background: rgba(235, 68, 90, 0.06);"
      >
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
          <strong>Copia esta llave ahora: no se volvera a mostrar.</strong>
          <ion-button fill="clear" size="small" (click)="llaveCreada = undefined">
            <ion-icon slot="icon-only" name="close-outline"></ion-icon>
          </ion-button>
        </div>
        <p style="margin: 8px 0;">
          API key para <strong>{{ llaveCreada.nombre }}</strong>:
        </p>
        <code style="display:block; padding: 8px; background: #00000010; border-radius: 4px; word-break: break-all;">{{
          llaveCreada.key
        }}</code>
        <p style="margin-top: 8px;">
          Envia esta llave en el header <code>X-API-Key</code> de cada peticion. Una vez que
          cierres este aviso, el valor completo no se podra recuperar de nuevo (solo el
          administrador puede desactivarla y generar una nueva).
        </p>
      </div>

      <form *ngIf="showForm" (ngSubmit)="crear()" class="ion-margin-bottom">
        <ion-item>
          <ion-label position="floating">Nombre (p.ej. "Tienda XYZ")</ion-label>
          <ion-input [(ngModel)]="nuevoNombre" name="nombre" required></ion-input>
        </ion-item>
        <ion-item>
          <ion-label>Actua como (alistador)</ion-label>
          <ion-select [(ngModel)]="nuevoActuaComo" name="actua_como" required>
            <ion-select-option *ngFor="let a of alistadores" [value]="a.id">
              {{ a.nombre }} ({{ a.username }})
            </ion-select-option>
          </ion-select>
        </ion-item>
        <ion-button expand="block" type="submit" class="ion-margin-top" [disabled]="creando">
          {{ creando ? 'Creando...' : 'Crear API Key' }}
        </ion-button>
      </form>

      <ion-spinner *ngIf="loading"></ion-spinner>
      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>

      <ion-list *ngIf="!loading && !error">
        <ion-item *ngFor="let k of items">
          <ion-label>
            <h3>{{ k.nombre }}</h3>
            <p>Prefijo: <code>{{ k.prefix }}...</code> - Actua como: {{ nombreAlistador(k.actua_como) }}</p>
            <p>
              Creada: {{ k.creado_en | date: 'short' }} - Ultimo uso:
              {{ k.ultimo_uso ? (k.ultimo_uso | date: 'short') : 'nunca' }}
            </p>
          </ion-label>
          <ion-badge slot="end" [color]="k.activa ? 'success' : 'medium'">
            {{ k.activa ? 'Activa' : 'Inactiva' }}
          </ion-badge>
          <ion-button slot="end" fill="clear" (click)="toggleActiva(k)">
            <ion-icon slot="icon-only" [name]="k.activa ? 'pause-outline' : 'play-outline'"></ion-icon>
          </ion-button>
          <ion-button slot="end" fill="clear" color="danger" (click)="remove(k)">
            <ion-icon slot="icon-only" name="trash-outline"></ion-icon>
          </ion-button>
        </ion-item>
      </ion-list>
    </div>
  `,
})
export class ApiKeysListPage implements OnInit {
  items: ApiKey[] = [];
  alistadores: Usuario[] = [];
  loading = false;
  creando = false;
  error = '';

  showForm = false;
  nuevoNombre = '';
  nuevoActuaComo?: number;

  llaveCreada?: ApiKeyCreada;

  constructor(
    private apiKeysService: ApiKeysService,
    private usuariosService: UsuariosService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.fetchAlistadores();
    this.fetch();
  }

  fetchAlistadores(): void {
    this.usuariosService.list().subscribe({
      next: (data) => {
        this.alistadores = data.filter((u) => u.rol === 'ALISTADOR');
        this.cdr.detectChanges();
      },
      error: () => {
        // No bloquea el listado principal si esto falla.
      },
    });
  }

  nombreAlistador(id: number): string {
    const usuario = this.alistadores.find((a) => a.id === id);
    return usuario ? `${usuario.nombre} (${usuario.username})` : `#${id}`;
  }

  fetch(): void {
    this.loading = true;
    this.error = '';
    this.apiKeysService.list().subscribe({
      next: (data) => {
        this.loading = false;
        this.items = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.loading = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  crear(): void {
    if (!this.nuevoNombre || !this.nuevoActuaComo) return;
    this.creando = true;
    this.error = '';
    this.apiKeysService.create({ nombre: this.nuevoNombre, actua_como: this.nuevoActuaComo }).subscribe({
      next: (creada) => {
        this.creando = false;
        this.llaveCreada = creada;
        this.showForm = false;
        this.nuevoNombre = '';
        this.nuevoActuaComo = undefined;
        this.fetch();
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.creando = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  toggleActiva(k: ApiKey): void {
    this.apiKeysService.setActiva(k.id, !k.activa).subscribe({
      next: () => this.fetch(),
      error: (err) => {
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  remove(k: ApiKey): void {
    if (!confirm(`Eliminar la API key "${k.nombre}"? Cualquier sistema que la use dejara de poder autenticarse.`)) return;
    this.apiKeysService.delete(k.id).subscribe({
      next: () => this.fetch(),
      error: (err) => {
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }
}
