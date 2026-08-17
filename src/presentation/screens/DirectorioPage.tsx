import { useRef, useState } from "react";
import { useDirectorio } from "../hooks/useDirectorio";
import type { UnidadOperativa, Dependencia } from "../../domain/entities/UnidadOperativa";

function Tarjeta({ children }: { children: React.ReactNode }) {
  return <section className="glass-card glass-card-interactiva rounded-2xl p-5 sm:p-6">{children}</section>;
}

/** Parsea un CSV con columnas: Dependencia,Servicio,Subdireccion,Nombre,Encargado
 *  (encabezado obligatorio, en ese orden -- exportable directo desde la hoja "Directorio" del
 *  Excel: Dependencia | Servicio | Subdirección Local | Unidad Operativa | Encargado). */
function parsearCSV(texto: string): Array<Omit<UnidadOperativa, "id">> {
  const lineas = texto.split(/\r?\n/).filter((l) => l.trim() !== "");
  const filas = lineas.slice(1); // salta encabezado
  return filas.map((linea) => {
    const [dependencia, servicio, subdireccionLocal, nombre, encargado] = linea.split(",").map((c) => c.trim());
    return {
      dependencia: dependencia as Dependencia,
      servicio, subdireccionLocal, nombre,
      encargado: encargado || undefined,
      capacidad: { metrosMedidos: null, largoEspacioM: null, anchoEspacioM: null },
    };
  }).filter((u) => u.nombre);
}

/** Pantalla para importar el Directorio REAL (Dependencia/Servicio/Subdirección/Unidad) desde
 *  un CSV exportado del Excel -- para no inventar nombres de unidades institucionales, cada
 *  SLIS/CDC/Lavandería/CIAM que la app conoce viene directo de tus datos reales. */
export function DirectorioPage() {
  const { unidades, subdirecciones, loading, recargar, repo } = useDirectorio();
  const [importando, setImportando] = useState(false);
  const [mensaje, setMensaje] = useState<{ tipo: "ok" | "error"; texto: string } | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  async function manejarArchivo(e: React.ChangeEvent<HTMLInputElement>) {
    const archivo = e.target.files?.[0];
    if (!archivo) return;
    setImportando(true);
    setMensaje(null);
    try {
      const texto = await archivo.text();
      const filas = parsearCSV(texto);
      if (filas.length === 0) throw new Error("El archivo no tiene filas válidas. Revisa el formato de columnas.");
      const escritas = await repo.importarLote(filas);
      setMensaje({ tipo: "ok", texto: `${escritas} unidades importadas correctamente.` });
      await recargar();
    } catch (err) {
      setMensaje({ tipo: "error", texto: err instanceof Error ? err.message : "No se pudo importar el archivo." });
    } finally {
      setImportando(false);
      if (inputRef.current) inputRef.current.value = "";
    }
  }

  return (
    <div className="space-y-5 pb-10">
      <div>
        <p className="text-xs font-bold uppercase tracking-widest text-primary-600">Directorio</p>
        <h1 className="mt-1 text-2xl font-bold text-slate-900">Catálogo de unidades operativas</h1>
        <p className="mt-1 text-sm text-slate-500">
          SLIS, CDC, Lavanderías, CIAM y demás — el mismo Directorio del Excel, importado una sola vez.
        </p>
      </div>

      <Tarjeta>
        <p className="text-sm font-semibold text-slate-700">Importar desde CSV</p>
        <p className="mt-1 text-xs text-slate-500">
          Exporta la hoja "Directorio" del Excel a CSV con las columnas, en este orden:{" "}
          <code className="rounded bg-slate-100 px-1 py-0.5 text-[11px]">Dependencia,Servicio,Subdireccion,Nombre,Encargado</code>
        </p>
        <input
          ref={inputRef} type="file" accept=".csv" onChange={manejarArchivo} disabled={importando}
          className="mt-3 block w-full text-sm text-slate-600 file:mr-3 file:rounded-lg file:border-0 file:bg-primary-600 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-white hover:file:bg-primary-700"
        />
        {importando && <p className="mt-2 text-xs text-slate-400">Importando…</p>}
        {mensaje && (
          <p className={`mt-2 text-sm ${mensaje.tipo === "ok" ? "text-green-600" : "text-red-600"}`}>{mensaje.texto}</p>
        )}
      </Tarjeta>

      <Tarjeta>
        <p className="mb-3 text-sm font-semibold text-slate-700">
          {loading ? "Cargando…" : `${unidades.length} unidades en ${subdirecciones.length} subdirecciones`}
        </p>
        {!loading && unidades.length === 0 && (
          <p className="text-sm text-slate-400">
            Todavía no hay unidades importadas. Sube el CSV de arriba para empezar.
          </p>
        )}
        {subdirecciones.map((sub) => (
          <div key={sub} className="mb-3 border-b border-slate-100 pb-3 last:border-0">
            <p className="text-sm font-semibold text-slate-700">{sub}</p>
            <div className="mt-1 flex flex-wrap gap-1.5">
              {unidades.filter((u) => u.subdireccionLocal === sub).map((u) => (
                <span key={u.id} className="rounded-full bg-primary-50 px-2.5 py-1 text-xs text-primary-700">
                  {u.servicio} · {u.nombre}
                </span>
              ))}
            </div>
          </div>
        ))}
      </Tarjeta>
    </div>
  );
}
