import { ChangeDetectorRef, Component, Input, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonItem, IonInput, IonButton, IonText, IonIcon } from '@ionic/angular';
import { ServiciosService } from '../core/services/servicios.service';
import { AuthService } from '../core/services/auth.service';
import { MensajeChat } from '../core/models';
import { extractErrorMessage, wsUrl } from '../core/utils';

const POLL_FALLBACK_MS = 5000;

/**
 * Chat de un servicio, compartido entre Cliente y Motorizado (ambos hablan
 * con el mismo hilo de mensajes) — de ahi que viva en shared/ y no dentro de
 * una sola feature. No depende del rol del usuario autenticado, solo de
 * quien sea el autor de cada mensaje.
 */
@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, IonItem, IonInput, IonButton, IonText, IonIcon],
  template: `
    <div class="ion-padding" style="display:flex; flex-direction:column; height: 100%;">
      <h2>
        Chat servicio #{{ id }}
        <span style="font-size: 11px; font-weight: 400; color: var(--ion-color-medium);">{{
          enVivo ? '(en vivo)' : '(reintentando conexion...)'
        }}</span>
      </h2>

      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>

      <div style="flex:1; overflow-y:auto; display:flex; flex-direction:column; gap:6px; padding: 8px 0;">
        <div
          *ngFor="let m of mensajes"
          [style.align-self]="esMio(m) ? 'flex-end' : 'flex-start'"
          [style.background]="esMio(m) ? 'var(--ion-color-primary)' : 'var(--ion-color-light)'"
          [style.color]="esMio(m) ? '#fff' : '#000'"
          style="max-width: 75%; padding: 8px 12px; border-radius: 12px;"
        >
          <div style="font-size: 11px; opacity: 0.8;">{{ m.autor_detalle?.nombre || m.autor }}</div>
          <div>{{ m.texto }}</div>
        </div>
        <p *ngIf="!mensajes.length" style="opacity:0.6;">No hay mensajes todavia.</p>
      </div>

      <div style="display:flex; gap: 8px;">
        <ion-item style="flex:1;">
          <ion-input
            [(ngModel)]="draft"
            placeholder="Escribe un mensaje..."
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
export class ChatPage implements OnInit, OnDestroy {
  @Input() id!: string;

  mensajes: MensajeChat[] = [];
  draft = '';
  sending = false;
  error = '';
  enVivo = false;

  private intervalRef: any = null;
  private socket: WebSocket | null = null;

  constructor(
    private serviciosService: ServiciosService,
    private authService: AuthService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.cargarHistorial();
    this.conectarEnVivo();
  }

  ngOnDestroy(): void {
    if (this.intervalRef) clearInterval(this.intervalRef);
    this.socket?.close(1000);
  }

  esMio(m: MensajeChat): boolean {
    return m.autor === this.authService.getUser()?.id;
  }

  private cargarHistorial(): void {
    this.serviciosService.mensajes(Number(this.id)).subscribe({
      next: (data) => {
        this.error = '';
        this.mensajes = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  private conectarEnVivo(): void {
    const token = this.authService.getAccessToken();
    this.socket = new WebSocket(wsUrl(`ws/chat/${this.id}/`, token));

    this.socket.onopen = () => {
      this.enVivo = true;
      this.detenerPollingDeRespaldo();
      this.cdr.detectChanges();
    };
    this.socket.onmessage = (event) => {
      try {
        const mensaje: MensajeChat = JSON.parse(event.data);
        this.mensajes = [...this.mensajes, mensaje];
        this.cdr.detectChanges();
      } catch {
        // ignora mensajes que no sean JSON valido
      }
    };
    this.socket.onerror = () => {
      this.enVivo = false;
      this.iniciarPollingDeRespaldo();
      this.cdr.detectChanges();
    };
    this.socket.onclose = (ev) => {
      if (ev.code !== 1000) {
        this.enVivo = false;
        this.iniciarPollingDeRespaldo();
        this.cdr.detectChanges();
      }
    };
  }

  private iniciarPollingDeRespaldo(): void {
    if (this.intervalRef) return;
    this.intervalRef = setInterval(() => this.cargarHistorial(), POLL_FALLBACK_MS);
  }

  private detenerPollingDeRespaldo(): void {
    if (this.intervalRef) {
      clearInterval(this.intervalRef);
      this.intervalRef = null;
    }
  }

  send(): void {
    const texto = this.draft.trim();
    if (!texto) return;
    this.sending = true;
    this.serviciosService.enviarMensaje(Number(this.id), texto).subscribe({
      next: () => {
        this.sending = false;
        this.draft = '';
        // El propio mensaje llega de vuelta por el WebSocket (el backend
        // difunde a todo el grupo, incluido el autor); si el socket no esta
        // en vivo, refrescamos por REST para no dejar el mensaje sin mostrar.
        if (!this.enVivo) this.cargarHistorial();
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.sending = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }
}
