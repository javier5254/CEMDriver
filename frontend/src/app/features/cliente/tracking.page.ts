import { ChangeDetectorRef, Component, Input, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonText, IonBadge } from '@ionic/angular';
import * as L from 'leaflet';
import { Subscription } from 'rxjs';
import { TrackingService } from '../../core/services/tracking.service';
import { ServiciosService } from '../../core/services/servicios.service';
import { Servicio } from '../../core/models';
import { estadoColor, extractErrorMessage } from '../../core/utils';

const POLL_FALLBACK_MS = 8000;
// Velocidad promedio asumida para el motorizado en trafico urbano, usada
// solo para estimar un ETA aproximado (no hay proveedor de ruteo real).
const VELOCIDAD_PROMEDIO_KMH = 22;

// Corrige las rutas de icono por defecto de Leaflet, que se rompen al empaquetar
// con Angular/webpack. Las imagenes se copian a assets/leaflet via angular.json.
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'assets/leaflet/marker-icon-2x.png',
  iconUrl: 'assets/leaflet/marker-icon.png',
  shadowUrl: 'assets/leaflet/marker-shadow.png',
});

const ICONO_DESTINO = L.divIcon({
  className: 'marcador-destino',
  html: '<div style="width:16px;height:16px;border-radius:50% 50% 50% 0;background:#FF3B30;border:2px solid #fff;transform:rotate(-45deg);box-shadow:0 1px 3px rgba(0,0,0,.4);"></div>',
  iconSize: [16, 16],
  iconAnchor: [8, 16],
});

