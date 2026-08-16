export interface DetalleFondo {
  ubicacion: 'CDC' | 'Lavandería';
  versionTRD: string;
  cajas: number;
  carpetas: number;
}

export interface MetricasVisita {
  detallesFondo: DetalleFondo[];
  granTotalCajas: number;
  granTotalCarpetas: number;
  procesosEliminacion: number;
  transferencias: number;
  procesosFDA: number;
  porcentajeCumplimiento: number;
}

export interface Compromiso {
  idCompromiso: string;
  descripcion: string;
  estado: string;
}

export interface VisitaAuditoria {
  idVisita: string;
  fecha: Date;
  idCDC: string;
  localidad: string;
  tipoVisita: string;
  tema: string;
  metricas: MetricasVisita;
  desarrolloCualitativo: string;
  compromisos: Compromiso[];
  asistentes: string[];
  estado: string;
}