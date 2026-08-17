import { useEffect, useMemo, useState } from "react";
import { FirebaseRegistroPeriodoRepository } from "../../infrastructure/repositories/FirebaseRegistroPeriodoRepository";
import { FirebasePQRSRepository } from "../../infrastructure/repositories/FirebasePQRSRepository";
import { FirebaseUnidadOperativaRepository } from "../../infrastructure/repositories/FirebaseUnidadOperativaRepository";
import { calcularResumenDashboard } from "../../application/services/CalcularResumenDashboard";
import type { FiltrosTablero } from "../../application/services/CalcularResumenDashboard";
import type { RegistroPeriodo } from "../../domain/entities/RegistroPeriodo";
import type { PQRS } from "../../domain/entities/PQRS";
import type { UnidadOperativa } from "../../domain/entities/UnidadOperativa";

/** Trae TODO una sola vez (registros, PQRS, Directorio) y lo deja en memoria -- filtrar despues
 *  es instantaneo (recalculo local con useMemo), sin volver a consultar Firestore cada vez que
 *  alguien cambia un filtro. Los 4 filtros son EXACTAMENTE los mismos del Excel, combinables. */
export function useTablero(filtros: FiltrosTablero) {
  const [registros, setRegistros] = useState<RegistroPeriodo[]>([]);
  const [pqrs, setPqrs] = useState<PQRS[]>([]);
  const [unidades, setUnidades] = useState<UnidadOperativa[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const repos = useMemo(() => ({
    registros: new FirebaseRegistroPeriodoRepository(),
    pqrs: new FirebasePQRSRepository(),
    directorio: new FirebaseUnidadOperativaRepository(),
  }), []);

  async function refrescar() {
    setLoading(true);
    setError(null);
    try {
      const [r, p, u] = await Promise.all([
        repos.registros.listarTodos(),
        repos.pqrs.listarTodos(),
        repos.directorio.listarTodas(),
      ]);
      setRegistros(r); setPqrs(p); setUnidades(u);
    } catch (err: any) {
      setError(err.message || "No se pudo cargar el tablero.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { refrescar(); }, []);

  const resumen = useMemo(
    () => calcularResumenDashboard(registros, pqrs, unidades, filtros),
    [registros, pqrs, unidades, filtros]
  );

  return { resumen, unidades, loading, error, refrescar };
}
