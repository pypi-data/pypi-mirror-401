# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rtb_gestionarReservas.ui'
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
    QComboBox,
    QDateEdit,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QWidget,
)
import ReservasHotel.recursos.recursos_rc


class Ui_rtb_W_GestionarReservas(object):
    def setupUi(self, rtb_W_GestionarReservas):
        if not rtb_W_GestionarReservas.objectName():
            rtb_W_GestionarReservas.setObjectName("rtb_W_GestionarReservas")
        rtb_W_GestionarReservas.setWindowModality(Qt.WindowModality.ApplicationModal)
        rtb_W_GestionarReservas.resize(327, 468)
        rtb_W_GestionarReservas.setMaximumSize(QSize(500, 500))
        font = QFont()
        font.setPointSize(11)
        rtb_W_GestionarReservas.setFont(font)
        icon = QIcon()
        icon.addFile(
            ":/Titles/booking.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        rtb_W_GestionarReservas.setWindowIcon(icon)
        rtb_W_GestionarReservas.setStyleSheet("background-color: rgb(201, 204, 255);")
        self.gridLayout = QGridLayout(rtb_W_GestionarReservas)
        self.gridLayout.setObjectName("gridLayout")
        self.rtb_gb_GestionarReservas = QGroupBox(rtb_W_GestionarReservas)
        self.rtb_gb_GestionarReservas.setObjectName("rtb_gb_GestionarReservas")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.rtb_gb_GestionarReservas.setFont(font1)
        self.rtb_gb_GestionarReservas.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.formLayout_2 = QFormLayout(self.rtb_gb_GestionarReservas)
        self.formLayout_2.setObjectName("formLayout_2")
        self.formLayout_2.setVerticalSpacing(12)
        self.rtb_lb_Nombre = QLabel(self.rtb_gb_GestionarReservas)
        self.rtb_lb_Nombre.setObjectName("rtb_lb_Nombre")
        font2 = QFont()
        font2.setPointSize(9)
        self.rtb_lb_Nombre.setFont(font2)

        self.formLayout_2.setWidget(
            0, QFormLayout.ItemRole.LabelRole, self.rtb_lb_Nombre
        )

        self.rtb_le_Nombre = QLineEdit(self.rtb_gb_GestionarReservas)
        self.rtb_le_Nombre.setObjectName("rtb_le_Nombre")
        self.rtb_le_Nombre.setStyleSheet("background-color:white; font-size: 14px;")

        self.formLayout_2.setWidget(
            0, QFormLayout.ItemRole.FieldRole, self.rtb_le_Nombre
        )

        self.rtb_lb_Telefono = QLabel(self.rtb_gb_GestionarReservas)
        self.rtb_lb_Telefono.setObjectName("rtb_lb_Telefono")

        self.formLayout_2.setWidget(
            1, QFormLayout.ItemRole.LabelRole, self.rtb_lb_Telefono
        )

        self.rtb_le_Telefono = QLineEdit(self.rtb_gb_GestionarReservas)
        self.rtb_le_Telefono.setObjectName("rtb_le_Telefono")
        self.rtb_le_Telefono.setStyleSheet("background-color:white; font-size: 14px;")

        self.formLayout_2.setWidget(
            1, QFormLayout.ItemRole.FieldRole, self.rtb_le_Telefono
        )

        self.rtb_lb_FechaReserva = QLabel(self.rtb_gb_GestionarReservas)
        self.rtb_lb_FechaReserva.setObjectName("rtb_lb_FechaReserva")

        self.formLayout_2.setWidget(
            2, QFormLayout.ItemRole.LabelRole, self.rtb_lb_FechaReserva
        )

        self.rtb_de_FechaReserva = QDateEdit(self.rtb_gb_GestionarReservas)
        self.rtb_de_FechaReserva.setObjectName("rtb_de_FechaReserva")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.rtb_de_FechaReserva.sizePolicy().hasHeightForWidth()
        )
        self.rtb_de_FechaReserva.setSizePolicy(sizePolicy)
        self.rtb_de_FechaReserva.setMaximumSize(QSize(120, 16777215))
        font3 = QFont()
        self.rtb_de_FechaReserva.setFont(font3)
        self.rtb_de_FechaReserva.setStyleSheet(
            "background-color:white; font-size: 14px;"
        )
        self.rtb_de_FechaReserva.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rtb_de_FechaReserva.setMinimumDateTime(
            QDateTime(QDate(2025, 12, 31), QTime(20, 0, 0))
        )
        self.rtb_de_FechaReserva.setMaximumDate(QDate(2036, 12, 31))
        self.rtb_de_FechaReserva.setCalendarPopup(True)

        self.formLayout_2.setWidget(
            2, QFormLayout.ItemRole.FieldRole, self.rtb_de_FechaReserva
        )

        self.rtb_lb_TipoReserva = QLabel(self.rtb_gb_GestionarReservas)
        self.rtb_lb_TipoReserva.setObjectName("rtb_lb_TipoReserva")

        self.formLayout_2.setWidget(
            3, QFormLayout.ItemRole.LabelRole, self.rtb_lb_TipoReserva
        )

        self.rtb_cb_TipoReserva = QComboBox(self.rtb_gb_GestionarReservas)
        self.rtb_cb_TipoReserva.addItem("")
        self.rtb_cb_TipoReserva.addItem("")
        self.rtb_cb_TipoReserva.addItem("")
        self.rtb_cb_TipoReserva.addItem("")
        self.rtb_cb_TipoReserva.setObjectName("rtb_cb_TipoReserva")
        self.rtb_cb_TipoReserva.setFont(font3)
        self.rtb_cb_TipoReserva.setStyleSheet(
            "background-color:white; font-size: 14px;"
        )
        self.rtb_cb_TipoReserva.setEditable(False)
        self.rtb_cb_TipoReserva.setMaxVisibleItems(4)

        self.formLayout_2.setWidget(
            3, QFormLayout.ItemRole.FieldRole, self.rtb_cb_TipoReserva
        )

        self.rtb_lb_NumAsistentes = QLabel(self.rtb_gb_GestionarReservas)
        self.rtb_lb_NumAsistentes.setObjectName("rtb_lb_NumAsistentes")

        self.formLayout_2.setWidget(
            4, QFormLayout.ItemRole.LabelRole, self.rtb_lb_NumAsistentes
        )

        self.rtb_sb_NumeroAsistentes = QSpinBox(self.rtb_gb_GestionarReservas)
        self.rtb_sb_NumeroAsistentes.setObjectName("rtb_sb_NumeroAsistentes")
        self.rtb_sb_NumeroAsistentes.setMaximumSize(QSize(50, 16777215))
        self.rtb_sb_NumeroAsistentes.setStyleSheet(
            "background-color:white; font-size: 14px;"
        )
        self.rtb_sb_NumeroAsistentes.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rtb_sb_NumeroAsistentes.setMinimum(1)
        self.rtb_sb_NumeroAsistentes.setMaximum(140)

        self.formLayout_2.setWidget(
            4, QFormLayout.ItemRole.FieldRole, self.rtb_sb_NumeroAsistentes
        )

        self.rtb_lb_TipoCocina = QLabel(self.rtb_gb_GestionarReservas)
        self.rtb_lb_TipoCocina.setObjectName("rtb_lb_TipoCocina")

        self.formLayout_2.setWidget(
            5, QFormLayout.ItemRole.LabelRole, self.rtb_lb_TipoCocina
        )

        self.rtb_cb_TipoCocina = QComboBox(self.rtb_gb_GestionarReservas)
        self.rtb_cb_TipoCocina.addItem("")
        self.rtb_cb_TipoCocina.addItem("")
        self.rtb_cb_TipoCocina.addItem("")
        self.rtb_cb_TipoCocina.addItem("")
        self.rtb_cb_TipoCocina.addItem("")
        self.rtb_cb_TipoCocina.setObjectName("rtb_cb_TipoCocina")
        self.rtb_cb_TipoCocina.setStyleSheet("background-color:white; font-size: 14px;")
        self.rtb_cb_TipoCocina.setMaxVisibleItems(5)

        self.formLayout_2.setWidget(
            5, QFormLayout.ItemRole.FieldRole, self.rtb_cb_TipoCocina
        )

        self.gridLayout.addWidget(self.rtb_gb_GestionarReservas, 2, 0, 1, 5)

        self.rtb_pb_Reservar = QPushButton(rtb_W_GestionarReservas)
        self.rtb_pb_Reservar.setObjectName("rtb_pb_Reservar")
        self.rtb_pb_Reservar.setFont(font)
        self.rtb_pb_Reservar.setStyleSheet(
            "background-color: rgb(170, 170, 255);padding:10px;"
        )
        icon1 = QIcon()
        icon1.addFile(
            ":/Buttons/accept.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.rtb_pb_Reservar.setIcon(icon1)

        self.gridLayout.addWidget(self.rtb_pb_Reservar, 5, 3, 1, 1)

        self.rtb_lb_ImagenReservas = QLabel(rtb_W_GestionarReservas)
        self.rtb_lb_ImagenReservas.setObjectName("rtb_lb_ImagenReservas")
        self.rtb_lb_ImagenReservas.setMaximumSize(QSize(50, 50))
        self.rtb_lb_ImagenReservas.setPixmap(QPixmap(":/Images/reserva_cocina.jpg"))
        self.rtb_lb_ImagenReservas.setScaledContents(True)
        self.rtb_lb_ImagenReservas.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.rtb_lb_ImagenReservas, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout.addItem(self.horizontalSpacer, 5, 0, 1, 3)

        self.rtb_le_TituloReservas = QLineEdit(rtb_W_GestionarReservas)
        self.rtb_le_TituloReservas.setObjectName("rtb_le_TituloReservas")
        font4 = QFont()
        font4.setPointSize(16)
        self.rtb_le_TituloReservas.setFont(font4)
        self.rtb_le_TituloReservas.setStyleSheet("border:none;\n" "padding:5px;")

        self.gridLayout.addWidget(self.rtb_le_TituloReservas, 0, 1, 1, 4)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout.addItem(self.verticalSpacer, 6, 2, 1, 2)

        self.rtb_pb_Volver = QPushButton(rtb_W_GestionarReservas)
        self.rtb_pb_Volver.setObjectName("rtb_pb_Volver")
        self.rtb_pb_Volver.setFont(font)
        self.rtb_pb_Volver.setStyleSheet(
            "background-color: rgb(170, 170, 255);padding:10px;"
        )
        icon2 = QIcon()
        icon2.addFile(
            ":/Buttons/cancel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.rtb_pb_Volver.setIcon(icon2)

        self.gridLayout.addWidget(self.rtb_pb_Volver, 5, 4, 1, 1)

        self.rtb_gb_Congreso = QGroupBox(rtb_W_GestionarReservas)
        self.rtb_gb_Congreso.setObjectName("rtb_gb_Congreso")
        self.rtb_gb_Congreso.setFont(font1)
        self.rtb_gb_Congreso.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.formLayout = QFormLayout(self.rtb_gb_Congreso)
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setVerticalSpacing(12)
        self.formLayout.setContentsMargins(-1, -1, -1, 9)
        self.rtb_lb_Habitaciones = QLabel(self.rtb_gb_Congreso)
        self.rtb_lb_Habitaciones.setObjectName("rtb_lb_Habitaciones")

        self.formLayout.setWidget(
            0, QFormLayout.ItemRole.LabelRole, self.rtb_lb_Habitaciones
        )

        self.rtb_lb_NumJornadas = QLabel(self.rtb_gb_Congreso)
        self.rtb_lb_NumJornadas.setObjectName("rtb_lb_NumJornadas")

        self.formLayout.setWidget(
            1, QFormLayout.ItemRole.LabelRole, self.rtb_lb_NumJornadas
        )

        self.rtb_sb_NumJornadas = QSpinBox(self.rtb_gb_Congreso)
        self.rtb_sb_NumJornadas.setObjectName("rtb_sb_NumJornadas")
        self.rtb_sb_NumJornadas.setMaximumSize(QSize(50, 16777215))
        self.rtb_sb_NumJornadas.setStyleSheet(
            "background-color:white; font-size: 14px;"
        )
        self.rtb_sb_NumJornadas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rtb_sb_NumJornadas.setMinimum(1)
        self.rtb_sb_NumJornadas.setMaximum(30)

        self.formLayout.setWidget(
            1, QFormLayout.ItemRole.FieldRole, self.rtb_sb_NumJornadas
        )

        self.rtb_sb_NumHabitaciones = QSpinBox(self.rtb_gb_Congreso)
        self.rtb_sb_NumHabitaciones.setObjectName("rtb_sb_NumHabitaciones")
        self.rtb_sb_NumHabitaciones.setMaximumSize(QSize(50, 16777215))
        self.rtb_sb_NumHabitaciones.setStyleSheet(
            "background-color:white; font-size: 14px;"
        )
        self.rtb_sb_NumHabitaciones.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rtb_sb_NumHabitaciones.setMaximum(140)

        self.formLayout.setWidget(
            0, QFormLayout.ItemRole.FieldRole, self.rtb_sb_NumHabitaciones
        )

        self.gridLayout.addWidget(self.rtb_gb_Congreso, 4, 0, 1, 5)

        self.retranslateUi(rtb_W_GestionarReservas)

        self.rtb_cb_TipoReserva.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(rtb_W_GestionarReservas)

    # setupUi

    def retranslateUi(self, rtb_W_GestionarReservas):
        rtb_W_GestionarReservas.setWindowTitle(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Reservas Salones - Reservar", None
            )
        )
        self.rtb_gb_GestionarReservas.setTitle(
            QCoreApplication.translate("rtb_W_GestionarReservas", "Nueva Reserva", None)
        )
        self.rtb_lb_Nombre.setText(
            QCoreApplication.translate("rtb_W_GestionarReservas", "Nombre", None)
        )
        # if QT_CONFIG(tooltip)
        self.rtb_le_Nombre.setToolTip(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Escribe el nombre del cliente", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rtb_lb_Telefono.setText(
            QCoreApplication.translate("rtb_W_GestionarReservas", "Tel\u00e9fono", None)
        )
        # if QT_CONFIG(tooltip)
        self.rtb_le_Telefono.setToolTip(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Escribe el tel\u00e9fono del cliente", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rtb_lb_FechaReserva.setText(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Fecha de la reserva", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.rtb_de_FechaReserva.setToolTip(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Indica la fecha de la reserva", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rtb_lb_TipoReserva.setText(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Tipo de reserva", None
            )
        )
        self.rtb_cb_TipoReserva.setItemText(
            0,
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Ninguno seleccionado", None
            ),
        )
        self.rtb_cb_TipoReserva.setItemText(
            1, QCoreApplication.translate("rtb_W_GestionarReservas", "Banquete", None)
        )
        self.rtb_cb_TipoReserva.setItemText(
            2, QCoreApplication.translate("rtb_W_GestionarReservas", "Jornada", None)
        )
        self.rtb_cb_TipoReserva.setItemText(
            3, QCoreApplication.translate("rtb_W_GestionarReservas", "Congreso", None)
        )

        # if QT_CONFIG(tooltip)
        self.rtb_cb_TipoReserva.setToolTip(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Selecciona el tipo de reserva", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rtb_cb_TipoReserva.setCurrentText(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Ninguno seleccionado", None
            )
        )
        self.rtb_cb_TipoReserva.setPlaceholderText("")
        self.rtb_lb_NumAsistentes.setText(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "N\u00famero de asistentes", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.rtb_sb_NumeroAsistentes.setToolTip(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas",
                "Indica el n\u00famero de asistentes (m\u00e1ximo 140)",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rtb_lb_TipoCocina.setText(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Tipo de cocina", None
            )
        )
        self.rtb_cb_TipoCocina.setItemText(
            0,
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Ninguno seleccionado", None
            ),
        )
        self.rtb_cb_TipoCocina.setItemText(
            1, QCoreApplication.translate("rtb_W_GestionarReservas", "Buf\u00e9", None)
        )
        self.rtb_cb_TipoCocina.setItemText(
            2, QCoreApplication.translate("rtb_W_GestionarReservas", "Carta", None)
        )
        self.rtb_cb_TipoCocina.setItemText(
            3,
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Pedir cita con el chef", None
            ),
        )
        self.rtb_cb_TipoCocina.setItemText(
            4, QCoreApplication.translate("rtb_W_GestionarReservas", "No precisa", None)
        )

        # if QT_CONFIG(tooltip)
        self.rtb_cb_TipoCocina.setToolTip(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Selecciona el tipo de cocina", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.rtb_pb_Reservar.setToolTip(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Guardar reserva", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rtb_pb_Reservar.setText(
            QCoreApplication.translate("rtb_W_GestionarReservas", "Reservar", None)
        )
        self.rtb_lb_ImagenReservas.setText("")
        self.rtb_le_TituloReservas.setText(
            QCoreApplication.translate("rtb_W_GestionarReservas", "Reservas", None)
        )
        # if QT_CONFIG(tooltip)
        self.rtb_pb_Volver.setToolTip(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Cerrar ventana sin guardar", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rtb_pb_Volver.setText(
            QCoreApplication.translate("rtb_W_GestionarReservas", "Volver", None)
        )
        self.rtb_gb_Congreso.setTitle(
            QCoreApplication.translate("rtb_W_GestionarReservas", "Congreso", None)
        )
        self.rtb_lb_Habitaciones.setText(
            QCoreApplication.translate("rtb_W_GestionarReservas", "Habitaciones", None)
        )
        self.rtb_lb_NumJornadas.setText(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "N\u00famero de jornadas", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.rtb_sb_NumJornadas.setToolTip(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Indica la duraci\u00f3n del congreso", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.rtb_sb_NumHabitaciones.setToolTip(
            QCoreApplication.translate(
                "rtb_W_GestionarReservas", "Indica el n\u00famero de habitaciones", None
            )
        )


# endif // QT_CONFIG(tooltip)
# retranslateUi
