import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import { FormularioVisita } from '@presentation/screens/FormularioVisita';
import { PQRSPage } from '@presentation/screens/PQRSPage';
import { AyudaDeMemoriaPage } from '@presentation/screens/AyudaDeMemoriaPage';
import { DirectorioPage } from '@presentation/screens/DirectorioPage';
import { TableroPage } from '@presentation/screens/TableroPage';
import { Navbar } from '@presentation/components/Navbar';
import type { Vista } from '@presentation/components/Navbar';
// @ts-ignore
import './index.css';

function App() {
  const [vista, setVista] = useState<Vista>("captura");

  return (
    // h-screen + overflow-hidden en el contenedor raiz: el PAGE (html/body) nunca hace scroll.
    // flex-col: el header ocupa lo que necesite arriba, y el area de abajo se reparte el resto
    // del alto con flex-1 -- solo ESA area interna hace scroll (overflow-y-auto). Asi el header
    // queda fisicamente fuera de lo que se desplaza, sin depender de position:fixed.
    <div className="flex h-screen flex-col overflow-hidden bg-documental-pattern text-slate-900">
      <div className="estanteria-ilustracion" aria-hidden="true" />
      <Navbar vista={vista} onCambiarVista={setVista} />

      <div className="contenido-con-scroll flex-1 overflow-y-auto">
        <main className="mx-auto max-w-3xl px-4 py-6">
          {vista === "captura" && <FormularioVisita />}
          {vista === "pqrs" && <PQRSPage />}
          {vista === "ayuda-memoria" && <AyudaDeMemoriaPage />}
          {vista === "directorio" && <DirectorioPage />}
          {vista === "tablero" && <TableroPage />}
        </main>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
