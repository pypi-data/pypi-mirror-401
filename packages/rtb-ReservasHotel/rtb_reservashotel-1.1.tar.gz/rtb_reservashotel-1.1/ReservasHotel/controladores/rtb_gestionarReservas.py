import sys
import re

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from ReservasHotel.vistas.rtb_gestionarReservas import Ui_rtb_W_GestionarReservas
from ReservasHotel.utilidades.rtb_estilosWidgets import estilosCalendario


class RTB_GestionarReservasForm(qtw.QWidget, Ui_rtb_W_GestionarReservas):
    def __init__(self, bdModelo, salonNombre, salonId, reservaIdFila=None):
        super().__init__()
        self.setupUi(self)

        self.bd = bdModelo
        self.salonNombre = salonNombre
        self.salonId = salonId
        self.reservaIdFila = reservaIdFila

        self.rtb_le_TituloReservas.setText(f"Reservas – {salonNombre}")

        # Aplicar estilos
        estilosCalendario(self.rtb_de_FechaReserva)

        # Ocultar grupo Congreso inicialmente
        self.rtb_gb_Congreso.setVisible(False)

        # Configurar fecha mínima del DateEdit a la fecha actual
        self.rtb_de_FechaReserva.setMinimumDate(qtc.QDate.currentDate())

        # Cargar tipos de reserva en el comboBox
        self.rtb_cb_TipoReserva.clear()
        self.rtb_cb_TipoReserva.addItem("Ninguno", None)
        tipos_reservas = self.bd.getListaTiposReservas()
        for id_res, nombre in tipos_reservas:
            # Añadir el nombre (tipo de reserva) como texto visible y el ID como 'userData'
            self.rtb_cb_TipoReserva.addItem(nombre, id_res)

        # Cargar tipos de cocina en el comboBox
        self.rtb_cb_TipoCocina.clear()
        self.rtb_cb_TipoCocina.addItem("Ninguno", None)
        tipos_cocina = self.bd.getListaTiposCocina()
        for id_coc, nombre in tipos_cocina:
            # Añadir el nombre (tipo de cocina) como texto visible y el ID como 'userData'
            self.rtb_cb_TipoCocina.addItem(nombre, id_coc)

        # Preparar formulario según si es nueva reserva o edición
        if reservaIdFila is None:
            self.f_limpiarFormulario()
            self.rtb_de_FechaReserva.setDate(qtc.QDate.currentDate())
        else:
            self.f_cargarDatosReserva(reservaIdFila)

        # Conectar señal de cambio en el comboBox
        self.rtb_cb_TipoReserva.currentTextChanged.connect(self.f_tipoReserva)

        # Conectar señal del botón Reservar
        self.rtb_pb_Reservar.clicked.connect(self.f_guardarReserva)

        # Conectar señal del botón Volver
        self.rtb_pb_Volver.clicked.connect(self.f_cerrarVentana)

    # Cerrar ventana al pulsar el botón Volver
    def f_cerrarVentana(self):
        self.close()

    # Override closeEvent para utilizar f_cerrarVentana al pulsar el aspa de cerrar ventana
    def closeEvent(self, event):
        event.ignore()
        self.f_cerrarVentana()

    # Limpiar formulario para nueva reserva
    def f_limpiarFormulario(self):
        self.rtb_le_Nombre.clear()
        self.rtb_le_Telefono.clear()
        self.rtb_de_FechaReserva.setDate(qtc.QDate.currentDate())
        self.rtb_cb_TipoReserva.setCurrentIndex(0)
        self.rtb_sb_NumeroAsistentes.setValue(1)
        self.rtb_cb_TipoCocina.setCurrentIndex(0)
        self.rtb_sb_NumHabitaciones.setValue(0)
        self.rtb_sb_NumJornadas.setValue(1)

    # Cargar datos de reserva para edición
    def f_cargarDatosReserva(self, reservaIdFila):
        reserva = self.bd.getReservasPorId(reservaIdFila)

        self.rtb_le_Nombre.setText(reserva["persona"])
        self.rtb_le_Telefono.setText(reserva["telefono"])
        self.rtb_de_FechaReserva.setDate(
            qtc.QDate.fromString(reserva["fecha"], "dd/MM/yyyy")
        )
        self.rtb_cb_TipoReserva.setCurrentText(reserva["tipo_reserva"])
        self.rtb_sb_NumeroAsistentes.setValue(reserva["ocupacion"])
        self.rtb_cb_TipoCocina.setCurrentText(reserva["tipo_cocina"])

        if reserva["tipo_reserva"] == "Congreso":
            self.rtb_gb_Congreso.setVisible(True)
            self.rtb_sb_NumHabitaciones.setValue(reserva["habitaciones"])
            self.rtb_sb_NumJornadas.setValue(reserva["jornadas"])

    # Evento: Cambiar visibilidad del grupo Congreso según tipo de reserva
    def f_tipoReserva(self, tipo):
        if tipo == "Congreso":
            self.rtb_gb_Congreso.setVisible(True)
        else:
            self.rtb_gb_Congreso.setVisible(False)

    # Validación de datos formulario
    def f_validarFormulario(self):
        erroresFormulario = []
        if not self.rtb_le_Nombre.text().strip():
            erroresFormulario.append("El campo Nombre es obligatorio.")
        if not self.rtb_le_Telefono.text().strip():
            erroresFormulario.append("El campo Teléfono es obligatorio.")
        else:
            if not re.match(r"^[67]\d{8}$", self.rtb_le_Telefono.text().strip()):
                erroresFormulario.append(
                    "El campo Teléfono debe comenzar con 6 o 7 y tener 9 dígitos."
                )
        if self.rtb_cb_TipoReserva.currentText() == "Ninguno":
            erroresFormulario.append("Debe seleccionar un Tipo de Reserva.")
        if self.rtb_cb_TipoCocina.currentText() == "Ninguno":
            erroresFormulario.append("Debe seleccionar un Tipo de Cocina.")
        if (
            self.bd.verificarFechaDisponible(
                self.rtb_de_FechaReserva.date().toString("dd/MM/yyyy"),
                self.salonId,
                self.reservaIdFila,
            )
            is False
        ):
            erroresFormulario.append(
                "La fecha seleccionada no está disponible para este salón."
            )
        if erroresFormulario:
            qtw.QMessageBox.warning(
                self,
                "Hay errores en el formulario",
                "\n".join(erroresFormulario),
            )
            return False
        return True

    # Evento: Guardar reserva (nueva o editada tras cargarla)
    def f_guardarReserva(self):
        # Validar formulario antes de guardar
        if not self.f_validarFormulario():
            return
        # Obtener los id de las claves foráneas
        tipo_cocina_id = self.bd.getTipoCocinaId(self.rtb_cb_TipoCocina.currentText())
        tipo_reserva_id = self.bd.getTipoReservaId(
            self.rtb_cb_TipoReserva.currentText()
        )

        # Preparar datos para guardar en la base de datos
        datosFormulario = {
            "tipo_reserva_id": tipo_reserva_id,
            "salon_id": self.salonId,
            "tipo_cocina_id": tipo_cocina_id,
            "nombre": self.rtb_le_Nombre.text(),
            "telefono": self.rtb_le_Telefono.text(),
            "fecha": self.rtb_de_FechaReserva.date().toString("dd/MM/yyyy"),
            "tipo_reserva": self.rtb_cb_TipoReserva.currentText(),
            "ocupacion": self.rtb_sb_NumeroAsistentes.value(),
            "tipo_cocina": self.rtb_cb_TipoCocina.currentText(),
            "habitaciones": self.rtb_sb_NumHabitaciones.value(),
            "jornadas": self.rtb_sb_NumJornadas.value(),
        }
        if self.reservaIdFila is None:
            # Guardar nueva reserva
            self.bd.guardarNuevaReserva(datosFormulario)
        else:
            # Actualizar reserva cargada
            datosFormulario["reserva_id"] = self.reservaIdFila
            self.bd.actualizarReserva(datosFormulario)

        qtw.QMessageBox.information(self, "Reserva", "Reserva guardada correctamente.")
        self.f_cerrarVentana()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = RTB_GestionarReservasForm(self.bd, "Otro Salón", 1)
    window.show()
    sys.exit(app.exec())
