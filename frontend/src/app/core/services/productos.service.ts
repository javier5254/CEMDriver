import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Producto } from '../models';

@Injectable({ providedIn: 'root' })
export class ProductosService {
  private base = `${environment.apiUrl}/productos/`;

  constructor(private http: HttpClient) {}

  list(): Observable<Producto[]> {
    return this.http.get<Producto[]>(this.base);
  }

  get(id: number): Observable<Producto> {
    return this.http.get<Producto>(`${this.base}${id}/`);
  }

  create(data: Partial<Producto>): Observable<Producto> {
    return this.http.post<Producto>(this.base, data);
  }

  update(id: number, data: Partial<Producto>): Observable<Producto> {
    return this.http.patch<Producto>(`${this.base}${id}/`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}${id}/`);
  }

  disponiblesChatbot(): Observable<Producto[]> {
    return this.http.get<Producto[]>(`${this.base}disponibles-chatbot/`);
  }
}
