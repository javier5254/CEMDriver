import { ChangeDetectorRef, Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import {
  IonItem,
  IonLabel,
  IonInput,
  IonSelect,
  IonSelectOption,
  IonButton,
  IonText,
  IonSpinner,
} from '@ionic/angular';
import { UsuariosService } from '../../core/services/usuarios.service';
import { Rol, Usuario } from '../../core/models';
import { extractErrorMessage } from '../../core/utils';

@Component({
  selector: 'app-usuario-form',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonItem,
    IonLabel,
    IonInput,
    IonSelect,
    IonSelectOption,
    IonButton,
    IonText,
    IonSpinner,
  ],
  template: `
    <div class="ion-padding">
      <h2>{{ id ? 'Editar usuario' : 'Nuevo usuario' }}</h2>

      <ion-spinner *ngIf="loading"></ion-spinner>

      <form (ngSubmit)="save()" *ngIf="!loading">
        <ion-item>
          <ion-label position="floating">Usuario (username)</ion-label>
          <ion-input [(ngModel)]="model.username" name="username" [disabled]="!!id" required></ion-input>
        </ion-item>
        <ion-item *ngIf="!id">
          <ion-label position="floating">Contrasena</ion-label>
          <ion-input [(ngModel)]="model.password" name="password" type="password" required></ion-input>
        </ion-item>
        <ion-item>
          <ion-label position="floating">Nombre completo</ion-label>
          <ion-input [(ngModel)]="model.nombre" name="nombre" required></ion-input>
        </ion-item>
        <ion-item>
          <ion-label position="floating">Correo</ion-label>
          <ion-input [(ngModel)]="model.email" name="email" type="email" required></ion-input>
        </ion-item>
        <ion-item>
          <ion-label>Rol</ion-label>
          <ion-select [(ngModel)]="model.rol" name="rol" required>
            <ion-select-option value="ADMIN">ADMIN</ion-select-option>
            <ion-select-option value="ALISTADOR">ALISTADOR</ion-select-option>
            <ion-select-option value="MOTORIZADO">MOTORIZADO</ion-select-option>
            <ion-select-option value="CLIENTE">CLIENTE</ion-select-option>
          </ion-select>
        </ion-item>
        <ion-item>
          <ion-label position="floating">Telefono</ion-label>
          <ion-input [(ngModel)]="model.telefono" name="telefono"></ion-input>
        </ion-item>

        <ion-button expand="block" type="submit" class="ion-margin-top" [disabled]="saving">
          {{ saving ? 'Guardando...' : 'Guardar' }}
        </ion-button>
      </form>

      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>
    </div>
  `,
})
export class UsuarioFormPage implements OnInit {
  @Input() id?: string;
  model: Partial<Usuario> = { rol: 'CLIENTE' as Rol };
  loading = false;
  saving = false;
  error = '';

  constructor(
    private usuariosService: UsuariosService,
    private router: Router,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    if (this.id) {
      this.loading = true;
      this.usuariosService.get(Number(this.id)).subscribe({
        next: (u) => {
          this.loading = false;
          this.model = { ...u };
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

  save(): void {
    this.saving = true;
    this.error = '';
    const payload = { ...this.model };
    const obs = this.id
      ? this.usuariosService.update(Number(this.id), payload)
      : this.usuariosService.create(payload);

    obs.subscribe({
      next: () => {
        this.saving = false;
        this.router.navigateByUrl('/admin/usuarios');
      },
      error: (err) => {
        this.saving = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }
}
