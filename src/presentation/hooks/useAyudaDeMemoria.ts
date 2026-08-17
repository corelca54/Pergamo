import { useMemo, useState } from "react";
import type { AyudaDeMemoria } from "../../domain/entities/AyudaDeMemoria";
import { validarAyudaDeMemoria } from "../../domain/entities/AyudaDeMemoria";
import { JsPDFExportadorReportes } from "../../infrastructure/services/JsPDFExportadorReportes";

export const useAyudaDeMemoria = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const exportador = useMemo(() => new JsPDFExportadorReportes(), []);

  const generarPDF = async (datos: Omit<AyudaDeMemoria, "id" | "creadoEn">) => {
    setError(null);
    const errores = validarAyudaDeMemoria(datos);
    if (errores.length > 0) {
      setError(errores.join(" "));
      throw new Error(errores.join(" "));
    }
    setLoading(true);
    try {
      const completa: AyudaDeMemoria = { ...datos, id: "", creadoEn: new Date().toISOString() };
      const blob = await exportador.generarAyudaDeMemoria(completa);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `ayuda-de-memoria-${datos.fecha || "sin-fecha"}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } finally {
      setLoading(false);
    }
  };

  return { generarPDF, loading, error };
};
