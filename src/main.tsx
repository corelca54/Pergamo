import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import { FormularioVisita } from '@presentation/screens/FormularioVisita';
import { PQRSPage } from '@presentation/screens/PQRSPage';
import { AyudaDeMemoriaPage } from '@presentation/screens/AyudaDeMemoriaPage';
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
      <Navbar vista={vista} onCambiarVista={setVista} />

      <main className="mx-auto max-w-3xl px-4 pt-32 sm:pt-24">
        {vista === "captura" && <FormularioVisita />}
        {vista === "pqrs" && <PQRSPage />}
        {vista === "ayuda-memoria" && <AyudaDeMemoriaPage />}
        {vista === "tablero" && <TableroPage />}
      </main>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
