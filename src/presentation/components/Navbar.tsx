import { useEffect, useRef, useState } from "react";

export type Vista = "captura" | "pqrs" | "ayuda-memoria" | "directorio" | "tablero";

interface SubItem {
  vista: Vista;
  label: string;
  descripcion: string;
  disponible: boolean;
}

interface ItemMenu {
  id: string;
  label: string;
  submenus: SubItem[];
}

const MENU: ItemMenu[] = [
  {
    id: "captura",
    label: "Captura",
    submenus: [
      { vista: "captura", label: "Nueva visita", descripcion: "Registrar avance de una unidad operativa", disponible: true },
      { vista: "pqrs", label: "PQRS", descripcion: "Organización y traslado a Gestión Institucional", disponible: true },
      { vista: "ayuda-memoria", label: "Ayuda de memoria", descripcion: "Generar PDF con el formato GD-040", disponible: true },
    ],
  },
  {
    id: "directorio",
    label: "Directorio",
    submenus: [
      { vista: "directorio", label: "Catálogo de unidades", descripcion: "SLIS, CDC, Lavanderías, CIAM — importar y consultar", disponible: true },
    ],
  },
  {
    id: "tablero",
    label: "Tablero",
    submenus: [
      { vista: "tablero", label: "Resumen general", descripcion: "KPIs consolidados, igual que el Excel", disponible: true },
    ],
  },
];

function grupoDe(vista: Vista): string {
  return MENU.find((m) => m.submenus.some((s) => s.vista === vista))?.id ?? "captura";
}

export function Navbar({ vista, onCambiarVista }: { vista: Vista; onCambiarVista: (v: Vista) => void }) {
  const [abierto, setAbierto] = useState<string | null>(null);
  const contenedorRef = useRef<HTMLElement>(null);
  const grupoActivo = grupoDe(vista);

  // Cambiado de "abrir con onMouseEnter/cerrar con onMouseLeave" a "abrir/cerrar con clic" --
  // el hover tenia un hueco entre el boton y el desplegable donde el mouse podia disparar
  // mouseleave antes de que el clic en un submenu llegara a registrarse (por eso "no se
  // dejaban clickear"). Con clic no depende de mantener el mouse en una zona exacta, y de paso
  // funciona en pantallas tactiles, donde el hover no existe.
  useEffect(() => {
    function alClicFuera(e: MouseEvent) {
      if (contenedorRef.current && !contenedorRef.current.contains(e.target as Node)) {
        setAbierto(null);
      }
    }
    document.addEventListener("mousedown", alClicFuera);
    return () => document.removeEventListener("mousedown", alClicFuera);
  }, []);

  function seleccionarSubmenu(sub: SubItem) {
    if (!sub.disponible) return;
    onCambiarVista(sub.vista);
    setAbierto(null);
  }

  return (
    <header ref={contenedorRef} className="relative z-50">
      {/* Header en flujo normal (SIN position:fixed) -- el layout completo vive en main.tsx
          como un contenedor de altura fija con scroll interno, para que el header nunca se
          mueva sin depender de que "fixed" se comporte bien en cada navegador/entorno. */}
      <div className="banner-animado h-2 bg-gradient-to-r from-primary-700 via-accent-500 to-primary-700" />

      <div className="glass-card border-b border-white/40 shadow-sm">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3 sm:px-6">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-primary-700 to-primary-500 text-xl font-black text-white shadow-md">
              P
            </div>
            <div>
              <h1 className="text-lg font-bold leading-none text-primary-950 sm:text-xl">Pérgamo</h1>
              <p className="mt-0.5 text-[11px] font-medium text-slate-500 sm:text-xs">Sistema de Auditoría &amp; Gestión Documental</p>
            </div>
          </div>

          {/* Menu con submenus (desktop) -- clic para abrir/cerrar, no hover */}
          <nav className="hidden items-center gap-1 sm:flex">
            {MENU.map((item) => (
              <div key={item.id} className="relative">
                <button
                  onClick={() => setAbierto(abierto === item.id ? null : item.id)}
                  className={`flex items-center gap-1 rounded-lg px-3 py-2 text-sm font-semibold transition ${
                    grupoActivo === item.id ? "bg-primary-700 text-white" : "text-slate-700 hover:bg-primary-50"
                  }`}
                >
                  {item.label}
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"
                       className={`transition-transform ${abierto === item.id ? "rotate-180" : ""}`}>
                    <path d="M6 9l6 6 6-6" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </button>
                {abierto === item.id && (
                  <div className="absolute left-0 top-full w-72 pt-2">
                    <div className="glass-card overflow-hidden rounded-xl p-1.5 shadow-lg">
                      {item.submenus.map((sub) => (
                        <div
                          key={sub.vista}
                          className={`rounded-lg px-3 py-2 text-sm ${
                            sub.disponible ? "cursor-pointer hover:bg-primary-50" : "cursor-default opacity-50"
                          } ${vista === sub.vista ? "bg-primary-50" : ""}`}
                          onClick={() => seleccionarSubmenu(sub)}
                        >
                          <div className="flex items-center justify-between font-semibold text-slate-800">
                            {sub.label}
                            {!sub.disponible && (
                              <span className="rounded-full bg-slate-200 px-2 py-0.5 text-[10px] font-bold text-slate-500">
                                Próximamente
                              </span>
                            )}
                          </div>
                          <p className="mt-0.5 text-xs text-slate-500">{sub.descripcion}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </nav>

          <span className="hidden items-center gap-1.5 rounded-full border border-primary-200 bg-primary-100 px-3 py-1 text-xs font-semibold text-primary-800 sm:inline-flex">
            <span className="h-2 w-2 animate-pulse rounded-full bg-primary-500" />
            PWA Activa
          </span>
        </div>

        {/* Menu movil: acordeon simple */}
        <div className="flex flex-wrap gap-1 border-t border-white/40 px-4 py-2 sm:hidden">
          {MENU.flatMap((item) => item.submenus.filter((s) => s.disponible)).map((sub) => (
            <button
              key={sub.vista}
              onClick={() => onCambiarVista(sub.vista)}
              className={`rounded-lg px-2.5 py-1.5 text-xs font-semibold transition ${
                vista === sub.vista ? "bg-primary-700 text-white" : "bg-white/60 text-slate-700"
              }`}
            >
              {sub.label}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
}
