// Placeholder honesto de la Fase 3 (Dashboard). Estructuralmente ya vive donde debe -- dentro
// del menu "Tablero" -- para que cuando se conecte a Firestore (leyendo el documento agregado
// ResumenDashboard), solo haga falta reemplazar el contenido de este componente, no rearmar
// la navegacion.
export function TableroPage() {
  return (
    <div className="space-y-5 pb-10">
      <div>
        <p className="text-xs font-bold uppercase tracking-widest text-primary-600">Tablero</p>
        <h1 className="mt-1 text-2xl font-bold text-slate-900">Resumen general</h1>
        <p className="mt-1 text-sm text-slate-500">
          Esta pantalla va a mostrar, en vivo, lo mismo que el Excel: KPIs, desglose por Subdirección y por
          Unidad Operativa -- alimentado directamente por lo que se capture en "Captura".
        </p>
      </div>

      <section className="glass-card rounded-2xl p-8 text-center">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-100">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#7D4E14" strokeWidth="1.8">
            <path d="M4 19V5a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v14" strokeLinecap="round" />
            <path d="M8 19v-6M12 19v-9M16 19v-3" strokeLinecap="round" />
          </svg>
        </div>
        <p className="text-base font-semibold text-slate-800">Todavía no hay datos conectados aquí</p>
        <p className="mx-auto mt-1.5 max-w-md text-sm text-slate-500">
          Esta vista se construye en el siguiente paso: leerá en tiempo real el resumen agregado de Firestore
          y lo pintará igual que el Excel -- KPIs, semáforo, desglose por Subdirección.
        </p>
      </section>
    </div>
  );
}
