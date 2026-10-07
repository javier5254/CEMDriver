import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Ruta } from '../models';

@Injectable({ providedIn: 'root' })
export class RutasService {
  private base = `${environment.apiUrl}/rutas/`;

  constructor(private http: HttpClient) {}

  list(): Observable<Ruta[]> {
    return this.http.get<Ruta[]>(this.base);
  }

  get(id: number): Observable<Ruta> {
    return this.http.get<Ruta>(`${this.base}${id}/`);
  }

  create(data: Partial<Ruta>): Observable<Ruta> {
    return this.http.post<Ruta>(this.base, data);
  }

  update(id: number, data: Partial<Ruta>): Observable<Ruta> {
    return this.http.patch<Ruta>(`${this.base}${id}/`, data);
  }
}
