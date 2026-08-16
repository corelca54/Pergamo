import React from 'react';
import ReactDOM from 'react-dom/client';
import { FormularioVisita } from '@presentation/screens/FormularioVisita';
// @ts-ignore
import './index.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <div className="min-h-screen bg-documental-pattern text-stone-900 pb-16">
      {/* Navbar Superior Institucional */}
      <header className="glass-card border-b border-stone-200/80 sticky top-0 z-50 mb-8 shadow-sm">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-primary-700 to-primary-500 flex items-center justify-center text-white font-black text-xl shadow-md">
              P
            </div>
            <div>
              <h1 className="text-xl font-bold text-primary-950 leading-none">Pérgamo</h1>
              <p className="text-xs text-stone-500 font-medium mt-0.5">Sistema de Auditoría & Gestión Documental</p>
            </div>
          </div>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-primary-100 text-primary-800 border border-primary-200">
            <span className="w-2 h-2 rounded-full bg-primary-500 animate-pulse"></span>
            PWA Activa
          </span>
        </div>
      </header>

      {/* Formulario Principal */}
      <main className="max-w-3xl mx-auto px-4">
        <FormularioVisita />
      </main>
    </div>
  </React.StrictMode>
);