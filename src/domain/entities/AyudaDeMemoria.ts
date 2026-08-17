// Espejo exacto del formato institucional GD-040 "Ayuda de Memoria" de la SDIS. Los nombres de
// campo siguen la plantilla real (Lugar, Tema, Desarrollo, Asistentes, Compromisos, Proxima
// reunion, Elaboro) para que el PDF que genera la PWA se vea igual al que ya usa el equipo --
// no una reinterpretacion mia del formato.

export interface AsistenteActa {
  nombre: string;
  cargoRol: string;
  /** "No aplica" si es usuario o beneficiario (asi lo indica la plantilla original). */
  dependencia: string;
  /** Firma fisica en papel (se imprime y se firma a mano) -- por eso queda como espacio en
   *  blanco en el PDF, no como un campo de texto a llenar en la app. */
}

export interface CompromisoActa {
  actividad: string;
  responsable: string;
  fechaLimite: string; // ISO date
}

export interface AyudaDeMemoria {
  id: string;
  /** "Lugar": dependencia o entidad donde se realizo la reunion (no una direccion fisica). */
  lugar: string;
  fecha: string; // ISO date, formato de despliegue DD/MM/AAAA como pide la plantilla
  tema: string;
  /** Puntos especificos tratados u orden del dia. */
  desarrollo: string;
  asistentes: AsistenteActa[];
  compromisos: CompromisoActa[];
  /** Opcional -- la plantilla dice "si fue establecida". */
  proximaReunion?: string;
  elaboroPor: string;
  unidadOperativaId?: string; // vinculo opcional a la visita/unidad que origino la reunion
  creadoEn: string;
}

export function validarAyudaDeMemoria(a: Pick<AyudaDeMemoria, "lugar" | "fecha" | "tema" | "elaboroPor" | "asistentes">): string[] {
  const errores: string[] = [];
  if (!a.lugar?.trim()) errores.push("Lugar es obligatorio.");
  if (!a.fecha) errores.push("Fecha es obligatoria.");
  if (!a.tema?.trim()) errores.push("Tema es obligatorio.");
  if (!a.elaboroPor?.trim()) errores.push("Elaboró es obligatorio.");
  if (!a.asistentes || a.asistentes.length === 0) errores.push("Debe registrar al menos un asistente.");
  return errores;
}
