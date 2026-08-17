// Espejo de una fila de "Datos_BD" en el Excel: Unidad Operativa + Periodo TRD + visita.
// Si cambia una regla aca, cambia la MISMA regla en Calculos del Excel -- deben decir lo mismo.

export type PeriodoTRD =
  | "Fondo Acumulado (FDA)"
  | "TRD 1 (2007-2014)"
  | "TRD 2 (2014-2017)"
  | "TRD 3 (2017-2021)"
  | "TRD 4 (2021-2022)"
  | "TRD 5 (2022-2023)"
  | "TRD 6 (2023-actual)";

export const PERIODOS_TRD: PeriodoTRD[] = [
  "Fondo Acumulado (FDA)",
  "TRD 1 (2007-2014)",
  "TRD 2 (2014-2017)",
  "TRD 3 (2017-2021)",
  "TRD 4 (2021-2022)",
  "TRD 5 (2022-2023)",
  "TRD 6 (2023-actual)",
];

export interface TareasCantidad {
  fuid: number;
  /** null/undefined = "N/A" -- ese periodo no tiene nada que eliminar. Se EXCLUYE del promedio,
   *  no cuenta como 0%. Nunca fuerces un 0 aqui solo para "llenar el campo". */
  eliminacion: number | null;
  clasificacion: number;
  ordenacion: number;
  foliacion: number;
  hojaControl: number;
  rotulacion: number;
}

export type TipoAlmacenamiento =
  | "Estantería adecuada"
  | "Piso"
  | "Piso y Estantería"
  | "Lugar no apropiado";

export interface DiagnosticoRiesgo {
  tipoAlmacenamiento: TipoAlmacenamiento | null;
  riesgoHumedad: boolean | null;
  riesgoRoedores: boolean | null;
  riesgoSobreapilamiento: boolean | null;
  riesgoFiltraciones: boolean | null;
  /** Medido en sitio, NO calculado: cuantas cajas estan fuera de la estanteria. */
  cajasSobreapiladas: number;
  /** Medido en sitio, NO calculado: metros de un espacio que es de OTRA cosa (pasillo, oficina)
   *  invadidos por cajas de archivo. El mismo exceso puede apilarse en el mismo rincon (0 aqui)
   *  o regarse por una oficina entera (invade mucho) -- no hay forma de deducirlo con matematicas. */
  metrosEspacioAjenoInvadido: number;
}

export interface Transferencia {
  correoSAF: boolean;
  aprobacionSAF: boolean;
  /** Cuando esto pasa a true, ese periodo ya se trasladó al archivo central -- ver cajasTrasladadas. */
  trasladoArchivoCentral: boolean;
  /** Cuantas cajas de ESTE periodo salieron fisicamente. Total Cajas (historico) NUNCA se toca;
   *  lo que se actualiza es "Cajas Vigentes en Sitio" = totalCajas - cajasTrasladadas. */
  cajasTrasladadas: number;
}

export type EstadoVisita = "Pendiente" | "Programada" | "Realizada";

export interface RegistroPeriodo {
  id: string;
  unidadOperativaId: string;
  periodo: PeriodoTRD;
  totalCajas: number; // "Total Cajas (Meta)" -- la base de todos los porcentajes, historico, nunca se edita
  tareas: TareasCantidad;
  transferencia: Transferencia;
  diagnostico: DiagnosticoRiesgo;
  encargado?: string;
  /** undefined = Pendiente. Fecha futura = Programada. Fecha <= hoy = Realizada (ver estadoVisita()). */
  fechaVisita?: string; // ISO date (solo la fecha, sin hora)
  observaciones?: string;
  creadoEn: string; // ISO datetime
  actualizadoEn: string; // ISO datetime
}

// ---------------------------------------------------------------------------------------------
// Reglas de negocio puras -- viven en el dominio, nunca se calculan solo en la UI ni se confia
// en lo que mande el cliente. Deben coincidir exactamente con las formulas de Calculos en Excel.
// ---------------------------------------------------------------------------------------------

export function calcularAvancePorTarea(cantidad: number | null, totalCajas: number): number | null {
  if (cantidad === null || cantidad === undefined) return null; // "N/A": se excluye, no es 0%
  if (!totalCajas || totalCajas <= 0) return 0;
  return cantidad / totalCajas;
}

export function calcularAvanceTotal(r: Pick<RegistroPeriodo, "totalCajas" | "tareas">): number {
  const { tareas, totalCajas } = r;
  const valores = [
    tareas.fuid,
    tareas.eliminacion,
    tareas.clasificacion,
    tareas.ordenacion,
    tareas.foliacion,
    tareas.hojaControl,
    tareas.rotulacion,
  ];
  const porcentajes = valores
    .map((v) => calcularAvancePorTarea(v, totalCajas))
    .filter((p): p is number => p !== null); // Eliminacion en null se cae aqui, no ensucia el promedio
  if (porcentajes.length === 0) return 0;
  return porcentajes.reduce((a, b) => a + b, 0) / porcentajes.length;
}

export type Semaforo = "verde" | "ambar" | "rojo";

export function semaforo(avanceTotal: number): Semaforo {
  if (avanceTotal >= 0.9) return "verde";
  if (avanceTotal >= 0.5) return "ambar";
  return "rojo";
}

/** Nivel de riesgo de conservacion: mismo criterio de 3 colores que el semaforo de avance,
 *  para que la Directora no tenga que aprender un codigo distinto en cada parte del sistema. */
export function nivelRiesgo(d: DiagnosticoRiesgo): Semaforo | null {
  const { tipoAlmacenamiento, riesgoHumedad, riesgoRoedores, riesgoSobreapilamiento, riesgoFiltraciones } = d;
  if (
    tipoAlmacenamiento === null &&
    riesgoHumedad === null &&
    riesgoRoedores === null &&
    riesgoSobreapilamiento === null &&
    riesgoFiltraciones === null
  ) {
    return null; // aun nadie diagnostico esta unidad
  }
  let puntos = tipoAlmacenamiento === "Estantería adecuada" || tipoAlmacenamiento === null ? 0 : 2;
  if (riesgoHumedad) puntos += 1;
  if (riesgoRoedores) puntos += 1;
  if (riesgoSobreapilamiento) puntos += 1;
  if (riesgoFiltraciones) puntos += 1;
  if (puntos >= 4) return "rojo";
  if (puntos >= 2) return "ambar";
  return "verde";
}

/** Cuantas cajas quedan HOY, fisicamente, en la unidad para este periodo. El historico
 *  (totalCajas) nunca cambia; esto sí, a medida que se registran traslados. */
export function cajasVigentes(r: Pick<RegistroPeriodo, "totalCajas" | "transferencia">): number {
  return r.totalCajas - (r.transferencia?.cajasTrasladadas ?? 0);
}

/** 3 estados, no 2: una visita programada a futuro NO es lo mismo que una ya realizada. */
export function estadoVisita(fechaVisitaISO: string | undefined | null): EstadoVisita {
  if (!fechaVisitaISO) return "Pendiente";
  const fecha = new Date(fechaVisitaISO);
  if (Number.isNaN(fecha.getTime())) return "Programada"; // texto libre tipo "reprogramada"
  const hoy = new Date();
  hoy.setHours(0, 0, 0, 0);
  return fecha.getTime() <= hoy.getTime() ? "Realizada" : "Programada";
}
