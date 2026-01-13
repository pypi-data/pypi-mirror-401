import sys

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from ReservasHotel.vistas.rtb_login import Ui_rtb_W_Login


class RTB_LoginForm(qtw.QWidget, Ui_rtb_W_Login):

    loginSuccess = qtc.Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.rtb_le_Usuario.setFocus()

        self.rtb_pb_Cancelar.clicked.connect(self.close)
        self.rtb_pb_Aceptar.clicked.connect(self.loginHandler)
        self.rtb_le_Password.returnPressed.connect(self.loginHandler)

    @qtc.Slot()
    def loginHandler(self):
        usuario = self.rtb_le_Usuario.text()
        password = self.rtb_le_Password.text()
        if usuario == "hotel" and password == "Brianda23$":
            qtw.QMessageBox.information(
                self, "Login correcto", "Sesión iniciada correctamente."
            )
            self.loginSuccess.emit()
            self.close()
        else:
            qtw.QMessageBox.information(
                self, "Login incorrecto", "Usuario o contraseña incorrectos."
            )
            self.rtb_le_Usuario.clear()
            self.rtb_le_Password.clear()
            self.rtb_le_Usuario.setFocus()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = RTB_LoginForm()
    window.show()
    sys.exit(app.exec())
