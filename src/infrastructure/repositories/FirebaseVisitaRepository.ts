import { db } from '../config/firebase';
import { collection, addDoc, getDocs, query, orderBy } from 'firebase/firestore';
import { VisitaAuditoria } from '../../domain/entities/VisitaAuditoria';
import { IVisitaRepository } from '../../domain/repositories/IVisitaRepository';

export class FirebaseVisitaRepository implements IVisitaRepository {
  private collectionName = 'visitas';

  async guardar(visita: Omit<VisitaAuditoria, 'idVisita'>): Promise<VisitaAuditoria> {
    // Convierte la fecha a string ISO de forma segura (sea tipo Date o string)
    const fechaString =
      visita.fecha instanceof Date
        ? visita.fecha.toISOString()
        : new Date(visita.fecha).toISOString();

    const docRef = await addDoc(collection(db, this.collectionName), {
      ...visita,
      fecha: fechaString
    });

    return {
      ...visita,
      idVisita: docRef.id
    };
  }

  async obtenerTodas(): Promise<VisitaAuditoria[]> {
    const q = query(collection(db, this.collectionName), orderBy('fecha', 'desc'));
    const querySnapshot = await getDocs(q);

    return querySnapshot.docs.map((doc) => {
      const data = doc.data();
      return {
        ...data,
        idVisita: doc.id,
        fecha: new Date(data.fecha)
      } as VisitaAuditoria;
    });
  }
}