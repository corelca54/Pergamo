import { useMemo, useState } from "react";
import { usePQRS } from "../hooks/usePQRS";
import {
  calcularAvancePorTarea,
  calcularAvanceTotal,
  semaforo,
} from "../../domain/entities/RegistroPeriodo";
import type { TareasCantidad, Semaforo } from "../../domain/entities/RegistroPeriodo";
import type { TrasladoPQRS } from "../../domain/entities/PQRS";
import { puedeIniciarTraslado } from "../../domain/entities/PQRS";

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
const TRASLADO_VACIO: TrasladoPQRS = {
  correoEnviado: false, aprobado: false, trasladado: false, cajasTrasladadas: 0,
};

const COLOR_SEMAFORO: Record<Semaforo, string> = {
  verde: "#16A34A", ambar: "#F59E0B", rojo: "#DC2626",
};

const campoBase =
  "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 " +
  "shadow-sm transition focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20";
const etiqueta = "block text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1.5";

function Tarjeta({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <section className={`glass-card glass-card-interactiva rounded-2xl p-5 sm:p-6 ${className}`}>{children}</section>;
}

export function PQRSPage() {
  const { registrar, loading } = usePQRS();
  const [unidadOperativaId, setUnidad] = useState("");
  const [totalCajas, setTotalCajas] = useState<number>(0);
  const [tareas, setTareas] = useState<TareasCantidad>(VACIAS);
  const [traslado, setTraslado] = useState<TrasladoPQRS>(TRASLADO_VACIO);
  const [encargado, setEncargado] = useState("");
  const [fechaVisita, setFechaVisita] = useState("");
  const [observaciones, setObservaciones] = useState("");
  const [mensaje, setMensaje] = useState<{ tipo: "ok" | "error"; texto: string } | null>(null);

  const avanceTotal = useMemo(() => calcularAvanceTotal({ totalCajas, tareas }), [totalCajas, tareas]);
  const estado = semaforo(avanceTotal);
  const listoParaTraslado = puedeIniciarTraslado({ totalCajas, tareas });

  const excedidas = TAREAS.filter(
    ({ key }) => totalCajas > 0 && typeof tareas[key] === "number" && (tareas[key] as number) > totalCajas
  );

  async function guardar() {
    setMensaje(null);
    try {
      await registrar({
        unidadOperativaId, totalCajas, tareas, traslado,
        encargado: encargado || undefined,
        fechaVisita: fechaVisita || undefined,
        observaciones: observaciones || undefined,
      });
      setMensaje({ tipo: "ok", texto: "PQRS registrado. El tablero ya refleja el cambio." });
      setTareas(VACIAS); setTotalCajas(0); setTraslado(TRASLADO_VACIO);
      setObservaciones(""); setFechaVisita("");
    } catch (e) {
      setMensaje({ tipo: "error", texto: e instanceof Error ? e.message : "No se pudo guardar." });
    }
  }

  const puedeGuardar = unidadOperativaId.trim() !== "" && totalCajas > 0 && excedidas.length === 0 && !loading;

  return (
    <div className="space-y-5 pb-10">
      <div>
        <p className="text-xs font-bold uppercase tracking-widest text-primary-600">Registro de PQRS</p>
        <h1 className="mt-1 text-2xl font-bold text-slate-900">Organización y traslado de PQRS</h1>
        <p className="mt-1 text-sm text-slate-500">
          Mismo flujo de organización que el TRD normal — se cuenta en cajas. El destino final es
          la Subsecretaría de Gestión Institucional, no el Archivo Central.
        </p>
      </div>

      <Tarjeta>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block sm:col-span-2">
            <span className={etiqueta}>Unidad operativa</span>
            <input className={campoBase} value={unidadOperativaId} onChange={(e) => setUnidad(e.target.value)}
                   placeholder="Ej. CDC Lago Timiza" />
          </label>
          <label className="block">
            <span className={etiqueta}>Total cajas PQRS</span>
            <input type="number" min={0} className={`${campoBase} font-mono text-base`}
                   value={totalCajas || ""} onChange={(e) => setTotalCajas(Number(e.target.value) || 0)} />
          </label>
          <label className="block">
            <span className={etiqueta}>Fecha de la visita</span>
            <input type="date" className={campoBase} value={fechaVisita} onChange={(e) => setFechaVisita(e.target.value)} />
          </label>
        </div>
      </Tarjeta>

      <Tarjeta>
        <p className="mb-3 text-sm font-semibold text-slate-700">Cajas organizadas por tarea</p>
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
                    <div className={`h-full rounded-full transition-all ${excede ? "bg-red-500" : "bg-primary-500"}`}
                         style={{ width: `${Math.min(pct ?? 0, 1) * 100}%` }} />
                  </div>
                </div>
                <input type="number" min={0} disabled={!!esNA} aria-label={`Cajas de ${label}`}
                  className={`w-20 rounded-lg border px-2 py-1.5 text-right text-sm font-mono shadow-sm
                    focus:outline-none focus:ring-2 focus:ring-primary-500/20 disabled:bg-slate-50 disabled:text-slate-300
                    ${excede ? "border-red-400 ring-1 ring-red-400" : "border-slate-300 focus:border-primary-500"}`}
                  value={esNA ? "" : (valor ?? 0) || ""}
                  onChange={(e) => setTareas({ ...tareas, [key]: Number(e.target.value) || 0 })} />
                <span className="w-11 shrink-0 text-right text-sm font-mono text-slate-500">
                  {pct === null ? "N/A" : `${Math.round(pct * 100)}%`}
                </span>
              </div>
            );
          })}
        </div>
        {excedidas.length > 0 && (
          <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3">
            <p className="text-sm text-red-700">
              {excedidas.map((t) => t.label).join(", ")} supera{excedidas.length > 1 ? "n" : ""} el total de cajas.
            </p>
          </div>
        )}
      </Tarjeta>

      <Tarjeta className="flex items-center gap-4">
        <div className="h-3 w-3 shrink-0 rounded-full" style={{ background: COLOR_SEMAFORO[estado] }} />
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Avance de organización</p>
          <p className="font-mono text-3xl font-bold" style={{ color: COLOR_SEMAFORO[estado] }}>
            {Math.round(avanceTotal * 100)}%
          </p>
        </div>
      </Tarjeta>

      <Tarjeta>
        <p className="text-sm font-semibold text-slate-700">Traslado a Subsecretaría de Gestión Institucional</p>
        <p className="mt-1 text-xs text-slate-400">
          {listoParaTraslado
            ? "La organización está completa — ya se puede notificar y trasladar."
            : "Solo se habilita cuando el avance de organización llega al 90% o más."}
        </p>
        <div className="mt-3 flex flex-wrap gap-x-6 gap-y-2">
          {([
            ["correoEnviado", "Correo enviado"],
            ["aprobado", "Aprobado"],
            ["trasladado", "Trasladado"],
          ] as const).map(([key, label]) => (
            <label key={key} className={`flex items-center gap-2 text-sm ${listoParaTraslado ? "text-slate-700" : "text-slate-300"}`}>
              <input type="checkbox" checked={traslado[key]} disabled={!listoParaTraslado}
                     onChange={(e) => setTraslado({ ...traslado, [key]: e.target.checked })} />
              {label}
            </label>
          ))}
        </div>
        {traslado.trasladado && (
          <label className="mt-3 block max-w-[220px]">
            <span className={etiqueta}>Cajas trasladadas</span>
            <input type="number" min={0} max={totalCajas} className={campoBase}
                   value={traslado.cajasTrasladadas || ""}
                   onChange={(e) => setTraslado({ ...traslado, cajasTrasladadas: Number(e.target.value) || 0 })} />
          </label>
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
            <textarea className={campoBase} rows={2} value={observaciones} onChange={(e) => setObservaciones(e.target.value)} />
          </label>
        </div>
      </Tarjeta>

      {mensaje && (
        <div className={`rounded-lg border px-4 py-3 text-sm ${
          mensaje.tipo === "ok" ? "border-green-200 bg-green-50 text-green-700" : "border-red-200 bg-red-50 text-red-700"
        }`}>
          {mensaje.texto}
        </div>
      )}

      <button onClick={guardar} disabled={!puedeGuardar}
        className="w-full sm:w-auto rounded-xl bg-primary-700 px-6 py-3 text-sm font-semibold text-white shadow-md
                   transition hover:bg-primary-800 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:shadow-none">
        {loading ? "Guardando…" : "Registrar PQRS"}
      </button>
    </div>
  );
}
