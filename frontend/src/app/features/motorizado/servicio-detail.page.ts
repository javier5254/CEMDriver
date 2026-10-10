import { ChangeDetectorRef, Component, Input, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import {
  IonBadge,
  IonButton,
  IonItem,
  IonLabel,
  IonList,
  IonSelect,
  IonSelectOption,
  IonSpinner,
  IonText,
  IonTextarea,
  IonNote,
} from '@ionic/angular';
import SignaturePad from 'signature_pad';
import { ServiciosService } from '../../core/services/servicios.service';
import { TrackingService } from '../../core/services/tracking.service';
import { Servicio } from '../../core/models';
import { estadoColor, extractErrorMessage, mediaUrl } from '../../core/utils';

@Component({
  selector: 'app-motorizado-servicio-detail',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,
    IonBadge,
    IonButton,
    IonItem,
    IonLabel,
    IonList,
    IonSelect,
    IonSelectOption,
    IonSpinner,
    IonText,
    IonTextarea,
    IonNote,
  ],
  template: `
    <div class="ion-padding">
      <ion-spinner *ngIf="loading"></ion-spinner>
      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>

      <div *ngIf="!loading && servicio as s">
        <h2>
          #{{ s.id }} - {{ s.tipo === 'ENTREGA' ? 'Entrega' : 'Recoleccion' }}
          <ion-badge [color]="colorFor(s.estado)">{{ s.estado }}</ion-badge>
        </h2>

        <ion-list>
          <ion-item lines="none">
            <ion-label>
              <p>Cliente</p>
              <h3>{{ s.cliente_detalle?.nombre || s.cliente }}</h3>
            </ion-label>
          </ion-item>
          <ion-item lines="none" *ngIf="s.tipo === 'ENTREGA'">
            <ion-label>
              <p>Direccion de destino</p>
              <h3>{{ s.direccion_destino || '(sin especificar)' }}</h3>
            </ion-label>
          </ion-item>
          <ion-item lines="none" *ngIf="s.tipo === 'RECOLECCION'">
            <ion-label>
              <p>Direccion de origen (recoleccion)</p>
              <h3>{{ s.direccion_origen || '(sin especificar)' }}</h3>
            </ion-label>
          </ion-item>
          <ion-item lines="none">
            <ion-label>
              <p>Zona / Fecha agenda</p>
              <h3>{{ s.zona }} - {{ s.fecha_agenda }}</h3>
            </ion-label>
          </ion-item>
        </ion-list>

        <ion-text color="success" *ngIf="actionMessage"><p>{{ actionMessage }}</p></ion-text>
        <ion-text color="danger" *ngIf="actionError"><p>{{ actionError }}</p></ion-text>

        <div style="display:flex; flex-direction:column; gap: 8px; margin-top: 12px;">
          <ion-button
            *ngIf="s.tipo === 'ENTREGA' && s.estado === 'ASIGNADO'"
            expand="block"
            [disabled]="acting"
            (click)="recibirEnCentro()"
          >
            Recibir en centro
          </ion-button>

          <ion-button
            *ngIf="puedeIniciarTransito(s)"
            expand="block"
            color="warning"
            [disabled]="acting"
            (click)="iniciarTransito()"
          >
            Iniciar transito
          </ion-button>

          <ion-button
            *ngIf="s.estado === 'EN_TRANSITO' && !showCerrarForm"
            expand="block"
            color="success"
            (click)="abrirCierre()"
          >
            Cerrar servicio
          </ion-button>

          <ion-button
            *ngIf="puedeRegistrarNovedad(s) && !showNovedadForm"
            expand="block"
            color="danger"
            fill="outline"
            (click)="showNovedadForm = true"
          >
            Registrar novedad
          </ion-button>

          <ion-button expand="block" fill="outline" [routerLink]="['/motorizado/servicios', s.id, 'chat']">
            Chatear con el cliente
          </ion-button>
        </div>

        <!-- Cierre: Entrega es directo; Recoleccion exige foto + firma -->
        <div *ngIf="showCerrarForm" class="ion-margin-top">
          <h3>Cerrar servicio</h3>

          <ng-container *ngIf="s.tipo === 'RECOLECCION'">
            <ion-item lines="none">
              <ion-label position="stacked">Foto del paquete</ion-label>
              <input type="file" accept="image/*" capture="environment" (change)="onFotoChange($event)" />
            </ion-item>
            <p *ngIf="fotoPreview"><img [src]="fotoPreview" style="max-width: 200px; border-radius: 6px;" /></p>

            <ion-label style="display:block; margin-top: 8px;">Firma del cliente</ion-label>
            <canvas
              id="signature-canvas"
              width="320"
              height="150"
              style="border: 1px solid var(--ion-color-medium); touch-action: none; background: #fff;"
            ></canvas>
            <div>
              <ion-button size="small" fill="clear" (click)="limpiarFirma()">Limpiar firma</ion-button>
            </div>
          </ng-container>

          <div style="display:flex; gap: 8px; margin-top: 8px;">
            <ion-button
              color="success"
              [disabled]="acting || (s.tipo === 'RECOLECCION' && !evidenciaLista())"
              (click)="cerrar()"
            >
              {{ acting ? 'Enviando...' : 'Confirmar cierre' }}
            </ion-button>
            <ion-button fill="clear" (click)="showCerrarForm = false">Cancelar</ion-button>
          </div>
          <ion-note color="medium" *ngIf="s.tipo === 'RECOLECCION'" style="display:block; font-size: 11px;">
            Se requiere foto y firma para cerrar una recoleccion (regla de negocio RN-02).
          </ion-note>
        </div>

        <!-- Novedad -->
        <div *ngIf="showNovedadForm" class="ion-margin-top">
          <h3>Registrar novedad</h3>
          <ion-item>
            <ion-label>Tipo</ion-label>
            <ion-select [(ngModel)]="novedad.tipo">
              <ion-select-option value="CLIENTE_AUSENTE">Cliente ausente</ion-select-option>
              <ion-select-option value="DIRECCION_ERRADA">Direccion errada</ion-select-option>
              <ion-select-option value="RECHAZO">Rechazo del cliente</ion-select-option>
              <ion-select-option value="OTRO">Otro</ion-select-option>
            </ion-select>
          </ion-item>
          <ion-item>
            <ion-label position="stacked">Detalle</ion-label>
            <ion-textarea [(ngModel)]="novedad.detalle" rows="3"></ion-textarea>
          </ion-item>
          <ion-item>
            <ion-label>Accion</ion-label>
            <ion-select [(ngModel)]="novedad.accion">
              <ion-select-option value="REINTENTAR">Reintentar</ion-select-option>
              <ion-select-option value="DEVOLVER_A_CENTRO">Devolver a centro</ion-select-option>
            </ion-select>
          </ion-item>
          <div style="display:flex; gap: 8px; margin-top: 8px;">
            <ion-button color="danger" [disabled]="acting || !novedad.tipo || !novedad.accion" (click)="enviarNovedad()">
              {{ acting ? 'Enviando...' : 'Registrar novedad' }}
            </ion-button>
            <ion-button fill="clear" (click)="showNovedadForm = false">Cancelar</ion-button>
          </div>
        </div>

        <div *ngIf="s.novedades?.length" class="ion-margin-top">
          <h3>Historial de novedades</h3>
          <ion-list>
            <ion-item lines="none" *ngFor="let n of s.novedades">
              <ion-label>
                <h3>{{ n.tipo }} - {{ n.accion }}</h3>
                <p>{{ n.detalle }}</p>
              </ion-label>
            </ion-item>
          </ion-list>
        </div>

        <div *ngIf="s.evidencia" class="ion-margin-top">
          <h3>Evidencia registrada</h3>
          <img [src]="mediaUrl(s.evidencia.foto)" style="max-width: 150px; margin-right: 8px;" />
          <img [src]="mediaUrl(s.evidencia.firma)" style="max-width: 150px;" />
        </div>

        <div *ngIf="s.estado === 'EN_TRANSITO'" class="ion-margin-top">
          <ion-text color="medium" *ngIf="gpsStatus === 'esperando'">
            <p style="font-size: 12px;">Obteniendo ubicacion GPS del dispositivo...</p>
          </ion-text>
          <ion-text color="success" *ngIf="gpsStatus === 'activo'">
            <p style="font-size: 12px;">
              Transmitiendo ubicacion GPS cada ~8s
              <span *ngIf="ultimoEnvioGps"> (ultimo envio: {{ ultimoEnvioGps }})</span>.
            </p>
          </ion-text>
          <ion-text color="danger" *ngIf="gpsStatus === 'error'">
            <p style="font-size: 12px;">
              No se pudo obtener la ubicacion automaticamente: {{ gpsErrorMsg }}
              Puedes enviarla manualmente abajo mientras se soluciona.
            </p>
          </ion-text>

          <div style="display:flex; gap: 6px; align-items:center; margin-top: 6px;" *ngIf="gpsStatus !== 'activo'">
            <input type="number" step="0.000001" placeholder="Latitud" [(ngModel)]="manualLat" style="width: 110px;" />
            <input type="number" step="0.000001" placeholder="Longitud" [(ngModel)]="manualLng" style="width: 110px;" />
            <ion-button size="small" fill="outline" [disabled]="manualLat == null || manualLng == null" (click)="enviarUbicacionManual()">
              Enviar ubicacion manual
            </ion-button>
          </div>
          <ion-text color="success" *ngIf="manualEnviada"><p style="font-size: 11px;">Ubicacion manual enviada.</p></ion-text>
        </div>
      </div>
    </div>
  `,
})
export class MotorizadoServicioDetailPage implements OnInit, OnDestroy {
  @Input() id!: string;
  mediaUrl = mediaUrl;

