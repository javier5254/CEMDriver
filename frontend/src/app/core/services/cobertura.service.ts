import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { AgendaDisponible, Cobertura } from '../models';

@Injectable({ providedIn: 'root' })
export class CoberturaService {
  private base = `${environment.apiUrl}/cobertura/`;

  constructor(private http: HttpClient) {}

  list(): Observable<Cobertura[]> {
    return this.http.get<Cobertura[]>(this.base);
  }

  get(id: number): Observable<Cobertura> {
    return this.http.get<Cobertura>(`${this.base}${id}/`);
  }

  create(data: Partial<Cobertura>): Observable<Cobertura> {
    return this.http.post<Cobertura>(this.base, data);
  }

  update(id: number, data: Partial<Cobertura>): Observable<Cobertura> {
    return this.http.patch<Cobertura>(`${this.base}${id}/`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}${id}/`);
  }

  agendaDisponible(zona: string): Observable<AgendaDisponible> {
    return this.http.get<AgendaDisponible>(`${this.base}agenda-disponible/`, { params: { zona } });
  }
}
