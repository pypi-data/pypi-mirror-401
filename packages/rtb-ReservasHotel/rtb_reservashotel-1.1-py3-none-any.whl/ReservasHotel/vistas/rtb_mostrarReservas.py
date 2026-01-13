# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rtb_mostrarReservas.ui'
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
    QAbstractScrollArea,
    QApplication,
    QDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHeaderView,
    QLabel,
    QLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
import ReservasHotel.recursos.recursos_rc


class Ui_rtb_D_MostrarReservas(object):
    def setupUi(self, rtb_D_MostrarReservas):
        if not rtb_D_MostrarReservas.objectName():
            rtb_D_MostrarReservas.setObjectName("rtb_D_MostrarReservas")
        rtb_D_MostrarReservas.setWindowModality(Qt.WindowModality.ApplicationModal)
        rtb_D_MostrarReservas.resize(686, 500)
        font = QFont()
        font.setPointSize(11)
        rtb_D_MostrarReservas.setFont(font)
        icon = QIcon()
        icon.addFile(":/Titles/hotel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        rtb_D_MostrarReservas.setWindowIcon(icon)
        rtb_D_MostrarReservas.setStyleSheet("background-color: rgb(201, 204, 255);")
        self.gridLayout = QGridLayout(rtb_D_MostrarReservas)
        self.gridLayout.setObjectName("gridLayout")
        self.rtb_gb_Reservas = QGroupBox(rtb_D_MostrarReservas)
        self.rtb_gb_Reservas.setObjectName("rtb_gb_Reservas")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.rtb_gb_Reservas.sizePolicy().hasHeightForWidth()
        )
        self.rtb_gb_Reservas.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.rtb_gb_Reservas.setFont(font1)
        self.verticalLayout_2 = QVBoxLayout(self.rtb_gb_Reservas)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(
            QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.rtb_vl_Reservas = QVBoxLayout()
        self.rtb_vl_Reservas.setObjectName("rtb_vl_Reservas")
        self.rtb_vl_Reservas.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.rtb_t_Reservas = QTableWidget(self.rtb_gb_Reservas)
        self.rtb_t_Reservas.setObjectName("rtb_t_Reservas")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.rtb_t_Reservas.sizePolicy().hasHeightForWidth()
        )
        self.rtb_t_Reservas.setSizePolicy(sizePolicy1)
        self.rtb_t_Reservas.setStyleSheet("background-color:white;")
        self.rtb_t_Reservas.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )

        self.rtb_vl_Reservas.addWidget(self.rtb_t_Reservas)

        self.verticalLayout_2.addLayout(self.rtb_vl_Reservas)

        self.gridLayout.addWidget(self.rtb_gb_Reservas, 1, 1, 1, 2)

        self.rtb_gb_Salones = QGroupBox(rtb_D_MostrarReservas)
        self.rtb_gb_Salones.setObjectName("rtb_gb_Salones")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.rtb_gb_Salones.sizePolicy().hasHeightForWidth()
        )
        self.rtb_gb_Salones.setSizePolicy(sizePolicy2)
        self.rtb_gb_Salones.setFont(font1)
        self.rtb_gb_Salones.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.verticalLayout = QVBoxLayout(self.rtb_gb_Salones)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSizeConstraint(
            QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.rtb_vl_Salones = QVBoxLayout()
        self.rtb_vl_Salones.setObjectName("rtb_vl_Salones")
        self.rtb_vl_Salones.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.rtb_t_Salones = QTableWidget(self.rtb_gb_Salones)
        self.rtb_t_Salones.setObjectName("rtb_t_Salones")
        sizePolicy2.setHeightForWidth(
            self.rtb_t_Salones.sizePolicy().hasHeightForWidth()
        )
        self.rtb_t_Salones.setSizePolicy(sizePolicy2)
        self.rtb_t_Salones.setStyleSheet("background-color:white;")

        self.rtb_vl_Salones.addWidget(self.rtb_t_Salones)

        self.verticalLayout.addLayout(self.rtb_vl_Salones)

        self.gridLayout.addWidget(self.rtb_gb_Salones, 1, 0, 1, 1)

        self.rtb_lb_MensajeAyuda = QLabel(rtb_D_MostrarReservas)
        self.rtb_lb_MensajeAyuda.setObjectName("rtb_lb_MensajeAyuda")
        font2 = QFont()
        font2.setPointSize(10)
        self.rtb_lb_MensajeAyuda.setFont(font2)
        self.rtb_lb_MensajeAyuda.setStyleSheet(
            "background-color: white;\n" "padding: 5px;"
        )

        self.gridLayout.addWidget(self.rtb_lb_MensajeAyuda, 3, 0, 1, 3)

        self.rtb_f_Botones = QFrame(rtb_D_MostrarReservas)
        self.rtb_f_Botones.setObjectName("rtb_f_Botones")
        self.rtb_f_Botones.setFrameShape(QFrame.Shape.StyledPanel)
        self.rtb_f_Botones.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.rtb_f_Botones)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.rtb_pb_NuevaReserva = QPushButton(self.rtb_f_Botones)
        self.rtb_pb_NuevaReserva.setObjectName("rtb_pb_NuevaReserva")
        self.rtb_pb_NuevaReserva.setFont(font)
        self.rtb_pb_NuevaReserva.setStyleSheet(
            "background-color: rgb(170, 170, 255);padding:10px;"
        )
        icon1 = QIcon()
        icon1.addFile(
            ":/Titles/booking.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.rtb_pb_NuevaReserva.setIcon(icon1)

        self.gridLayout_2.addWidget(self.rtb_pb_NuevaReserva, 0, 1, 1, 1)

        self.rtb_pb_CerrarVentana = QPushButton(self.rtb_f_Botones)
        self.rtb_pb_CerrarVentana.setObjectName("rtb_pb_CerrarVentana")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.rtb_pb_CerrarVentana.sizePolicy().hasHeightForWidth()
        )
        self.rtb_pb_CerrarVentana.setSizePolicy(sizePolicy3)
        self.rtb_pb_CerrarVentana.setFont(font)
        self.rtb_pb_CerrarVentana.setStyleSheet(
            "background-color: rgb(170, 170, 255);padding:10px;"
        )
        icon2 = QIcon()
        icon2.addFile(
            ":/Buttons/cancel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.rtb_pb_CerrarVentana.setIcon(icon2)

        self.gridLayout_2.addWidget(self.rtb_pb_CerrarVentana, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.rtb_f_Botones, 2, 0, 1, 3)

        self.rtb_lb_ImgMostrarReservas = QLabel(rtb_D_MostrarReservas)
        self.rtb_lb_ImgMostrarReservas.setObjectName("rtb_lb_ImgMostrarReservas")
        self.rtb_lb_ImgMostrarReservas.setMaximumSize(QSize(75, 75))
        self.rtb_lb_ImgMostrarReservas.setPixmap(QPixmap(":/Titles/calendario.png"))
        self.rtb_lb_ImgMostrarReservas.setScaledContents(True)

        self.gridLayout.addWidget(self.rtb_lb_ImgMostrarReservas, 0, 2, 1, 1)

        self.rtb_le_TituloMostrarReservas = QLineEdit(rtb_D_MostrarReservas)
        self.rtb_le_TituloMostrarReservas.setObjectName("rtb_le_TituloMostrarReservas")
        font3 = QFont()
        font3.setPointSize(16)
        font3.setBold(False)
        self.rtb_le_TituloMostrarReservas.setFont(font3)
        self.rtb_le_TituloMostrarReservas.setStyleSheet("border:none;\n" "padding:5px;")

        self.gridLayout.addWidget(self.rtb_le_TituloMostrarReservas, 0, 0, 1, 2)

        QWidget.setTabOrder(self.rtb_le_TituloMostrarReservas, self.rtb_t_Salones)
        QWidget.setTabOrder(self.rtb_t_Salones, self.rtb_t_Reservas)
        QWidget.setTabOrder(self.rtb_t_Reservas, self.rtb_pb_NuevaReserva)
        QWidget.setTabOrder(self.rtb_pb_NuevaReserva, self.rtb_pb_CerrarVentana)

        self.retranslateUi(rtb_D_MostrarReservas)

        QMetaObject.connectSlotsByName(rtb_D_MostrarReservas)

    # setupUi

    def retranslateUi(self, rtb_D_MostrarReservas):
        rtb_D_MostrarReservas.setWindowTitle(
            QCoreApplication.translate(
                "rtb_D_MostrarReservas", "Reservas Salones", None
            )
        )
        self.rtb_gb_Reservas.setTitle(
            QCoreApplication.translate("rtb_D_MostrarReservas", "Reservas", None)
        )
        # if QT_CONFIG(tooltip)
        self.rtb_t_Reservas.setToolTip(
            QCoreApplication.translate(
                "rtb_D_MostrarReservas", "Reservas del sal\u00f3n seleccionado", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rtb_gb_Salones.setTitle(
            QCoreApplication.translate("rtb_D_MostrarReservas", "Salones", None)
        )
        # if QT_CONFIG(tooltip)
        self.rtb_t_Salones.setToolTip(
            QCoreApplication.translate(
                "rtb_D_MostrarReservas", "Salones disponibles", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rtb_lb_MensajeAyuda.setText(
            QCoreApplication.translate(
                "rtb_D_MostrarReservas",
                "Selecciona un sal\u00f3n para ver el listado de reservas",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.rtb_pb_NuevaReserva.setToolTip(
            QCoreApplication.translate(
                "rtb_D_MostrarReservas",
                "Abre la ventana de reservas para el sal\u00f3n seleccionado",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rtb_pb_NuevaReserva.setText(
            QCoreApplication.translate("rtb_D_MostrarReservas", "Nueva Reserva", None)
        )
        # if QT_CONFIG(tooltip)
        self.rtb_pb_CerrarVentana.setToolTip(
            QCoreApplication.translate(
                "rtb_D_MostrarReservas", "Cierra la ventana actual", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rtb_pb_CerrarVentana.setText(
            QCoreApplication.translate("rtb_D_MostrarReservas", "Cerrar", None)
        )
        self.rtb_lb_ImgMostrarReservas.setText("")
        self.rtb_le_TituloMostrarReservas.setText(
            QCoreApplication.translate(
                "rtb_D_MostrarReservas", "Gesti\u00f3n de reservas de Salones", None
            )
        )

    # retranslateUi
