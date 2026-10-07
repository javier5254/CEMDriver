import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { wsUrl } from '../utils';
import { PosicionGps } from '../models';
import { AuthService } from './auth.service';

@Injectable({ providedIn: 'root' })
export class TrackingService {
  private base = `${environment.apiUrl}/tracking/`;

  constructor(
    private http: HttpClient,
    private auth: AuthService,
  ) {}

  /**
   * Conecta al consumer de Channels para recibir la posicion de un servicio
   * en tiempo real (push), en vez de hacer polling. Se cierra el socket al
   * desuscribirse (ngOnDestroy del componente que consuma esto).
   */
  conectarTracking(servicioId: number): Observable<PosicionGps> {
    return new Observable((subscriber) => {
      const token = this.auth.getAccessToken();
      const socket = new WebSocket(wsUrl(`ws/tracking/${servicioId}/`, token));

      socket.onmessage = (event) => {
        try {
          subscriber.next(JSON.parse(event.data));
        } catch {
          // ignora mensajes que no sean JSON valido
        }
      };
      socket.onerror = () => subscriber.error(new Error('Error en la conexion de tracking en tiempo real.'));
      socket.onclose = (ev) => {
        if (ev.code !== 1000) {
          subscriber.error(new Error('Se perdio la conexion de tracking en tiempo real.'));
        } else {
          subscriber.complete();
        }
      };

      return () => socket.close(1000);
    });
  }

  // Nota: el campo esperado por el backend es "servicio" (id numerico), no
  // "servicio_id" como indica 05-api.md. Ver desviaciones reportadas.
  //
  // El backend guarda lat/lng como Decimal(max_digits=9, decimal_places=6).
  // navigator.geolocation devuelve floats con muchos mas de 6 decimales
  // (ej. 4.710989879663872), que DRF rechaza por exceder max_digits antes
  // de redondear. Se redondea aqui, en el unico punto de entrada, para que
  // tanto el GPS automatico como la carga manual queden a salvo.
  postPosicion(servicio: number, lat: number, lng: number): Observable<PosicionGps> {
    const redondear = (n: number) => Math.round(n * 1e6) / 1e6;
    return this.http.post<PosicionGps>(`${this.base}posicion/`, {
      servicio,
      lat: redondear(lat),
      lng: redondear(lng),
    });
  }

  ultimaPosicion(servicioId: number): Observable<PosicionGps> {
    return this.http.get<PosicionGps>(`${this.base}ultima-posicion/`, {
      params: { servicio_id: servicioId },
    });
  }

  /** Geocodifica (con cache) la direccion de destino/origen del servicio, para mostrarla en el mapa. */
  obtenerDestino(servicioId: number): Observable<{ lat: number; lng: number; direccion: string }> {
    return this.http.get<{ lat: number; lng: number; direccion: string }>(`${this.base}destino/`, {
      params: { servicio_id: servicioId },
    });
  }
}
