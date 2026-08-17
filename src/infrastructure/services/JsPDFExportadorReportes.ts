// Implementacion CONCRETA del contrato IExportadorReportes usando jsPDF + jspdf-autotable +
// xlsx. Esta es la UNICA clase del proyecto que sabe que existen esas librerias especificas --
// si mañana se cambia de libreria, solo se toca este archivo.
//
// Requiere instalar las dependencias primero:
//   npm install xlsx jspdf jspdf-autotable
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import * as XLSX from "xlsx";
import type { RegistroPeriodo } from "../../domain/entities/RegistroPeriodo";
import { calcularAvanceTotal, cajasVigentes } from "../../domain/entities/RegistroPeriodo";
import type { PQRS } from "../../domain/entities/PQRS";
import { avanceOrganizacionPQRS, cajasVigentesPQRS } from "../../domain/entities/PQRS";
import type { AyudaDeMemoria } from "../../domain/entities/AyudaDeMemoria";
import type { IExportadorReportes } from "../../domain/services/IExportadorReportes";

function formatearFecha(iso?: string): string {
  if (!iso) return "";
  const [a, m, d] = iso.split("-");
  return d && m && a ? `${d}/${m}/${a}` : iso;
}

export class JsPDFExportadorReportes implements IExportadorReportes {
  async exportarExcel(registros: RegistroPeriodo[], pqrs: PQRS[]): Promise<Blob> {
    // Mismas columnas conceptuales que Datos_BD en el Excel original, para poder comparar
    // directo el archivo que sale de la PWA contra el que ya conoce el equipo.
    const filas = registros.map((r) => ({
      "Unidad Operativa": r.unidadOperativaId,
      "Periodo / Fase": r.periodo,
      "Total Cajas (Meta)": r.totalCajas,
      "FUID (Cant)": r.tareas.fuid,
      "Eliminación (Cant)": r.tareas.eliminacion ?? "N/A",
      "Clasificación (Cant)": r.tareas.clasificacion,
      "Ordenación (Cant)": r.tareas.ordenacion,
      "Foliación (Cant)": r.tareas.foliacion,
      "Hoja de Control (Cant)": r.tareas.hojaControl,
      "Rotulación (Cant)": r.tareas.rotulacion,
      "% Avance Total": calcularAvanceTotal(r),
      "Cajas Vigentes en Sitio": cajasVigentes(r),
      "Encargado": r.encargado ?? "",
      "Fecha Visita": formatearFecha(r.fechaVisita),
      "Observaciones": r.observaciones ?? "",
    }));
    const filasPQRS = pqrs.map((p) => ({
      "Unidad Operativa": p.unidadOperativaId,
      "Total Cajas PQRS": p.totalCajas,
      "% Avance Organización": avanceOrganizacionPQRS(p),
      "Cajas Vigentes PQRS": cajasVigentesPQRS(p),
      "Notificado Subsecretaría": p.traslado.correoEnviado ? "SI" : "NO",
      "Trasladado": p.traslado.trasladado ? "SI" : "NO",
    }));

    const libro = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(libro, XLSX.utils.json_to_sheet(filas), "Datos_BD");
    XLSX.utils.book_append_sheet(libro, XLSX.utils.json_to_sheet(filasPQRS), "PQRS");
    const buffer = XLSX.write(libro, { bookType: "xlsx", type: "array" });
    return new Blob([buffer], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
  }

  async exportarPDF(registros: RegistroPeriodo[], pqrs: PQRS[]): Promise<Blob> {
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text("Reporte de Gestión Documental — Pérgamo", 14, 18);
    doc.setFontSize(10);
    doc.text(`Generado: ${new Date().toLocaleDateString("es-CO")}`, 14, 25);

    autoTable(doc, {
      startY: 32,
      head: [["Unidad Operativa", "Periodo", "Total Cajas", "% Avance", "Cajas Vigentes"]],
      body: registros.map((r) => [
        r.unidadOperativaId, r.periodo, r.totalCajas,
        `${Math.round(calcularAvanceTotal(r) * 100)}%`, cajasVigentes(r),
      ]),
      headStyles: { fillColor: [37, 99, 235] },
    });

    if (pqrs.length > 0) {
      const finalY = (doc as any).lastAutoTable.finalY + 10;
      doc.setFontSize(12);
      doc.text("PQRS", 14, finalY);
      autoTable(doc, {
        startY: finalY + 4,
        head: [["Unidad Operativa", "Total Cajas", "% Avance", "Notificado", "Trasladado"]],
        body: pqrs.map((p) => [
          p.unidadOperativaId, p.totalCajas,
          `${Math.round(avanceOrganizacionPQRS(p) * 100)}%`,
          p.traslado.correoEnviado ? "Sí" : "No",
          p.traslado.trasladado ? "Sí" : "No",
        ]),
        headStyles: { fillColor: [15, 118, 110] },
      });
    }
    return doc.output("blob");
  }

  /** Formato institucional GD-040 exacto: Lugar / Fecha / Tema / Desarrollo / tabla de
   *  Asistentes (con espacio en blanco para firma física) / tabla de Compromisos / Próxima
   *  reunión / Elaboró. */
  async generarAyudaDeMemoria(datos: AyudaDeMemoria): Promise<Blob> {
    const doc = new jsPDF();
    let y = 18;

    doc.setFontSize(15);
    doc.text("Ayuda de Memoria", 14, y);
    y += 10;

    doc.setFontSize(10);
    const campo = (etiqueta: string, valor: string) => {
      doc.setFont("helvetica", "bold");
      doc.text(`${etiqueta}:`, 14, y);
      doc.setFont("helvetica", "normal");
      const lineas = doc.splitTextToSize(valor || "", 150);
      doc.text(lineas, 45, y);
      y += Math.max(6, lineas.length * 5);
    };
    campo("Lugar", datos.lugar);
    campo("Fecha", formatearFecha(datos.fecha));
    campo("Tema", datos.tema);
    campo("Desarrollo", datos.desarrollo);
    y += 4;

    doc.setFont("helvetica", "bold");
    doc.text("Asistentes", 14, y);
    y += 2;
    autoTable(doc, {
      startY: y,
      head: [["Nombre", "Cargo/Rol", "Dependencia", "Firma"]],
      body: datos.asistentes.map((a) => [a.nombre, a.cargoRol, a.dependencia, ""]), // firma en blanco -- se firma a mano
      headStyles: { fillColor: [37, 99, 235] },
      columnStyles: { 3: { minCellHeight: 14 } }, // deja espacio real para firmar a mano
    });
    y = (doc as any).lastAutoTable.finalY + 8;

    doc.setFont("helvetica", "bold");
    doc.text("Compromisos", 14, y);
    y += 2;
    autoTable(doc, {
      startY: y,
      head: [["Actividad", "Responsable", "Fecha límite"]],
      body: datos.compromisos.map((c) => [c.actividad, c.responsable, formatearFecha(c.fechaLimite)]),
      headStyles: { fillColor: [37, 99, 235] },
    });
    y = (doc as any).lastAutoTable.finalY + 10;

    doc.setFont("helvetica", "normal");
    campo("Próxima reunión", datos.proximaReunion ? formatearFecha(datos.proximaReunion) : "No establecida");
    campo("Elaboró", datos.elaboroPor);

    return doc.output("blob");
  }
}
