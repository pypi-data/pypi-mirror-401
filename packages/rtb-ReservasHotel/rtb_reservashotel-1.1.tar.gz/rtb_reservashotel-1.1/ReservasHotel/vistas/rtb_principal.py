# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rtb_principal.ui'
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
    QAction,
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
    QGridLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSizePolicy,
    QStatusBar,
    QWidget,
)
import ReservasHotel.recursos.recursos_rc


class Ui_rtb_M_VentanaPrincipal(object):
    def setupUi(self, rtb_M_VentanaPrincipal):
        if not rtb_M_VentanaPrincipal.objectName():
            rtb_M_VentanaPrincipal.setObjectName("rtb_M_VentanaPrincipal")
        rtb_M_VentanaPrincipal.resize(553, 471)
        font = QFont()
        font.setPointSize(11)
        rtb_M_VentanaPrincipal.setFont(font)
        icon = QIcon()
        icon.addFile(":/Titles/hotel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        rtb_M_VentanaPrincipal.setWindowIcon(icon)
        rtb_M_VentanaPrincipal.setStyleSheet("background-color: rgb(201, 204, 255);")
        self.rtb_ac_Salir = QAction(rtb_M_VentanaPrincipal)
        self.rtb_ac_Salir.setObjectName("rtb_ac_Salir")
        icon1 = QIcon()
        icon1.addFile(
            ":/Buttons/cancel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.rtb_ac_Salir.setIcon(icon1)
        font1 = QFont()
        font1.setPointSize(10)
        self.rtb_ac_Salir.setFont(font1)
        self.rtb_ac_MostrarReservas = QAction(rtb_M_VentanaPrincipal)
        self.rtb_ac_MostrarReservas.setObjectName("rtb_ac_MostrarReservas")
        icon2 = QIcon()
        icon2.addFile(
            ":/Titles/calendario.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.rtb_ac_MostrarReservas.setIcon(icon2)
        self.rtb_ac_MostrarReservas.setFont(font1)
        self.centralwidget = QWidget(rtb_M_VentanaPrincipal)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.rtb_lb_LogoPrincipal = QLabel(self.centralwidget)
        self.rtb_lb_LogoPrincipal.setObjectName("rtb_lb_LogoPrincipal")
        self.rtb_lb_LogoPrincipal.setMaximumSize(QSize(250, 250))
        self.rtb_lb_LogoPrincipal.setPixmap(QPixmap(":/Images/hotel_login.png"))
        self.rtb_lb_LogoPrincipal.setScaledContents(True)

        self.gridLayout.addWidget(self.rtb_lb_LogoPrincipal, 0, 0, 1, 1)

        rtb_M_VentanaPrincipal.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(rtb_M_VentanaPrincipal)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 553, 22))
        self.menuArchivo = QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        self.menuSalones = QMenu(self.menubar)
        self.menuSalones.setObjectName("menuSalones")
        rtb_M_VentanaPrincipal.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(rtb_M_VentanaPrincipal)
        self.statusbar.setObjectName("statusbar")
        rtb_M_VentanaPrincipal.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuSalones.menuAction())
        self.menuArchivo.addAction(self.rtb_ac_Salir)
        self.menuSalones.addAction(self.rtb_ac_MostrarReservas)

        self.retranslateUi(rtb_M_VentanaPrincipal)

        QMetaObject.connectSlotsByName(rtb_M_VentanaPrincipal)

    # setupUi

    def retranslateUi(self, rtb_M_VentanaPrincipal):
        rtb_M_VentanaPrincipal.setWindowTitle(
            QCoreApplication.translate(
                "rtb_M_VentanaPrincipal", "Gesti\u00f3n Hotel", None
            )
        )
        self.rtb_ac_Salir.setText(
            QCoreApplication.translate("rtb_M_VentanaPrincipal", "Salir", None)
        )
        self.rtb_ac_MostrarReservas.setText(
            QCoreApplication.translate(
                "rtb_M_VentanaPrincipal", "Reservas salones", None
            )
        )
        self.rtb_lb_LogoPrincipal.setText("")
        self.menuArchivo.setTitle(
            QCoreApplication.translate("rtb_M_VentanaPrincipal", "Archivo", None)
        )
        self.menuSalones.setTitle(
            QCoreApplication.translate("rtb_M_VentanaPrincipal", "Reservas", None)
        )

    # retranslateUi
