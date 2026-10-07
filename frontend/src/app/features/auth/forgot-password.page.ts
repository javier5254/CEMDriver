import { ChangeDetectorRef, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import {
  IonContent,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonItem,
  IonLabel,
  IonInput,
  IonButton,
  IonText,
  IonSpinner,
  IonCard,
  IonCardContent,
} from '@ionic/angular';
import { AuthService } from '../../core/services/auth.service';
import { extractErrorMessage } from '../../core/utils';

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,
    IonContent,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonItem,
    IonLabel,
    IonInput,
    IonButton,
    IonText,
    IonSpinner,
    IonCard,
    IonCardContent,
  ],
  template: `
    <ion-header>
      <ion-toolbar color="primary">
        <ion-title>CMEDriver</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <ion-card style="max-width: 420px; margin: 40px auto;">
        <ion-card-content>
          <h2 style="text-align:center;">Restablecer contrasena</h2>
          <p style="font-size: 13px; color: var(--ion-color-medium);">
            Ingresa el correo con el que te registraste. Si existe una cuenta, te enviaremos un enlace para elegir
            una nueva contrasena.
          </p>

          <form (ngSubmit)="onSubmit()" *ngIf="!enviado">
            <ion-item>
              <ion-label position="floating">Correo</ion-label>
              <ion-input [(ngModel)]="email" name="email" type="email" required autocomplete="email"></ion-input>
            </ion-item>

            <ion-button expand="block" type="submit" class="ion-margin-top" [disabled]="loading">
              <ion-spinner *ngIf="loading" name="dots"></ion-spinner>
              <span *ngIf="!loading">Enviar enlace</span>
            </ion-button>
          </form>

          <ion-text color="success" *ngIf="enviado">
            <p>
              Si el correo esta registrado, revisa tu bandeja (o la consola del servidor en modo desarrollo) para
              ver el enlace de restablecimiento.
            </p>
          </ion-text>

          <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>

          <p style="text-align:center; margin-top: 16px;">
            <a routerLink="/login" style="font-size: 13px;">Volver a iniciar sesion</a>
          </p>
        </ion-card-content>
      </ion-card>
    </ion-content>
  `,
})
export class ForgotPasswordPage {
  email = '';
  loading = false;
  enviado = false;
  error = '';

  constructor(
    private auth: AuthService,
    private cdr: ChangeDetectorRef,
  ) {}

  onSubmit(): void {
    if (!this.email) return;
    this.loading = true;
    this.error = '';
    this.auth.requestPasswordReset(this.email).subscribe({
      next: () => {
        this.loading = false;
        this.enviado = true;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.loading = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }
}
