import os
import sys
from PySide6.QtWidgets import QDialog, QVBoxLayout, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


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


class tl_VLogin(QDialog):
    """
    Ventana de inicio de sesión.
    """

    def __init__(self):
        super().__init__()
        self._cargar_ui()
        self._conectar_eventos()

    def _cargar_ui(self):
        loader = QUiLoader()

        # 🔑 Cargar UI SIN pasar self como parent
        ruta_ui = ruta_recurso(os.path.join("ui", "frmlogin.ui"))
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
        self.ui.tl_btnEntrar.clicked.connect(self._validar_login)

    def _validar_login(self):
        usuario = self.ui.tl_txtUsuario.text().strip()
        password = self.ui.tl_txtPassword.text().strip()

        if usuario == "hotel" and password == "Brianda23$":
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Acceso denegado",
                "Usuario o contraseña incorrectos"
            )