  servicio: Servicio | null = null;
  loading = false;
  error = '';
  acting = false;
  actionMessage = '';
  actionError = '';

  showCerrarForm = false;
  showNovedadForm = false;

  fotoFile: File | null = null;
  fotoPreview: string | null = null;
  signaturePad: SignaturePad | null = null;

  novedad: { tipo: string; detalle: string; accion: 'DEVOLVER_A_CENTRO' | 'REINTENTAR' | '' } = {
    tipo: '',
    detalle: '',
    accion: '',
  };

  private watchId: number | null = null;
  private trackingInterval: any = null;
  private lastCoords: { lat: number; lng: number } | null = null;

  gpsStatus: 'esperando' | 'activo' | 'error' = 'esperando';
  gpsErrorMsg = '';
  ultimoEnvioGps = '';
  manualLat: number | null = null;
  manualLng: number | null = null;
  manualEnviada = false;

  constructor(
    private serviciosService: ServiciosService,
    private trackingService: TrackingService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.fetch();
  }

  ngOnDestroy(): void {
    this.stopTracking();
  }

  fetch(): void {
    this.loading = true;
    this.error = '';
    this.serviciosService.get(Number(this.id)).subscribe({
      next: (s) => {
        this.loading = false;
        this.servicio = s;
        if (s.estado === 'EN_TRANSITO') this.startTracking();
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

  puedeIniciarTransito(s: Servicio): boolean {
    if (s.tipo === 'ENTREGA') return s.estado === 'RECIBIDO_CENTRO';
    return s.estado === 'ASIGNADO';
  }

  puedeRegistrarNovedad(s: Servicio): boolean {
    return ['ASIGNADO', 'RECIBIDO_CENTRO', 'EN_TRANSITO'].includes(s.estado);
  }

  private runAction(obs: any, mensaje: string): void {
    this.acting = true;
    this.actionMessage = '';
    this.actionError = '';
    obs.subscribe({
      next: (s: Servicio) => {
        this.acting = false;
        this.servicio = s;
        this.actionMessage = mensaje;
        this.showCerrarForm = false;
        this.showNovedadForm = false;
        if (s.estado !== 'EN_TRANSITO') this.stopTracking();
        this.cdr.detectChanges();
      },
      error: (err: any) => {
        this.acting = false;
        this.actionError = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  recibirEnCentro(): void {
    this.runAction(this.serviciosService.recibirEnCentro(Number(this.id)), 'Paquete recibido en centro.');
  }

  iniciarTransito(): void {
    this.runAction(this.serviciosService.iniciarTransito(Number(this.id)), 'Servicio en transito.');
    this.startTracking();
  }

  abrirCierre(): void {
    this.showCerrarForm = true;
    if (this.servicio?.tipo === 'RECOLECCION') {
      setTimeout(() => this.initSignaturePad(), 0);
    }
  }

  private initSignaturePad(): void {
    const canvas = document.getElementById('signature-canvas') as HTMLCanvasElement | null;
    if (canvas && !this.signaturePad) {
      this.signaturePad = new SignaturePad(canvas);
      // signature_pad dibuja usando sus propios listeners nativos (fuera de
      // Angular), asi que el boton "Confirmar cierre" (que depende de
      // evidenciaLista()) no se refresca solo al terminar un trazo.
      const refresh = () => this.cdr.detectChanges();
      canvas.addEventListener('mouseup', refresh);
      canvas.addEventListener('touchend', refresh);
      canvas.addEventListener('pointerup', refresh);
    }
  }

  limpiarFirma(): void {
    this.signaturePad?.clear();
    this.cdr.detectChanges();
  }

  onFotoChange(ev: Event): void {
    const input = ev.target as HTMLInputElement;
    const file = input.files?.[0] || null;
    this.fotoFile = file;
    this.fotoPreview = file ? URL.createObjectURL(file) : null;
    this.cdr.detectChanges();
  }

  evidenciaLista(): boolean {
    return !!this.fotoFile && !!this.signaturePad && !this.signaturePad.isEmpty();
  }

  cerrar(): void {
    if (this.servicio?.tipo === 'RECOLECCION') {
      if (!this.evidenciaLista()) return;
      const canvas = document.getElementById('signature-canvas') as HTMLCanvasElement;
      canvas.toBlob((firmaBlob) => {
        if (!firmaBlob || !this.fotoFile) return;
        this.runAction(
          this.serviciosService.cerrar(Number(this.id), { foto: this.fotoFile, firma: firmaBlob }),
          'Recoleccion cerrada con evidencia.',
        );
      }, 'image/png');
    } else {
      this.runAction(this.serviciosService.cerrar(Number(this.id)), 'Entrega confirmada.');
    }
  }

  enviarNovedad(): void {
    if (!this.novedad.tipo || !this.novedad.accion) return;
    this.runAction(
      this.serviciosService.novedad(Number(this.id), {
        tipo: this.novedad.tipo,
        detalle: this.novedad.detalle,
        accion: this.novedad.accion as 'DEVOLVER_A_CENTRO' | 'REINTENTAR',
      }),
      'Novedad registrada.',
    );
  }

  private startTracking(): void {
    if (this.trackingInterval) return;
    if (!('geolocation' in navigator)) {
      this.gpsStatus = 'error';
      this.gpsErrorMsg = 'Este navegador no soporta geolocalizacion.';
      this.cdr.detectChanges();
      return;
    }

    this.watchId = navigator.geolocation.watchPosition(
      (pos) => {
        this.lastCoords = { lat: pos.coords.latitude, lng: pos.coords.longitude };
        this.gpsStatus = 'activo';
        this.gpsErrorMsg = '';
        this.cdr.detectChanges();
      },
      (err) => {
        this.gpsStatus = 'error';
        this.gpsErrorMsg = this.mensajeErrorGps(err);
        this.cdr.detectChanges();
      },
      { enableHighAccuracy: true, maximumAge: 5000 },
    );

    this.trackingInterval = setInterval(() => {
      if (this.lastCoords && this.servicio) {
        this.trackingService
          .postPosicion(this.servicio.id, this.lastCoords.lat, this.lastCoords.lng)
          .subscribe({
            next: () => {
              this.ultimoEnvioGps = new Date().toLocaleTimeString();
              this.cdr.detectChanges();
            },
            error: (err) => {
              this.gpsStatus = 'error';
              this.gpsErrorMsg = extractErrorMessage(err);
              this.cdr.detectChanges();
            },
          });
      }
    }, 8000);
  }

  private mensajeErrorGps(err: GeolocationPositionError): string {
    switch (err.code) {
      case err.PERMISSION_DENIED:
        return 'Permiso de ubicacion denegado en el navegador.';
      case err.POSITION_UNAVAILABLE:
        return 'Ubicacion no disponible en este dispositivo.';
      case err.TIMEOUT:
        return 'Se agoto el tiempo esperando la ubicacion.';
      default:
        return 'Error desconocido obteniendo la ubicacion.';
    }
  }

  enviarUbicacionManual(): void {
    if (this.manualLat == null || this.manualLng == null || !this.servicio) return;
    this.trackingService.postPosicion(this.servicio.id, this.manualLat, this.manualLng).subscribe({
      next: () => {
        this.manualEnviada = true;
        this.ultimoEnvioGps = new Date().toLocaleTimeString();
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.actionError = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  private stopTracking(): void {
    if (this.watchId != null) {
      navigator.geolocation.clearWatch(this.watchId);
      this.watchId = null;
    }
    if (this.trackingInterval) {
      clearInterval(this.trackingInterval);
      this.trackingInterval = null;
    }
  }
}
