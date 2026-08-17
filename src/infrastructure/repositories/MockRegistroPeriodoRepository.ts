// Implementacion en memoria -- util para desarrollar la UI sin gastar cuota de Firestore,
// y para pruebas. Implementa el MISMO contrato que la version real.
import type { RegistroPeriodo } from "../../domain/entities/RegistroPeriodo";
import type {
  IRegistroPeriodoRepository,
  ResumenDashboard,
} from "../../domain/repositories/IRegistroPeriodoRepository";

export class MockRegistroPeriodoRepository implements IRegistroPeriodoRepository {
  private registros: RegistroPeriodo[] = [];
  private idSeq = 1;

  async listarPorUnidad(unidadOperativaId: string): Promise<RegistroPeriodo[]> {
    return this.registros.filter((r) => r.unidadOperativaId === unidadOperativaId);
  }

  async listarTodos(): Promise<RegistroPeriodo[]> {
    return [...this.registros];
  }

  async listarPagina(params: Parameters<IRegistroPeriodoRepository["listarPagina"]>[0]) {
    let items = [...this.registros];
    if (params.periodo) items = items.filter((r) => r.periodo === params.periodo);
    const pagina = items.slice(0, params.tamanoPagina);
    return { items: pagina, nextCursor: null };
  }

  async guardar(registro: Omit<RegistroPeriodo, "id" | "creadoEn" | "actualizadoEn">): Promise<RegistroPeriodo> {
    const ahora = new Date().toISOString();
    const nuevo: RegistroPeriodo = { ...registro, id: String(this.idSeq++), creadoEn: ahora, actualizadoEn: ahora };
    this.registros.push(nuevo);
    return nuevo;
  }

  async actualizar(id: string, cambios: Partial<RegistroPeriodo>): Promise<void> {
    const idx = this.registros.findIndex((r) => r.id === id);
    if (idx >= 0) this.registros[idx] = { ...this.registros[idx], ...cambios, actualizadoEn: new Date().toISOString() };
  }

  suscribirseAResumen(_filtros: unknown, onCambio: (resumen: ResumenDashboard) => void): () => void {
    onCambio({
      cajasVigentesEnSitio: 0, totalCajasHistorico: 0, avancePromedioGlobal: 0, unidadesOperativas: 0,
      cajasEliminacionHistorico: 0, cajasEliminacionEstePeriodo: 0, unidadesEnRiesgoAlto: 0,
      cajasSobreapiladas: 0, metrosEspacioAjenoInvadido: 0,
      porDependenciaServicio: [], porTarea: [], porPeriodo: [], sobreapilamientoPorSubdireccion: [],
      actualizadoEn: new Date().toISOString(),
    });
    return () => {};
  }
}
