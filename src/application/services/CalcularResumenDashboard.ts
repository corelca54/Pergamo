// Calcula el resumen del Tablero del lado del cliente -- reutiliza EXACTAMENTE las mismas
// funciones de dominio que ya validamos (calcularAvanceTotal, semaforo, cajasVigentes,
// avanceOrganizacionPQRS) en vez de reinventar la formula aqui. Si algun dia se agrega una
// Cloud Function para pre-calcular esto en el servidor, la logica de negocio no cambia -- solo
// cambia QUIEN la ejecuta.
import type { RegistroPeriodo } from "../../domain/entities/RegistroPeriodo";
import { calcularAvanceTotal, cajasVigentes, semaforo, nivelRiesgo } from "../../domain/entities/RegistroPeriodo";
import type { PQRS } from "../../domain/entities/PQRS";
import { avanceOrganizacionPQRS, cajasVigentesPQRS } from "../../domain/entities/PQRS";
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

export function calcularResumenDashboard(registros: RegistroPeriodo[], pqrs: PQRS[]): ResumenDashboard {
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

  const cajasSobreapiladas = registros.reduce((acc, r) => acc + (r.diagnostico.cajasSobreapiladas || 0), 0)
    + pqrs.reduce((acc, p) => acc + 0, 0); // PQRS no tiene diagnostico de riesgo propio, solo RegistroPeriodo
  const metrosEspacioAjenoInvadido = registros.reduce((acc, r) => acc + (r.diagnostico.metrosEspacioAjenoInvadido || 0), 0);

  // Por Dependencia/Servicio -- agrupado sobre el id de unidad (no tenemos Directorio con
  // Dependencia/Servicio real todavia; se usa el identificador de la unidad como agrupador
  // temporal hasta que se construya esa vinculacion, ver nota en README).
  const grupos = new Map<string, RegistroPeriodo[]>();
  for (const r of registros) {
    const clave = r.unidadOperativaId;
    grupos.set(clave, [...(grupos.get(clave) ?? []), r]);
  }
  const porDependenciaServicio = Array.from(grupos.entries()).map(([unidad, regs]) => ({
    dependencia: unidad, servicio: "",
    totalCajas: regs.reduce((acc, r) => acc + cajasVigentes(r), 0),
    avancePromedio: regs.reduce((acc, r) => acc + calcularAvanceTotal(r), 0) / regs.length,
  }));

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

  return {
    cajasVigentesEnSitio, totalCajasHistorico, avancePromedioGlobal, unidadesOperativas,
    cajasEliminacionHistorico, cajasEliminacionEstePeriodo, unidadesEnRiesgoAlto,
    cajasSobreapiladas, metrosEspacioAjenoInvadido,
    porDependenciaServicio, porTarea, porPeriodo,
    // Sobreapilamiento por Subdireccion: pendiente de un Directorio real que vincule
    // unidadOperativaId -> subdireccionLocal (ver README, "Proximo paso").
    sobreapilamientoPorSubdireccion: [],
    actualizadoEn: new Date().toISOString(),
  };
}

export { semaforo };
