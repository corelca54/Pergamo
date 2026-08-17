import { useEffect, useMemo, useState } from "react";
import type { UnidadOperativa } from "../../domain/entities/UnidadOperativa";
import { FirebaseUnidadOperativaRepository } from "../../infrastructure/repositories/FirebaseUnidadOperativaRepository";

/** Trae el catalogo completo de unidades operativas (el "Directorio") una sola vez y lo deja en
 *  memoria -- se usa para armar los selectores en cascada Subdireccion -> Servicio -> Unidad en
 *  toda la app, sin repetir la consulta a Firestore en cada pantalla. */
export function useDirectorio() {
  const [unidades, setUnidades] = useState<UnidadOperativa[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const repo = useMemo(() => new FirebaseUnidadOperativaRepository(), []);

  async function recargar() {
    setLoading(true);
    setError(null);
    try {
      setUnidades(await repo.listarTodas());
    } catch (err: any) {
      setError(err.message || "No se pudo cargar el Directorio.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { recargar(); }, []);

  const subdirecciones = useMemo(
    () => Array.from(new Set(unidades.map((u) => u.subdireccionLocal))).sort(),
    [unidades]
  );

  function serviciosDe(subdireccionLocal: string) {
    return Array.from(new Set(unidades.filter((u) => u.subdireccionLocal === subdireccionLocal).map((u) => u.servicio))).sort();
  }

  function unidadesDe(subdireccionLocal: string, servicio: string) {
    return unidades.filter((u) => u.subdireccionLocal === subdireccionLocal && u.servicio === servicio);
  }

  return { unidades, subdirecciones, serviciosDe, unidadesDe, loading, error, recargar, repo };
}
