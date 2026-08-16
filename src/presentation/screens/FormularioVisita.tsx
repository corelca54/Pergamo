import React, { useState } from 'react';
import { useVisitas } from '@presentation/hooks/useVisitas';
import { VisitaAuditoria, DetalleFondo } from '@domain/entities/VisitaAuditoria';

export const FormularioVisita = () => {
  const { registrarVisita, loading, error, visitas } = useVisitas();
  
  const [idCDC, setIdCDC] = useState('');
  const [localidad, setLocalidad] = useState('');

  const [ubicacion, setUbicacion] = useState<'CDC' | 'Lavandería'>('CDC');
  const [versionTRD, setVersionTRD] = useState('');
  const [cajas, setCajas] = useState(0);
  const [carpetas, setCarpetas] = useState(0);

  const [detalles, setDetalles] = useState<DetalleFondo[]>([]);

  const agregarDetalle = () => {
    if (!versionTRD || cajas <= 0 || carpetas <= 0) {
      alert('Por favor completa la versión TRD y pon valores mayores a cero.');
      return;
    }
    
    const nuevoDetalle: DetalleFondo = { ubicacion, versionTRD, cajas, carpetas };
    setDetalles([...detalles, nuevoDetalle]);
    
    setVersionTRD('');
    setCajas(0);
    setCarpetas(0);
  };

  const eliminarDetalle = (index: number) => {
    setDetalles(detalles.filter((_, i) => i !== index));
  };

  const granTotalCajas = detalles.reduce((acc, det) => acc + det.cajas, 0);
  const granTotalCarpetas = detalles.reduce((acc, det) => acc + det.carpetas, 0);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (detalles.length === 0) {
      alert('Debes agregar al menos un registro de cajas antes de guardar.');
      return;
    }

    const nuevaVisita: Omit<VisitaAuditoria, 'idVisita'> = {
      fecha: new Date(),
      idCDC,
      localidad,
      tipoVisita: 'Diagnóstico',
      tema: 'Revisión de Tablas de Retención Documental',
      metricas: {
        detallesFondo: detalles,
        granTotalCajas,
        granTotalCarpetas,
        procesosEliminacion: 0,
        transferencias: 0,
        procesosFDA: 0,
        porcentajeCumplimiento: 100
      },
      desarrolloCualitativo: 'Registro inicial desde PWA',
      compromisos: [],
      asistentes: [],
      estado: 'Borrador'
    };

    await registrarVisita(nuevaVisita);
    
    setIdCDC('');
    setLocalidad('');
    setDetalles([]);
  };

  return (
    <div className="space-y-6">
      <div className="glass-card rounded-2xl shadow-xl border border-stone-200/80 overflow-hidden transition-all">
        
        {/* Encabezado con degradado verde forestal */}
        <div className="bg-gradient-to-r from-primary-900 via-primary-800 to-primary-700 px-6 py-5 text-white">
          <h2 className="text-xl font-bold tracking-tight flex items-center gap-2">
            📄 Registrar Nueva Visita de Auditoría
          </h2>
          <p className="text-primary-100/80 text-xs mt-1">Levantamiento de inventario documental en centro operativo</p>
        </div>

        <div className="p-6 md:p-8 space-y-6">
          {error && (
            <div className="p-4 bg-red-50 border-l-4 border-danger text-danger text-sm rounded-r-lg font-medium">
              ⚠️ {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* 1. Información del Centro */}
            <div className="bg-white/70 p-5 rounded-xl border border-stone-200/80 shadow-sm space-y-4">
              <h3 className="text-sm font-bold text-primary-900 uppercase tracking-wider flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-primary-600"></span> 
                1. Datos del Centro
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-stone-700 mb-1">ID del Centro (CDC)</label>
                  <input 
                    type="text" 
                    value={idCDC} 
                    onChange={(e) => setIdCDC(e.target.value)} 
                    required 
                    className="w-full px-3.5 py-2.5 border border-stone-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all bg-white text-sm"
                    placeholder="Ej. CDC Porvenir"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-stone-700 mb-1">Localidad</label>
                  <input 
                    type="text" 
                    value={localidad} 
                    onChange={(e) => setLocalidad(e.target.value)} 
                    required 
                    className="w-full px-3.5 py-2.5 border border-stone-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all bg-white text-sm"
                    placeholder="Ej. Bosa"
                  />
                </div>
              </div>
            </div>

            {/* 2. Captura Dinámica de Cajas y TRD */}
            <div className="bg-primary-50/50 p-5 rounded-xl border border-primary-200/80 shadow-sm space-y-4">
              <h3 className="text-sm font-bold text-primary-950 uppercase tracking-wider flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-primary-600"></span> 
                2. Captura de Cajas y Carpetas por TRD
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-stone-700 mb-1">Ubicación Física</label>
                  <select 
                    value={ubicacion} 
                    onChange={(e) => setUbicacion(e.target.value as 'CDC' | 'Lavandería')}
                    className="w-full px-3.5 py-2.5 border border-stone-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none bg-white text-sm"
                  >
                    <option value="CDC">Área Administrativa (CDC)</option>
                    <option value="Lavandería">Lavandería Comunitaria</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-stone-700 mb-1">Versión TRD</label>
                  <input 
                    type="text" 
                    value={versionTRD} 
                    onChange={(e) => setVersionTRD(e.target.value)}
                    className="w-full px-3.5 py-2.5 border border-stone-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none bg-white text-sm"
                    placeholder="Ej. TRD Versión 1"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-stone-700 mb-1">Cantidad de Cajas</label>
                  <input 
                    type="number" 
                    value={cajas} 
                    onChange={(e) => setCajas(Number(e.target.value))} 
                    min="0"
                    className="w-full px-3.5 py-2.5 border border-stone-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none bg-white text-sm"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-stone-700 mb-1">Cantidad de Carpetas</label>
                  <input 
                    type="number" 
                    value={carpetas} 
                    onChange={(e) => setCarpetas(Number(e.target.value))} 
                    min="0"
                    className="w-full px-3.5 py-2.5 border border-stone-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none bg-white text-sm"
                  />
                </div>
              </div>

              <button 
                type="button" 
                onClick={agregarDetalle}
                className="w-full bg-primary-600 hover:bg-primary-700 text-white font-semibold py-2.5 px-4 rounded-lg transition-all shadow-sm hover:shadow active:scale-[0.99] flex justify-center items-center gap-2 text-sm"
              >
                <span>+</span> Añadir Lote al Listado
              </button>
            </div>

            {/* 3. Lotes Registrados en la Sesión */}
            {detalles.length > 0 && (
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-stone-500 uppercase tracking-wider">Lotes vinculados a la visita</h4>
                <div className="space-y-2">
                  {detalles.map((det, index) => (
                    <div key={index} className="flex justify-between items-center bg-white border border-stone-200 p-3.5 rounded-xl shadow-xs hover:border-primary-300 transition-colors">
                      <div className="text-xs">
                        <span className="font-bold text-stone-900">{det.ubicacion}</span> 
                        <span className="text-stone-500 ml-2">| {det.versionTRD}</span>
                        <div className="text-stone-600 mt-0.5">📦 {det.cajas} cajas / 📁 {det.carpetas} carpetas</div>
                      </div>
                      <button 
                        type="button" 
                        onClick={() => eliminarDetalle(index)}
                        className="text-red-600 hover:text-red-800 hover:bg-red-50 px-2.5 py-1 rounded-md text-xs font-semibold transition-colors"
                      >
                        Eliminar
                      </button>
                    </div>
                  ))}
                </div>
                
                <div className="flex justify-between items-center bg-primary-100/60 p-3.5 rounded-xl border border-primary-200 text-xs">
                  <span className="font-semibold text-primary-950">Gran Total Consolidado:</span>
                  <span className="font-bold text-primary-800 text-sm">{granTotalCajas} cajas • {granTotalCarpetas} carpetas</span>
                </div>
              </div>
            )}

            <button 
              type="submit" 
              disabled={loading}
              className={`w-full font-bold py-3.5 px-4 rounded-xl transition-all shadow-md active:scale-[0.99] ${
                loading ? 'bg-stone-400 cursor-not-allowed' : 'bg-gradient-to-r from-primary-700 to-primary-600 hover:from-primary-800 hover:to-primary-700 text-white shadow-primary-900/10'
              }`}
            >
              {loading ? 'Guardando Registro...' : 'Guardar Visita Completa'}
            </button>
          </form>
        </div>
      </div>

      {/* Historial en Memoria */}
      {visitas.length > 0 && (
        <div className="space-y-3 pt-4">
          <h3 className="text-md font-bold text-stone-900">Historial Registrado en Sesión</h3>
          <div className="space-y-3">
            {visitas.map((v, index) => (
              <div key={index} className="glass-card p-4 rounded-xl border border-stone-200 shadow-xs flex justify-between items-center">
                <div>
                  <h4 className="font-bold text-sm text-stone-900">{v.idVisita} - {v.localidad}</h4>
                  <p className="text-xs text-stone-500">CDC: {v.idCDC} • {v.metricas.granTotalCajas} Cajas / {v.metricas.granTotalCarpetas} Carpetas</p>
                </div>
                <span className="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-2.5 py-1 rounded-full border border-emerald-200">
                  {v.estado}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};