import sys

import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc

from ReservasHotel.vistas.rtb_principal import Ui_rtb_M_VentanaPrincipal
from ReservasHotel.controladores.rtb_login import RTB_LoginForm


class PrincipalForm(qtw.QMainWindow, Ui_rtb_M_VentanaPrincipal):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.rtb_ac_Salir.triggered.connect(self.close)

        self.rtb_ac_MostrarReservas.triggered.connect(self.abrirMostrarReservas)

        self.form = RTB_LoginForm()
        self.form.loginSuccess.connect(self.show)
        self.form.show()

    @qtc.Slot()
    def abrirMostrarReservas(self):
        from ReservasHotel.controladores.rtb_mostrarReservas import (
            RTB_MostrarReservasForm,
        )

        self.dialogo = RTB_MostrarReservasForm()
        self.dialogo.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = PrincipalForm()
    sys.exit(app.exec())
