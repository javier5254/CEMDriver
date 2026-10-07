import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Usuario } from '../models';

@Injectable({ providedIn: 'root' })
export class UsuariosService {
  private base = `${environment.apiUrl}/usuarios/`;

  constructor(private http: HttpClient) {}

  list(): Observable<Usuario[]> {
    return this.http.get<Usuario[]>(this.base);
  }

  get(id: number): Observable<Usuario> {
    return this.http.get<Usuario>(`${this.base}${id}/`);
  }

  create(data: Partial<Usuario>): Observable<Usuario> {
    return this.http.post<Usuario>(this.base, data);
  }

  update(id: number, data: Partial<Usuario>): Observable<Usuario> {
    return this.http.patch<Usuario>(`${this.base}${id}/`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}${id}/`);
  }
}
