// Mismo patron que los repositorios: el dominio solo conoce este CONTRATO. La implementacion
// real (que sabe de librerias de Excel/PDF especificas) vive en infrastructure/, para poder
// cambiar de libreria sin tocar ni un caso de uso ni una pantalla.
import type { RegistroPeriodo } from "../entities/RegistroPeriodo";
import type { PQRS } from "../entities/PQRS";
import type { AyudaDeMemoria } from "../entities/AyudaDeMemoria";

export interface IExportadorReportes {
  /** Genera un .xlsx con la misma estructura de columnas que Datos_BD en el Excel -- para que
   *  el archivo que sale de la PWA se pueda abrir y comparar directo contra el original. */
  exportarExcel(registros: RegistroPeriodo[], pqrs: PQRS[]): Promise<Blob>;
  /** PDF de reporte para imprimir o entregar -- KPIs + tabla resumida, no la base de datos cruda. */
  exportarPDF(registros: RegistroPeriodo[], pqrs: PQRS[]): Promise<Blob>;
  /** Ayuda de memoria: usa exactamente el formato institucional GD-040. */
  generarAyudaDeMemoria(datos: AyudaDeMemoria): Promise<Blob>;
}
