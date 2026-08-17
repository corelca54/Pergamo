import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import { FormularioVisita } from '@presentation/screens/FormularioVisita';
import { TableroPage } from '@presentation/screens/TableroPage';
import { Navbar } from '@presentation/components/Navbar';
import type { Vista } from '@presentation/components/Navbar';
// @ts-ignore
import './index.css';

function App() {
  const [vista, setVista] = useState<Vista>("captura");

  return (
    <div className="min-h-screen bg-documental-pattern text-slate-900 pb-16">
      <div className="estanteria-ilustracion" aria-hidden="true" />
      {/* Header FIJO arriba (position: fixed, no "sticky"). La causa real de que antes no se
          quedara fijo era "overflow-x: hidden" en .bg-documental-pattern -- eso crea un
          contenedor de scroll propio en algunos navegadores que rompe el fixed. Ya se quito
          (ver index.css), asi que esta vez si se queda en su sitio de verdad. */}
      <Navbar vista={vista} onCambiarVista={setVista} />

      <main className="mx-auto max-w-3xl px-4 pt-32 sm:pt-24">
        {vista === "captura" ? <FormularioVisita /> : <TableroPage />}
      </main>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