/** Distancia entre dos puntos (km) usando la formula de haversine. */
function distanciaKm(lat1: number, lng1: number, lat2: number, lng2: number): number {
  const R = 6371;
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLng = ((lng2 - lng1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos((lat1 * Math.PI) / 180) * Math.cos((lat2 * Math.PI) / 180) * Math.sin(dLng / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

@Component({
  selector: 'app-tracking',
  standalone: true,
  imports: [CommonModule, IonText, IonBadge],
  template: `
    <div class="ion-padding">
      <h2>
        Tracking servicio #{{ id }}
        <ion-badge *ngIf="servicio" [color]="colorFor(servicio.estado)">{{ servicio.estado }}</ion-badge>
      </h2>

      <div id="tracking-map" style="height: 55vh; width: 100%; border-radius: 8px;"></div>

      <ion-text color="medium" *ngIf="destinoDireccion">
        <p style="font-size: 12px; margin-top: 8px;">
          <strong>Destino:</strong> {{ destinoDireccion }}
        </p>
      </ion-text>

      <ion-text color="primary" *ngIf="etaMinutos != null">
        <p style="font-size: 14px; font-weight: 600;">
          Llega en ~{{ etaMinutos }} min ({{ distanciaKmTexto }} km, estimado)
        </p>
      </ion-text>

      <ion-text color="medium" *ngIf="!hasPosition"><p>Esperando ubicacion del motorizado...</p></ion-text>
      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>
      <ion-text [color]="enVivo ? 'success' : 'medium'" *ngIf="hasPosition">
        <p style="font-size: 12px;">
          {{ enVivo ? 'En vivo' : 'Actualizando cada 8s' }} &middot; ultima actualizacion: {{ lastUpdate }}
        </p>
      </ion-text>
    </div>
  `,
})
export class TrackingPage implements OnInit, OnDestroy {
  @Input() id!: string;

  servicio: Servicio | null = null;
  hasPosition = false;
  enVivo = false;
  error = '';
  lastUpdate = '';
  destinoDireccion = '';
  etaMinutos: number | null = null;
  distanciaKmTexto = '';

  private map: L.Map | null = null;
  private marker: L.Marker | null = null;
  private destinoMarker: L.Marker | null = null;
  private destinoCoords: { lat: number; lng: number } | null = null;
  private intervalRef: any = null;
  private wsSub: Subscription | null = null;

  constructor(
    private trackingService: TrackingService,
    private serviciosService: ServiciosService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.serviciosService.get(Number(this.id)).subscribe({
      next: (s) => {
        this.servicio = s;
        this.cdr.detectChanges();
      },
      error: () => {},
    });

    setTimeout(() => this.initMap(), 0);
    this.cargarDestino();

    // Primero un fetch inicial por REST (por si ya hay una posicion), y luego
    // nos conectamos por WebSocket para recibir actualizaciones en vivo. Si el
    // socket falla, caemos de vuelta a polling para no dejar la pantalla muerta.
    this.fetchInicial();
    this.conectarEnVivo();
  }

  ngOnDestroy(): void {
    this.wsSub?.unsubscribe();
    if (this.intervalRef) clearInterval(this.intervalRef);
    this.map?.remove();
  }

  colorFor(estado: string): string {
    return estadoColor(estado as any);
  }

  private initMap(): void {
    const el = document.getElementById('tracking-map');
    if (!el || this.map) return;
    this.map = L.map(el).setView([4.65, -74.05], 12); // Bogota por defecto
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(this.map);

    if (this.destinoCoords) this.dibujarDestino();
  }

  private cargarDestino(): void {
    this.trackingService.obtenerDestino(Number(this.id)).subscribe({
      next: (d) => {
        this.destinoCoords = { lat: Number(d.lat), lng: Number(d.lng) };
        this.destinoDireccion = d.direccion;
        this.dibujarDestino();
        this.actualizarEta();
        this.cdr.detectChanges();
      },
      error: () => {
        // Sin geocodificacion disponible (direccion ambigua, sin red, etc.):
        // el tracking sigue funcionando, solo sin marcador de destino ni ETA.
      },
    });
  }

  private dibujarDestino(): void {
    if (!this.map || !this.destinoCoords) return;
    const { lat, lng } = this.destinoCoords;
    if (!this.destinoMarker) {
      this.destinoMarker = L.marker([lat, lng], { icon: ICONO_DESTINO }).addTo(this.map);
    } else {
      this.destinoMarker.setLatLng([lat, lng]);
    }
    this.ajustarVista();
  }

  private ajustarVista(): void {
    if (!this.map || !this.marker || !this.destinoMarker) return;
    this.map.fitBounds(L.latLngBounds([this.marker.getLatLng(), this.destinoMarker.getLatLng()]), {
      padding: [40, 40],
    });
  }

  private fetchInicial(): void {
    this.trackingService.ultimaPosicion(Number(this.id)).subscribe({
      next: (pos) => this.actualizarMarcador(pos),
      error: () => {
        // sin posicion todavia; no es un error real, se espera la primera
      },
    });
  }

  private conectarEnVivo(): void {
    this.wsSub = this.trackingService.conectarTracking(Number(this.id)).subscribe({
      next: (pos) => {
        this.enVivo = true;
        this.error = '';
        this.detenerPolling();
        this.actualizarMarcador(pos);
      },
      error: () => {
        this.enVivo = false;
        this.iniciarPollingDeRespaldo();
        this.cdr.detectChanges();
      },
    });
  }

  private iniciarPollingDeRespaldo(): void {
    if (this.intervalRef) return;
    this.poll();
    this.intervalRef = setInterval(() => this.poll(), POLL_FALLBACK_MS);
  }

  private detenerPolling(): void {
    if (this.intervalRef) {
      clearInterval(this.intervalRef);
      this.intervalRef = null;
    }
  }

  private poll(): void {
    this.trackingService.ultimaPosicion(Number(this.id)).subscribe({
      next: (pos) => {
        this.error = '';
        this.actualizarMarcador(pos);
      },
      error: (err) => {
        if (err.status !== 404) {
          this.error = extractErrorMessage(err);
        }
        this.cdr.detectChanges();
      },
    });
  }

  private ultimaPosicionConocida: { lat: number; lng: number } | null = null;

  private actualizarMarcador(pos: { lat: number | string; lng: number | string; timestamp?: string }): void {
    const lat = Number(pos.lat);
    const lng = Number(pos.lng);
    this.hasPosition = true;
    this.lastUpdate = pos.timestamp ? new Date(pos.timestamp).toLocaleTimeString() : '';
    this.ultimaPosicionConocida = { lat, lng };

    if (!this.map) {
      setTimeout(() => this.initMap(), 0);
    }
    if (this.map) {
      if (!this.marker) {
        this.marker = L.marker([lat, lng]).addTo(this.map);
      } else {
        this.marker.setLatLng([lat, lng]);
      }
      if (this.destinoMarker) {
        this.ajustarVista();
      } else {
        this.map.setView([lat, lng], this.map.getZoom());
      }
    }
    this.actualizarEta();
    this.cdr.detectChanges();
  }

  private actualizarEta(): void {
    if (!this.ultimaPosicionConocida || !this.destinoCoords) return;
    const km = distanciaKm(
      this.ultimaPosicionConocida.lat,
      this.ultimaPosicionConocida.lng,
      this.destinoCoords.lat,
      this.destinoCoords.lng,
    );
    this.distanciaKmTexto = km.toFixed(1);
    this.etaMinutos = Math.max(1, Math.round((km / VELOCIDAD_PROMEDIO_KMH) * 60));
  }
}
