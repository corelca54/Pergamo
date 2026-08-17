import { useState } from "react";
import { useAyudaDeMemoria } from "../hooks/useAyudaDeMemoria";
import type { AsistenteActa, CompromisoActa } from "../../domain/entities/AyudaDeMemoria";

const campoBase =
  "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 " +
  "shadow-sm transition focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20";
const etiqueta = "block text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1.5";

function Tarjeta({ children }: { children: React.ReactNode }) {
  return <section className="glass-card glass-card-interactiva rounded-2xl p-5 sm:p-6">{children}</section>;
}

const ASISTENTE_VACIO: AsistenteActa = { nombre: "", cargoRol: "", dependencia: "" };
const COMPROMISO_VACIO: CompromisoActa = { actividad: "", responsable: "", fechaLimite: "" };

/** Formato institucional GD-040: Lugar / Fecha / Tema / Desarrollo / Asistentes (filas
 *  dinamicas, "Inserte tantas filas como requiera" dice la plantilla) / Compromisos (mismo
 *  patron) / Proxima reunion / Elaboro. */
export function AyudaDeMemoriaPage() {
  const { generarPDF, loading, error } = useAyudaDeMemoria();
  const [lugar, setLugar] = useState("");
  const [fecha, setFecha] = useState("");
  const [tema, setTema] = useState("");
  const [desarrollo, setDesarrollo] = useState("");
  const [asistentes, setAsistentes] = useState<AsistenteActa[]>([{ ...ASISTENTE_VACIO }]);
  const [compromisos, setCompromisos] = useState<CompromisoActa[]>([{ ...COMPROMISO_VACIO }]);
  const [proximaReunion, setProximaReunion] = useState("");
  const [elaboroPor, setElaboroPor] = useState("");
  const [mensaje, setMensaje] = useState<{ tipo: "ok" | "error"; texto: string } | null>(null);

  function actualizarAsistente(i: number, campo: keyof AsistenteActa, valor: string) {
    setAsistentes(asistentes.map((a, idx) => (idx === i ? { ...a, [campo]: valor } : a)));
  }
  function actualizarCompromiso(i: number, campo: keyof CompromisoActa, valor: string) {
    setCompromisos(compromisos.map((c, idx) => (idx === i ? { ...c, [campo]: valor } : c)));
  }

  async function generar() {
    setMensaje(null);
    try {
      await generarPDF({
        lugar, fecha, tema, desarrollo,
        asistentes: asistentes.filter((a) => a.nombre.trim() !== ""),
        compromisos: compromisos.filter((c) => c.actividad.trim() !== ""),
        proximaReunion: proximaReunion || undefined,
        elaboroPor,
      });
      setMensaje({ tipo: "ok", texto: "PDF generado y descargado con el formato institucional GD-040." });
    } catch (e) {
      setMensaje({ tipo: "error", texto: e instanceof Error ? e.message : "No se pudo generar el PDF." });
    }
  }

  return (
    <div className="space-y-5 pb-10">
      <div>
        <p className="text-xs font-bold uppercase tracking-widest text-primary-600">Ayuda de memoria</p>
        <h1 className="mt-1 text-2xl font-bold text-slate-900">Formato GD-040</h1>
        <p className="mt-1 text-sm text-slate-500">Genera el PDF con el mismo formato institucional que ya usa el equipo.</p>
      </div>

      <Tarjeta>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block">
            <span className={etiqueta}>Lugar</span>
            <input className={campoBase} value={lugar} onChange={(e) => setLugar(e.target.value)}
                   placeholder="Dependencia o entidad donde se realizó la reunión" />
          </label>
          <label className="block">
            <span className={etiqueta}>Fecha</span>
            <input type="date" className={campoBase} value={fecha} onChange={(e) => setFecha(e.target.value)} />
          </label>
          <label className="block sm:col-span-2">
            <span className={etiqueta}>Tema</span>
            <input className={campoBase} value={tema} onChange={(e) => setTema(e.target.value)}
                   placeholder="Objetivo de la reunión" />
          </label>
          <label className="block sm:col-span-2">
            <span className={etiqueta}>Desarrollo</span>
            <textarea className={campoBase} rows={4} value={desarrollo} onChange={(e) => setDesarrollo(e.target.value)}
                       placeholder="Puntos específicos tratados u orden del día" />
          </label>
        </div>
      </Tarjeta>

      <Tarjeta>
        <div className="mb-3 flex items-center justify-between">
          <p className="text-sm font-semibold text-slate-700">Asistentes</p>
          <button onClick={() => setAsistentes([...asistentes, { ...ASISTENTE_VACIO }])}
                  className="text-xs font-semibold text-primary-600 hover:text-primary-700">
            + Agregar asistente
          </button>
        </div>
        <div className="space-y-3">
          {asistentes.map((a, i) => (
            <div key={i} className="grid grid-cols-[1fr_1fr_1fr_auto] items-end gap-2 border-b border-slate-100 pb-3">
              <label className="block">
                <span className="text-[10px] text-slate-400">Nombre</span>
                <input className={campoBase} value={a.nombre} onChange={(e) => actualizarAsistente(i, "nombre", e.target.value)} />
              </label>
              <label className="block">
                <span className="text-[10px] text-slate-400">Cargo/Rol</span>
                <input className={campoBase} value={a.cargoRol} onChange={(e) => actualizarAsistente(i, "cargoRol", e.target.value)} />
              </label>
              <label className="block">
                <span className="text-[10px] text-slate-400">Dependencia</span>
                <input className={campoBase} value={a.dependencia} onChange={(e) => actualizarAsistente(i, "dependencia", e.target.value)}
                       placeholder="No aplica si es usuario/beneficiario" />
              </label>
              <button onClick={() => setAsistentes(asistentes.filter((_, idx) => idx !== i))}
                      disabled={asistentes.length === 1}
                      className="h-9 rounded-lg px-2 text-xs text-red-500 hover:bg-red-50 disabled:opacity-30">
                Quitar
              </button>
            </div>
          ))}
        </div>
        <p className="mt-2 text-xs text-slate-400">La firma queda en blanco en el PDF — se firma físicamente en papel.</p>
      </Tarjeta>

      <Tarjeta>
        <div className="mb-3 flex items-center justify-between">
          <p className="text-sm font-semibold text-slate-700">Compromisos</p>
          <button onClick={() => setCompromisos([...compromisos, { ...COMPROMISO_VACIO }])}
                  className="text-xs font-semibold text-primary-600 hover:text-primary-700">
            + Agregar compromiso
          </button>
        </div>
        <div className="space-y-3">
          {compromisos.map((c, i) => (
            <div key={i} className="grid grid-cols-[1.5fr_1fr_1fr_auto] items-end gap-2 border-b border-slate-100 pb-3">
              <label className="block">
                <span className="text-[10px] text-slate-400">Actividad</span>
                <input className={campoBase} value={c.actividad} onChange={(e) => actualizarCompromiso(i, "actividad", e.target.value)} />
              </label>
              <label className="block">
                <span className="text-[10px] text-slate-400">Responsable</span>
                <input className={campoBase} value={c.responsable} onChange={(e) => actualizarCompromiso(i, "responsable", e.target.value)} />
              </label>
              <label className="block">
                <span className="text-[10px] text-slate-400">Fecha límite</span>
                <input type="date" className={campoBase} value={c.fechaLimite} onChange={(e) => actualizarCompromiso(i, "fechaLimite", e.target.value)} />
              </label>
              <button onClick={() => setCompromisos(compromisos.filter((_, idx) => idx !== i))}
                      disabled={compromisos.length === 1}
                      className="h-9 rounded-lg px-2 text-xs text-red-500 hover:bg-red-50 disabled:opacity-30">
                Quitar
              </button>
            </div>
          ))}
        </div>
      </Tarjeta>

      <Tarjeta>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block">
            <span className={etiqueta}>Próxima reunión</span>
            <input type="date" className={campoBase} value={proximaReunion} onChange={(e) => setProximaReunion(e.target.value)} />
          </label>
          <label className="block">
            <span className={etiqueta}>Elaboró</span>
            <input className={campoBase} value={elaboroPor} onChange={(e) => setElaboroPor(e.target.value)} />
          </label>
        </div>
      </Tarjeta>

      {(mensaje || error) && (
        <div className={`rounded-lg border px-4 py-3 text-sm ${
          mensaje?.tipo === "ok" ? "border-green-200 bg-green-50 text-green-700" : "border-red-200 bg-red-50 text-red-700"
        }`}>
          {mensaje?.texto ?? error}
        </div>
      )}

      <button onClick={generar} disabled={loading}
        className="w-full sm:w-auto rounded-xl bg-primary-700 px-6 py-3 text-sm font-semibold text-white shadow-md
                   transition hover:bg-primary-800 disabled:cursor-not-allowed disabled:bg-slate-300">
        {loading ? "Generando…" : "Generar PDF"}
      </button>
    </div>
  );
}
