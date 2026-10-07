import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import { LoginResponse, Rol, Usuario } from '../models';

const ACCESS_KEY = 'cme_access';
const REFRESH_KEY = 'cme_refresh';
const USER_KEY = 'cme_user';

@Injectable({ providedIn: 'root' })
export class AuthService {
  currentUser = signal<Usuario | null>(this.readUser());

  constructor(private http: HttpClient) {}

  private readUser(): Usuario | null {
    try {
      const raw = localStorage.getItem(USER_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }

  login(username: string, password: string): Observable<LoginResponse> {
    return this.http
      .post<LoginResponse>(`${environment.apiUrl}/auth/login/`, { username, password })
      .pipe(
        tap((res) => {
          localStorage.setItem(ACCESS_KEY, res.access);
          localStorage.setItem(REFRESH_KEY, res.refresh);
          localStorage.setItem(USER_KEY, JSON.stringify(res.user));
          this.currentUser.set(res.user);
        }),
      );
  }

  refreshToken(): Observable<{ access: string }> {
    const refresh = this.getRefreshToken();
    return this.http.post<{ access: string }>(`${environment.apiUrl}/auth/refresh/`, { refresh }).pipe(
      tap((res) => localStorage.setItem(ACCESS_KEY, res.access)),
    );
  }

  requestPasswordReset(email: string): Observable<{ detail: string }> {
    return this.http.post<{ detail: string }>(`${environment.apiUrl}/auth/password-reset/`, { email });
  }

  confirmPasswordReset(uid: string, token: string, newPassword: string): Observable<{ detail: string }> {
    return this.http.post<{ detail: string }>(`${environment.apiUrl}/auth/password-reset/confirm/`, {
      uid,
      token,
      new_password: newPassword,
    });
  }

  logout(): void {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(USER_KEY);
    this.currentUser.set(null);
  }

  isLoggedIn(): boolean {
    return !!this.getAccessToken();
  }

  getAccessToken(): string | null {
    return localStorage.getItem(ACCESS_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_KEY);
  }

  getUser(): Usuario | null {
    return this.currentUser();
  }

  homeRouteForRole(rol?: Rol | string): string {
    switch (rol) {
      case 'ADMIN':
        return '/admin';
      case 'ALISTADOR':
        return '/alistador';
      case 'MOTORIZADO':
        return '/motorizado';
      case 'CLIENTE':
        return '/cliente';
      default:
        return '/login';
    }
  }
}
