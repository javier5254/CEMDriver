import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

// Nota: estos modelos viven aqui (y no en core/models.ts) porque ese archivo
// puede estar siendo editado en paralelo por otro proceso.

/** Debe coincidir con integrations.models.EVENTOS_WEBHOOK en el backend. */
export const EVENTOS_WEBHOOK = [
  'servicio.creado',
  'servicio.asignado',
  'servicio.entregado',
  'servicio.recolectado',
  'servicio.novedad',
  'servicio.devuelto',
] as const;

export interface WebhookEndpoint {
  id: number;
  nombre: string;
  url: string;
  /** Presente en create/retrieve; ausente en list (ver WebhooksListPage/backend). */
  secret?: string;
  eventos: string; // csv, p.ej. "servicio.entregado,servicio.novedad"
  activo: boolean;
  creado_en: string;
}

export interface WebhookDelivery {
  id: number;
  endpoint: number;
  evento: string;
  payload: unknown;
  status_code: number | null;
  exito: boolean;
  error: string;
  creado_en: string;
}

@Injectable({ providedIn: 'root' })
export class WebhooksService {
  private base = `${environment.apiUrl}/integraciones/webhooks/`;

  constructor(private http: HttpClient) {}

  list(): Observable<WebhookEndpoint[]> {
    return this.http.get<WebhookEndpoint[]>(this.base);
  }

  get(id: number): Observable<WebhookEndpoint> {
    return this.http.get<WebhookEndpoint>(`${this.base}${id}/`);
  }

  create(data: Partial<WebhookEndpoint>): Observable<WebhookEndpoint> {
    return this.http.post<WebhookEndpoint>(this.base, data);
  }

  update(id: number, data: Partial<WebhookEndpoint>): Observable<WebhookEndpoint> {
    return this.http.patch<WebhookEndpoint>(`${this.base}${id}/`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}${id}/`);
  }

  entregas(id: number): Observable<WebhookDelivery[]> {
    return this.http.get<WebhookDelivery[]>(`${this.base}${id}/entregas/`);
  }
}
