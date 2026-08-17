import { useTablero } from "../hooks/useTablero";

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

/** Tablero real, Fase 3: lee TODO lo capturado en Firestore (RegistroPeriodo + PQRS) y calcula
 *  los mismos KPIs que el Excel -- Cajas Vigentes, % Avance Global, Unidades Operativas,
 *  Eliminación, Unidades en Riesgo Alto -- mas el desglose por Tarea y por Periodo TRD. */
export function TableroPage() {
  const { resumen, loading, error, refrescar } = useTablero();

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <p className="text-sm text-slate-400">Cargando tablero…</p>
      </div>
    );
  }

  if (error || !resumen) {
    return (
      <Tarjeta className="text-center">
        <p className="text-sm text-red-600">{error || "No se pudo cargar el tablero."}</p>
        <button onClick={refrescar} className="mt-3 text-sm font-semibold text-primary-600 hover:text-primary-700">
          Reintentar
        </button>
      </Tarjeta>
    );
  }

  return (
    <div className="space-y-5 pb-10">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-widest text-primary-600">Tablero</p>
          <h1 className="mt-1 text-2xl font-bold text-slate-900">Resumen general</h1>
          <p className="mt-1 text-sm text-slate-500">
            Calculado en vivo con lo capturado hasta ahora — {resumen.unidadesOperativas} unidades operativas.
          </p>
        </div>
        <button onClick={refrescar} className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50">
          ↻ Actualizar
        </button>
      </div>

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
          <div className="space-y-2.5">
            {resumen.porTarea.map((t) => (
              <div key={t.tarea} className="flex items-center gap-3">
                <span className="w-28 shrink-0 text-xs text-slate-600">{t.tarea}</span>
                <div className="h-2 flex-1 overflow-hidden rounded-full bg-slate-100">
                  <div className="h-full rounded-full bg-primary-500" style={{ width: `${Math.min(t.avancePromedio, 1) * 100}%` }} />
                </div>
                <span className="w-10 shrink-0 text-right font-mono text-xs text-slate-500">{Math.round(t.avancePromedio * 100)}%</span>
              </div>
            ))}
          </div>
        </Tarjeta>

        <Tarjeta>
          <p className="mb-3 text-sm font-semibold text-slate-700">Cajas por Periodo TRD</p>
          <div className="space-y-2.5">
            {resumen.porPeriodo.length === 0 && <p className="text-sm text-slate-400">Sin datos capturados todavía.</p>}
            {resumen.porPeriodo.map((p) => (
              <div key={p.periodo} className="flex items-center justify-between text-sm">
                <span className="text-slate-600">{p.periodo}</span>
                <span className="font-mono font-semibold text-slate-800">{p.totalCajas} cajas · {Math.round(p.avancePromedio * 100)}%</span>
              </div>
            ))}
          </div>
        </Tarjeta>
      </div>

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
                  <th className="pb-2 pr-4">Cajas Vigentes</th>
                  <th className="pb-2">% Avance</th>
                </tr>
              </thead>
              <tbody>
                {resumen.porDependenciaServicio.map((u) => (
                  <tr key={u.dependencia} className="border-b border-slate-100">
                    <td className="py-2 pr-4 text-slate-700">{u.dependencia}</td>
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
