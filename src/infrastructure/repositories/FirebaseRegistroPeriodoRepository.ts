import {
  collection,
  doc,
  addDoc,
  updateDoc,
  query,
  where,
  limit,
  startAfter,
  getDocs,
  onSnapshot,
  serverTimestamp,
  Timestamp,
} from "firebase/firestore";
import { db } from "../config/firebase";
import type { RegistroPeriodo } from "../../domain/entities/RegistroPeriodo";
import type {
  IRegistroPeriodoRepository,
  ResumenDashboard,
} from "../../domain/repositories/IRegistroPeriodoRepository";

const REGISTROS = "registrosPeriodo";
const RESUMENES = "resumenes"; // 1 documento por Dependencia (o "GLOBAL"), recalculado al guardar

function fromFirestore(id: string, data: any): RegistroPeriodo {
  return {
    id,
    unidadOperativaId: data.unidadOperativaId,
    periodo: data.periodo,
    totalCajas: data.totalCajas,
    tareas: data.tareas,
    transferencia: data.transferencia ?? {
      correoSAF: false,
      aprobacionSAF: false,
      trasladoArchivoCentral: false,
      cajasTrasladadas: 0,
    },
    diagnostico: data.diagnostico ?? {
      tipoAlmacenamiento: null,
      riesgoHumedad: null,
      riesgoRoedores: null,
      riesgoSobreapilamiento: null,
      riesgoFiltraciones: null,
      cajasSobreapiladas: 0,
      metrosEspacioAjenoInvadido: 0,
    },
    encargado: data.encargado ?? "",
    fechaVisita: data.fechaVisita ?? "",
    observaciones: data.observaciones ?? "",
    creadoEn: (data.creadoEn as Timestamp)?.toDate?.().toISOString() ?? "",
    actualizadoEn: (data.actualizadoEn as Timestamp)?.toDate?.().toISOString() ?? "",
  };
}

// Implementa el CONTRATO del dominio. Esta es la UNICA clase del proyecto que sabe
// que "por debajo" hay Firestore. Si manana migras a otra base, solo se reemplaza este archivo.
export class FirebaseRegistroPeriodoRepository implements IRegistroPeriodoRepository {
  async listarPorUnidad(unidadOperativaId: string): Promise<RegistroPeriodo[]> {
    const q = query(collection(db, REGISTROS), where("unidadOperativaId", "==", unidadOperativaId));
    const snap = await getDocs(q);
    return snap.docs.map((d) => fromFirestore(d.id, d.data()));
  }

  async listarPagina({
    dependencia,
    subdireccionLocal,
    servicio,
    periodo,
    cursor,
    tamanoPagina,
  }: Parameters<IRegistroPeriodoRepository["listarPagina"]>[0]) {
    const clauses: any[] = [];
    if (dependencia) clauses.push(where("dependencia", "==", dependencia));
    if (subdireccionLocal) clauses.push(where("subdireccionLocal", "==", subdireccionLocal));
    if (servicio) clauses.push(where("servicio", "==", servicio));
    if (periodo) clauses.push(where("periodo", "==", periodo));

    let q = query(collection(db, REGISTROS), ...clauses, limit(tamanoPagina));
    if (cursor) q = query(q, startAfter(cursor));

    const snap = await getDocs(q);
    const items = snap.docs.map((d) => fromFirestore(d.id, d.data()));
    const nextCursor = snap.docs.length === tamanoPagina ? snap.docs[snap.docs.length - 1] : null;
    return { items, nextCursor };
  }

  async guardar(registro: Omit<RegistroPeriodo, "id" | "creadoEn" | "actualizadoEn">): Promise<RegistroPeriodo> {
    const ref = await addDoc(collection(db, REGISTROS), {
      ...registro,
      creadoEn: serverTimestamp(),
      actualizadoEn: serverTimestamp(),
    });
    // El recalculo del "resumen" agregado se dispara aqui mismo (barato) o via Cloud Function
    // (mas robusto si varias personas guardan al mismo tiempo). Empieza simple, migra si hace falta.
    return { ...registro, id: ref.id, creadoEn: new Date().toISOString(), actualizadoEn: new Date().toISOString() };
  }

  async actualizar(id: string, cambios: Partial<RegistroPeriodo>): Promise<void> {
    await updateDoc(doc(db, REGISTROS, id), { ...cambios, actualizadoEn: serverTimestamp() });
  }

  suscribirseAResumen(
    filtros: { dependencia?: string; subdireccionLocal?: string },
    onCambio: (resumen: ResumenDashboard) => void
  ): () => void {
    // UNA sola lectura en tiempo real sobre UN documento agregado -- nunca sobre la coleccion cruda.
    const docId = filtros.dependencia ?? "GLOBAL";
    const unsub = onSnapshot(doc(db, RESUMENES, docId), (snap) => {
      if (snap.exists()) onCambio(snap.data() as ResumenDashboard);
    });
    return unsub;
  }
}
