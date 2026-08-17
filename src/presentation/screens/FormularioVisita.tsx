import { useMemo, useState } from "react";
import { useRegistroPeriodo } from "../hooks/useRegistroPeriodo";
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

// Orden del ciclo documental, igual que en el Excel: Eliminación va justo después de FUID.
// eliminacion es null por defecto -- "N/A" hasta que el usuario la toque, nunca 0 forzado.
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

const COLOR_SEMAFORO = {
  verde: "#2E9E6C",
  ambar: "#E8A33D",
  rojo: "#D9503F",
} as const;

export function FormularioVisita() {
  const { registrar, loading } = useRegistroPeriodo();
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

  const avanceTotal = useMemo(() => calcularAvanceTotal({ totalCajas, tareas }), [totalCajas, tareas]);
  const estado = semaforo(avanceTotal);

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
      setTareas(VACIAS);
      setTotalCajas(0);
      setTransferencia(TRANSFERENCIA_VACIA);
      setDiagnostico(DIAGNOSTICO_VACIO);
      setObservaciones("");
      setFechaVisita("");
    } catch (e) {
      setMensaje({ tipo: "error", texto: e instanceof Error ? e.message : "No se pudo guardar." });
    }
  }

  const puedeGuardar = unidadOperativaId.trim() !== "" && totalCajas > 0 && excedidas.length === 0 && !loading;

  return (
    <div style={{ maxWidth: 720, margin: "0 auto", padding: 24 }}>
      <header>
        <p style={{ color: "#0F9D8C", fontWeight: 700, fontSize: 12, textTransform: "uppercase" }}>Registro de visita</p>
        <h1 style={{ fontSize: 24, fontWeight: 600 }}>Capturar avance por periodo</h1>
        <p style={{ fontSize: 14, color: "#666" }}>Digita solo cantidades de cajas. Los porcentajes se calculan solos.</p>
      </header>

      <section style={{ marginTop: 16 }}>
        <label style={{ display: "block", marginBottom: 8 }}>
          <span>Unidad operativa</span>
          <input value={unidadOperativaId} onChange={(e) => setUnidad(e.target.value)}
                 placeholder="Ej. CDC Lago Timiza" style={{ display: "block", width: "100%" }} />
        </label>
        <label style={{ display: "block", marginBottom: 8 }}>
          <span>Periodo / fase TRD</span>
          <select value={periodo} onChange={(e) => setPeriodo(e.target.value as PeriodoTRD)} style={{ display: "block", width: "100%" }}>
            {PERIODOS.map((p) => <option key={p} value={p}>{p}</option>)}
          </select>
        </label>
        <label style={{ display: "block", marginBottom: 8, maxWidth: 220 }}>
          <span>Total cajas (meta)</span>
          <input type="number" min={0} value={totalCajas || ""} onChange={(e) => setTotalCajas(Number(e.target.value) || 0)}
                 style={{ display: "block", width: "100%" }} />
        </label>
        <label style={{ display: "block", marginBottom: 8, maxWidth: 220 }}>
          <span>Fecha de la visita</span>
          <input type="date" value={fechaVisita} onChange={(e) => setFechaVisita(e.target.value)} style={{ display: "block", width: "100%" }} />
          <span style={{ fontSize: 11, color: "#999" }}>En blanco = Pendiente. Futura = Programada. Hoy o antes = Realizada.</span>
        </label>
      </section>

      <section style={{ marginTop: 16 }}>
        <p style={{ fontWeight: 600 }}>Cajas completadas por tarea</p>
        {TAREAS.map(({ key, label, opcional }) => {
          const valor = tareas[key];
          const esNA = opcional && (valor === null || valor === undefined);
          const pct = calcularAvancePorTarea(valor, totalCajas);
          const excede = totalCajas > 0 && typeof valor === "number" && valor > totalCajas;
          return (
            <div key={key} style={{ display: "grid", gridTemplateColumns: "1fr auto auto auto", gap: 8, alignItems: "center", marginBottom: 6 }}>
              <span>{label}</span>
              {opcional ? (
                <label style={{ fontSize: 11 }}>
                  <input type="checkbox" checked={!!esNA} onChange={(e) => setTareas({ ...tareas, [key]: e.target.checked ? null : 0 })} /> N/A
                </label>
              ) : <span />}
              <input type="number" min={0} disabled={!!esNA}
                     style={{ width: 90, borderColor: excede ? "#D9503F" : undefined }}
                     value={esNA ? "" : (valor ?? 0) || ""}
                     onChange={(e) => setTareas({ ...tareas, [key]: Number(e.target.value) || 0 })} />
              <span style={{ width: 48, textAlign: "right" }}>{pct === null ? "N/A" : `${Math.round(pct * 100)}%`}</span>
            </div>
          );
        })}
        {excedidas.length > 0 && (
          <p style={{ color: "#D9503F", fontSize: 13 }}>
            {excedidas.map((t) => t.label).join(", ")} supera{excedidas.length > 1 ? "n" : ""} el Total Cajas. Revisa el dato.
          </p>
        )}
      </section>

      <section style={{ marginTop: 16, display: "flex", alignItems: "center", gap: 12 }}>
        <div style={{ width: 12, height: 12, borderRadius: "50%", background: COLOR_SEMAFORO[estado] }} />
        <div>
          <p style={{ fontSize: 12, color: "#666" }}>Avance total del periodo</p>
          <p style={{ fontSize: 22, fontWeight: 700 }}>{Math.round(avanceTotal * 100)}%</p>
        </div>
      </section>

      <section style={{ marginTop: 16 }}>
        <p style={{ fontWeight: 600 }}>Transferencia al archivo central</p>
        <p style={{ fontSize: 12, color: "#999" }}>
          Se activa solo cuando el periodo llegó al 100% y ya se trasladó. El histórico nunca cambia.
        </p>
        {([
          ["correoSAF", "Correo SAF"],
          ["aprobacionSAF", "Aprobación SAF"],
          ["trasladoArchivoCentral", "Traslado Archivo Central"],
        ] as const).map(([key, label]) => (
          <label key={key} style={{ marginRight: 16, fontSize: 13 }}>
            <input type="checkbox" checked={transferencia[key]}
                   onChange={(e) => setTransferencia({ ...transferencia, [key]: e.target.checked })} /> {label}
          </label>
        ))}
        {transferencia.trasladoArchivoCentral && (
          <label style={{ display: "block", marginTop: 8, maxWidth: 220 }}>
            <span>Cajas trasladadas</span>
            <input type="number" min={0} max={totalCajas} value={transferencia.cajasTrasladadas || ""}
                   onChange={(e) => setTransferencia({ ...transferencia, cajasTrasladadas: Number(e.target.value) || 0 })}
                   style={{ display: "block", width: "100%" }} />
          </label>
        )}
      </section>

      <section style={{ marginTop: 16 }}>
        <p style={{ fontWeight: 600 }}>Diagnóstico de conservación (esta visita)</p>
        <label style={{ display: "block", maxWidth: 260 }}>
          <span>Tipo de almacenamiento</span>
          <select value={diagnostico.tipoAlmacenamiento ?? ""}
                  onChange={(e) => setDiagnostico({ ...diagnostico, tipoAlmacenamiento: (e.target.value || null) as TipoAlmacenamiento | null })}
                  style={{ display: "block", width: "100%" }}>
            <option value="">Sin diagnosticar</option>
            {TIPOS_ALMACENAMIENTO.map((t) => <option key={t} value={t}>{t}</option>)}
          </select>
        </label>
        {([
          ["riesgoHumedad", "Humedad"],
          ["riesgoRoedores", "Roedores"],
          ["riesgoSobreapilamiento", "Sobreapilamiento"],
          ["riesgoFiltraciones", "Filtraciones / lluvias"],
        ] as const).map(([key, label]) => (
          <label key={key} style={{ marginRight: 16, fontSize: 13 }}>
            <input type="checkbox" checked={diagnostico[key] === true}
                   onChange={(e) => setDiagnostico({ ...diagnostico, [key]: e.target.checked })} /> {label}
          </label>
        ))}
        {diagnostico.riesgoSobreapilamiento && (
          <div style={{ marginTop: 8 }}>
            <label style={{ display: "block", maxWidth: 260 }}>
              <span>Cajas sobreapiladas (fuera de estantería)</span>
              <input type="number" min={0} value={diagnostico.cajasSobreapiladas || ""}
                     onChange={(e) => setDiagnostico({ ...diagnostico, cajasSobreapiladas: Number(e.target.value) || 0 })}
                     style={{ display: "block", width: "100%" }} />
            </label>
            <label style={{ display: "block", maxWidth: 260, marginTop: 8 }}>
              <span>Metros de espacio ajeno invadido</span>
              <input type="number" min={0} step={0.1} value={diagnostico.metrosEspacioAjenoInvadido || ""}
                     onChange={(e) => setDiagnostico({ ...diagnostico, metrosEspacioAjenoInvadido: Number(e.target.value) || 0 })}
                     style={{ display: "block", width: "100%" }} />
              <span style={{ fontSize: 11, color: "#999" }}>
                Pasillo, oficina u otro espacio que no es de archivo. 0 si el exceso está en el mismo rincón.
              </span>
            </label>
          </div>
        )}
      </section>

      <label style={{ display: "block", marginTop: 16 }}>
        <span>Encargado</span>
        <input value={encargado} onChange={(e) => setEncargado(e.target.value)} style={{ display: "block", width: "100%" }} />
      </label>
      <label style={{ display: "block", marginTop: 8 }}>
        <span>Observaciones</span>
        <textarea rows={2} value={observaciones} onChange={(e) => setObservaciones(e.target.value)}
                   style={{ display: "block", width: "100%" }} />
      </label>

      {mensaje && (
        <p style={{ marginTop: 16, color: mensaje.tipo === "ok" ? "#0F9D8C" : "#D9503F" }}>{mensaje.texto}</p>
      )}

      <button onClick={guardar} disabled={!puedeGuardar} style={{ marginTop: 16, padding: "12px 24px" }}>
        {loading ? "Guardando…" : "Registrar visita"}
      </button>
    </div>
  );
}
