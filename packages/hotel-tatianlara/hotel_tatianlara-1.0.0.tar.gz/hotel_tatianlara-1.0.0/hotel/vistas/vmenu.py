import os
import sys
from PySide6.QtWidgets import QDialog, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QPalette, QColor, QPixmap

from hotel.vistas.vmostrarreservas import tl_VMostrarReservas


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


class tl_VMenu(QDialog):
    """
    Ventana de menú principal.
    """

    def __init__(self):
        super().__init__()
        self._cargar_ui()
        self._conectar_eventos()

    def _cargar_ui(self):
        loader = QUiLoader()

        # 🔑 Cargar UI SIN pasar self como parent
        ruta_ui = ruta_recurso(os.path.join("ui", "frmmenu.ui"))
        archivo_ui = QFile(ruta_ui)
        archivo_ui.open(QFile.ReadOnly)

        self.ui = loader.load(archivo_ui)
        archivo_ui.close()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)
        self.setLayout(layout)

        self.setWindowTitle(self.ui.windowTitle())
        self.resize(self.ui.sizeHint())

        # Fondo de la ventana
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#F4F6F8"))
        self.setPalette(palette)

        # Cargar imagen del menú
        ruta_img = ruta_recurso(os.path.join("img", "imagen_menu.png"))
        pixmap = QPixmap(ruta_img)
        self.ui.tl_lblImagenMenu.setPixmap(pixmap)
        self.ui.tl_lblImagenMenu.setScaledContents(True)

    def _conectar_eventos(self):
        """
        Conecta los botones del menú.
        """
        self.ui.tl_btnReservas.clicked.connect(self._abrir_reservas)

    def _abrir_reservas(self):
        """
        Abre la ventana MostrarReservas en modo modal.
        """
        ventana = tl_VMostrarReservas()
        ventana.exec()




