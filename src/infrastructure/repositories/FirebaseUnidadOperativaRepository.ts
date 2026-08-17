import { collection, doc, addDoc, updateDoc, getDoc, getDocs, query, where, writeBatch } from "firebase/firestore";
import { db } from "../config/firebase";
import type { UnidadOperativa } from "../../domain/entities/UnidadOperativa";
import type { IUnidadOperativaRepository } from "../../domain/repositories/IUnidadOperativaRepository";

const COLECCION = "unidadesOperativas";

function fromFirestore(id: string, data: any): UnidadOperativa {
  return {
    id,
    dependencia: data.dependencia,
    servicio: data.servicio,
    subdireccionLocal: data.subdireccionLocal,
    nombre: data.nombre,
    encargado: data.encargado ?? "",
    capacidad: data.capacidad ?? { metrosMedidos: null, largoEspacioM: null, anchoEspacioM: null },
  };
}

/** Misma correccion que ya se aplico en FirebaseRegistroPeriodoRepository y
 *  FirebasePQRSRepository: Firestore rechaza CUALQUIER campo con valor undefined (el error
 *  "WriteBatch.set() called with invalid data" que se vio al importar el CSV real -- muchas
 *  unidades no tienen Encargado, y ese campo quedaba en undefined). Se limpia recursivamente
 *  antes de cada escritura, para que este bug no vuelva a aparecer en ningun repositorio. */
function limpiar<T extends Record<string, any>>(obj: T): T {
  const limpio: Record<string, any> = {};
  for (const [k, v] of Object.entries(obj)) {
    if (v === undefined) continue;
    limpio[k] = v && typeof v === "object" && !Array.isArray(v) ? limpiar(v) : v;
  }
  return limpio as T;
}

export class FirebaseUnidadOperativaRepository implements IUnidadOperativaRepository {
  async listarTodas(): Promise<UnidadOperativa[]> {
    const snap = await getDocs(collection(db, COLECCION));
    return snap.docs.map((d) => fromFirestore(d.id, d.data()));
  }

  async listarPorSubdireccion(subdireccionLocal: string): Promise<UnidadOperativa[]> {
    const q = query(collection(db, COLECCION), where("subdireccionLocal", "==", subdireccionLocal));
    const snap = await getDocs(q);
    return snap.docs.map((d) => fromFirestore(d.id, d.data()));
  }

  async obtenerPorId(id: string): Promise<UnidadOperativa | null> {
    const snap = await getDoc(doc(db, COLECCION, id));
    return snap.exists() ? fromFirestore(snap.id, snap.data()) : null;
  }

  async guardar(u: Omit<UnidadOperativa, "id">): Promise<UnidadOperativa> {
    const ref = await addDoc(collection(db, COLECCION), limpiar(u));
    return { ...u, id: ref.id };
  }

  async actualizar(id: string, cambios: Partial<UnidadOperativa>): Promise<void> {
    await updateDoc(doc(db, COLECCION, id), limpiar(cambios));
  }

  /** Escribe en lotes de 500 (limite de Firestore por batch) -- para importar el Directorio
   *  completo del Excel de una sola vez sin agotar la cuota con cientos de escrituras sueltas. */
  async importarLote(unidades: Array<Omit<UnidadOperativa, "id">>): Promise<number> {
    let escritas = 0;
    for (let i = 0; i < unidades.length; i += 500) {
      const lote = unidades.slice(i, i + 500);
      const batch = writeBatch(db);
      for (const u of lote) {
        const ref = doc(collection(db, COLECCION));
        batch.set(ref, limpiar(u));
      }
      await batch.commit();
      escritas += lote.length;
    }
    return escritas;
  }
}
