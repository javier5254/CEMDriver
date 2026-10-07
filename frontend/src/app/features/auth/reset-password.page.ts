import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
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
  selector: 'app-reset-password',
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
          <h2 style="text-align:center;">Elegir nueva contrasena</h2>

          <ion-text color="danger" *ngIf="!uid || !token">
            <p>Enlace invalido o incompleto. Solicita uno nuevo desde "Olvidaste tu contrasena?".</p>
          </ion-text>

          <form (ngSubmit)="onSubmit()" *ngIf="uid && token && !listo">
            <ion-item>
              <ion-label position="floating">Nueva contrasena</ion-label>
              <ion-input
                [(ngModel)]="newPassword"
                name="newPassword"
                type="password"
                required
                autocomplete="new-password"
              ></ion-input>
            </ion-item>

            <ion-button expand="block" type="submit" class="ion-margin-top" [disabled]="loading">
              <ion-spinner *ngIf="loading" name="dots"></ion-spinner>
              <span *ngIf="!loading">Guardar nueva contrasena</span>
            </ion-button>
          </form>

          <ion-text color="success" *ngIf="listo">
            <p>Contrasena actualizada. Ya puedes iniciar sesion con ella.</p>
          </ion-text>

          <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>

          <p style="text-align:center; margin-top: 16px;">
            <a routerLink="/login" style="font-size: 13px;">Ir a iniciar sesion</a>
          </p>
        </ion-card-content>
      </ion-card>
    </ion-content>
  `,
})
export class ResetPasswordPage implements OnInit {
  uid = '';
  token = '';
  newPassword = '';
  loading = false;
  listo = false;
  error = '';

  constructor(
    private auth: AuthService,
    private route: ActivatedRoute,
    private router: Router,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.uid = this.route.snapshot.queryParamMap.get('uid') || '';
    this.token = this.route.snapshot.queryParamMap.get('token') || '';
  }

  onSubmit(): void {
    if (!this.newPassword) return;
    this.loading = true;
    this.error = '';
    this.auth.confirmPasswordReset(this.uid, this.token, this.newPassword).subscribe({
      next: () => {
        this.loading = false;
        this.listo = true;
        this.cdr.detectChanges();
        setTimeout(() => this.router.navigateByUrl('/login'), 2500);
      },
      error: (err) => {
        this.loading = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }
}
