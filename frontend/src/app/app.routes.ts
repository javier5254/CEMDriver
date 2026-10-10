import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';
import { RoleShellComponent } from './shared/role-shell.component';

import { LoginPage } from './features/auth/login.page';
import { ForgotPasswordPage } from './features/auth/forgot-password.page';
import { ResetPasswordPage } from './features/auth/reset-password.page';

import { AdminDashboardPage } from './features/admin/dashboard.page';
import { UsuariosListPage } from './features/admin/usuarios-list.page';
import { UsuarioFormPage } from './features/admin/usuario-form.page';
import { CoberturaListPage } from './features/admin/cobertura-list.page';
import { CoberturaFormPage } from './features/admin/cobertura-form.page';
import { ApiKeysListPage } from './features/admin/api-keys-list.page';
import { WebhooksListPage } from './features/admin/webhooks-list.page';

import { ServiciosListPage as AlistadorServiciosListPage } from './features/alistador/servicios-list.page';
import { ServicioFormPage } from './features/alistador/servicio-form.page';
import { RutaFormPage } from './features/alistador/ruta-form.page';
import { OptimizarRutaPage } from './features/alistador/optimizar-ruta.page';

import { MotorizadoServiciosListPage } from './features/motorizado/servicios-list.page';
import { MotorizadoServicioDetailPage } from './features/motorizado/servicio-detail.page';

import { ClienteServiciosListPage } from './features/cliente/servicios-list.page';
import { TrackingPage } from './features/cliente/tracking.page';
import { PlanificarPage } from './features/cliente/planificar.page';
import { ChatPage } from './shared/chat.page';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'login' },
  { path: 'login', component: LoginPage },
  { path: 'forgot-password', component: ForgotPasswordPage },
  { path: 'reset-password', component: ResetPasswordPage },

  {
    path: 'admin',
    component: RoleShellComponent,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['ADMIN'],
      title: 'Admin',
      segments: [
        { label: 'Dashboard', path: 'dashboard' },
        { label: 'Usuarios', path: 'usuarios' },
        { label: 'Cobertura', path: 'cobertura' },
        { label: 'API Keys', path: 'api-keys' },
        { label: 'Webhooks', path: 'webhooks' },
      ],
    },
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
      { path: 'dashboard', component: AdminDashboardPage },
      { path: 'usuarios', component: UsuariosListPage },
      { path: 'usuarios/nuevo', component: UsuarioFormPage },
      { path: 'usuarios/:id/editar', component: UsuarioFormPage },
      { path: 'cobertura', component: CoberturaListPage },
      { path: 'cobertura/nueva', component: CoberturaFormPage },
      { path: 'cobertura/:id/editar', component: CoberturaFormPage },
      { path: 'api-keys', component: ApiKeysListPage },
      { path: 'webhooks', component: WebhooksListPage },
    ],
  },

  {
    path: 'alistador',
    component: RoleShellComponent,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['ALISTADOR'],
      title: 'Alistador',
      segments: [
        { label: 'Servicios', path: 'servicios' },
        { label: 'Nuevo servicio', path: 'servicios/nuevo' },
        { label: 'Nueva ruta', path: 'rutas/nueva' },
        { label: 'Optimizar ruta', path: 'optimizar-ruta' },
      ],
    },
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'servicios' },
      { path: 'servicios', component: AlistadorServiciosListPage },
      { path: 'servicios/nuevo', component: ServicioFormPage },
      { path: 'rutas/nueva', component: RutaFormPage },
      { path: 'optimizar-ruta', component: OptimizarRutaPage },
    ],
  },

  {
    path: 'motorizado',
    component: RoleShellComponent,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['MOTORIZADO'],
      title: 'Motorizado',
      segments: [{ label: 'Mis servicios', path: 'servicios' }],
    },
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'servicios' },
      { path: 'servicios', component: MotorizadoServiciosListPage },
      { path: 'servicios/:id', component: MotorizadoServicioDetailPage },
      { path: 'servicios/:id/chat', component: ChatPage },
    ],
  },

  {
    path: 'cliente',
    component: RoleShellComponent,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['CLIENTE'],
      title: 'Cliente',
      segments: [
        { label: 'Mis servicios', path: 'servicios' },
        { label: 'Planificar recoleccion', path: 'planificar' },
      ],
    },
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'servicios' },
      { path: 'servicios', component: ClienteServiciosListPage },
      { path: 'servicios/:id/tracking', component: TrackingPage },
      { path: 'servicios/:id/chat', component: ChatPage },
      { path: 'planificar', component: PlanificarPage },
    ],
  },

  { path: '**', redirectTo: 'login' },
];
