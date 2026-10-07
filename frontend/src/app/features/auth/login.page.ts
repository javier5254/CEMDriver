import { ChangeDetectorRef, Component } from '@angular/core';
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
  selector: 'app-login',
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
          <h2 style="text-align:center;">Iniciar sesion</h2>
          <form (ngSubmit)="onSubmit()">
            <ion-item>
              <ion-label position="floating">Usuario o correo</ion-label>
              <ion-input
                [(ngModel)]="username"
                name="username"
                required
                autocapitalize="off"
                autocomplete="off"
              ></ion-input>
            </ion-item>
            <ion-item>
              <ion-label position="floating">Contrasena</ion-label>
              <ion-input
                [(ngModel)]="password"
                name="password"
                type="password"
                required
                autocomplete="new-password"
              ></ion-input>
            </ion-item>

            <ion-button expand="block" type="submit" class="ion-margin-top" [disabled]="loading">
              <ion-spinner *ngIf="loading" name="dots"></ion-spinner>
              <span *ngIf="!loading">Entrar</span>
            </ion-button>
          </form>

          <ion-text color="danger" *ngIf="error">
            <p>{{ error }}</p>
          </ion-text>

          <p style="text-align:center; margin-top: 12px;">
            <a routerLink="/forgot-password" style="font-size: 13px;">Olvidaste tu contrasena?</a>
          </p>

          <ion-text color="medium">
            <p style="font-size: 12px; margin-top: 16px;">
              Demo: admin/admin1234, alistador1/alistador1234, motorizado1/motorizado1234, cliente1/cliente1234
            </p>
          </ion-text>
        </ion-card-content>
      </ion-card>
    </ion-content>
  `,
})
export class LoginPage {
  username = '';
  password = '';
  loading = false;
  error = '';

  constructor(
    private auth: AuthService,
    private router: Router,
    private route: ActivatedRoute,
    private cdr: ChangeDetectorRef,
  ) {}

  onSubmit(): void {
    if (!this.username || !this.password) {
      this.error = 'Ingresa usuario y contrasena.';
      return;
    }
    this.loading = true;
    this.error = '';
    this.auth.login(this.username, this.password).subscribe({
      next: (res) => {
        this.loading = false;
        this.cdr.detectChanges();
        const returnUrl = this.route.snapshot.queryParamMap.get('returnUrl');
        this.router.navigateByUrl(returnUrl || this.auth.homeRouteForRole(res.user.rol));
      },
      error: (err) => {
        this.loading = false;
        this.error = err.status === 401 ? 'Usuario o contrasena incorrectos.' : extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }
}
