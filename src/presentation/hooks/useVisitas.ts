import { useState, useMemo } from 'react';
import { VisitaAuditoria } from '../../domain/entities/VisitaAuditoria';
import { CrearVisitaUseCase } from '../../application/useCases/CrearVisitaUseCase';
import { FirebaseVisitaRepository } from '../../infrastructure/repositories/FirebaseVisitaRepository';

export const useVisitas = () => {
  const [visitas, setVisitas] = useState<VisitaAuditoria[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Instanciamos el repositorio real de Firebase
  const crearVisitaUseCase = useMemo(() => {
    const repository = new FirebaseVisitaRepository();
    return new CrearVisitaUseCase(repository);
  }, []);

  const registrarVisita = async (datosVisita: Omit<VisitaAuditoria, 'idVisita'>) => {
    setLoading(true);
    setError(null);
    try {
      const nuevaVisita = await crearVisitaUseCase.ejecutar(datosVisita);
      setVisitas((prev) => [nuevaVisita, ...prev]);
      alert('¡Visita registrada con éxito en Firestore!');
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Error al conectar con la base de datos');
      alert(`Error: ${err.message || 'No se pudo guardar la visita'}`);
    } finally {
      setLoading(false);
    }
  };

  return {
    visitas,
    loading,
    error,
    registrarVisita
  };
};