import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { IonIcon, IonSpinner } from '@ionic/angular';

/** Estado de pantalla (cargando, vacio o error) con icono, mensaje y acciones proyectadas. */
@Component({
  selector: 'app-state-card',
  standalone: true,
  imports: [IonIcon, IonSpinner],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @if (cargando()) {
      <ion-spinner name="crescent"></ion-spinner>
    } @else if (icono()) {
      <ion-icon [name]="icono()" [class.err]="error()"></ion-icon>
    }
    @if (titulo()) {
      <strong>{{ titulo() }}</strong>
    }
    @if (mensaje()) {
      <p>{{ mensaje() }}</p>
    }
    <div class="acc"><ng-content /></div>
  `,
  styles: [
    `
      :host {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        padding: 40px 16px;
        text-align: center;
        border-radius: 14px;
        background: var(--ion-item-background, #fff);
        box-shadow: 0 0 0 1px rgba(var(--ion-text-color-rgb), 0.06);
      }
      p {
        max-width: 460px;
        margin: 0;
        font-size: 13px;
        color: rgba(var(--ion-text-color-rgb), 0.68);
      }
      ion-icon {
        font-size: 40px;
        color: rgba(var(--ion-text-color-rgb), 0.4);
      }
      ion-icon.err {
        color: var(--ion-color-danger);
      }
      .acc {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
        margin-top: 8px;
      }
      .acc:empty {
        display: none;
      }
    `,
  ],
})
export class StateCardComponent {
  readonly icono = input('');
  readonly titulo = input('');
  readonly mensaje = input('');
  readonly cargando = input(false);
  readonly error = input(false);
}
