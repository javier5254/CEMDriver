import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

// Nota: estos modelos viven aqui (y no en core/models.ts) porque ese archivo
// puede estar siendo editado en paralelo por otro proceso.

export interface ApiKey {
  id: number;
  nombre: string;
  prefix: string;
  actua_como: number;
  activa: boolean;
  creado_en: string;
  ultimo_uso: string | null;
}

/** Respuesta de creacion: incluye `key` (la llave cruda), unica vez que se expone. */
export interface ApiKeyCreada extends ApiKey {
  key: string;
}

@Injectable({ providedIn: 'root' })
export class ApiKeysService {
  private base = `${environment.apiUrl}/integraciones/api-keys/`;

  constructor(private http: HttpClient) {}

  list(): Observable<ApiKey[]> {
    return this.http.get<ApiKey[]>(this.base);
  }

  create(data: { nombre: string; actua_como: number }): Observable<ApiKeyCreada> {
    return this.http.post<ApiKeyCreada>(this.base, data);
  }

  setActiva(id: number, activa: boolean): Observable<ApiKey> {
    return this.http.patch<ApiKey>(`${this.base}${id}/`, { activa });
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}${id}/`);
  }
}
