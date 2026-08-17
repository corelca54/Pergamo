import type { Compromiso } from "../entities/Compromiso";

export interface ICompromisoRepository {
  listarPorUnidad(unidadOperativaId: string): Promise<Compromiso[]>;
  guardar(c: Omit<Compromiso, "id" | "creadoEn">): Promise<Compromiso>;
  actualizarEstado(id: string, estado: Compromiso["estado"]): Promise<void>;
}
