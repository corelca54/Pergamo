# -*- coding: utf-8 -*-
"""
Tablero con filtros reales (los mismos 4 del Excel: Subdireccion, Dependencia, Servicio,
Periodo TRD, combinables entre si) y graficos con Chart.js con estilo de profundidad --
degradado vertical + barras redondeadas en el grafico de Tareas, dona con separacion y
etiquetas de porcentaje en el grafico de Periodos. package.json ya trae chart.js,
react-chartjs-2 y chartjs-plugin-datalabels declarados.

Correlo desde la raiz de tu proyecto: python actualizar_tablero_filtros_graficos.py
Despues corre: npm install
"""
import os

ARCHIVOS_TEXTO = {
    "package.json": """{
  "name": "pergamo",
  "version": "1.0.0",
  "description": "Aplicación PWA para auditoría de gestión documental y TRD",
  "main": "index.js",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "keywords": [
    "sgil",
    "gestion-documental",
    "react"
  ],
  "author": "Developer_Ecc",
  "license": "ISC",
  "dependencies": {
    "chart.js": "^4.5.1",
    "chartjs-plugin-datalabels": "^2.2.0",
    "firebase": "^12.16.0",
    "jspdf": "^4.2.1",
    "jspdf-autotable": "^5.0.8",
    "react": "^19.2.7",
    "react-chartjs-2": "^5.3.1",
    "react-dom": "^19.2.7",
    "xlsx": "^0.18.5"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4.3.3",
    "@types/react": "^19.2.17",
    "@types/react-dom": "^19.2.3",
    "@vitejs/plugin-react": "^6.0.3",
    "autoprefixer": "^10.5.4",
    "postcss": "^8.5.23",
    "tailwindcss": "^4.3.3",
    "typescript": "^5.5.4",
    "vite": "^8.1.5",
    "vite-plugin-pwa": "^1.3.0",
    "vite-tsconfig-paths": "^6.1.1"
  }
}
""",
    "src/application/services/CalcularResumenDashboard.ts": """// Calcula el resumen del Tablero del lado del cliente -- reutiliza EXACTAMENTE las mismas
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
""",
    "src/presentation/hooks/useTablero.ts": """import { useEffect, useMemo, useState } from "react";
import { FirebaseRegistroPeriodoRepository } from "../../infrastructure/repositories/FirebaseRegistroPeriodoRepository";
import { FirebasePQRSRepository } from "../../infrastructure/repositories/FirebasePQRSRepository";
import { FirebaseUnidadOperativaRepository } from "../../infrastructure/repositories/FirebaseUnidadOperativaRepository";
import { calcularResumenDashboard } from "../../application/services/CalcularResumenDashboard";
import type { FiltrosTablero } from "../../application/services/CalcularResumenDashboard";
import type { RegistroPeriodo } from "../../domain/entities/RegistroPeriodo";
import type { PQRS } from "../../domain/entities/PQRS";
import type { UnidadOperativa } from "../../domain/entities/UnidadOperativa";

/** Trae TODO una sola vez (registros, PQRS, Directorio) y lo deja en memoria -- filtrar despues
 *  es instantaneo (recalculo local con useMemo), sin volver a consultar Firestore cada vez que
 *  alguien cambia un filtro. Los 4 filtros son EXACTAMENTE los mismos del Excel, combinables. */
export function useTablero(filtros: FiltrosTablero) {
  const [registros, setRegistros] = useState<RegistroPeriodo[]>([]);
  const [pqrs, setPqrs] = useState<PQRS[]>([]);
  const [unidades, setUnidades] = useState<UnidadOperativa[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const repos = useMemo(() => ({
    registros: new FirebaseRegistroPeriodoRepository(),
    pqrs: new FirebasePQRSRepository(),
    directorio: new FirebaseUnidadOperativaRepository(),
  }), []);

  async function refrescar() {
    setLoading(true);
    setError(null);
    try {
      const [r, p, u] = await Promise.all([
        repos.registros.listarTodos(),
        repos.pqrs.listarTodos(),
        repos.directorio.listarTodas(),
      ]);
      setRegistros(r); setPqrs(p); setUnidades(u);
    } catch (err: any) {
      setError(err.message || "No se pudo cargar el tablero.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { refrescar(); }, []);

  const resumen = useMemo(
    () => calcularResumenDashboard(registros, pqrs, unidades, filtros),
    [registros, pqrs, unidades, filtros]
  );

  return { resumen, unidades, loading, error, refrescar };
}
""",
    "src/presentation/screens/TableroPage.tsx": """import { useMemo, useState } from "react";
import { Bar, Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement,
  Tooltip, Legend, type ChartOptions,
} from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { useTablero } from "../hooks/useTablero";
import { useDirectorio } from "../hooks/useDirectorio";
import type { FiltrosTablero } from "../../application/services/CalcularResumenDashboard";
import { PERIODOS_TRD } from "../../domain/entities/RegistroPeriodo";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend, ChartDataLabels);

// Paleta corporativa (misma del resto de la app) para los gradientes de los graficos
const AZUL = "#2563EB", AZUL_CLARO = "#93C5FD", TEAL = "#0F766E", TEAL_CLARO = "#5EEAD4";
const COLORES_DONA = ["#2563EB", "#0F766E", "#F59E0B", "#7C3AED", "#DC2626", "#0891B2", "#65A30D"];

function Tarjeta({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <section className={`glass-card glass-card-interactiva rounded-2xl p-5 ${className}`}>{children}</section>;
}

function TarjetaKPI({ etiqueta, valor, color }: { etiqueta: string; valor: string; color: string }) {
  return (
    <Tarjeta className="flex flex-col gap-1">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">{etiqueta}</p>
      <p className="font-mono text-2xl font-bold" style={{ color }}>{valor}</p>
    </Tarjeta>
  );
}

const campoFiltro =
  "w-full rounded-lg border border-slate-300 bg-white px-2.5 py-2 text-sm text-slate-900 shadow-sm " +
  "focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20";

/** Tablero real, Fase 3: lee TODO lo capturado en Firestore (RegistroPeriodo + PQRS), con los
 *  mismos 4 filtros combinables del Excel (Subdirección, Dependencia, Servicio, Periodo TRD), y
 *  graficos con degradados/sombra para una sensacion de profundidad tipo "3D" -- Chart.js no
 *  hace WebGL real, pero con relleno degradado + barras redondeadas + sombra de proyeccion se
 *  logra un look mucho mas premium que barras planas de un solo color. */
export function TableroPage() {
  const [filtros, setFiltros] = useState<FiltrosTablero>({});
  const { resumen, loading, error, refrescar } = useTablero(filtros);
  const { subdirecciones, serviciosDe, unidades: unidadesDirectorio } = useDirectorio();

  const dependenciasDisponibles = useMemo(() => {
    const base = filtros.subdireccionLocal
      ? unidadesDirectorio.filter((u) => u.subdireccionLocal === filtros.subdireccionLocal)
      : unidadesDirectorio;
    return Array.from(new Set(base.map((u) => u.dependencia))).sort();
  }, [unidadesDirectorio, filtros.subdireccionLocal]);

  const serviciosDisponibles = useMemo(() => {
    if (!filtros.subdireccionLocal) {
      const base = filtros.dependencia ? unidadesDirectorio.filter((u) => u.dependencia === filtros.dependencia) : unidadesDirectorio;
      return Array.from(new Set(base.map((u) => u.servicio))).sort();
    }
    return serviciosDe(filtros.subdireccionLocal).filter(
      (s) => !filtros.dependencia || unidadesDirectorio.some((u) => u.subdireccionLocal === filtros.subdireccionLocal && u.servicio === s && u.dependencia === filtros.dependencia)
    );
  }, [unidadesDirectorio, filtros, serviciosDe]);

  const graficoTareaOpciones: ChartOptions<"bar"> = {
    responsive: true, maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      datalabels: { color: "#0F172A", anchor: "end", align: "top", font: { weight: "bold", size: 11 }, formatter: (v: number) => `${Math.round(v * 100)}%` },
      tooltip: { callbacks: { label: (ctx) => `${Math.round((ctx.raw as number) * 100)}%` } },
    },
    scales: {
      y: { beginAtZero: true, max: 1, ticks: { callback: (v) => `${Math.round(Number(v) * 100)}%` }, grid: { color: "#E2E8F0" } },
      x: { grid: { display: false } },
    },
  };

  const graficoDonaOpciones: ChartOptions<"doughnut"> = {
    responsive: true, maintainAspectRatio: false,
    plugins: {
      legend: { position: "bottom", labels: { boxWidth: 12, font: { size: 11 } } },
      datalabels: { color: "#fff", font: { weight: "bold", size: 11 }, formatter: (v: number, ctx) => {
        const total = (ctx.chart.data.datasets[0].data as number[]).reduce((a, b) => a + b, 0);
        return total > 0 ? `${Math.round((v / total) * 100)}%` : "";
      } },
    },
  };

  if (loading) {
    return <div className="flex items-center justify-center py-20"><p className="text-sm text-slate-400">Cargando tablero…</p></div>;
  }
  if (error || !resumen) {
    return (
      <Tarjeta className="text-center">
        <p className="text-sm text-red-600">{error || "No se pudo cargar el tablero."}</p>
        <button onClick={refrescar} className="mt-3 text-sm font-semibold text-primary-600 hover:text-primary-700">Reintentar</button>
      </Tarjeta>
    );
  }

  const datosTarea = {
    labels: resumen.porTarea.map((t) => t.tarea),
    datasets: [{
      data: resumen.porTarea.map((t) => t.avancePromedio),
      backgroundColor: (ctx: any) => {
        const { chart } = ctx;
        const { ctx: c, chartArea } = chart;
        if (!chartArea) return AZUL;
        const g = c.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
        g.addColorStop(0, TEAL); g.addColorStop(1, AZUL_CLARO);
        return g;
      },
      borderRadius: 8, borderSkipped: false,
      barThickness: 34,
    }],
  };

  const datosPeriodo = {
    labels: resumen.porPeriodo.map((p) => p.periodo),
    datasets: [{
      data: resumen.porPeriodo.map((p) => p.totalCajas),
      backgroundColor: COLORES_DONA,
      borderColor: "#ffffff", borderWidth: 3,
      hoverOffset: 10,
    }],
  };

  return (
    <div className="space-y-5 pb-10">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-widest text-primary-600">Tablero</p>
          <h1 className="mt-1 text-2xl font-bold text-slate-900">Resumen general</h1>
        </div>
        <button onClick={refrescar} className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50">
          ↻ Actualizar
        </button>
      </div>

      {/* Los mismos 4 filtros combinables del Excel */}
      <Tarjeta className="grid gap-3 sm:grid-cols-4">
        <label className="block">
          <span className="mb-1 block text-[11px] font-semibold uppercase text-slate-400">Subdirección</span>
          <select className={campoFiltro} value={filtros.subdireccionLocal ?? ""}
                  onChange={(e) => setFiltros({ ...filtros, subdireccionLocal: e.target.value || undefined, servicio: undefined })}>
            <option value="">Todas</option>
            {subdirecciones.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
        </label>
        <label className="block">
          <span className="mb-1 block text-[11px] font-semibold uppercase text-slate-400">Dependencia</span>
          <select className={campoFiltro} value={filtros.dependencia ?? ""}
                  onChange={(e) => setFiltros({ ...filtros, dependencia: e.target.value || undefined, servicio: undefined })}>
            <option value="">Todas</option>
            {dependenciasDisponibles.map((d) => <option key={d} value={d}>{d}</option>)}
          </select>
        </label>
        <label className="block">
          <span className="mb-1 block text-[11px] font-semibold uppercase text-slate-400">Servicio</span>
          <select className={campoFiltro} value={filtros.servicio ?? ""}
                  onChange={(e) => setFiltros({ ...filtros, servicio: e.target.value || undefined })}>
            <option value="">Todos</option>
            {serviciosDisponibles.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
        </label>
        <label className="block">
          <span className="mb-1 block text-[11px] font-semibold uppercase text-slate-400">Periodo TRD</span>
          <select className={campoFiltro} value={filtros.periodo ?? ""}
                  onChange={(e) => setFiltros({ ...filtros, periodo: e.target.value || undefined })}>
            <option value="">Todos</option>
            {PERIODOS_TRD.map((p) => <option key={p} value={p}>{p}</option>)}
          </select>
        </label>
        {(filtros.subdireccionLocal || filtros.dependencia || filtros.servicio || filtros.periodo) && (
          <button onClick={() => setFiltros({})} className="text-left text-xs font-semibold text-primary-600 hover:text-primary-700 sm:col-span-4">
            × Limpiar filtros
          </button>
        )}
      </Tarjeta>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
        <TarjetaKPI etiqueta="Cajas Vigentes" valor={String(resumen.cajasVigentesEnSitio)} color="#2563EB" />
        <TarjetaKPI etiqueta="% Avance Global" valor={`${Math.round(resumen.avancePromedioGlobal * 100)}%`} color="#0F766E" />
        <TarjetaKPI etiqueta="Unidades Operativas" valor={String(resumen.unidadesOperativas)} color="#F59E0B" />
        <TarjetaKPI etiqueta="Eliminación (histórico)" valor={String(resumen.cajasEliminacionHistorico)} color="#0F766E" />
        <TarjetaKPI etiqueta="Riesgo Alto" valor={String(resumen.unidadesEnRiesgoAlto)} color="#DC2626" />
      </div>

      <div className="grid gap-5 lg:grid-cols-2">
        <Tarjeta>
          <p className="mb-3 text-sm font-semibold text-slate-700">% Avance por Tarea</p>
          <div style={{ height: 260 }}>
            {resumen.porTarea.some((t) => t.avancePromedio > 0) || resumen.porTarea.length > 0 ? (
              <Bar data={datosTarea} options={graficoTareaOpciones} />
            ) : <p className="text-sm text-slate-400">Sin datos capturados todavía.</p>}
          </div>
        </Tarjeta>

        <Tarjeta>
          <p className="mb-3 text-sm font-semibold text-slate-700">Cajas por Periodo TRD</p>
          <div style={{ height: 260 }}>
            {resumen.porPeriodo.length === 0 ? (
              <p className="text-sm text-slate-400">Sin datos capturados todavía.</p>
            ) : <Doughnut data={datosPeriodo} options={graficoDonaOpciones} />}
          </div>
        </Tarjeta>
      </div>

      <Tarjeta>
        <p className="mb-3 text-sm font-semibold text-slate-700">Sobreapilamiento por Subdirección</p>
        {resumen.sobreapilamientoPorSubdireccion.length === 0 ? (
          <p className="text-sm text-slate-400">Sin datos todavía.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-left text-xs uppercase text-slate-400">
                  <th className="pb-2 pr-4">Subdirección</th>
                  <th className="pb-2 pr-4">Cajas Sobreapiladas</th>
                  <th className="pb-2">Metros de Espacio Invadido</th>
                </tr>
              </thead>
              <tbody>
                {resumen.sobreapilamientoPorSubdireccion.map((s) => (
                  <tr key={s.subdireccionLocal} className="border-b border-slate-100">
                    <td className="py-2 pr-4 text-slate-700">{s.subdireccionLocal}</td>
                    <td className="py-2 pr-4 font-mono text-slate-600">{s.cajasSobreapiladas}</td>
                    <td className="py-2 font-mono text-slate-600">{s.metrosEspacioAjenoInvadido.toFixed(1)} m</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Tarjeta>

      <Tarjeta>
        <p className="mb-3 text-sm font-semibold text-slate-700">Detalle por Unidad Operativa</p>
        {resumen.porDependenciaServicio.length === 0 ? (
          <p className="text-sm text-slate-400">Aún no hay visitas registradas.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-left text-xs uppercase text-slate-400">
                  <th className="pb-2 pr-4">Unidad</th>
                  <th className="pb-2 pr-4">Servicio</th>
                  <th className="pb-2 pr-4">Cajas Vigentes</th>
                  <th className="pb-2">% Avance</th>
                </tr>
              </thead>
              <tbody>
                {resumen.porDependenciaServicio.map((u, i) => (
                  <tr key={i} className="border-b border-slate-100">
                    <td className="py-2 pr-4 text-slate-700">{u.dependencia}</td>
                    <td className="py-2 pr-4 text-slate-500">{u.servicio}</td>
                    <td className="py-2 pr-4 font-mono text-slate-600">{u.totalCajas}</td>
                    <td className="py-2 font-mono text-slate-600">{Math.round(u.avancePromedio * 100)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Tarjeta>

      <p className="text-center text-xs text-slate-400">
        Actualizado: {new Date(resumen.actualizadoEn).toLocaleString("es-CO")}
      </p>
    </div>
  );
}
""",
}


def main():
    if not os.path.exists("package.json"):
        print("AVISO: corre esto desde la raiz de tu proyecto (donde esta package.json).")
        return
    for ruta, c in ARCHIVOS_TEXTO.items():
        os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
        with open(ruta, "w", encoding="utf-8", newline="\n") as f:
            f.write(c)
        print(f"OK  {ruta}  ({len(c)} caracteres)")
    print("\nListo. Corre: npm install")
    print("Despues: reinicia npm run dev y Ctrl+Shift+R")

if __name__ == "__main__":
    main()
