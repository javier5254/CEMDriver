import { ChangeDetectorRef, Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import {
  IonItem,
  IonLabel,
  IonInput,
  IonButton,
  IonText,
  IonSpinner,
  IonCheckbox,
} from '@ionic/angular';
import { CoberturaService } from '../../core/services/cobertura.service';
import { Cobertura } from '../../core/models';
import { extractErrorMessage } from '../../core/utils';

const DIAS = ['LUN', 'MAR', 'MIE', 'JUE', 'VIE', 'SAB', 'DOM'];

@Component({
  selector: 'app-cobertura-form',
  standalone: true,
  imports: [CommonModule, FormsModule, IonItem, IonLabel, IonInput, IonButton, IonText, IonSpinner, IonCheckbox],
  template: `
    <div class="ion-padding">
      <h2>{{ id ? 'Editar zona de cobertura' : 'Nueva zona de cobertura' }}</h2>

      <ion-spinner *ngIf="loading"></ion-spinner>

      <form (ngSubmit)="save()" *ngIf="!loading">
        <ion-item>
          <ion-label position="floating">Zona</ion-label>
          <ion-input [(ngModel)]="model.zona" name="zona" required></ion-input>
        </ion-item>
        <ion-item>
          <ion-label position="floating">Leadtime (dias)</ion-label>
          <ion-input [(ngModel)]="model.leadtime_dias" name="leadtime_dias" type="number" required></ion-input>
        </ion-item>

        <ion-label class="ion-margin-top" style="display:block; margin-top: 12px;">Dias disponibles</ion-label>
        <div style="display:flex; flex-wrap:wrap; gap: 8px; padding: 8px 0;">
          <ion-item *ngFor="let d of dias" lines="none" style="--min-height: 30px;">
            <ion-checkbox slot="start" [checked]="isChecked(d)" (ionChange)="toggleDia(d, $event)"></ion-checkbox>
            <ion-label>{{ d }}</ion-label>
          </ion-item>
        </div>

        <ion-item>
          <ion-label position="floating">Hora inicio (HH:mm:ss)</ion-label>
          <ion-input [(ngModel)]="model.hora_inicio" name="hora_inicio" placeholder="08:00:00" required></ion-input>
        </ion-item>
        <ion-item>
          <ion-label position="floating">Hora fin (HH:mm:ss)</ion-label>
          <ion-input [(ngModel)]="model.hora_fin" name="hora_fin" placeholder="18:00:00" required></ion-input>
        </ion-item>

        <ion-button expand="block" type="submit" class="ion-margin-top" [disabled]="saving">
          {{ saving ? 'Guardando...' : 'Guardar' }}
        </ion-button>
      </form>

      <ion-text color="danger" *ngIf="error"><p>{{ error }}</p></ion-text>
    </div>
  `,
})
export class CoberturaFormPage implements OnInit {
  @Input() id?: string;
  dias = DIAS;
  model: Partial<Cobertura> & { dias_disponibles: string } = {
    dias_disponibles: '',
    hora_inicio: '08:00:00',
    hora_fin: '18:00:00',
  };
  loading = false;
  saving = false;
  error = '';

  constructor(
    private coberturaService: CoberturaService,
    private router: Router,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    if (this.id) {
      this.loading = true;
      this.coberturaService.get(Number(this.id)).subscribe({
        next: (c) => {
          this.loading = false;
          this.model = { ...c };
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

  private diasArray(): string[] {
    return (this.model.dias_disponibles || '').split(',').map((d) => d.trim()).filter(Boolean);
  }

  isChecked(d: string): boolean {
    return this.diasArray().includes(d);
  }

  toggleDia(d: string, ev: any): void {
    const checked = ev.detail.checked;
    let arr = this.diasArray();
    if (checked && !arr.includes(d)) arr.push(d);
    if (!checked) arr = arr.filter((x) => x !== d);
    // mantener orden estandar
    arr = DIAS.filter((x) => arr.includes(x));
    this.model.dias_disponibles = arr.join(',');
  }

  save(): void {
    this.saving = true;
    this.error = '';
    const payload = { ...this.model, leadtime_dias: Number(this.model.leadtime_dias) };
    const obs = this.id
      ? this.coberturaService.update(Number(this.id), payload)
      : this.coberturaService.create(payload);

    obs.subscribe({
      next: () => {
        this.saving = false;
        this.router.navigateByUrl('/admin/cobertura');
      },
      error: (err) => {
        this.saving = false;
        this.error = extractErrorMessage(err);
        this.cdr.detectChanges();
      },
    });
  }
}
