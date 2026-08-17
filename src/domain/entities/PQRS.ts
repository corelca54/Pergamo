// PQRS (Peticiones, Quejas, Reclamos y Sugerencias) vive en cada Unidad Operativa como cualquier
// otro expediente, y pasa por EL MISMO flujo de organizacion archivistico que el TRD normal
// (misma logica de tareas/porcentaje que RegistroPeriodo) -- la diferencia real esta en el
// destino final: NO es Archivo Central, es la Subsecretaria de Gestion Institucional, que es la
// responsable de su custodia. Por eso es una entidad aparte, aunque comparte estructura.
import type { TareasCantidad } from "./RegistroPeriodo";
import { calcularAvanceTotal as calcularAvanceTareas, semaforo, type Semaforo } from "./RegistroPeriodo";

export interface TrasladoPQRS {
  correoEnviado: boolean;
  fechaCorreo?: string; // ISO date -- cuando se notifico a la Subsecretaria de Gestion Institucional
  aprobado: boolean;
  fechaAprobacion?: string;
  /** El traslado en si -- distinto del traslado a Archivo Central de RegistroPeriodo. */
  trasladado: boolean;
  fechaTraslado?: string;
  cajasTrasladadas: number;
}

export interface PQRS {
  id: string;
  unidadOperativaId: string;
  /** Se cuenta en CAJAS, igual que el resto del proceso archivistico (no en carpetas). */
  totalCajas: number;
  tareas: TareasCantidad;
  traslado: TrasladoPQRS;
  encargado?: string;
  fechaVisita?: string;
  observaciones?: string;
  creadoEn: string;
  actualizadoEn: string;
}

/** Reutiliza EXACTAMENTE la misma formula de avance y el mismo semaforo de 3 colores que
 *  RegistroPeriodo -- "mismo flujo de organizacion" significa que no debe haber una regla
 *  paralela que se pueda desincronizar de la real. */
export function avanceOrganizacionPQRS(p: Pick<PQRS, "totalCajas" | "tareas">): number {
  return calcularAvanceTareas({ totalCajas: p.totalCajas, tareas: p.tareas });
}

export function semaforoPQRS(p: Pick<PQRS, "totalCajas" | "tareas">): Semaforo {
  return semaforo(avanceOrganizacionPQRS(p));
}

/** Solo se puede notificar/trasladar cuando el avance de organizacion esta completo (90%+,
 *  mismo umbral "verde" que el resto de la app) -- evita avisarle a la Subsecretaria por algo
 *  que en realidad todavia no esta listo. */
export function puedeIniciarTraslado(p: Pick<PQRS, "totalCajas" | "tareas">): boolean {
  return semaforoPQRS(p) === "verde";
}

export function cajasVigentesPQRS(p: Pick<PQRS, "totalCajas" | "traslado">): number {
  return p.totalCajas - (p.traslado?.cajasTrasladadas ?? 0);
}
