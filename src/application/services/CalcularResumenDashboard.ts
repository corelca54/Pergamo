// Calcula el resumen del Tablero del lado del cliente -- reutiliza EXACTAMENTE las mismas
// funciones de dominio que ya validamos (calcularAvanceTotal, semaforo, cajasVigentes,
// avanceOrganizacionPQRS) en vez de reinventar la formula aqui. Si algun dia se agrega una
// Cloud Function para pre-calcular esto en el servidor, la logica de negocio no cambia -- solo
// cambia QUIEN la ejecuta.
import type { RegistroPeriodo } from "../../domain/entities/RegistroPeriodo";
import { calcularAvanceTotal, cajasVigentes, nivelRiesgo } from "../../domain/entities/RegistroPeriodo";
import type { PQRS } from "../../domain/entities/PQRS";
import type { UnidadOperativa } from "../../domain/entities/UnidadOperativa";
import type { ResumenDashboard } from "../../domain/repositories/IRegistroPeriodoRepository";

const TAREAS_ORDEN: Array<{ key: keyof RegistroPeriodo["tareas"]; label: string }> = [
  { key: "fuid", label: "FUID" },
  { key: "eliminacion", label: "Eliminación" },
  { key: "clasificacion", label: "Clasificación" },
  { key: "ordenacion", label: "Ordenación" },
  { key: "foliacion", label: "Foliación" },
  { key: "hojaControl", label: "Hoja de Control" },
  { key: "rotulacion", label: "Rotulación" },
];

const SIN_DIRECTORIO = "(sin datos en Directorio)";

export interface FiltrosTablero {
  subdireccionLocal?: string;
  dependencia?: string;
  servicio?: string;
  periodo?: string;
}

/** Ahora que existe el Directorio real, esta funcion recibe tambien la lista de unidades para
 *  poder resolver cada RegistroPeriodo.unidadOperativaId (un id interno de Firestore, no algo
 *  legible) hacia su nombre, servicio y subdireccion reales -- antes de esto, el Tablero
 *  agrupaba por el id crudo, que no le dice nada a nadie.
 *
 *  Los 4 filtros (Subdireccion, Dependencia, Servicio, Periodo) son EXACTAMENTE los mismos 4
 *  del Excel, combinables entre si -- se resuelven aqui mismo, antes de agregar nada, para que
 *  todo el resumen (KPIs, graficos, tablas) respete el mismo filtro a la vez. */
