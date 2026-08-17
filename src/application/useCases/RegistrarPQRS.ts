import type { IPQRSRepository } from "../../domain/repositories/IPQRSRepository";
import type { PQRS, TrasladoPQRS } from "../../domain/entities/PQRS";
import { puedeIniciarTraslado } from "../../domain/entities/PQRS";
import type { TareasCantidad } from "../../domain/entities/RegistroPeriodo";

export interface RegistrarPQRSInput {
  unidadOperativaId: string;
  totalCajas: number;
  tareas: TareasCantidad;
  traslado: TrasladoPQRS;
  encargado?: string;
  fechaVisita?: string;
  observaciones?: string;
}

export class ValidacionPQRSError extends Error {}

export class RegistrarPQRS {
  constructor(private readonly repo: IPQRSRepository) {}

  async ejecutar(input: RegistrarPQRSInput): Promise<PQRS> {
    if (input.totalCajas <= 0) {
      throw new ValidacionPQRSError("El total de cajas debe ser mayor a 0.");
    }
    for (const [tarea, cantidad] of Object.entries(input.tareas)) {
      if (cantidad === null || cantidad === undefined) continue;
      if (cantidad < 0) throw new ValidacionPQRSError(`${tarea}: la cantidad no puede ser negativa.`);
      if (cantidad > input.totalCajas) {
        throw new ValidacionPQRSError(`${tarea}: ${cantidad} cajas supera el total de ${input.totalCajas}.`);
      }
    }
    // Regla de negocio central de PQRS: no se puede notificar a la Subsecretaria de Gestion
    // Institucional ni marcar traslado sobre PQRS que aun no completo su organizacion.
    if (
      (input.traslado.correoEnviado || input.traslado.trasladado) &&
      !puedeIniciarTraslado({ totalCajas: input.totalCajas, tareas: input.tareas })
    ) {
      throw new ValidacionPQRSError(
        "No se puede notificar ni trasladar PQRS cuya organización aún no está completa."
      );
    }
    if (input.traslado.cajasTrasladadas > input.totalCajas) {
      throw new ValidacionPQRSError("Cajas trasladadas no puede superar el total de cajas.");
    }
    return this.repo.guardar(input);
  }
}
