import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

/**
 * Accion resultante cuando la respuesta del bot invoco una "tool" que creo
 * algo en el dominio (ver chatbot/views.py MensajeChatbotView._extraer_accion
 * en el backend).
 */
export interface ChatbotAccion {
  tipo: 'servicio_creado' | 'pago';
  servicio_id: number;
  estado?: string; // estado del servicio (tipo=servicio_creado) o del pago (tipo=pago)
  pago_id?: number;
}

export interface ChatbotMensajeResponse {
  conversacion_id: number;
  respuesta: string;
  accion: ChatbotAccion | null;
}

export interface ChatbotMensaje {
  id: number;
  conversacion: number;
  autor: 'CLIENTE' | 'BOT';
  texto: string;
  function_call: Record<string, unknown> | null;
  creado_en: string;
}

@Injectable({ providedIn: 'root' })
export class ChatbotService {
  private base = `${environment.apiUrl}/chatbot/`;

  constructor(private http: HttpClient) {}

  enviarMensaje(texto: string, conversacionId?: number | null): Observable<ChatbotMensajeResponse> {
    const body: { texto: string; conversacion_id?: number } = { texto };
    if (conversacionId) body.conversacion_id = conversacionId;
    return this.http.post<ChatbotMensajeResponse>(`${this.base}mensaje/`, body);
  }

  historial(conversacionId: number): Observable<ChatbotMensaje[]> {
    return this.http.get<ChatbotMensaje[]>(`${this.base}conversaciones/${conversacionId}/mensajes/`);
  }
}
