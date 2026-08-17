import type { UnidadOperativa } from "../entities/UnidadOperativa";

// El Directorio real (Dependencia -> Servicio -> Subdireccion -> Unidad), espejo exacto del
// Directorio del Excel. Vive en Firestore como un catalogo -- no cambia con cada visita, solo
// cuando se agrega/edita una unidad operativa.
export interface IUnidadOperativaRepository {
  listarTodas(): Promise<UnidadOperativa[]>;
  listarPorSubdireccion(subdireccionLocal: string): Promise<UnidadOperativa[]>;
  obtenerPorId(id: string): Promise<UnidadOperativa | null>;
  guardar(u: Omit<UnidadOperativa, "id">): Promise<UnidadOperativa>;
  actualizar(id: string, cambios: Partial<UnidadOperativa>): Promise<void>;
  /** Carga masiva -- para importar el Directorio real del Excel de una sola vez. */
  importarLote(unidades: Array<Omit<UnidadOperativa, "id">>): Promise<number>;
}
