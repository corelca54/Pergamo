import { useEffect, useMemo, useState } from "react";
import { FirebaseRegistroPeriodoRepository } from "../../infrastructure/repositories/FirebaseRegistroPeriodoRepository";
import { FirebasePQRSRepository } from "../../infrastructure/repositories/FirebasePQRSRepository";
import { calcularResumenDashboard } from "../../application/services/CalcularResumenDashboard";
import type { ResumenDashboard } from "../../domain/repositories/IRegistroPeriodoRepository";

/** Trae TODOS los registros y PQRS, y calcula el resumen en el navegador -- ver la nota en
 *  CalcularResumenDashboard sobre por que no hay un documento pre-agregado (Firestore free
 *  tier no tiene Cloud Functions). Se puede llamar "refrescar" despues de cada captura nueva
 *  para que el Tablero se vea actualizado sin recargar la pagina entera. */
export function useTablero() {
  const [resumen, setResumen] = useState<ResumenDashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const repos = useMemo(() => ({
    registros: new FirebaseRegistroPeriodoRepository(),
    pqrs: new FirebasePQRSRepository(),
  }), []);

  async function refrescar() {
    setLoading(true);
    setError(null);
    try {
      const [registros, pqrs] = await Promise.all([
        repos.registros.listarTodos(),
        repos.pqrs.listarTodos(),
      ]);
      setResumen(calcularResumenDashboard(registros, pqrs));
    } catch (err: any) {
      setError(err.message || "No se pudo cargar el tablero.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refrescar();
  }, []);

  return { resumen, loading, error, refrescar };
}
