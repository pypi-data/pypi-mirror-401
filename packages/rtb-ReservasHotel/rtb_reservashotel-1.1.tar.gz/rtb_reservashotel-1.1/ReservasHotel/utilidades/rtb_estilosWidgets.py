from PySide6 import QtWidgets as qtw


def estilosTabla(tabla: qtw.QTableWidget):

    tabla.setStyleSheet(
        f"""
            QTableWidget {{
                background-color: white;
                alternate-background-color: rgba(201, 204, 255,.5);
                gridline-color: rgb(120, 90, 180);
            }}

            QHeaderView::section {{
                background-color: rgb(190, 190, 255);
                color: white;
                padding: 3px;                
                font-size: 11pt;
                text-align: center;
            }}

            QTableWidget::item {{
                padding: 3px;
            }}
        """
    )
    tabla.setAlternatingRowColors(True)
    tabla.horizontalHeader().setStretchLastSection(True)
    tabla.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
    tabla.verticalHeader().setVisible(False)
    tabla.verticalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeToContents)


def estilosCalendario(calendario: qtw.QWidget):
    calendario.setStyleSheet(
        f"""
            QDateEdit {{
            background-color: white;
            color: black;            
            font-size: 11pt;    
            padding: 1px;                   
            }}
            QCalendarWidget QWidget#qt_calendar_navigationbar {{
                background-color: rgb(190, 190, 255);
                color: black;  
                font-size: 11pt;           
            }}
        """
    )
