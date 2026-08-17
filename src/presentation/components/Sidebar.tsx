import { useState, type ReactNode } from "react";
import type { Vista } from "./Navbar";

interface ItemNav {
  id: Vista;
  label: string;
  icono: ReactNode;
  submenus: Array<{ label: string; descripcion: string; disponible: boolean }>;
}

const iconoCaptura = (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 20h9" /><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z" />
  </svg>
);
const iconoTablero = (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="2" /><path d="M9 3v18M3 9h6" />
  </svg>
);

const NAV: ItemNav[] = [
  {
    id: "captura", label: "Captura", icono: iconoCaptura,
    submenus: [
      { label: "Nueva visita", descripcion: "Registrar avance de una unidad operativa", disponible: true },
      { label: "Historial de visitas", descripcion: "Ver capturas anteriores por unidad", disponible: false },
    ],
  },
  {
    id: "tablero", label: "Tablero", icono: iconoTablero,
    submenus: [
      { label: "Resumen general", descripcion: "KPIs consolidados, igual que el Excel", disponible: false },
      { label: "Por Subdirección", descripcion: "Desglose SLIS, sobreapilamiento, avance", disponible: false },
      { label: "Por Unidad Operativa", descripcion: "Detalle unidad por unidad", disponible: false },
    ],
  },
];

/** Sidebar fijo estilo Canva: barra vertical de iconos a la izquierda, siempre en su sitio
 *  (position: fixed, left:0, alto completo). Estructuralmente mucho mas simple que un header de
 *  2 pisos -- un solo elemento fijo, sin banners apilados -- por eso es mas dificil que un bug
 *  de CSS lo desalinee. En movil se colapsa a una barra inferior (mismo patron que apps como
 *  Instagram/Notion en celular). */
export function Sidebar({ vista, onCambiarVista }: { vista: Vista; onCambiarVista: (v: Vista) => void }) {
  const [abierto, setAbierto] = useState<Vista | null>(null);

  return (
    <>
      {/* Desktop: columna fija a la izquierda -- mas compacta: los botones son cuadrados
          ajustados al icono (no bloques que estiran todo el ancho), con un divisor bajo el
          logo y un icono de ayuda anclado abajo para que el sidebar no se sienta vacio. */}
      <aside className="fixed inset-y-0 left-0 z-50 hidden w-[72px] flex-col items-center bg-archivo-900 sm:flex">
        <div className="flex h-16 w-full items-center justify-center">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary-600 text-sm font-black text-white">
            P
          </div>
        </div>
        <div className="mx-3 h-px w-8 bg-white/10" />

        <nav className="flex flex-1 flex-col items-center gap-2 pt-4">
          {NAV.map((item) => (
            <div
              key={item.id}
              className="group relative"
              onMouseEnter={() => setAbierto(item.id)}
              onMouseLeave={() => setAbierto(null)}
            >
              <button
                onClick={() => onCambiarVista(item.id)}
                className={`flex h-11 w-11 items-center justify-center rounded-xl transition ${
                  vista === item.id
                    ? "bg-primary-600 text-white shadow-md shadow-primary-900/40"
                    : "text-slate-400 hover:bg-white/[0.06] hover:text-white"
                }`}
                title={item.label}
              >
                {item.icono}
              </button>
              <p className={`mt-1 text-center text-[10px] font-semibold ${vista === item.id ? "text-white" : "text-slate-500"}`}>
                {item.label}
              </p>

              {abierto === item.id && (
                <div className="absolute left-full top-0 z-10 pl-2">
                  <div className="glass-card w-64 overflow-hidden rounded-xl p-1.5 shadow-lg">
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

        {/* Ancla la parte inferior -- evita el vacio que se veia antes bajo el menu */}
        <div className="flex flex-col items-center gap-3 pb-4">
          <button className="flex h-9 w-9 items-center justify-center rounded-full text-slate-500 transition hover:bg-white/[0.06] hover:text-white" title="Ayuda">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" /><path d="M9.5 9a2.5 2.5 0 0 1 4.9.8c0 1.7-2.4 1.9-2.4 3.4" /><path d="M12 17.5v.01" />
            </svg>
          </button>
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-accent-600 text-xs font-bold text-white" title="Elmer Cabrera">
            EC
          </div>
        </div>
      </aside>

      {/* Movil: barra fija abajo */}
      <nav className="fixed inset-x-0 bottom-0 z-50 flex border-t border-white/50 bg-white/85 backdrop-blur-xl sm:hidden">
        {NAV.map((item) => (
          <button
            key={item.id}
            onClick={() => onCambiarVista(item.id)}
            className={`flex flex-1 flex-col items-center gap-0.5 py-2.5 text-[11px] font-semibold transition ${
              vista === item.id ? "text-primary-700" : "text-slate-500"
            }`}
          >
            {item.icono}
            {item.label}
          </button>
        ))}
      </nav>
    </>
  );
}
