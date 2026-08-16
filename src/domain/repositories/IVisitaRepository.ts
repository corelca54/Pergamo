import { VisitaAuditoria } from '../entities/VisitaAuditoria';

export interface IVisitaRepository {
  guardarVisita(visita: VisitaAuditoria): Promise<void>;
  obtenerVisitasPorCDC(idCDC: string): Promise<VisitaAuditoria[]>;
  obtenerTodasLasVisitas(): Promise<VisitaAuditoria[]>;
  actualizarEstadoCompromiso(idVisita: string, idCompromiso: string, nuevoEstado: string): Promise<void>;
}