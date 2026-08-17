// Idea que ya traia el scaffold original (seguimiento de compromisos de una visita/reunion) --
// NO existe en el Excel, asi que vive aparte, sin mezclarse con RegistroPeriodo. Util para
// actas de mesas de trabajo con la Subdireccion, pero no es "avance de tareas archivisticas".

export type EstadoCompromiso = "Pendiente" | "En Proceso" | "Cumplido";

export interface Compromiso {
  id: string;
  unidadOperativaId: string;
  descripcion: string;
  responsable?: string;
  fechaLimite?: string; // ISO date
  estado: EstadoCompromiso;
  creadoEn: string;
}
