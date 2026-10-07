import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonBadge, IonButton, IonIcon, IonInput, IonItem, IonSpinner, IonText } from '@ionic/angular';
import { ChatbotAccion, ChatbotService } from '../../core/services/chatbot.service';
import { extractErrorMessage } from '../../core/utils';

interface HiloMensaje {
  autor: 'CLIENTE' | 'BOT';
  texto: string;
  accion?: ChatbotAccion | null;
}

/**
 * Chatbot conversacional (RF de "innovacion"): hilo de mensajes libres contra
 * POST /api/chatbot/mensaje/, en vez del menu fijo de botones que tenia antes
 * esta pantalla. El backend responde con una "tool" invocada por un LLM
 * simulado (ver chatbot/llm.py); cuando esa tool crea un servicio o procesa
 * un pago, se muestra una tarjeta/insignia de confirmacion en el hilo.
 */
@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule, IonBadge, IonButton, IonIcon, IonInput, IonItem, IonSpinner, IonText],
  template: `
    <div class="ion-padding" style="display:flex; flex-direction:column; height: 100%;">
      <h2>
        <ion-icon name="chatbubble-outline"></ion-icon>
        Chatbot CMEDriver
      </h2>

      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>

      <div style="flex:1; overflow-y:auto; display:flex; flex-direction:column; gap:6px; padding: 8px 0;">
        <ng-container *ngFor="let m of hilo">
          <div
            [style.align-self]="m.autor === 'CLIENTE' ? 'flex-end' : 'flex-start'"
            [style.background]="m.autor === 'CLIENTE' ? 'var(--ion-color-primary)' : 'var(--ion-color-light)'"
            [style.color]="m.autor === 'CLIENTE' ? '#fff' : '#000'"
            style="max-width: 80%; padding: 8px 12px; border-radius: 12px; white-space: pre-line;"
          >
            <div style="font-size: 11px; opacity: 0.8;">{{ m.autor === 'CLIENTE' ? 'Tu' : 'Asistente' }}</div>
            <div>{{ m.texto }}</div>
          </div>
          <ion-badge
            *ngIf="m.accion"
            [color]="accionColor(m.accion)"
            style="align-self: flex-start; margin-left: 4px; white-space: normal;"
          >
            {{ accionLabel(m.accion) }}
          </ion-badge>
        </ng-container>

        <ion-spinner *ngIf="sending" name="dots" style="align-self: flex-start;"></ion-spinner>
        <p *ngIf="!hilo.length" style="opacity:0.6;">Escribe un mensaje para empezar.</p>
      </div>

      <div style="display:flex; gap: 8px;">
        <ion-item style="flex:1;">
          <ion-input
            [(ngModel)]="draft"
            placeholder="Escribe tu mensaje..."
            (keyup.enter)="send()"
          ></ion-input>
        </ion-item>
        <ion-button (click)="send()" [disabled]="!draft.trim() || sending">
          <ion-icon slot="icon-only" name="send-outline"></ion-icon>
        </ion-button>
      </div>
    </div>
  `,
})
export class ChatbotPage implements OnInit {
  hilo: HiloMensaje[] = [];
  draft = '';
  sending = false;
  error = '';
  conversacionId: number | null = null;

  constructor(
    private chatbotService: ChatbotService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.hilo.push({
      autor: 'BOT',
      texto:
        'Hola! Escribeme "hola" para ver el menu, o cuentame directamente que necesitas ' +
        '(ej. "quiero comprar" o "quiero que recojan un paquete").',
    });
  }

  send(): void {
    const texto = this.draft.trim();
    if (!texto || this.sending) return;

    this.hilo.push({ autor: 'CLIENTE', texto });
    this.draft = '';
    this.sending = true;
    this.error = '';
    this.cdr.detectChanges();

    this.chatbotService.enviarMensaje(texto, this.conversacionId).subscribe({
      next: (res) => {
        this.sending = false;
        this.conversacionId = res.conversacion_id;
        this.hilo.push({ autor: 'BOT', texto: res.respuesta, accion: res.accion });
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.sending = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  accionLabel(accion?: ChatbotAccion | null): string {
    if (!accion) return '';
    if (accion.tipo === 'servicio_creado') return `Servicio #${accion.servicio_id} creado (${accion.estado})`;
    if (accion.tipo === 'pago') {
      const estado = accion.estado === 'APROBADO' ? 'aprobado' : 'rechazado';
      return `Pago ${estado} - servicio #${accion.servicio_id}`;
    }
    return '';
  }

  accionColor(accion?: ChatbotAccion | null): string {
    if (!accion) return 'medium';
    if (accion.tipo === 'servicio_creado') return 'success';
    if (accion.tipo === 'pago') return accion.estado === 'APROBADO' ? 'success' : 'danger';
    return 'medium';
  }
}
