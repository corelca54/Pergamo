import { VisitaAuditoria } from '@domain/entities/VisitaAuditoria';
import { IVisitaRepository } from '@domain/repositories/IVisitaRepository';

export class CrearVisitaUseCase {
  // Inyección de dependencias: Recibe cualquier base de datos que cumpla el contrato
  constructor(private visitaRepository: IVisitaRepository) {}

  async ejecutar(visita: Omit<VisitaAuditoria, 'idVisita'>): Promise<VisitaAuditoria> {
    // 1. Aquí podemos poner reglas de negocio. Por ejemplo, validar que tenga métricas:
    if (visita.metricas.porcentajeCumplimiento < 0 || visita.metricas.porcentajeCumplimiento > 100) {
      throw new Error('El porcentaje de cumplimiento debe estar entre 0 y 100');
    }

    // 2. Generar un ID único (temporalmente usaremos la fecha, luego Firebase lo hará)
    const nuevaVisita: VisitaAuditoria = {
      ...visita,
      idVisita: `VIS-${new Date().getTime()}`,
    };

    // 3. Guardar en el repositorio
    await this.visitaRepository.guardarVisita(nuevaVisita);

    return nuevaVisita;
  }
}