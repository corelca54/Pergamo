import { useState } from "react";

export type Vista = "captura" | "tablero";

interface ItemMenu {
  id: Vista;
  label: string;
  submenus: Array<{ label: string; descripcion: string; disponible: boolean }>;
}

const MENU: ItemMenu[] = [
  {
    id: "captura",
    label: "Captura",
    submenus: [
      { label: "Nueva visita", descripcion: "Registrar avance de una unidad operativa", disponible: true },
      { label: "Historial de visitas", descripcion: "Ver capturas anteriores por unidad", disponible: false },
    ],
  },
  {
    id: "tablero",
    label: "Tablero",
    submenus: [
      { label: "Resumen general", descripcion: "KPIs consolidados, igual que el Excel", disponible: false },
      { label: "Por Subdirección", descripcion: "Desglose SLIS, sobreapilamiento, avance", disponible: false },
      { label: "Por Unidad Operativa", descripcion: "Detalle unidad por unidad", disponible: false },
    ],
  },
];

export function Navbar({ vista, onCambiarVista }: { vista: Vista; onCambiarVista: (v: Vista) => void }) {
  const [abierto, setAbierto] = useState<Vista | null>(null);

  return (
    <header className="fixed inset-x-0 top-0 z-50">
      {/* Banner superior: franja institucional alusiva a gestion documental. Texto mas corto
          en movil -- el completo no cabe en una linea y se veia cortado feo. */}
      <div className="bg-gradient-to-r from-primary-900 via-primary-800 to-primary-700 text-primary-50">
        <div className="mx-auto flex max-w-5xl items-center justify-center gap-2 px-4 py-1.5 text-xs font-medium tracking-wide">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="shrink-0 opacity-80">
            <path d="M4 4h16v16H4z" strokeLinejoin="round" />
            <path d="M4 9h16M9 4v16" />
          </svg>
          <span className="hidden sm:inline">Trazabilidad TRD de principio a fin — de la visita en sitio al tablero de la Dirección</span>
          <span className="sm:hidden">Trazabilidad TRD, de la visita al tablero</span>
        </div>
      </div>

      {/* Barra principal */}
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

          {/* Menu con submenus (desktop) */}
          <nav className="hidden items-center gap-1 sm:flex">
            {MENU.map((item) => (
              <div
                key={item.id}
                className="relative"
                onMouseEnter={() => setAbierto(item.id)}
                onMouseLeave={() => setAbierto(null)}
              >
                <button
                  onClick={() => onCambiarVista(item.id)}
                  className={`rounded-lg px-3 py-2 text-sm font-semibold transition ${
                    vista === item.id ? "bg-primary-700 text-white" : "text-slate-700 hover:bg-primary-50"
                  }`}
                >
                  {item.label}
                </button>
                {abierto === item.id && (
                  <div className="absolute left-0 top-full w-72 pt-2">
                    <div className="glass-card overflow-hidden rounded-xl p-1.5 shadow-lg">
                      {item.submenus.map((sub) => (
                        <div
                          key={sub.label}
                          className={`rounded-lg px-3 py-2 text-sm ${
                            sub.disponible ? "cursor-pointer hover:bg-primary-50" : "cursor-default opacity-50"
                          }`}
                          onClick={() => sub.disponible && onCambiarVista(item.id)}
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

        {/* Menu movil: simple, sin submenus desplegables (mas facil de tocar en celular) */}
        <div className="flex gap-1 border-t border-white/40 px-4 py-2 sm:hidden">
          {MENU.map((item) => (
            <button
              key={item.id}
              onClick={() => onCambiarVista(item.id)}
              className={`flex-1 rounded-lg py-2 text-sm font-semibold transition ${
                vista === item.id ? "bg-primary-700 text-white" : "text-slate-700"
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
}
