// Contrato de GET /api/indicadores/?dias=30[&zona=Texto]
// (JWT; solo roles ADMIN y ALISTADOR). Todo se calcula en vivo sobre la base
// de datos del sistema. Las tasas son fracciones 0..1 (o null si no hay base).

export interface IndicadoresPeriodo {
  dias: number;
  desde: string; // YYYY-MM-DD
  hasta: string; // YYYY-MM-DD
  zona: string | null;
}

export interface IndicadoresResumen {
  servicios_total: number;
  entregas: number;
  recolecciones: number;
  en_curso: number;
  cerrados_exitosos: number;
  devueltos: number;
  tasa_exito: number | null;
  servicios_con_novedad: number;
  tasa_novedad: number | null;
}

export interface IndicadorPorEstado {
  estado: string;
  etiqueta: string;
  total: number;
}

export interface IndicadorDia {
  fecha: string; // YYYY-MM-DD
  entregas: number;
  recolecciones: number;
}

export interface IndicadorZona {
  zona: string;
  total: number;
  exitosos: number;
  con_novedad: number;
}

export interface IndicadorNovedadTipo {
  tipo: string;
  total: number;
}

export interface IndicadorNovedadAccion {
  accion: string;
  etiqueta: string;
  total: number;
}

export interface IndicadoresNovedades {
  total: number;
  por_tipo: IndicadorNovedadTipo[];
  por_accion: IndicadorNovedadAccion[];
}

export interface IndicadoresEvidencia {
  recolecciones_cerradas: number;
  con_evidencia_completa: number;
  porcentaje: number | null;
  horas_promedio_a_cierre: number | null;
}

export interface IndicadorMotorizado {
  id: number;
  nombre: string;
  servicios: number;
  cerrados_exitosos: number;
  con_novedad: number;
}

export interface IndicadoresOperacion {
  rutas: number;
  sin_asignar: number;
  posiciones_gps: number;
  mensajes_chat: number;
}

export interface IndicadoresEnviosWebhook {
  total: number;
  exitosos: number;
  fallidos: number;
  tasa_exito: number | null;
}

export interface IndicadoresIntegraciones {
  api_keys_activas: number;
  webhooks_activos: number;
  envios_webhook: IndicadoresEnviosWebhook;
}

export interface Indicadores {
  generado_en: string; // ISO
  periodo: IndicadoresPeriodo;
  resumen: IndicadoresResumen;
  por_estado: IndicadorPorEstado[];
  serie_diaria: IndicadorDia[];
  por_zona: IndicadorZona[];
  novedades: IndicadoresNovedades;
  evidencia: IndicadoresEvidencia;
  motorizados: IndicadorMotorizado[];
  operacion: IndicadoresOperacion;
  integraciones: IndicadoresIntegraciones;
}
