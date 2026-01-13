import os
import sys
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from hotel.modelos.datos import tl_Datos
from hotel.vistas.vreservar import tl_VReservar


def ruta_recurso(ruta_relativa):
    """
    Devuelve la ruta correcta tanto en desarrollo como en PyInstaller
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ruta_relativa
    )


class tl_VMostrarReservas(QDialog):
    """
    Ventana Mostrar Reservas.
    """

    def __init__(self):
        super().__init__()
        self._cargar_ui()
        self._conectar_eventos()

    def _cargar_ui(self):
        """
        Carga el archivo frmmostrarreservas.ui
        """
        loader = QUiLoader()

        # 🔑 Cargar UI SIN pasar self como parent
        ruta_ui = ruta_recurso(os.path.join("ui", "frmmostrarreservas.ui"))
        archivo_ui = QFile(ruta_ui)
        archivo_ui.open(QFile.ReadOnly)

        self.ui = loader.load(archivo_ui)
        archivo_ui.close()

        # 🔑 Layout correcto
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)
        self.setLayout(layout)

        self.setWindowTitle(self.ui.windowTitle())
        self.resize(self.ui.sizeHint())

    def _conectar_eventos(self):
        """
        Carga salones y conecta eventos.
        """
        self._cargar_salones()
        self.ui.tl_lstSalones.currentRowChanged.connect(self._salon_seleccionado)
        self.ui.tl_btnReservar.clicked.connect(self._abrir_reservar)
        self.ui.tl_tblReservas.cellDoubleClicked.connect(self._editar_reserva)

    def _abrir_reservar(self):
        """
        Abre la ventana de nueva reserva.
        """
        fila = self.ui.tl_lstSalones.currentRow()
        if fila < 0:
            return

        datos = tl_Datos()
        datos.conectar()
        salones = datos.obtener_salones()
        salon_id = salones[fila][0]
        datos.cerrar()

        ventana = tl_VReservar(salon_id)
        ventana.exec()

        # Al volver, recargar reservas
        self._salon_seleccionado(fila)

    def _cargar_salones(self):
        """
        Carga los salones desde la base de datos en la lista.
        """
        datos = tl_Datos()
        datos.conectar()

        salones = datos.obtener_salones()
        self.ui.tl_lstSalones.clear()

        for salon in salones:
            self.ui.tl_lstSalones.addItem(salon[1])

        datos.cerrar()

    def _salon_seleccionado(self, fila):
        """
        Se ejecuta al seleccionar un salón de la lista.
        """
        if fila < 0:
            return

        datos = tl_Datos()
        datos.conectar()
        salones = datos.obtener_salones()
        salon_id = salones[fila][0]
        datos.cerrar()

        self._cargar_reservas(salon_id)

    def _cargar_reservas(self, salon_id):
        """
        Carga las reservas del salón seleccionado en la tabla.
        """
        datos = tl_Datos()
        datos.conectar()

        reservas = datos.obtener_reservas_por_salon(salon_id)

        tabla = self.ui.tl_tblReservas
        tabla.setRowCount(0)
        tabla.setColumnCount(4)

        tabla.setHorizontalHeaderLabels([
            "Fecha",
            "Persona",
            "Teléfono",
            "Tipo de reserva"
        ])

        for fila, reserva in enumerate(reservas):
            tabla.insertRow(fila)
            tabla.setItem(fila, 0, QTableWidgetItem(reserva[1]))
            tabla.item(fila, 0).setData(256, reserva[0])  # Qt.UserRole
            tabla.setItem(fila, 1, QTableWidgetItem(reserva[2]))
            tabla.setItem(fila, 2, QTableWidgetItem(reserva[3]))
            tabla.setItem(fila, 3, QTableWidgetItem(reserva[4]))

        datos.cerrar()

    def _editar_reserva(self, fila, columna):
        """
        Abre la ventana Reservar en modo edición.
        """
        item = self.ui.tl_tblReservas.item(fila, 0)
        if not item:
            return

        reserva_id = item.data(256)

        fila_salon = self.ui.tl_lstSalones.currentRow()
        if fila_salon < 0:
            return

        datos = tl_Datos()
        datos.conectar()
        salones = datos.obtener_salones()
        salon_id = salones[fila_salon][0]
        datos.cerrar()

        ventana = tl_VReservar(salon_id, reserva_id)
        ventana.exec()

        self._salon_seleccionado(fila_salon)






