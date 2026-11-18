import { ChangeDetectionStrategy, Component, DestroyRef, OnInit, computed, inject, signal } from '@angular/core';
import { Subscription } from 'rxjs';
import {
  IonButton,
  IonIcon,
  IonLabel,
  IonSegment,
  IonSegmentButton,
  IonSelect,
  IonSelectOption,
  IonSpinner,
} from '@ionic/angular';
import { IndicadoresService } from '../../core/services/indicadores.service';
import { CoberturaService } from '../../core/services/cobertura.service';
import { Indicadores } from '../../core/indicadores.models';
import { extractErrorMessage } from '../../core/utils';
import { PanelComponent } from '../../shared/charts/panel.component';
import { KpiTileComponent } from '../../shared/charts/kpi-tile.component';
import { RingGaugeComponent } from '../../shared/charts/ring-gauge.component';
import { SegmentedBarComponent } from '../../shared/charts/segmented-bar.component';
import { StackedColumnsComponent, StackedDatum } from '../../shared/charts/stacked-columns.component';
import { HBarListComponent, HBarRow } from '../../shared/charts/hbar-list.component';
import { StatItem, StatListComponent } from '../../shared/charts/stat-list.component';
import { StateCardComponent } from '../../shared/charts/state-card.component';
import { FilaMotorizado, MotorizadosTableComponent } from './motorizados-table.component';
import {
  ChartSegment,
  ChartSeries,
  fmtFechaCorta,
  fmtFechaHora,
  fmtFechaLarga,
  fmtFechaMedia,
  fmtHoras,
  fmtInt,
  fmtPct,
  humanizar,
} from '../../shared/charts/chart-utils';

const TODAS = '__todas__';
const MAX_ZONAS = 12;

// Semantica de color: verde = exito, ambar = en curso, rojo = novedad/devuelto.
// Los acentos (azul/turquesa) solo identifican series (entregas/recolecciones).
const VERDE = 'var(--ion-color-success)';
const AMBAR = 'var(--ion-color-warning)';
const ROJO = 'var(--ion-color-danger)';
const NEUTRO = 'rgba(var(--ion-text-color-rgb), 0.38)';
const RIEL = 'rgba(var(--ion-text-color-rgb), 0.14)';
const ACENTO_A = 'var(--ch-a)';
const ACENTO_B = 'var(--ch-b)';
// Intensidades por tema (variables CSS en :host): en oscuro los pasos claros
// necesitan mas opacidad para no hundirse en el fondo.
const PASO_1 = 'var(--o-1)';
const PASO_2 = 'var(--o-2)';
const PASO_3 = 'var(--o-3)';
const ROJO_SUAVE = 'var(--o-soft)';
const VERDE_ALT = 'var(--o-alt)';

const ESTILO_ESTADO: Record<string, { color: string; opacity: number | string }> = {
  CREADO: { color: AMBAR, opacity: PASO_1 },
  ASIGNADO: { color: AMBAR, opacity: PASO_2 },
  RECIBIDO_CENTRO: { color: AMBAR, opacity: PASO_3 },
  EN_TRANSITO: { color: AMBAR, opacity: 1 },
  NOVEDAD: { color: ROJO, opacity: ROJO_SUAVE },
  ENTREGADO: { color: VERDE, opacity: 1 },
  RECOLECTADO: { color: VERDE, opacity: VERDE_ALT },
  DEVUELTO: { color: ROJO, opacity: 1 },
};

interface Kpi {
  id: string;
  label: string;
  value: string;
  hint: string;
  dot?: string;
  ring?: number | null;
  ringColor?: string;
}

const frac = (a: number, b: number): number | null => (b > 0 ? a / b : null);
const plural = (n: number, s: string, p: string): string => (n === 1 ? s : p);

