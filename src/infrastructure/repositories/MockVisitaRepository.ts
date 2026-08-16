import { VisitaAuditoria } from '@domain/entities/VisitaAuditoria';
import { IVisitaRepository } from '@domain/repositories/IVisitaRepository';

export class MockVisitaRepository implements IVisitaRepository {
  private visitasDB: VisitaAuditoria[] = [];

  async guardarVisita(visita: VisitaAuditoria): Promise<void> {
    console.log('Guardando en memoria...', visita);
    this.visitasDB.push(visita);
  }

  async obtenerVisitasPorCDC(idCDC: string): Promise<VisitaAuditoria[]> {
    return this.visitasDB.filter(v => v.idCDC === idCDC);
  }

  async obtenerTodasLasVisitas(): Promise<VisitaAuditoria[]> {
    return this.visitasDB;
  }

  async actualizarEstadoCompromiso(idVisita: string, idCompromiso: string, nuevoEstado: string): Promise<void> {
    const visita = this.visitasDB.find(v => v.idVisita === idVisita);
    if (visita) {
      const compromiso = visita.compromisos.find(c => c.idCompromiso === idCompromiso);
      if (compromiso) {
        // Actualizamos el estado del compromiso encontrado
        compromiso.estado = nuevoEstado;
      }
    }
  }
}