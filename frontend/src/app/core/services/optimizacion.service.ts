import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

/** Un punto de la ruta ya geocodificado, en el orden sugerido por el backend. */
export interface PuntoRutaSugerido {
  servicio_id: number;
  lat: number;
  lng: number;
  direccion: string;
}

/** Una direccion de servicio que no se pudo geocodificar (queda fuera del orden). */
export interface ServicioNoGeocodificado {
  servicio_id: number;
  direccion: string;
}

export interface OptimizacionRutaResponse {
  ruta_id: number;
  orden_sugerido: PuntoRutaSugerido[];
  distancia_total_km: number;
  no_geocodificados: ServicioNoGeocodificado[];
}

@Injectable({ providedIn: 'root' })
export class OptimizacionService {
  private base = `${environment.apiUrl}/optimizacion/rutas/`;

  constructor(private http: HttpClient) {}

  optimizar(rutaId: number): Observable<OptimizacionRutaResponse> {
    return this.http.post<OptimizacionRutaResponse>(`${this.base}${rutaId}/`, {});
  }
}
