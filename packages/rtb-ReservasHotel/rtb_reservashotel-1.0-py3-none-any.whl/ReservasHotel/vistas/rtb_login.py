# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rtb_login.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QWidget,
)
import ReservasHotel.recursos.recursos_rc


class Ui_rtb_W_Login(object):
    def setupUi(self, rtb_W_Login):
        if not rtb_W_Login.objectName():
            rtb_W_Login.setObjectName("rtb_W_Login")
        rtb_W_Login.setWindowModality(Qt.WindowModality.ApplicationModal)
        rtb_W_Login.resize(392, 215)
        rtb_W_Login.setMaximumSize(QSize(450, 250))
        font = QFont()
        font.setPointSize(10)
        rtb_W_Login.setFont(font)
        icon = QIcon()
        icon.addFile(":/Titles/key.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        rtb_W_Login.setWindowIcon(icon)
        rtb_W_Login.setStyleSheet("background-color: rgb(201, 204, 255);")
        self.gridLayout = QGridLayout(rtb_W_Login)
        self.gridLayout.setObjectName("gridLayout")
        self.rtb_pb_Cancelar = QPushButton(rtb_W_Login)
        self.rtb_pb_Cancelar.setObjectName("rtb_pb_Cancelar")
        font1 = QFont()
        font1.setPointSize(11)
        self.rtb_pb_Cancelar.setFont(font1)
        self.rtb_pb_Cancelar.setStyleSheet(
            "background-color: rgb(170, 170, 255);padding:10px;"
        )
        icon1 = QIcon()
        icon1.addFile(
            ":/Buttons/cancel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.rtb_pb_Cancelar.setIcon(icon1)

        self.gridLayout.addWidget(self.rtb_pb_Cancelar, 1, 1, 1, 1)

        self.rtb_gb_Login = QGroupBox(rtb_W_Login)
        self.rtb_gb_Login.setObjectName("rtb_gb_Login")
        font2 = QFont()
        font2.setPointSize(12)
        self.rtb_gb_Login.setFont(font2)
        self.rtb_gb_Login.setStyleSheet("")
        self.rtb_gb_Login.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.formLayout = QFormLayout(self.rtb_gb_Login)
        self.formLayout.setObjectName("formLayout")
        self.rtb_lb_Usuario = QLabel(self.rtb_gb_Login)
        self.rtb_lb_Usuario.setObjectName("rtb_lb_Usuario")
        self.rtb_lb_Usuario.setFont(font1)

        self.formLayout.setWidget(
            0, QFormLayout.ItemRole.LabelRole, self.rtb_lb_Usuario
        )

        self.rtb_le_Usuario = QLineEdit(self.rtb_gb_Login)
        self.rtb_le_Usuario.setObjectName("rtb_le_Usuario")
        self.rtb_le_Usuario.setFont(font1)
        self.rtb_le_Usuario.setStyleSheet(
            "background-color: rgb(255, 255, 255);padding:3px;"
        )

        self.formLayout.setWidget(
            0, QFormLayout.ItemRole.FieldRole, self.rtb_le_Usuario
        )

        self.rtb_lb_Password = QLabel(self.rtb_gb_Login)
        self.rtb_lb_Password.setObjectName("rtb_lb_Password")
        self.rtb_lb_Password.setFont(font1)

        self.formLayout.setWidget(
            1, QFormLayout.ItemRole.LabelRole, self.rtb_lb_Password
        )

        self.rtb_le_Password = QLineEdit(self.rtb_gb_Login)
        self.rtb_le_Password.setObjectName("rtb_le_Password")
        self.rtb_le_Password.setFont(font1)
        self.rtb_le_Password.setStyleSheet(
            "background-color: rgb(255, 255, 255);padding:3px;"
        )
        self.rtb_le_Password.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.setWidget(
            1, QFormLayout.ItemRole.FieldRole, self.rtb_le_Password
        )

        self.gridLayout.addWidget(self.rtb_gb_Login, 0, 0, 1, 2)

        self.rtb_pb_Aceptar = QPushButton(rtb_W_Login)
        self.rtb_pb_Aceptar.setObjectName("rtb_pb_Aceptar")
        self.rtb_pb_Aceptar.setFont(font1)
        self.rtb_pb_Aceptar.setStyleSheet(
            "background-color: rgb(170, 170, 255);padding:10px;"
        )
        icon2 = QIcon()
        icon2.addFile(
            ":/Buttons/accept.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.rtb_pb_Aceptar.setIcon(icon2)

        self.gridLayout.addWidget(self.rtb_pb_Aceptar, 1, 0, 1, 1)

        QWidget.setTabOrder(self.rtb_le_Usuario, self.rtb_le_Password)
        QWidget.setTabOrder(self.rtb_le_Password, self.rtb_pb_Aceptar)
        QWidget.setTabOrder(self.rtb_pb_Aceptar, self.rtb_pb_Cancelar)

        self.retranslateUi(rtb_W_Login)

        self.rtb_pb_Aceptar.setDefault(True)

        QMetaObject.connectSlotsByName(rtb_W_Login)

    # setupUi

    def retranslateUi(self, rtb_W_Login):
        rtb_W_Login.setWindowTitle(
            QCoreApplication.translate("rtb_W_Login", "Reservas Hotel - Login", None)
        )
        self.rtb_pb_Cancelar.setText(
            QCoreApplication.translate("rtb_W_Login", "Cancelar", None)
        )
        self.rtb_gb_Login.setTitle(
            QCoreApplication.translate(
                "rtb_W_Login", "Bienvenid@ - Introduce usuario y contrase\u00f1a", None
            )
        )
        self.rtb_lb_Usuario.setText(
            QCoreApplication.translate("rtb_W_Login", "Usuario", None)
        )
        # if QT_CONFIG(tooltip)
        self.rtb_le_Usuario.setToolTip(
            QCoreApplication.translate(
                "rtb_W_Login",
                "<html><head/><body><p>Escribe tu usuario</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rtb_le_Usuario.setText("")
        self.rtb_lb_Password.setText(
            QCoreApplication.translate("rtb_W_Login", "Contrase\u00f1a", None)
        )
        # if QT_CONFIG(tooltip)
        self.rtb_le_Password.setToolTip(
            QCoreApplication.translate(
                "rtb_W_Login",
                "<html><head/><body><p>Escribe tu contrase\u00f1a</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rtb_pb_Aceptar.setText(
            QCoreApplication.translate("rtb_W_Login", "Aceptar", None)
        )

    # retranslateUi
