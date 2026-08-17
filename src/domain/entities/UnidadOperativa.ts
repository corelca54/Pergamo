// Entidad pura: sin dependencias de Firebase ni de React.
// Espejo del Directorio del Excel (Dependencia / Servicio / Subdireccion / Unidad + capacidad).

export type Dependencia = "SUBGIL" | "SUBICI" | "DT";

export interface CapacidadEstanteria {
  /** Medida directa con cinta metrica, si ya hay estanteria instalada. */
  metrosMedidos: number | null;
  /** Si el espacio esta vacio: largo x ancho del local, para que la calculadora estime cuanto
   *  cabria (regla AGN: ~3 metros lineales de estanteria por m2, estanteria fija de 2.20m). */
  largoEspacioM: number | null;
  anchoEspacioM: number | null;
}

export interface UnidadOperativa {
  id: string; // slug estable, ej. "subgil-cdc-kennedy-bellavista"
  dependencia: Dependencia;
  servicio: string; // "CDC" | "LAVANDERIAS COMUNITARIAS" | "EMERGENCIA SOCIAL" | "CIAM" | "SEGUIMIENTO SUBDIRECCION" | "NIVEL CENTRAL"
  subdireccionLocal: string;
  nombre: string;
  encargado?: string;
  capacidad: CapacidadEstanteria;
}

const AGN_M2_A_METROS_LINEALES = 3; // Acuerdo 049/2000 AGN: estanteria fija ~3 m lineales por m2
const CAJAS_POR_METRO_LINEAL = 4; // 4 cajas X-200 = 1 metro lineal de archivo

export function areaEspacioM2(u: Pick<UnidadOperativa, "capacidad">): number | null {
  const { largoEspacioM, anchoEspacioM } = u.capacidad;
  if (largoEspacioM == null || anchoEspacioM == null) return null;
  return largoEspacioM * anchoEspacioM;
}

export function capacidadPotencialEstimada(u: Pick<UnidadOperativa, "capacidad">): number | null {
  const area = areaEspacioM2(u);
  if (area == null) return null;
  return Math.floor(area * AGN_M2_A_METROS_LINEALES);
}

/** La medida directa manda; si no hay, cae a la calculadora (largo x ancho). */
export function capacidadEfectivaM(u: Pick<UnidadOperativa, "capacidad">): number {
  const { metrosMedidos } = u.capacidad;
  if (metrosMedidos && metrosMedidos > 0) return metrosMedidos;
  return capacidadPotencialEstimada(u) ?? 0;
}

export function metrosNecesarios(cajasVigentesTotalesUnidad: number): number {
  return Math.ceil(cajasVigentesTotalesUnidad / CAJAS_POR_METRO_LINEAL);
}

export type EstadoEspacio =
  | { tipo: "sin_dato" }
  | { tipo: "suficiente" }
  | { tipo: "insuficiente"; faltanM: number };

export function estadoEspacio(u: Pick<UnidadOperativa, "capacidad">, cajasVigentesTotalesUnidad: number): EstadoEspacio {
  const capacidad = capacidadEfectivaM(u);
  if (capacidad === 0) return { tipo: "sin_dato" };
  const necesarios = metrosNecesarios(cajasVigentesTotalesUnidad);
  if (necesarios <= capacidad) return { tipo: "suficiente" };
  return { tipo: "insuficiente", faltanM: necesarios - capacidad };
}
