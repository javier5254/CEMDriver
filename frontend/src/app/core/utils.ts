import { EstadoServicio } from './models';
import { environment } from '../../environments/environment';

export function estadoColor(estado: EstadoServicio | string): string {
  switch (estado) {
    case 'CREADO':
      return 'medium';
    case 'ASIGNADO':
      return 'primary';
    case 'RECIBIDO_CENTRO':
      return 'tertiary';
    case 'EN_TRANSITO':
      return 'warning';
    case 'ENTREGADO':
    case 'RECOLECTADO':
      return 'success';
    case 'NOVEDAD':
      return 'danger';
    case 'DEVUELTO':
      return 'dark';
    default:
      return 'medium';
  }
}

/** Extrae un mensaje de error legible de una respuesta HTTP de Django/DRF. */
export function extractErrorMessage(err: any): string {
  if (!err) return 'Error desconocido';
  if (err.status === 0) return 'No se pudo conectar con el servidor.';
  const body = err.error;
  if (typeof body === 'string') return body;
  if (body && typeof body === 'object') {
    const parts: string[] = [];
    for (const key of Object.keys(body)) {
      const val = body[key];
      if (Array.isArray(val)) parts.push(`${key}: ${val.join(', ')}`);
      else parts.push(`${key}: ${val}`);
    }
    if (parts.length) return parts.join(' | ');
  }
  return err.message || 'Ocurrio un error inesperado.';
}

/**
 * El backend a veces serializa foto/firma de evidencia como URL absoluta
 * (http://host/media/...) y otras como ruta relativa (/media/...) segun el
 * contexto de la request. Normaliza siempre contra el origen del backend.
 */
export function mediaUrl(path: string | null | undefined): string {
  if (!path) return '';
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  const origin = environment.apiUrl.replace(/\/api\/?$/, '');
  return `${origin}${path.startsWith('/') ? '' : '/'}${path}`;
}

/** Construye una URL ws:// para conectarse a los consumers de Channels, con el access token como query param. */
export function wsUrl(path: string, token: string | null): string {
  const httpOrigin = environment.apiUrl.replace(/\/api\/?$/, '');
  const wsOrigin = httpOrigin.replace(/^http/, 'ws');
  const cleanPath = path.startsWith('/') ? path.slice(1) : path;
  return `${wsOrigin}/${cleanPath}${token ? `?token=${encodeURIComponent(token)}` : ''}`;
}
