import { useState, useMemo } from "react";
import type { PQRS } from "../../domain/entities/PQRS";
import { RegistrarPQRS, type RegistrarPQRSInput } from "../../application/useCases/RegistrarPQRS";
import { FirebasePQRSRepository } from "../../infrastructure/repositories/FirebasePQRSRepository";

export const usePQRS = () => {
  const [items, setItems] = useState<PQRS[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const registrarPQRS = useMemo(() => {
    const repository = new FirebasePQRSRepository();
    return new RegistrarPQRS(repository);
  }, []);

  const registrar = async (input: RegistrarPQRSInput) => {
    setLoading(true);
    setError(null);
    try {
      const nuevo = await registrarPQRS.ejecutar(input);
      setItems((prev) => [nuevo, ...prev]);
      return nuevo;
    } catch (err: any) {
      setError(err.message || "Error al conectar con la base de datos");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { items, loading, error, registrar };
};
