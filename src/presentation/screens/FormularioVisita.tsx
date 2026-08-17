import { useMemo, useState } from "react";
import { useRegistroPeriodo } from "../hooks/useRegistroPeriodo";
import { useDirectorio } from "../hooks/useDirectorio";
import {
  calcularAvancePorTarea,
  calcularAvanceTotal,
  semaforo,
  PERIODOS_TRD,
} from "../../domain/entities/RegistroPeriodo";
import type {
  PeriodoTRD,
  TareasCantidad,
  Transferencia,
  DiagnosticoRiesgo,
  TipoAlmacenamiento,
} from "../../domain/entities/RegistroPeriodo";

const PERIODOS = PERIODOS_TRD;

const TAREAS: Array<{ key: keyof TareasCantidad; label: string; opcional?: boolean }> = [
  { key: "fuid", label: "FUID" },
  { key: "eliminacion", label: "Eliminación", opcional: true },
  { key: "clasificacion", label: "Clasificación" },
  { key: "ordenacion", label: "Ordenación" },
  { key: "foliacion", label: "Foliación" },
  { key: "hojaControl", label: "Hoja de Control" },
  { key: "rotulacion", label: "Rotulación" },
];

const VACIAS: TareasCantidad = {
  fuid: 0, eliminacion: null, clasificacion: 0, ordenacion: 0,
  foliacion: 0, hojaControl: 0, rotulacion: 0,
};
const TRANSFERENCIA_VACIA: Transferencia = {
  correoSAF: false, aprobacionSAF: false, trasladoArchivoCentral: false, cajasTrasladadas: 0,
};
const DIAGNOSTICO_VACIO: DiagnosticoRiesgo = {
  tipoAlmacenamiento: null,
  riesgoHumedad: null, riesgoRoedores: null, riesgoSobreapilamiento: null, riesgoFiltraciones: null,
  cajasSobreapiladas: 0, metrosEspacioAjenoInvadido: 0,
};
const TIPOS_ALMACENAMIENTO: TipoAlmacenamiento[] = [
  "Estantería adecuada", "Piso", "Piso y Estantería", "Lugar no apropiado",
];

const SEMAFORO_ESTILO = {
  verde: { punto: "bg-emerald-500", texto: "text-emerald-700", fondo: "bg-emerald-50", borde: "border-emerald-200" },
  ambar: { punto: "bg-amber-500", texto: "text-amber-700", fondo: "bg-amber-50", borde: "border-amber-200" },
  rojo: { punto: "bg-red-500", texto: "text-red-700", fondo: "bg-red-50", borde: "border-red-200" },
} as const;

const campoBase =
  "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 " +
  "shadow-sm transition focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20";
const etiqueta = "block text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1.5";

function Tarjeta({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <section className={`glass-card glass-card-interactiva rounded-2xl p-5 sm:p-6 ${className}`}>
      {children}
    </section>
  );
}