export function calcularResumenDashboard(
  registrosSinFiltrar: RegistroPeriodo[],
  pqrsSinFiltrar: PQRS[],
  unidades: UnidadOperativa[],
  filtros: FiltrosTablero = {}
): ResumenDashboard {
  const porId = new Map(unidades.map((u) => [u.id, u]));
  const resolver = (id: string) => porId.get(id) ?? null;

  function pasaFiltro(unidadId: string): boolean {
    const u = resolver(unidadId);
    if (!u) return !filtros.subdireccionLocal && !filtros.dependencia && !filtros.servicio;
    if (filtros.subdireccionLocal && u.subdireccionLocal !== filtros.subdireccionLocal) return false;
    if (filtros.dependencia && u.dependencia !== filtros.dependencia) return false;
    if (filtros.servicio && u.servicio !== filtros.servicio) return false;
    return true;
  }

  const registros = registrosSinFiltrar.filter(
    (r) => pasaFiltro(r.unidadOperativaId) && (!filtros.periodo || r.periodo === filtros.periodo)
  );
  const pqrs = pqrsSinFiltrar.filter((p) => pasaFiltro(p.unidadOperativaId));

  const cajasVigentesEnSitio = registros.reduce((acc, r) => acc + cajasVigentes(r), 0);
  const totalCajasHistorico = registros.reduce((acc, r) => acc + r.totalCajas, 0);
  const avances = registros.map((r) => calcularAvanceTotal(r));
  const avancePromedioGlobal = avances.length ? avances.reduce((a, b) => a + b, 0) / avances.length : 0;
  const unidadesOperativas = new Set(registros.map((r) => r.unidadOperativaId)).size;

  const cajasEliminacionHistorico = registros.reduce((acc, r) => acc + (r.tareas.eliminacion ?? 0), 0);
  const hoy = new Date(); const inicioMes = new Date(hoy.getFullYear(), hoy.getMonth(), 1).toISOString();
  const cajasEliminacionEstePeriodo = registros
    .filter((r) => r.actualizadoEn >= inicioMes)
    .reduce((acc, r) => acc + (r.tareas.eliminacion ?? 0), 0);

  const unidadesEnRiesgoAlto = new Set(
    registros.filter((r) => nivelRiesgo(r.diagnostico) === "rojo").map((r) => r.unidadOperativaId)
  ).size;

  const cajasSobreapiladas = registros.reduce((acc, r) => acc + (r.diagnostico.cajasSobreapiladas || 0), 0);
  const metrosEspacioAjenoInvadido = registros.reduce((acc, r) => acc + (r.diagnostico.metrosEspacioAjenoInvadido || 0), 0);

  // Por Dependencia/Servicio -- ahora resuelve el nombre real de la unidad via el Directorio,
  // en vez de mostrar el id interno de Firestore.
  const grupos = new Map<string, RegistroPeriodo[]>();
  for (const r of registros) grupos.set(r.unidadOperativaId, [...(grupos.get(r.unidadOperativaId) ?? []), r]);
  const porDependenciaServicio = Array.from(grupos.entries()).map(([unidadId, regs]) => {
    const u = resolver(unidadId);
    return {
      dependencia: u ? `${u.dependencia} · ${u.nombre}` : SIN_DIRECTORIO,
      servicio: u?.servicio ?? "",
      totalCajas: regs.reduce((acc, r) => acc + cajasVigentes(r), 0),
      avancePromedio: regs.reduce((acc, r) => acc + calcularAvanceTotal(r), 0) / regs.length,
    };
  });

  const porTarea = TAREAS_ORDEN.map(({ key, label }) => {
    const valores = registros
      .map((r) => {
        const cant = r.tareas[key];
        if (cant === null || cant === undefined) return null;
        return r.totalCajas > 0 ? cant / r.totalCajas : 0;
      })
      .filter((v): v is number => v !== null);
    return { tarea: label, avancePromedio: valores.length ? valores.reduce((a, b) => a + b, 0) / valores.length : 0 };
  });

  const periodos = new Map<string, RegistroPeriodo[]>();
  for (const r of registros) periodos.set(r.periodo, [...(periodos.get(r.periodo) ?? []), r]);
  const porPeriodo = Array.from(periodos.entries()).map(([periodo, regs]) => ({
    periodo,
    totalCajas: regs.reduce((acc, r) => acc + cajasVigentes(r), 0),
    avancePromedio: regs.reduce((acc, r) => acc + calcularAvanceTotal(r), 0) / regs.length,
  }));

  // Sobreapilamiento por Subdireccion: el nivel intermedio que faltaba -- ya se puede calcular
  // de verdad porque el Directorio conoce la subdireccion de cada unidad.
  const porSubdireccion = new Map<string, RegistroPeriodo[]>();
  for (const r of registros) {
    const u = resolver(r.unidadOperativaId);
    const sub = u?.subdireccionLocal ?? SIN_DIRECTORIO;
    porSubdireccion.set(sub, [...(porSubdireccion.get(sub) ?? []), r]);
  }
  const sobreapilamientoPorSubdireccion = Array.from(porSubdireccion.entries())
    .filter(([sub]) => sub !== SIN_DIRECTORIO)
    .map(([subdireccionLocal, regs]) => ({
      subdireccionLocal,
      cajasSobreapiladas: regs.reduce((acc, r) => acc + (r.diagnostico.cajasSobreapiladas || 0), 0),
      metrosEspacioAjenoInvadido: regs.reduce((acc, r) => acc + (r.diagnostico.metrosEspacioAjenoInvadido || 0), 0),
    }));

  return {
    cajasVigentesEnSitio, totalCajasHistorico, avancePromedioGlobal, unidadesOperativas,
    cajasEliminacionHistorico, cajasEliminacionEstePeriodo, unidadesEnRiesgoAlto,
    cajasSobreapiladas, metrosEspacioAjenoInvadido,
    porDependenciaServicio, porTarea, porPeriodo, sobreapilamientoPorSubdireccion,
    actualizadoEn: new Date().toISOString(),
  };
}
