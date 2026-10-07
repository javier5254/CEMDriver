import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { MensajeChat, Novedad, Servicio } from '../models';

@Injectable({ providedIn: 'root' })
export class ServiciosService {
  private base = `${environment.apiUrl}/servicios/`;

  constructor(private http: HttpClient) {}

  list(): Observable<Servicio[]> {
    return this.http.get<Servicio[]>(this.base);
  }

  get(id: number): Observable<Servicio> {
    return this.http.get<Servicio>(`${this.base}${id}/`);
  }

  create(data: Partial<Servicio>): Observable<Servicio> {
    return this.http.post<Servicio>(this.base, data);
  }

  update(id: number, data: Partial<Servicio>): Observable<Servicio> {
    return this.http.patch<Servicio>(`${this.base}${id}/`, data);
  }

  asignarRuta(id: number, rutaId: number): Observable<Servicio> {
    return this.http.post<Servicio>(`${this.base}${id}/asignar-ruta/`, { ruta_id: rutaId });
  }

  recibirEnCentro(id: number): Observable<Servicio> {
    return this.http.post<Servicio>(`${this.base}${id}/recibir-en-centro/`, {});
  }

  iniciarTransito(id: number): Observable<Servicio> {
    return this.http.post<Servicio>(`${this.base}${id}/iniciar-transito/`, {});
  }

  /** Entrega: sin cuerpo. Recoleccion: requiere foto+firma (multipart). */
  cerrar(id: number, evidencia?: { foto: Blob; firma: Blob }): Observable<Servicio> {
    if (evidencia) {
      const form = new FormData();
      form.append('foto', evidencia.foto, 'foto.jpg');
      form.append('firma', evidencia.firma, 'firma.png');
      return this.http.post<Servicio>(`${this.base}${id}/cerrar/`, form);
    }
    return this.http.post<Servicio>(`${this.base}${id}/cerrar/`, {});
  }

  novedad(id: number, data: Omit<Novedad, 'servicio' | 'id' | 'creado_en'>): Observable<Servicio> {
    return this.http.post<Servicio>(`${this.base}${id}/novedad/`, data);
  }

  // Nota: el backend acepta un campo opcional "producto" (no documentado en
  // 05-api.md) que asocia el producto comprado, pero el servicio resultante
  // siempre queda con tipo=RECOLECCION sin importar lo que se envie en "tipo"
  // (tambien no documentado). Ver desviaciones reportadas.
  planificar(data: {
    zona: string;
    direccion_origen: string;
    fecha_agenda: string;
    producto?: number;
  }): Observable<Servicio> {
    return this.http.post<Servicio>(`${this.base}planificar/`, data);
  }

  mensajes(id: number): Observable<MensajeChat[]> {
    return this.http.get<MensajeChat[]>(`${this.base}${id}/mensajes/`);
  }

  enviarMensaje(id: number, texto: string): Observable<MensajeChat> {
    return this.http.post<MensajeChat>(`${this.base}${id}/mensajes/`, { texto });
  }
}