@Component({
  selector: 'app-indicadores',
  standalone: true,
  imports: [
    IonButton,
    IonIcon,
    IonLabel,
    IonSegment,
    IonSegmentButton,
    IonSelect,
    IonSelectOption,
    IonSpinner,
    PanelComponent,
    KpiTileComponent,
    RingGaugeComponent,
    SegmentedBarComponent,
    StackedColumnsComponent,
    HBarListComponent,
    StatListComponent,
    StateCardComponent,
    MotorizadosTableComponent,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="pg">
      <header class="hd">
        <div>
          <h2>Indicadores</h2>
          @if (vista(); as v) {
            <p class="sub">{{ v.periodo }}</p>
          }
        </div>
        <div class="ctl">
          <ion-segment [value]="dias()" (ionChange)="onDias($event)" aria-label="Periodo">
            @for (p of periodos; track p) {
              <ion-segment-button [value]="p"><ion-label>{{ p }} días</ion-label></ion-segment-button>
            }
          </ion-segment>
          <ion-select
            aria-label="Zona"
            interface="popover"
            [value]="zona() || todas"
            (ionChange)="onZona($event)"
          >
            <ion-select-option [value]="todas">Todas las zonas</ion-select-option>
            @for (z of zonas(); track z) {
              <ion-select-option [value]="z">{{ z }}</ion-select-option>
            }
          </ion-select>
          <ion-button fill="outline" size="small" [disabled]="cargando()" (click)="cargar()">
            @if (cargando()) {
              <ion-spinner slot="start" name="crescent"></ion-spinner>
            } @else {
              <ion-icon slot="start" name="refresh-outline"></ion-icon>
            }
            Actualizar
          </ion-button>
        </div>
      </header>

      @if (error(); as msg) {
        <app-state-card
          role="alert"
          icono="alert-circle-outline"
          [error]="true"
          titulo="No se pudieron cargar los indicadores"
          [mensaje]="msg"
        >
          <ion-button size="small" (click)="cargar()">Reintentar</ion-button>
        </app-state-card>
      } @else if (vista(); as v) {
        @if (v.vacio) {
          <app-state-card
            icono="bar-chart-outline"
            titulo="Sin servicios en el periodo"
            [mensaje]="v.vacioTxt"
          >
            @if (dias() < 90) {
              <ion-button size="small" (click)="ampliar()">Ver últimos 90 días</ion-button>
            }
            @if (zona()) {
              <ion-button size="small" fill="outline" (click)="quitarZona()">Todas las zonas</ion-button>
            }
          </app-state-card>
        } @else {
          <div class="cont" [class.stale]="cargando()" [attr.aria-busy]="cargando()">
            <section class="kpis" aria-label="Resumen">
              @for (k of v.kpis; track k.id) {
                <app-kpi-tile
                  [label]="k.label"
                  [value]="k.value"
                  [hint]="k.hint"
                  [dot]="k.dot ?? ''"
                  [ring]="k.ring"
                  [ringColor]="k.ringColor ?? verde"
                />
              }
            </section>

            <div class="grid">
              <app-panel class="w" titulo="Servicios por día" [subtitulo]="v.serieTxt">
                <app-stacked-columns [data]="v.serie" [series]="v.series" [ariaLabel]="v.serieAria" />
              </app-panel>

              <app-panel titulo="Estado de los servicios" [subtitulo]="v.estadosTxt">
                <app-segmented-bar [segments]="v.estados" [ariaLabel]="'Servicios por estado. ' + v.estadosTxt" />
              </app-panel>

              <app-panel titulo="Zonas" [subtitulo]="v.zonasTxt">
                @if (v.zonas.length) {
                  <app-hbar-list [rows]="v.zonas" [legend]="leyendaZonas" />
                } @else {
                  <p class="nd">Sin servicios por zona en el periodo.</p>
                }
              </app-panel>

              <app-panel titulo="Novedades" [subtitulo]="v.novedadesTxt">
                @if (v.novedadesTipo.length || v.novedadesAccion.length) {
                  <h4>Por tipo</h4>
                  <app-hbar-list [rows]="v.novedadesTipo" />
                  <h4>Por acción tomada</h4>
                  <app-hbar-list [rows]="v.novedadesAccion" />
                } @else {
                  <p class="nd">No se registraron novedades en el periodo.</p>
                }
              </app-panel>

              <app-panel titulo="Motorizados" subtitulo="Servicios asignados y avance de cierre exitoso">
                @if (v.motorizados.length) {
                  <app-motorizados-table [filas]="v.motorizados" />
                } @else {
                  <p class="nd">Ningún motorizado con servicios en el periodo.</p>
                }
              </app-panel>

              <app-panel titulo="Operación" subtitulo="Estado actual de rutas, seguimiento y chat">
                <app-stat-list [items]="v.operacion" />
              </app-panel>

              <app-panel titulo="Integraciones" subtitulo="Llaves, webhooks y entrega de eventos">
                <app-stat-list [items]="v.integraciones" />
                <div class="env">
                  <app-ring-gauge
                    [value]="v.envios.tasa"
                    [color]="verde"
                    [size]="56"
                    [stroke]="7"
                    [ariaLabel]="'Tasa de éxito de envíos de webhook'"
                  />
                  <div class="et">
                    <strong>Envíos de webhook: {{ v.envios.tasaTxt }} exitosos</strong>
                    <span>{{ v.envios.detalle }}</span>
                    <app-segmented-bar
                      [segments]="v.envios.segs"
                      [total]="v.envios.total"
                      [height]="8"
                      [legend]="false"
                      [ariaLabel]="v.envios.detalle"
                    />
                  </div>
                </div>
              </app-panel>
            </div>
          </div>
        }
        <footer class="ft">
          Calculado en vivo sobre la base de datos del sistema · {{ v.generado }}
        </footer>
      } @else {
        <app-state-card role="status" [cargando]="true" mensaje="Cargando indicadores…" />
      }
    </div>
  `,
  styles: [
    `
      :host {
        display: block;
        font-variant-numeric: tabular-nums;
        --ch-a: #0a60c9;
        --ch-b: #13a0b0;
        --o-1: 0.5;
        --o-2: 0.68;
        --o-3: 0.84;
        --o-soft: 0.55;
        --o-alt: 0.62;
      }
      @media (prefers-color-scheme: dark) {
        :host {
          --ch-a: #0a84ff;
          --ch-b: #30c8d8;
          --o-1: 0.62;
          --o-2: 0.76;
          --o-3: 0.88;
          --o-soft: 0.72;
          --o-alt: 0.7;
        }
      }
      .pg {
        max-width: 1280px;
        margin: 0 auto;
        padding: 16px 16px 32px;
      }
      .hd {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-end;
        justify-content: space-between;
        gap: 12px 16px;
        margin-bottom: 16px;
      }
      h2 {
        margin: 0;
        font-size: 24px;
        font-weight: 700;
      }
      .sub {
        margin: 2px 0 0;
        font-size: 13px;
        color: rgba(var(--ion-text-color-rgb), 0.62);
      }
      .ctl {
        display: flex;
        flex: 1 1 420px;
        flex-wrap: wrap;
        align-items: center;
        justify-content: flex-end;
        gap: 8px;
      }
      ion-segment {
        flex: 1 1 260px;
        max-width: 360px;
        min-width: 0;
      }
      ion-select {
        flex: 0 1 200px;
        min-width: 150px;
        min-height: 36px;
        padding: 0 12px;
        border-radius: 10px;
        background: var(--ion-item-background, #fff);
      }
      ion-button {
        margin: 0;
      }
      .cont {
        transition: opacity 0.15s;
      }
      .stale {
        opacity: 0.55;
        pointer-events: none;
      }
      .kpis {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 12px;
        margin-bottom: 12px;
      }
      .grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        align-items: start;
        gap: 12px;
      }
      .grid > * {
        grid-column: span 2;
      }
      @media (min-width: 960px) {
        .grid > * {
          grid-column: span 1;
        }
        .grid > .w {
          grid-column: span 2;
        }
      }
      h4 {
        margin: 16px 0 8px;
        font-size: 12px;
        font-weight: 600;
        color: rgba(var(--ion-text-color-rgb), 0.62);
      }
      h4:first-child {
        margin-top: 0;
      }
      .nd {
        margin: 0;
        font-size: 13px;
        color: rgba(var(--ion-text-color-rgb), 0.62);
      }
      .env {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-top: 16px;
        padding-top: 14px;
        border-top: 1px solid rgba(var(--ion-text-color-rgb), 0.07);
      }
      .et {
        display: grid;
        flex: 1;
        gap: 4px;
        min-width: 0;
        font-size: 13px;
      }
      .et span {
        font-size: 12px;
        color: rgba(var(--ion-text-color-rgb), 0.62);
      }
      .ft {
        margin-top: 16px;
        font-size: 12px;
        color: rgba(var(--ion-text-color-rgb), 0.62);
      }
    `,
  ],
})
export class IndicadoresPage implements OnInit {
  private readonly api = inject(IndicadoresService);
  private readonly cobertura = inject(CoberturaService);
  private readonly destroyRef = inject(DestroyRef);
  private sub?: Subscription;

  protected readonly periodos = [7, 30, 60, 90];
  protected readonly todas = TODAS;
  protected readonly verde = VERDE;
  protected readonly leyendaZonas: ChartSeries[] = [
    { label: 'Cerrados con éxito', color: VERDE },
    { label: 'Con novedad', color: ROJO, opacity: ROJO_SUAVE },
    { label: 'Total de la zona', color: RIEL },
  ];

  protected readonly dias = signal(30);
  protected readonly zona = signal('');
  protected readonly datos = signal<Indicadores | null>(null);
  protected readonly cargando = signal(false);
  protected readonly error = signal('');
  private readonly zonasCobertura = signal<string[]>([]);

  /** Zonas de cobertura + las que trae el reporte (+ la seleccionada). */
  protected readonly zonas = computed(() => {
    const set = new Set<string>(this.zonasCobertura());
    for (const z of this.datos()?.por_zona ?? []) set.add(z.zona);
    if (this.zona()) set.add(this.zona());
    return [...set].sort((a, b) => a.localeCompare(b, 'es'));
  });

  protected readonly vista = computed(() => {
    const d = this.datos();
    return d ? this.armarVista(d) : null;
  });

  ngOnInit(): void {
    this.destroyRef.onDestroy(() => this.sub?.unsubscribe());
    this.cargar();
    // El filtro de zona se alimenta de la cobertura; si falla, se usan las zonas del reporte.
    this.cobertura.list().subscribe({
      next: (c) => this.zonasCobertura.set(c.map((x) => x.zona)),
      error: () => this.zonasCobertura.set([]),
    });
  }

  cargar(): void {
    this.sub?.unsubscribe();
    this.cargando.set(true);
    this.error.set('');
    this.sub = this.api.obtener(this.dias(), this.zona() || null).subscribe({
      next: (d) => {
        this.datos.set(d);
        this.cargando.set(false);
      },
      error: (err) => {
        this.datos.set(null);
        this.error.set(extractErrorMessage(err));
        this.cargando.set(false);
      },
    });
  }

  protected onDias(e: Event): void {
    const v = Number((e as CustomEvent).detail?.value);
    if (!v || v === this.dias()) return;
    this.dias.set(v);
    this.cargar();
  }

  protected onZona(e: Event): void {
    const raw = (e as CustomEvent).detail?.value;
    const z = !raw || raw === TODAS ? '' : String(raw);
    if (z === this.zona()) return;
    this.zona.set(z);
    this.cargar();
  }

  protected ampliar(): void {
    this.dias.set(90);
    this.cargar();
  }

  protected quitarZona(): void {
    this.zona.set('');
    this.cargar();
  }

  private armarVista(d: Indicadores) {
    const r = d.resumen;
    const ev = d.evidencia;
    const op = d.operacion;
    const ig = d.integraciones;
    const env = ig.envios_webhook;

    const kpis: Kpi[] = [
      {
        id: 'total',
        label: 'Servicios del periodo',
        value: fmtInt(r.servicios_total),
        hint: `${fmtInt(r.entregas)} ${plural(r.entregas, 'entrega', 'entregas')} · ${fmtInt(r.recolecciones)} ${plural(r.recolecciones, 'recolección', 'recolecciones')}`,
      },
      {
        id: 'exito',
        label: 'Tasa de éxito',
        value: fmtPct(r.tasa_exito),
        hint: `${fmtInt(r.cerrados_exitosos)} cerrados con éxito`,
        ring: r.tasa_exito,
        ringColor: VERDE,
      },
      {
        id: 'novedad',
        label: 'Tasa de novedad',
        value: fmtPct(r.tasa_novedad),
        hint: `${fmtInt(r.servicios_con_novedad)} ${plural(r.servicios_con_novedad, 'servicio', 'servicios')} con novedad`,
        ring: r.tasa_novedad,
        ringColor: ROJO,
      },
      {
        id: 'curso',
        label: 'En curso',
        value: fmtInt(r.en_curso),
        hint: `Devueltos: ${fmtInt(r.devueltos)}`,
        dot: AMBAR,
      },
      {
        id: 'evidencia',
        label: 'Evidencia completa',
        value: fmtPct(ev.porcentaje),
        hint: `${fmtInt(ev.con_evidencia_completa)} de ${fmtInt(ev.recolecciones_cerradas)} recolecciones cerradas`,
        ring: ev.porcentaje,
        ringColor: VERDE,
      },
      {
        id: 'horas',
        label: 'Promedio a cierre',
        value: fmtHoras(ev.horas_promedio_a_cierre),
        hint: 'Horas hasta cerrar una recolección',
      },
    ];

    const serie: StackedDatum[] = d.serie_diaria.map((x) => ({
      key: x.fecha,
      label: fmtFechaCorta(x.fecha),
      title: fmtFechaLarga(x.fecha),
      values: [x.entregas, x.recolecciones],
    }));
    const series: ChartSeries[] = [
      { label: 'Entregas', color: ACENTO_A },
      { label: 'Recolecciones', color: ACENTO_B },
    ];
    const totalSerie = d.serie_diaria.reduce((a, x) => a + x.entregas + x.recolecciones, 0);
    const primero = d.serie_diaria[0]?.fecha;
    const ultimo = d.serie_diaria[d.serie_diaria.length - 1]?.fecha;
    const serieAria = primero
      ? `Servicios por día entre ${fmtFechaCorta(primero)} y ${fmtFechaCorta(ultimo)}: ${fmtInt(totalSerie)} en total`
      : 'Servicios por día';

    const estados: ChartSegment[] = d.por_estado.map((e) => ({
      id: e.estado,
      label: e.etiqueta,
      value: e.total,
      color: ESTILO_ESTADO[e.estado]?.color ?? NEUTRO,
      opacity: ESTILO_ESTADO[e.estado]?.opacity ?? 1,
    }));
    const totalEstados = d.por_estado.reduce((a, e) => a + e.total, 0);

    const porZona = [...d.por_zona].sort((a, b) => b.total - a.total);
    const zonas: HBarRow[] = porZona.slice(0, MAX_ZONAS).map((z) => ({
      id: z.zona,
      label: z.zona,
      valueText: `${fmtInt(z.total)} ${plural(z.total, 'servicio', 'servicios')}`,
      ref: z.total,
      bars: [
        { value: z.exitosos, color: VERDE },
        { value: z.con_novedad, color: ROJO, opacity: ROJO_SUAVE },
      ],
      sub: `Éxito ${fmtInt(z.exitosos)} (${fmtPct(frac(z.exitosos, z.total))}) · Novedad ${fmtInt(z.con_novedad)} (${fmtPct(frac(z.con_novedad, z.total))})`,
    }));

    const novedadesTipo: HBarRow[] = [...d.novedades.por_tipo]
      .sort((a, b) => b.total - a.total)
      .map((n) => ({
        id: n.tipo,
        label: humanizar(n.tipo),
        valueText: fmtInt(n.total),
        bars: [{ value: n.total, color: ROJO, opacity: ROJO_SUAVE }],
      }));
    const novedadesAccion: HBarRow[] = [...d.novedades.por_accion]
      .sort((a, b) => b.total - a.total)
      .map((n) => ({
        id: n.accion,
        label: n.etiqueta,
        valueText: fmtInt(n.total),
        bars: [{ value: n.total, color: ACENTO_A }],
      }));

    const motorizados: FilaMotorizado[] = [...d.motorizados]
      .sort((a, b) => b.servicios - a.servicios)
      .map((m) => ({
        id: m.id,
        nombre: m.nombre,
        servicios: fmtInt(m.servicios),
        cerrados: fmtInt(m.cerrados_exitosos),
        novedad: fmtInt(m.con_novedad),
        total: m.servicios,
        segs: [{ id: 'ok', label: 'Cerrados con éxito', value: m.cerrados_exitosos, color: VERDE }],
        aria: `${m.nombre}: ${fmtPct(frac(m.cerrados_exitosos, m.servicios))} cerrados con éxito`,
      }));

    const operacion: StatItem[] = [
      { label: 'Rutas', value: fmtInt(op.rutas) },
      { label: 'Sin asignar', value: fmtInt(op.sin_asignar), dot: op.sin_asignar > 0 ? AMBAR : undefined },
      { label: 'Posiciones GPS', value: fmtInt(op.posiciones_gps) },
      { label: 'Mensajes de chat', value: fmtInt(op.mensajes_chat) },
    ];
    const integraciones: StatItem[] = [
      { label: 'API keys activas', value: fmtInt(ig.api_keys_activas) },
      { label: 'Webhooks activos', value: fmtInt(ig.webhooks_activos) },
    ];

    return {
      vacio: r.servicios_total === 0,
      vacioTxt: `No hay servicios en los últimos ${d.periodo.dias} días${d.periodo.zona ? ' para la zona ' + d.periodo.zona : ''}. Amplía el periodo o quita el filtro de zona para ver indicadores.`,
      periodo: `${fmtFechaMedia(d.periodo.desde)} – ${fmtFechaMedia(d.periodo.hasta)} · ${d.periodo.zona ?? 'Todas las zonas'}`,
      generado: fmtFechaHora(d.generado_en),
      kpis,
      serie,
      series,
      serieAria,
      serieTxt: `${fmtInt(totalSerie)} servicios en ${fmtInt(d.serie_diaria.length)} días`,
      estados,
      estadosTxt: `${fmtInt(totalEstados)} ${plural(totalEstados, 'servicio', 'servicios')} en total`,
      zonas,
      zonasTxt:
        porZona.length > MAX_ZONAS
          ? `Las ${MAX_ZONAS} zonas con más servicios, de ${fmtInt(porZona.length)}`
          : 'Servicios cerrados con éxito y con novedad por zona',
      novedadesTipo,
      novedadesAccion,
      novedadesTxt: `${fmtInt(d.novedades.total)} ${plural(d.novedades.total, 'novedad', 'novedades')} en el periodo`,
      motorizados,
      operacion,
      integraciones,
      envios: {
        total: env.total,
        tasa: env.tasa_exito,
        tasaTxt: fmtPct(env.tasa_exito),
        detalle:
          env.total > 0
            ? `${fmtInt(env.total)} envíos · ${fmtInt(env.exitosos)} exitosos · ${fmtInt(env.fallidos)} fallidos`
            : 'Sin envíos en el periodo',
        segs: [
          { id: 'ok', label: 'Exitosos', value: env.exitosos, color: VERDE },
          { id: 'fail', label: 'Fallidos', value: env.fallidos, color: ROJO },
        ] as ChartSegment[],
      },
    };
  }
}
