import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import {
  IonList,
  IonItem,
  IonLabel,
  IonBadge,
  IonButton,
  IonIcon,
  IonSpinner,
  IonText,
} from '@ionic/angular';
import { UsuariosService } from '../../core/services/usuarios.service';
import { Usuario } from '../../core/models';
import { extractErrorMessage } from '../../core/utils';

@Component({
  selector: 'app-usuarios-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    IonList,
    IonItem,
    IonLabel,
    IonBadge,
    IonButton,
    IonIcon,
    IonSpinner,
    IonText,
  ],
  template: `
    <div class="ion-padding">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2>Usuarios</h2>
        <ion-button routerLink="/admin/usuarios/nuevo">
          <ion-icon slot="start" name="add-outline"></ion-icon>
          Nuevo usuario
        </ion-button>
      </div>

      <ion-spinner *ngIf="loading"></ion-spinner>
      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>

      <ion-list *ngIf="!loading && !error">
        <ion-item *ngFor="let u of usuarios">
          <ion-label>
            <h3>{{ u.nombre }} ({{ u.username }})</h3>
            <p>{{ u.telefono || 'sin telefono' }}</p>
          </ion-label>
          <ion-badge slot="end" color="primary">{{ u.rol }}</ion-badge>
          <ion-badge slot="end" [color]="u.is_active === false ? 'medium' : 'success'">
            {{ u.is_active === false ? 'Inactivo' : 'Activo' }}
          </ion-badge>
          <ion-button slot="end" fill="clear" [routerLink]="['/admin/usuarios', u.id, 'editar']">
            <ion-icon slot="icon-only" name="create-outline"></ion-icon>
          </ion-button>
          <ion-button slot="end" fill="clear" color="danger" (click)="remove(u)">
            <ion-icon slot="icon-only" name="trash-outline"></ion-icon>
          </ion-button>
        </ion-item>
      </ion-list>
    </div>
  `,
})
export class UsuariosListPage implements OnInit {
  usuarios: Usuario[] = [];
  loading = false;
  error = '';

  constructor(
    private usuariosService: UsuariosService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.fetch();
  }

  fetch(): void {
    this.loading = true;
    this.error = '';
    this.usuariosService.list().subscribe({
      next: (data) => {
        this.loading = false;
        this.usuarios = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.loading = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  remove(u: Usuario): void {
    if (!confirm(`Desactivar/eliminar a ${u.nombre}?`)) return;
    this.usuariosService.delete(u.id).subscribe({
      next: () => this.fetch(),
      error: (err) => {
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }
}
