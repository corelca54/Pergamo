import type { RegistroPeriodo } from "../entities/RegistroPeriodo";

// CONTRATO. El dominio y los casos de uso solo conocen esta interfaz.
// Hoy la implementa Firestore (infrastructure/repositories). Manana podria implementarla
// Azure SQL o cualquier otra cosa, sin tocar una sola linea de application/ ni presentation/.
export interface IRegistroPeriodoRepository {
  listarPorUnidad(unidadOperativaId: string): Promise<RegistroPeriodo[]>;
  /** Trae TODOS los registros -- se usa para calcular el resumen del lado del cliente (ver
   *  CalcularResumenDashboard). En el plan gratuito de Firestore no hay Cloud Functions para
   *  mantener un documento agregado, asi que el calculo se hace en el navegador, igual que
   *  hace Excel al recalcular. Para el volumen de datos de este proyecto (cientos de filas,
   *  no millones) esto es rapido y no cuesta nada extra. */
  listarTodos(): Promise<RegistroPeriodo[]>;
  listarPagina(params: {
    dependencia?: string;
    subdireccionLocal?: string;
    servicio?: string;
    periodo?: string;
    cursor?: unknown;
    tamanoPagina: number;
  }): Promise<{ items: RegistroPeriodo[]; nextCursor: unknown | null }>;
  guardar(registro: Omit<RegistroPeriodo, "id" | "creadoEn" | "actualizadoEn">): Promise<RegistroPeriodo>;
  actualizar(id: string, cambios: Partial<RegistroPeriodo>): Promise<void>;
  suscribirseAResumen(
    filtros: { dependencia?: string; subdireccionLocal?: string; servicio?: string; periodo?: string },
    onCambio: (resumen: ResumenDashboard) => void
  ): () => void; // devuelve la funcion "unsubscribe"
}

/** Documento agregado precalculado -- 1 sola lectura para pintar todo el dashboard. Espejo de
 *  las tarjetas KPI + tablas del Dashboard en Excel. */
export interface ResumenDashboard {
  cajasVigentesEnSitio: number;
  totalCajasHistorico: number;
  avancePromedioGlobal: number;
  unidadesOperativas: number;
  cajasEliminacionHistorico: number;
  cajasEliminacionEstePeriodo: number;
  unidadesEnRiesgoAlto: number;
  cajasSobreapiladas: number;
  metrosEspacioAjenoInvadido: number;
  porDependenciaServicio: Array<{
    dependencia: string;
    servicio: string;
    totalCajas: number;
    avancePromedio: number;
  }>;
  porTarea: Array<{ tarea: string; avancePromedio: number }>;
  porPeriodo: Array<{ periodo: string; totalCajas: number; avancePromedio: number }>;
  /** Nivel intermedio "por SLIS", no solo consolidado -- igual que en el Excel. */
  sobreapilamientoPorSubdireccion: Array<{
    subdireccionLocal: string;
    cajasSobreapiladas: number;
    metrosEspacioAjenoInvadido: number;
  }>;
  actualizadoEn: string;
}
