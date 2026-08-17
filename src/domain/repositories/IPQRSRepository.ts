import type { PQRS } from "../entities/PQRS";

export interface IPQRSRepository {
  listarPorUnidad(unidadOperativaId: string): Promise<PQRS[]>;
  guardar(p: Omit<PQRS, "id" | "creadoEn" | "actualizadoEn">): Promise<PQRS>;
  actualizar(id: string, cambios: Partial<PQRS>): Promise<void>;
}
