import { collection, addDoc, updateDoc, doc, query, where, getDocs, serverTimestamp, Timestamp } from "firebase/firestore";
import { db } from "../config/firebase";
import type { PQRS } from "../../domain/entities/PQRS";
import type { IPQRSRepository } from "../../domain/repositories/IPQRSRepository";

const PQRS_COLECCION = "pqrs";

function fromFirestore(id: string, data: any): PQRS {
  return {
    id,
    unidadOperativaId: data.unidadOperativaId,
    totalCajas: data.totalCajas,
    tareas: data.tareas,
    traslado: data.traslado ?? {
      correoEnviado: false, aprobado: false, trasladado: false, cajasTrasladadas: 0,
    },
    encargado: data.encargado ?? "",
    fechaVisita: data.fechaVisita ?? "",
    observaciones: data.observaciones ?? "",
    creadoEn: (data.creadoEn as Timestamp)?.toDate?.().toISOString() ?? "",
    actualizadoEn: (data.actualizadoEn as Timestamp)?.toDate?.().toISOString() ?? "",
  };
}

/** Misma correccion que en FirebaseRegistroPeriodoRepository: Firestore rechaza campos con
 *  valor undefined -- se limpia recursivamente antes de escribir. */
function limpiar<T extends Record<string, any>>(obj: T): T {
  const limpio: Record<string, any> = {};
  for (const [k, v] of Object.entries(obj)) {
    if (v === undefined) continue;
    limpio[k] = v && typeof v === "object" && !Array.isArray(v) ? limpiar(v) : v;
  }
  return limpio as T;
}

export class FirebasePQRSRepository implements IPQRSRepository {
  async listarPorUnidad(unidadOperativaId: string): Promise<PQRS[]> {
    const q = query(collection(db, PQRS_COLECCION), where("unidadOperativaId", "==", unidadOperativaId));
    const snap = await getDocs(q);
    return snap.docs.map((d) => fromFirestore(d.id, d.data()));
  }

  async guardar(p: Omit<PQRS, "id" | "creadoEn" | "actualizadoEn">): Promise<PQRS> {
    const ref = await addDoc(collection(db, PQRS_COLECCION), {
      ...limpiar(p),
      creadoEn: serverTimestamp(),
      actualizadoEn: serverTimestamp(),
    });
    return { ...p, id: ref.id, creadoEn: new Date().toISOString(), actualizadoEn: new Date().toISOString() };
  }

  async actualizar(id: string, cambios: Partial<PQRS>): Promise<void> {
    await updateDoc(doc(db, PQRS_COLECCION, id), { ...limpiar(cambios), actualizadoEn: serverTimestamp() });
  }
}
