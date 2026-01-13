import sys
import os

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from ReservasHotel.vistas.rtb_mostrarReservas import Ui_rtb_D_MostrarReservas
from ReservasHotel.modelo.datos import RTB_BaseDatos
from ReservasHotel.utilidades.rtb_estilosWidgets import estilosTabla

RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_DB_ABSOLUTA = os.path.join(RUTA_BASE, "..", "modelo", "reservas.db")


class RTB_MostrarReservasForm(qtw.QWidget, Ui_rtb_D_MostrarReservas):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.rtb_pb_NuevaReserva.setEnabled(
            False
        )  # Botón nueva reserva desactivado hasta seleccionar un salón
        self.rtb_lb_MensajeAyuda.setText(
            "Selecciona un salón para ver sus reservas o crear una nueva"
        )  # Mensaje de ayuda inicial

        self.bd = RTB_BaseDatos(RUTA_DB_ABSOLUTA)

        self.f_cargarSalones()  # Carga la lista de salones

        self.rtb_t_Salones.itemSelectionChanged.connect(
            self.f_salonSeleccionado
        )  # Evento selección salón
        self.rtb_t_Reservas.itemDoubleClicked.connect(
            self.f_reservaDobleClick
        )  # Evento doble clic reserva

        self.rtb_pb_NuevaReserva.clicked.connect(
            self.f_nuevaReserva
        )  # Botón nueva reserva
        self.rtb_pb_CerrarVentana.clicked.connect(self.close)  # Botón cerrar ventana

    # Cargar salones en la tabla
    def f_cargarSalones(self):

        estilosTabla(self.rtb_t_Salones)
        salones = self.bd.getSalones()

        self.rtb_t_Salones.setRowCount(len(salones))
        self.rtb_t_Salones.setColumnCount(1)
        self.rtb_t_Salones.setHorizontalHeaderLabels(["Salones"])

        for fila, (salon_id, nombre) in enumerate(salones):
            item = qtw.QTableWidgetItem(nombre)
            item.setData(
                qtc.Qt.UserRole, salon_id
            )  # Guardar el ID del salón para cargar las reservas
            self.rtb_t_Salones.setItem(fila, 0, item)

    # Evento: Al seleccionar un salón carga reservas asociadas
    def f_salonSeleccionado(self):
        items = self.rtb_t_Salones.selectedItems()
        if not items:
            return

        salonItem = items[0]
        self.salonId = salonItem.data(qtc.Qt.UserRole)

        # Si se selecciona un salón se activa el botón para nueva reserva y se actualiza el mensaje de la etiqueta de ayuda
        self.rtb_pb_NuevaReserva.setEnabled(True)
        self.rtb_lb_MensajeAyuda.setText(
            "Añade una nueva reserva o haz 2 clicks en una existente para modificarla"
        )

        # Cargar reservas asociadas
        self.f_cargarReservas(self.salonId)

    # Cargar reservas para un salón
    def f_cargarReservas(self, salonId):
        reservas = self.bd.getReservasPorSalon(salonId)

        estilosTabla(self.rtb_t_Reservas)

        self.rtb_t_Reservas.clear()
        self.rtb_t_Reservas.setColumnCount(4)
        self.rtb_t_Reservas.setRowCount(len(reservas))
        self.rtb_t_Reservas.setHorizontalHeaderLabels(
            ["Fecha", "Nombre", "Teléfono", "Tipo"]
        )

        for fila, (reserva_id, fecha, persona, telefono, nombre) in enumerate(reservas):
            item_fecha = qtw.QTableWidgetItem(fecha)
            item_fecha.setData(qtc.Qt.UserRole, reserva_id)
            self.rtb_t_Reservas.setItem(fila, 0, item_fecha)
            self.rtb_t_Reservas.setItem(fila, 1, qtw.QTableWidgetItem(persona))
            self.rtb_t_Reservas.setItem(fila, 2, qtw.QTableWidgetItem(telefono))
            self.rtb_t_Reservas.setItem(fila, 3, qtw.QTableWidgetItem(nombre))

    # Evento: Al hacer doble clic en una reserva llama a editar
    def f_reservaDobleClick(self, celda):
        fila = celda.row()
        reservaIdFila = self.rtb_t_Reservas.item(fila, 0).data(qtc.Qt.UserRole)
        nombre = self.rtb_t_Reservas.item(fila, 1).text()

        salon = self.rtb_t_Salones.selectedItems()
        if not salon:
            return

        salonNombre = salon[0].text()

        qtw.QMessageBox.information(
            self, "Editar reserva", f"Editar reserva de {nombre}"
        )
        # Abrir RTB_GestionarReservasForm con datos de la reserva
        from ReservasHotel.controladores.rtb_gestionarReservas import (
            RTB_GestionarReservasForm,
        )

        self.form = RTB_GestionarReservasForm(
            bdModelo=self.bd,
            salonNombre=salonNombre,
            salonId=self.salonId,
            reservaIdFila=reservaIdFila,
        )
        self.f_abrirGestionarReservas()

    # Evento: Botón Nueva Reserva
    def f_nuevaReserva(self):
        salon = self.rtb_t_Salones.selectedItems()
        if not salon:
            return

        salonNombre = salon[0].text()

        # Abrir RTB_GestionarReservasForm para nueva reserva
        from ReservasHotel.controladores.rtb_gestionarReservas import (
            RTB_GestionarReservasForm,
        )

        self.form = RTB_GestionarReservasForm(
            bdModelo=self.bd, salonNombre=salonNombre, salonId=self.salonId
        )
        self.f_abrirGestionarReservas()

    # Cambiar de ventana con control del retorno desde gestionar reservas
    def f_abrirGestionarReservas(self):
        self.form.closeEvent = self.f_cerrarDesdeGestionarReservas
        self.form.show()
        self.hide()

    # Al cerrar desde gestionar reservas, recargar reservas y aceptar el evento
    def f_cerrarDesdeGestionarReservas(self, event):
        self.f_reservaRealizada()
        event.accept()

    # Al cerrar la ventana de gestionar reservas, recargar las reservas del salón y mostrar esta ventana
    def f_reservaRealizada(self):
        self.f_cargarReservas(self.salonId)
        self.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = RTB_MostrarReservasForm()
    window.show()
    sys.exit(app.exec())
