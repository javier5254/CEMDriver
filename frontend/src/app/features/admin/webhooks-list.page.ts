import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonList,
  IonItem,
  IonLabel,
  IonInput,
  IonCheckbox,
  IonButton,
  IonIcon,
  IonBadge,
  IonSpinner,
  IonText,
} from '@ionic/angular';
import {
  WebhooksService,
  WebhookEndpoint,
  WebhookDelivery,
  EVENTOS_WEBHOOK,
} from '../../core/services/webhooks.service';
import { extractErrorMessage } from '../../core/utils';

type FormModel = {
  nombre: string;
  url: string;
  activo: boolean;
  eventosSeleccionados: string[];
};

const FORM_VACIO = (): FormModel => ({ nombre: '', url: '', activo: true, eventosSeleccionados: [] });

@Component({
  selector: 'app-webhooks-list',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonList,
    IonItem,
    IonLabel,
    IonInput,
    IonCheckbox,
    IonButton,
    IonIcon,
    IonBadge,
    IonSpinner,
    IonText,
  ],
  template: `
    <div class="ion-padding">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2>Webhooks</h2>
        <ion-button (click)="nuevo()">
          <ion-icon slot="start" name="add-outline"></ion-icon>
          Nuevo webhook
        </ion-button>
      </div>
      <p>
        Notifican a un sistema externo (ERP, e-commerce) cuando ocurren eventos de servicios.
        Cada envio se firma con HMAC-SHA256 (header <code>X-CMEDriver-Signature</code>) usando el
        <code>secret</code> del endpoint, para que el receptor pueda verificar su autenticidad.
      </p>

      <form *ngIf="showForm" (ngSubmit)="guardar()" class="ion-margin-bottom">
        <h3>{{ editingId ? 'Editar webhook' : 'Nuevo webhook' }}</h3>
        <ion-item>
          <ion-label position="floating">Nombre</ion-label>
          <ion-input [(ngModel)]="model.nombre" name="nombre" required></ion-input>
        </ion-item>
        <ion-item>
          <ion-label position="floating">URL</ion-label>
          <ion-input [(ngModel)]="model.url" name="url" type="url" placeholder="https://..." required></ion-input>
        </ion-item>

        <ion-label style="display:block; margin-top: 12px;">Eventos suscritos</ion-label>
        <div style="display:flex; flex-wrap:wrap; gap: 8px; padding: 8px 0;">
          <ion-item *ngFor="let e of eventosDisponibles" lines="none" style="--min-height: 30px;">
            <ion-checkbox slot="start" [checked]="isChecked(e)" (ionChange)="toggleEvento(e, $event)"></ion-checkbox>
            <ion-label>{{ e }}</ion-label>
          </ion-item>
        </div>

        <ion-item>
          <ion-label>Activo</ion-label>
          <ion-checkbox slot="start" [(ngModel)]="model.activo" name="activo"></ion-checkbox>
        </ion-item>

        <div *ngIf="secretActual" style="margin: 12px 0;">
          <ion-label>Secret (para verificar la firma HMAC en tu receptor)</ion-label>
          <code style="display:block; padding: 8px; background: #00000010; border-radius: 4px; word-break: break-all;">{{
            secretActual
          }}</code>
        </div>

        <div style="display:flex; gap: 8px;">
          <ion-button type="submit" [disabled]="guardando">
            {{ guardando ? 'Guardando...' : 'Guardar' }}
          </ion-button>
          <ion-button fill="outline" type="button" (click)="cancelar()">Cancelar</ion-button>
        </div>
      </form>

      <ion-spinner *ngIf="loading"></ion-spinner>
      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>

      <ion-list *ngIf="!loading && !error">
        <ng-container *ngFor="let w of items">
          <ion-item>
            <ion-label>
              <h3>{{ w.nombre }}</h3>
              <p>{{ w.url }}</p>
              <p>Eventos: {{ w.eventos }}</p>
            </ion-label>
            <ion-badge slot="end" [color]="w.activo ? 'success' : 'medium'">
              {{ w.activo ? 'Activo' : 'Inactivo' }}
            </ion-badge>
            <ion-button slot="end" fill="clear" (click)="verEntregas(w)">
              <ion-icon slot="icon-only" [name]="expandedId === w.id ? 'chevron-up-outline' : 'time-outline'"></ion-icon>
            </ion-button>
            <ion-button slot="end" fill="clear" (click)="editar(w)">
              <ion-icon slot="icon-only" name="create-outline"></ion-icon>
            </ion-button>
            <ion-button slot="end" fill="clear" color="danger" (click)="remove(w)">
              <ion-icon slot="icon-only" name="trash-outline"></ion-icon>
            </ion-button>
          </ion-item>

          <!-- Bitacora de entregas de este endpoint, expandible en linea. -->
          <ion-item *ngIf="expandedId === w.id">
            <ion-label>
              <ion-spinner *ngIf="loadingEntregas"></ion-spinner>
              <p *ngIf="!loadingEntregas && entregas.length === 0">Sin entregas registradas todavia.</p>
              <div *ngFor="let d of entregas" style="padding: 6px 0; border-bottom: 1px solid #00000010;">
                <strong [style.color]="d.exito ? 'var(--ion-color-success)' : 'var(--ion-color-danger)'">
                  {{ d.exito ? 'OK' : 'FALLO' }}
                </strong>
                - {{ d.evento }} - HTTP {{ d.status_code ?? 's/r' }} - {{ d.creado_en | date: 'short' }}
                <div *ngIf="d.error">{{ d.error }}</div>
              </div>
            </ion-label>
          </ion-item>
        </ng-container>
      </ion-list>
    </div>
  `,
})
export class WebhooksListPage implements OnInit {
  items: WebhookEndpoint[] = [];
  loading = false;
  error = '';

