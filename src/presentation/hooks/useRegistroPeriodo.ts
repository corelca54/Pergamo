import { useState, useMemo } from "react";
import type { RegistroPeriodo } from "../../domain/entities/RegistroPeriodo";
import { RegistrarAvancePeriodo, type RegistrarAvanceInput } from "../../application/useCases/RegistrarAvancePeriodo";
import { FirebaseRegistroPeriodoRepository } from "../../infrastructure/repositories/FirebaseRegistroPeriodoRepository";

export const useRegistroPeriodo = () => {
  const [registros, setRegistros] = useState<RegistroPeriodo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const registrarAvancePeriodo = useMemo(() => {
    const repository = new FirebaseRegistroPeriodoRepository();
    return new RegistrarAvancePeriodo(repository);
  }, []);

  const registrar = async (input: RegistrarAvanceInput) => {
    setLoading(true);
    setError(null);
    try {
      const nuevo = await registrarAvancePeriodo.ejecutar(input);
      setRegistros((prev) => [nuevo, ...prev]);
      return nuevo;
    } catch (err: any) {
      setError(err.message || "Error al conectar con la base de datos");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { registros, loading, error, registrar };
};
