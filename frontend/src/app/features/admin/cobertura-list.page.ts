import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import {
  IonList,
  IonItem,
  IonLabel,
  IonButton,
  IonIcon,
  IonSpinner,
  IonText,
} from '@ionic/angular';
import { CoberturaService } from '../../core/services/cobertura.service';
import { Cobertura } from '../../core/models';
import { extractErrorMessage } from '../../core/utils';

@Component({
  selector: 'app-cobertura-list',
  standalone: true,
  imports: [CommonModule, RouterLink, IonList, IonItem, IonLabel, IonButton, IonIcon, IonSpinner, IonText],
  template: `
    <div class="ion-padding">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2>Matriz de cobertura</h2>
        <ion-button routerLink="/admin/cobertura/nueva">
          <ion-icon slot="start" name="add-outline"></ion-icon>
          Nueva zona
        </ion-button>
      </div>

      <ion-spinner *ngIf="loading"></ion-spinner>
      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>

      <ion-list *ngIf="!loading && !error">
        <ion-item *ngFor="let c of items">
          <ion-label>
            <h3>{{ c.zona }}</h3>
            <p>Leadtime: {{ c.leadtime_dias }} dia(s) - Dias: {{ c.dias_disponibles }}</p>
            <p>Horario: {{ c.hora_inicio }} - {{ c.hora_fin }}</p>
          </ion-label>
          <ion-button slot="end" fill="clear" [routerLink]="['/admin/cobertura', c.id, 'editar']">
            <ion-icon slot="icon-only" name="create-outline"></ion-icon>
          </ion-button>
          <ion-button slot="end" fill="clear" color="danger" (click)="remove(c)">
            <ion-icon slot="icon-only" name="trash-outline"></ion-icon>
          </ion-button>
        </ion-item>
      </ion-list>
    </div>
  `,
})
export class CoberturaListPage implements OnInit {
  items: Cobertura[] = [];
  loading = false;
  error = '';

  constructor(
    private coberturaService: CoberturaService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.fetch();
  }

  fetch(): void {
    this.loading = true;
    this.error = '';
    this.coberturaService.list().subscribe({
      next: (data) => {
        this.loading = false;
        this.items = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.loading = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }

  remove(c: Cobertura): void {
    if (!confirm(`Eliminar zona ${c.zona}?`)) return;
    this.coberturaService.delete(c.id).subscribe({
      next: () => this.fetch(),
      error: (err) => {
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }
}