  eventosDisponibles = EVENTOS_WEBHOOK as unknown as string[];

  showForm = false;
  editingId: number | null = null;
  model: FormModel = FORM_VACIO();
  secretActual = '';
  guardando = false;

  expandedId: number | null = null;
  entregas: WebhookDelivery[] = [];
  loadingEntregas = false;

  constructor(
    private webhooksService: WebhooksService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.fetch();
  }

  fetch(): void {
    this.loading = true;
    this.error = '';
    this.webhooksService.list().subscribe({
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

  isChecked(evento: string): boolean {
    return this.model.eventosSeleccionados.includes(evento);
  }

  toggleEvento(evento: string, ev: any): void {
    const checked = ev.detail.checked;
    let arr = this.model.eventosSeleccionados;
    if (checked && !arr.includes(evento)) arr = [...arr, evento];
    if (!checked) arr = arr.filter((x) => x !== evento);
    this.model.eventosSeleccionados = arr;
  }

  nuevo(): void {
    this.editingId = null;
    this.model = FORM_VACIO();
    this.secretActual = '';
    this.showForm = true;
  }

  editar(w: WebhookEndpoint): void {
    this.error = '';
    // Se vuelve a pedir el detalle (no el objeto del listado) porque el
    // listado no incluye `secret` -- ver WebhookEndpointListSerializer.
    this.webhooksService.get(w.id).subscribe({
      next: (detalle) => {
        this.editingId = detalle.id;
        this.model = {
          nombre: detalle.nombre,
          url: detalle.url,
          activo: detalle.activo,
          eventosSeleccionados: detalle.eventos.split(',').map((e) => e.trim()).filter(Boolean),
        };
        this.secretActual = detalle.secret || '';
        this.showForm = true;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  cancelar(): void {
    this.showForm = false;
    this.editingId = null;
    this.secretActual = '';
  }

  guardar(): void {
    if (!this.model.nombre || !this.model.url || this.model.eventosSeleccionados.length === 0) {
      this.error = 'Completa nombre, url y al menos un evento.';
      return;
    }
    this.guardando = true;
    this.error = '';
    const payload = {
      nombre: this.model.nombre,
      url: this.model.url,
      activo: this.model.activo,
      eventos: this.model.eventosSeleccionados.join(','),
    };
    const obs = this.editingId
      ? this.webhooksService.update(this.editingId, payload)
      : this.webhooksService.create(payload);

    obs.subscribe({
      next: (guardado) => {
        this.guardando = false;
        this.secretActual = guardado.secret || this.secretActual;
        this.showForm = false;
        this.editingId = null;
        this.fetch();
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.guardando = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  verEntregas(w: WebhookEndpoint): void {
    if (this.expandedId === w.id) {
      this.expandedId = null;
      return;
    }
    this.expandedId = w.id;
    this.entregas = [];
    this.loadingEntregas = true;
    this.webhooksService.entregas(w.id).subscribe({
      next: (data) => {
        this.loadingEntregas = false;
        this.entregas = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.loadingEntregas = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  remove(w: WebhookEndpoint): void {
    if (!confirm(`Eliminar el webhook "${w.nombre}"?`)) return;
    this.webhooksService.delete(w.id).subscribe({
      next: () => this.fetch(),
      error: (err) => {
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }
}