export function FormularioVisita() {
  const { registrar, loading } = useRegistroPeriodo();
  const { subdirecciones, serviciosDe, unidadesDe, loading: cargandoDirectorio } = useDirectorio();
  const [subdireccionSel, setSubdireccionSel] = useState("");
  const [servicioSel, setServicioSel] = useState("");
  const [unidadOperativaId, setUnidad] = useState("");
  const [periodo, setPeriodo] = useState<PeriodoTRD>(PERIODOS[0]);
  const [totalCajas, setTotalCajas] = useState<number>(0);
  const [tareas, setTareas] = useState<TareasCantidad>(VACIAS);
  const [transferencia, setTransferencia] = useState<Transferencia>(TRANSFERENCIA_VACIA);
  const [diagnostico, setDiagnostico] = useState<DiagnosticoRiesgo>(DIAGNOSTICO_VACIO);
  const [encargado, setEncargado] = useState("");
  const [fechaVisita, setFechaVisita] = useState("");
  const [observaciones, setObservaciones] = useState("");
  const [mensaje, setMensaje] = useState<{ tipo: "ok" | "error"; texto: string } | null>(null);

  const serviciosDisponibles = subdireccionSel ? serviciosDe(subdireccionSel) : [];
  const unidadesDisponibles = subdireccionSel && servicioSel ? unidadesDe(subdireccionSel, servicioSel) : [];

  const avanceTotal = useMemo(() => calcularAvanceTotal({ totalCajas, tareas }), [totalCajas, tareas]);
  const estado = semaforo(avanceTotal);
  const estiloEstado = SEMAFORO_ESTILO[estado];

  const excedidas = TAREAS.filter(
    ({ key }) => totalCajas > 0 && typeof tareas[key] === "number" && (tareas[key] as number) > totalCajas
  );

  async function guardar() {
    setMensaje(null);
    try {
      await registrar({
        unidadOperativaId, periodo, totalCajas, tareas, transferencia, diagnostico,
        encargado: encargado || undefined,
        fechaVisita: fechaVisita || undefined,
        observaciones: observaciones || undefined,
      });
      setMensaje({ tipo: "ok", texto: "Visita registrada. El tablero ya refleja el cambio." });
      setTareas(VACIAS); setTotalCajas(0);
      setTransferencia(TRANSFERENCIA_VACIA); setDiagnostico(DIAGNOSTICO_VACIO);
      setObservaciones(""); setFechaVisita("");
    } catch (e) {
      setMensaje({ tipo: "error", texto: e instanceof Error ? e.message : "No se pudo guardar." });
    }
  }

  const puedeGuardar = unidadOperativaId.trim() !== "" && totalCajas > 0 && excedidas.length === 0 && !loading;

  return (
    <div className="space-y-5 pb-10">
      <div>
        <p className="text-xs font-bold uppercase tracking-widest text-primary-600">Registro de visita</p>
        <h1 className="mt-1 text-2xl font-bold text-slate-900">Capturar avance por periodo</h1>
        <p className="mt-1 text-sm text-slate-500">Digita solo cantidades de cajas. Los porcentajes se calculan solos.</p>
      </div>

      <Tarjeta>
        <div className="grid gap-4 sm:grid-cols-3">
          <label className="block">
            <span className={etiqueta}>Subdirección Local</span>
            <select className={campoBase} value={subdireccionSel}
                    onChange={(e) => { setSubdireccionSel(e.target.value); setServicioSel(""); setUnidad(""); }}
                    disabled={cargandoDirectorio}>
              <option value="">{cargandoDirectorio ? "Cargando…" : "Selecciona…"}</option>
              {subdirecciones.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </label>
          <label className="block">
            <span className={etiqueta}>Servicio</span>
            <select className={campoBase} value={servicioSel} disabled={!subdireccionSel}
                    onChange={(e) => { setServicioSel(e.target.value); setUnidad(""); }}>
              <option value="">{subdireccionSel ? "Selecciona…" : "Elige subdirección primero"}</option>
              {serviciosDisponibles.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </label>
          <label className="block">
            <span className={etiqueta}>Unidad operativa</span>
            <select className={campoBase} value={unidadOperativaId} disabled={!servicioSel}
                    onChange={(e) => setUnidad(e.target.value)}>
              <option value="">{servicioSel ? "Selecciona…" : "Elige servicio primero"}</option>
              {unidadesDisponibles.map((u) => <option key={u.id} value={u.id}>{u.nombre}</option>)}
            </select>
            {servicioSel && unidadesDisponibles.length === 0 && (
              <p className="mt-1 text-xs text-amber-600">No hay unidades registradas aquí — impórtalas en "Directorio".</p>
            )}
          </label>
          <label className="block">
            <span className={etiqueta}>Periodo / fase TRD</span>
            <select className={campoBase} value={periodo} onChange={(e) => setPeriodo(e.target.value as PeriodoTRD)}>
              {PERIODOS.map((p) => <option key={p} value={p}>{p}</option>)}
            </select>
          </label>
          <label className="block">
            <span className={etiqueta}>Total cajas (meta)</span>
            <input type="number" min={0} className={`${campoBase} font-mono text-base`}
                   value={totalCajas || ""} onChange={(e) => setTotalCajas(Number(e.target.value) || 0)} />
          </label>
          <label className="block sm:col-span-2">
            <span className={etiqueta}>Fecha de la visita</span>
            <input type="date" className={`${campoBase} max-w-xs`} value={fechaVisita}
                   onChange={(e) => setFechaVisita(e.target.value)} />
            <span className="mt-1 block text-xs text-slate-400">
              En blanco = Pendiente. Futura = Programada. Hoy o antes = Realizada.
            </span>
          </label>
        </div>
      </Tarjeta>

      <Tarjeta>
        <p className="mb-3 text-sm font-semibold text-slate-700">Cajas completadas por tarea</p>
        <div className="space-y-3">
          {TAREAS.map(({ key, label, opcional }) => {
            const valor = tareas[key];
            const esNA = opcional && (valor === null || valor === undefined);
            const pct = calcularAvancePorTarea(valor, totalCajas);
            const excede = totalCajas > 0 && typeof valor === "number" && valor > totalCajas;
            return (
              <div key={key} className="flex items-center gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-700">{label}</span>
                    {opcional && (
                      <label className="flex items-center gap-1.5 text-xs text-slate-400">
                        <input type="checkbox" checked={!!esNA}
                               onChange={(e) => setTareas({ ...tareas, [key]: e.target.checked ? null : 0 })} />
                        N/A
                      </label>
                    )}
                  </div>
                  <div className="mt-1.5 h-1.5 w-full overflow-hidden rounded-full bg-slate-100">
                    <div
                      className={`h-full rounded-full transition-all ${excede ? "bg-red-500" : "bg-primary-500"}`}
                      style={{ width: `${Math.min(pct ?? 0, 1) * 100}%` }}
                    />
                  </div>
                </div>
                <input
                  type="number" min={0} disabled={!!esNA} aria-label={`Cajas de ${label}`}
                  className={`w-20 rounded-lg border px-2 py-1.5 text-right text-sm font-mono shadow-sm
                    focus:outline-none focus:ring-2 focus:ring-primary-500/20 disabled:bg-slate-50 disabled:text-slate-300
                    ${excede ? "border-red-400 ring-1 ring-red-400" : "border-slate-300 focus:border-primary-500"}`}
                  value={esNA ? "" : (valor ?? 0) || ""}
                  onChange={(e) => setTareas({ ...tareas, [key]: Number(e.target.value) || 0 })}
                />
                <span className="w-11 shrink-0 text-right text-sm font-mono text-slate-500">
                  {pct === null ? "N/A" : `${Math.round(pct * 100)}%`}
                </span>
              </div>
            );
          })}
        </div>
        {excedidas.length > 0 && (
          <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3">
            <p className="text-xs font-bold uppercase tracking-wide text-red-700">Revisa estas cantidades</p>
            <p className="mt-1 text-sm text-red-700">
              {excedidas.map((t) => t.label).join(", ")} supera{excedidas.length > 1 ? "n" : ""} las{" "}
              <span className="font-mono">{totalCajas}</span> cajas del periodo.
            </p>
          </div>
        )}
      </Tarjeta>

      <Tarjeta className={`flex items-center gap-4 ${estiloEstado.fondo} ${estiloEstado.borde}`}>
        <div className={`h-3 w-3 shrink-0 rounded-full ${estiloEstado.punto}`} />
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Avance total del periodo</p>
          <p className={`font-mono text-3xl font-bold ${estiloEstado.texto}`}>{Math.round(avanceTotal * 100)}%</p>
        </div>
      </Tarjeta>

      <Tarjeta>
        <p className="text-sm font-semibold text-slate-700">Transferencia al archivo central</p>
        <p className="mt-1 text-xs text-slate-400">
          Se activa solo cuando el periodo llegó al 100% y ya se trasladó. El histórico nunca cambia.
        </p>
        <div className="mt-3 flex flex-wrap gap-x-6 gap-y-2">
          {([
            ["correoSAF", "Correo SAF"],
            ["aprobacionSAF", "Aprobación SAF"],
            ["trasladoArchivoCentral", "Traslado Archivo Central"],
          ] as const).map(([key, label]) => (
            <label key={key} className="flex items-center gap-2 text-sm text-slate-700">
              <input type="checkbox" checked={transferencia[key]}
                     onChange={(e) => setTransferencia({ ...transferencia, [key]: e.target.checked })} />
              {label}
            </label>
          ))}
        </div>
        {transferencia.trasladoArchivoCentral && (
          <label className="mt-3 block max-w-[220px]">
            <span className={etiqueta}>Cajas trasladadas</span>
            <input type="number" min={0} max={totalCajas} className={campoBase}
                   value={transferencia.cajasTrasladadas || ""}
                   onChange={(e) => setTransferencia({ ...transferencia, cajasTrasladadas: Number(e.target.value) || 0 })} />
          </label>
        )}
      </Tarjeta>

      <Tarjeta>
        <p className="text-sm font-semibold text-slate-700">Diagnóstico de conservación (esta visita)</p>
        <label className="mt-3 block max-w-xs">
          <span className={etiqueta}>Tipo de almacenamiento</span>
          <select className={campoBase} value={diagnostico.tipoAlmacenamiento ?? ""}
                  onChange={(e) => setDiagnostico({ ...diagnostico, tipoAlmacenamiento: (e.target.value || null) as TipoAlmacenamiento | null })}>
            <option value="">Sin diagnosticar</option>
            {TIPOS_ALMACENAMIENTO.map((t) => <option key={t} value={t}>{t}</option>)}
          </select>
        </label>
        <div className="mt-3 flex flex-wrap gap-x-6 gap-y-2">
          {([
            ["riesgoHumedad", "Humedad"],
            ["riesgoRoedores", "Roedores"],
            ["riesgoSobreapilamiento", "Sobreapilamiento"],
            ["riesgoFiltraciones", "Filtraciones / lluvias"],
          ] as const).map(([key, label]) => (
            <label key={key} className="flex items-center gap-2 text-sm text-slate-700">
              <input type="checkbox" checked={diagnostico[key] === true}
                     onChange={(e) => setDiagnostico({ ...diagnostico, [key]: e.target.checked })} />
              {label}
            </label>
          ))}
        </div>
        {diagnostico.riesgoSobreapilamiento && (
          <div className="mt-4 grid gap-4 border-t border-slate-100 pt-4 sm:grid-cols-2">
            <label className="block">
              <span className={etiqueta}>Cajas sobreapiladas (fuera de estantería)</span>
              <input type="number" min={0} className={campoBase}
                     value={diagnostico.cajasSobreapiladas || ""}
                     onChange={(e) => setDiagnostico({ ...diagnostico, cajasSobreapiladas: Number(e.target.value) || 0 })} />
            </label>
            <label className="block">
              <span className={etiqueta}>Metros de espacio ajeno invadido</span>
              <input type="number" min={0} step={0.1} className={campoBase}
                     value={diagnostico.metrosEspacioAjenoInvadido || ""}
                     onChange={(e) => setDiagnostico({ ...diagnostico, metrosEspacioAjenoInvadido: Number(e.target.value) || 0 })} />
              <span className="mt-1 block text-xs text-slate-400">
                Pasillo, oficina u otro espacio que no es de archivo. 0 si el exceso está en el mismo rincón.
              </span>
            </label>
          </div>
        )}
      </Tarjeta>

      <Tarjeta>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block">
            <span className={etiqueta}>Encargado</span>
            <input className={campoBase} value={encargado} onChange={(e) => setEncargado(e.target.value)} />
          </label>
          <label className="block">
            <span className={etiqueta}>Observaciones</span>
            <textarea className={campoBase} rows={2} value={observaciones}
                      onChange={(e) => setObservaciones(e.target.value)}
                      placeholder="Novedades de la visita (opcional)" />
          </label>
        </div>
      </Tarjeta>

      {mensaje && (
        <div className={`rounded-lg border px-4 py-3 text-sm ${
          mensaje.tipo === "ok" ? "border-emerald-200 bg-emerald-50 text-emerald-700" : "border-red-200 bg-red-50 text-red-700"
        }`}>
          {mensaje.texto}
        </div>
      )}

      <button
        onClick={guardar}
        disabled={!puedeGuardar}
        className="w-full sm:w-auto rounded-xl bg-primary-700 px-6 py-3 text-sm font-semibold text-white shadow-md
                   transition hover:bg-primary-800 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:shadow-none"
      >
        {loading ? "Guardando…" : "Registrar visita"}
      </button>
    </div>
  );
}
