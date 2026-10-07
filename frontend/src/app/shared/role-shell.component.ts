import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonButton,
  IonIcon,
  IonContent,
} from '@ionic/angular';
import { AuthService } from '../core/services/auth.service';

export interface ShellSegment {
  label: string;
  path: string;
}

@Component({
  selector: 'app-role-shell',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    RouterLinkActive,
    RouterOutlet,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonButton,
    IonIcon,
    IonContent,
  ],
  template: `
    <ion-header>
      <ion-toolbar color="primary">
        <ion-title>{{ title }} <span class="user-name" *ngIf="userName"> - {{ userName }}</span></ion-title>
        <ion-buttons slot="end">
          <ion-button (click)="logout()">
            <ion-icon slot="icon-only" name="log-out-outline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar>
        <div class="nav-row">
          <ion-button
            *ngFor="let s of segments"
            [routerLink]="s.path"
            routerLinkActive="nav-active"
            fill="clear"
            size="small"
          >
            {{ s.label }}
          </ion-button>
        </div>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <router-outlet></router-outlet>
    </ion-content>
  `,
  styles: [
    `
      .nav-row {
        display: flex;
        gap: 4px;
        overflow-x: auto;
        padding: 0 4px;
      }
      .nav-active {
        --color: var(--ion-color-primary);
        font-weight: 600;
        text-decoration: underline;
      }
      .user-name {
        font-size: 13px;
        font-weight: 400;
        opacity: 0.85;
      }
    `,
  ],
})
export class RoleShellComponent {
  @Input() title = '';
  @Input() segments: ShellSegment[] = [];

  constructor(
    private auth: AuthService,
    private router: Router,
  ) {}

  get userName(): string {
    return this.auth.getUser()?.nombre || '';
  }

  logout(): void {
    this.auth.logout();
    this.router.navigateByUrl('/login');
  }
}
