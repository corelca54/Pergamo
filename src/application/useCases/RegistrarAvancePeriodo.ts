import type { IRegistroPeriodoRepository } from "../../domain/repositories/IRegistroPeriodoRepository";
import type {
  RegistroPeriodo,
  TareasCantidad,
  Transferencia,
  DiagnosticoRiesgo,
} from "../../domain/entities/RegistroPeriodo";

export interface RegistrarAvanceInput {
  unidadOperativaId: string;
  periodo: RegistroPeriodo["periodo"];
  totalCajas: number;
  tareas: TareasCantidad;
  transferencia: Transferencia;
  diagnostico: DiagnosticoRiesgo;
  encargado?: string;
  fechaVisita?: string;
  observaciones?: string;
}

export class ValidacionError extends Error {}

// Caso de uso: orquesta la regla de negocio + el repositorio. No sabe que existe Firebase.
export class RegistrarAvancePeriodo {
  constructor(private readonly repo: IRegistroPeriodoRepository) {}

  async ejecutar(input: RegistrarAvanceInput): Promise<RegistroPeriodo> {
    if (input.totalCajas <= 0) {
      throw new ValidacionError("Total Cajas (Meta) debe ser mayor a 0.");
    }
    // Espejo de la regla que vive en las Security Rules de Firestore (defensa en profundidad):
    // ninguna tarea puede tener mas cajas que el total del periodo. Eliminacion puede ser null
    // ("N/A" -- ese periodo no tiene nada que eliminar), en ese caso no se valida.
    for (const [tarea, cantidad] of Object.entries(input.tareas)) {
      if (cantidad === null || cantidad === undefined) continue; // N/A valido, no es un error
      if (cantidad < 0) throw new ValidacionError(`${tarea}: la cantidad no puede ser negativa.`);
      if (cantidad > input.totalCajas) {
        throw new ValidacionError(
          `${tarea}: ${cantidad} cajas supera el Total Cajas (Meta) de ${input.totalCajas}. Revisa el dato.`
        );
      }
    }
    if (input.transferencia.cajasTrasladadas > input.totalCajas) {
      throw new ValidacionError("Cajas Trasladadas no puede superar el Total Cajas (Meta).");
    }
    return this.repo.guardar(input);
  }
}
