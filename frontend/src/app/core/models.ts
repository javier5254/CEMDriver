// Modelos alineados al contrato real observado en el backend (ver docs/05-api.md
// y notas de desviacion reportadas al finalizar el frontend).

export type Rol = 'ADMIN' | 'ALISTADOR' | 'MOTORIZADO' | 'CLIENTE';

export interface Usuario {
  id: number;
  username: string;
  nombre: string;
  rol: Rol;
  telefono?: string;
  email?: string;
  is_active?: boolean;
  password?: string; // solo para creacion
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: Usuario;
}

export interface Cobertura {
  id: number;
  zona: string;
  leadtime_dias: number;
  dias_disponibles: string; // ej: "LUN,MAR,MIE"
  hora_inicio: string;
  hora_fin: string;
}

export interface AgendaDisponible {
  zona: string;
  leadtime_dias: number;
  hora_inicio: string;
  hora_fin: string;
  fechas_disponibles: string[];
}

export type TipoServicio = 'ENTREGA' | 'RECOLECCION';

export type EstadoServicio =
  | 'CREADO'
  | 'ASIGNADO'
  | 'RECIBIDO_CENTRO'
  | 'EN_TRANSITO'
  | 'ENTREGADO'
  | 'RECOLECTADO'
  | 'NOVEDAD'
  | 'DEVUELTO';

export interface Evidencia {
  id: number;
  foto: string;
  firma: string;
  capturado_en: string;
}

export interface Novedad {
  id?: number;
  servicio: number;
  tipo: string;
  detalle: string;
  accion: 'DEVOLVER_A_CENTRO' | 'REINTENTAR';
  creado_en?: string;
}

export interface Servicio {
  id: number;
  tipo: TipoServicio;
  cliente: number;
  cliente_detalle?: Usuario;
  zona: string;
  direccion_origen?: string;
  direccion_destino?: string;
  fecha_agenda: string;
  estado: EstadoServicio;
  ruta?: number | null;
  creado_en?: string;
  evidencia?: Evidencia | null;
  novedades?: Novedad[];
}

export interface Ruta {
  id: number;
  motorizado: number;
  motorizado_detalle?: Usuario;
  fecha: string;
  estado: 'PLANEADA' | 'EN_CURSO' | 'FINALIZADA';
}

export interface MensajeChat {
  id: number;
  servicio: number;
  autor: number;
  autor_detalle?: Usuario;
  texto: string;
  enviado_en: string;
}

export interface PosicionGps {
  id?: number;
  servicio: number;
  lat: number | string;
  lng: number | string;
  timestamp?: string;
}
