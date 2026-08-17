// Patron Builder: arma un RegistroPeriodo paso a paso, con valores por defecto sensatos para
// cada sub-objeto (tareas, transferencia, diagnostico), en vez de que cada pantalla tenga que
// saber construir a mano toda la forma del objeto. Sirve tanto para el formulario de captura
// como para pruebas/semillas de datos.
import type {
  RegistroPeriodo,
  PeriodoTRD,
  TareasCantidad,
  Transferencia,
  DiagnosticoRiesgo,
  TipoAlmacenamiento,
} from "../../domain/entities/RegistroPeriodo";

type RegistroBorrador = Omit<RegistroPeriodo, "id" | "creadoEn" | "actualizadoEn">;

export class RegistroPeriodoBuilder {
  private borrador: RegistroBorrador = {
    unidadOperativaId: "",
    periodo: "Fondo Acumulado (FDA)",
    totalCajas: 0,
    tareas: {
      fuid: 0, eliminacion: null, clasificacion: 0, ordenacion: 0,
      foliacion: 0, hojaControl: 0, rotulacion: 0,
    },
    transferencia: {
      correoSAF: false, aprobacionSAF: false, trasladoArchivoCentral: false, cajasTrasladadas: 0,
    },
    diagnostico: {
      tipoAlmacenamiento: null,
      riesgoHumedad: null, riesgoRoedores: null, riesgoSobreapilamiento: null, riesgoFiltraciones: null,
      cajasSobreapiladas: 0, metrosEspacioAjenoInvadido: 0,
    },
  };

  paraUnidad(unidadOperativaId: string): this {
    this.borrador.unidadOperativaId = unidadOperativaId;
    return this;
  }

  enPeriodo(periodo: PeriodoTRD): this {
    this.borrador.periodo = periodo;
    return this;
  }

  conTotalCajas(totalCajas: number): this {
    this.borrador.totalCajas = totalCajas;
    return this;
  }

  conTareas(tareas: Partial<TareasCantidad>): this {
    this.borrador.tareas = { ...this.borrador.tareas, ...tareas };
    return this;
  }

  conTransferencia(transferencia: Partial<Transferencia>): this {
    this.borrador.transferencia = { ...this.borrador.transferencia, ...transferencia };
    return this;
  }

  conDiagnostico(diagnostico: Partial<DiagnosticoRiesgo>): this {
    this.borrador.diagnostico = { ...this.borrador.diagnostico, ...diagnostico };
    return this;
  }

  conTipoAlmacenamiento(tipo: TipoAlmacenamiento): this {
    this.borrador.diagnostico.tipoAlmacenamiento = tipo;
    return this;
  }

  conEncargado(encargado: string): this {
    this.borrador.encargado = encargado;
    return this;
  }

  conFechaVisita(fechaISO: string): this {
    this.borrador.fechaVisita = fechaISO;
    return this;
  }

  conObservaciones(observaciones: string): this {
    this.borrador.observaciones = observaciones;
    return this;
  }

  /** Valida lo mínimo indispensable antes de entregar el objeto -- espejo de las reglas del
   *  caso de uso RegistrarAvancePeriodo, para fallar rápido si algo llega incompleto. */
  build(): RegistroBorrador {
    if (!this.borrador.unidadOperativaId) {
      throw new Error("RegistroPeriodoBuilder: falta especificar la unidad operativa (.paraUnidad()).");
    }
    if (this.borrador.totalCajas <= 0) {
      throw new Error("RegistroPeriodoBuilder: totalCajas debe ser mayor a 0 (.conTotalCajas()).");
    }
    return { ...this.borrador };
  }
}
