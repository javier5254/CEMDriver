import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Indicadores } from '../indicadores.models';

@Injectable({ providedIn: 'root' })
export class IndicadoresService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/indicadores/`;

  /** Indicadores del periodo (ultimos `dias`), opcionalmente filtrados por zona. */
  obtener(dias = 30, zona?: string | null): Observable<Indicadores> {
    let params = new HttpParams().set('dias', String(dias));
    if (zona) params = params.set('zona', zona);
    return this.http.get<Indicadores>(this.base, { params });
  }
}
