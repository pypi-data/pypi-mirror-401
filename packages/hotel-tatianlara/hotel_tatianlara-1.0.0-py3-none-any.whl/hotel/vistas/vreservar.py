import os
import sys
from PySide6.QtWidgets import QDialog, QVBoxLayout, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QDate

from hotel.modelos.datos import tl_Datos


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


class tl_VReservar(QDialog):
    """
    Ventana para crear / editar una reserva.
    """

    def __init__(self, salon_id, reserva_id=None):
        super().__init__()
        self.salon_id = salon_id
        self.reserva_id = reserva_id
        self._cargar_ui()
        self._conectar_eventos()

        if self.reserva_id:
            self._cargar_datos_reserva()

    def _cargar_ui(self):
        """
        Carga el archivo frmreservar.ui
        """
        loader = QUiLoader()

        # 🔑 Cargar UI SIN pasar self como parent
        ruta_ui = ruta_recurso(os.path.join("ui", "frmreservar.ui"))
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

        self.ui.tl_grpCongreso.setEnabled(False)

    def _conectar_eventos(self):
        """
        Conecta eventos y carga combos.
        """
        self.ui.tl_btnVolver.clicked.connect(self.reject)
        self.ui.tl_btnGuardar.clicked.connect(self._guardar)

        self._cargar_tipos_reserva()
        self._cargar_tipos_cocina()

        self.ui.tl_cmbTipoReserva.currentIndexChanged.connect(
            self._tipo_reserva_cambiado
        )

        self._tipo_reserva_cambiado(
            self.ui.tl_cmbTipoReserva.currentIndex()
        )

    def _cargar_tipos_reserva(self):
        """
        Carga los tipos de reserva en el combo.
        """
        datos = tl_Datos()
        datos.conectar()

        tipos = datos.obtener_tipos_reserva()
        self.ui.tl_cmbTipoReserva.clear()

        for tipo in tipos:
            self.ui.tl_cmbTipoReserva.addItem(tipo[1], tipo)

        datos.cerrar()

    def _cargar_tipos_cocina(self):
        """
        Carga los tipos de cocina en el combo.
        """
        datos = tl_Datos()
        datos.conectar()

        cocinas = datos.obtener_tipos_cocina()
        self.ui.tl_cmbTipoCocina.clear()

        for cocina in cocinas:
            self.ui.tl_cmbTipoCocina.addItem(cocina[1], cocina[0])

        datos.cerrar()

    def _tipo_reserva_cambiado(self, index):
        """
        Activa o desactiva las opciones de Congreso según el tipo seleccionado.
        """
        tipo = self.ui.tl_cmbTipoReserva.itemData(index)

        if not tipo:
            return

        requiere_jornadas = tipo[2]
        requiere_habitaciones = tipo[3]

        self.ui.tl_grpCongreso.setEnabled(
            requiere_jornadas or requiere_habitaciones
        )

    def _cargar_datos_reserva(self):
        """
        Carga los datos de la reserva en el formulario para edición.
        """
        datos = tl_Datos()
        datos.conectar()

        reserva = datos.obtener_reserva_por_id(self.reserva_id)
        datos.cerrar()

        if not reserva:
            return

        (
            reserva_id,
            tipo_reserva_id,
            tipo_cocina_id,
            persona,
            telefono,
            fecha,
            ocupacion,
            jornadas,
            habitaciones
        ) = reserva

        self.ui.tl_txtPersona.setText(persona)
        self.ui.tl_txtTelefono.setText(telefono)
        self.ui.tl_spnOcupacion.setValue(ocupacion)
        self.ui.tl_spnJornadas.setValue(jornadas)
        self.ui.tl_chkHabitaciones.setChecked(bool(habitaciones))

        self.ui.tl_datFecha.setDate(
            QDate.fromString(fecha, "dd/MM/yyyy")
        )

        for i in range(self.ui.tl_cmbTipoReserva.count()):
            if self.ui.tl_cmbTipoReserva.itemData(i)[0] == tipo_reserva_id:
                self.ui.tl_cmbTipoReserva.setCurrentIndex(i)
                break

        for i in range(self.ui.tl_cmbTipoCocina.count()):
            if self.ui.tl_cmbTipoCocina.itemData(i) == tipo_cocina_id:
                self.ui.tl_cmbTipoCocina.setCurrentIndex(i)
                break

    def _guardar(self):
        """
        Guarda la reserva en la base de datos tras validar.
        """
        if not self.ui.tl_txtPersona.text().strip():
            QMessageBox.warning(self, "Datos incompletos", "Debe introducir el nombre.")
            return

        if not self.ui.tl_txtTelefono.text().strip():
            QMessageBox.warning(self, "Datos incompletos", "Debe introducir el teléfono.")
            return

        if self.ui.tl_spnOcupacion.value() <= 0:
            QMessageBox.warning(self, "Datos incorrectos", "El número de personas debe ser mayor que 0.")
            return

        if self.ui.tl_grpCongreso.isEnabled() and self.ui.tl_spnJornadas.value() <= 0:
            QMessageBox.warning(self, "Datos incorrectos", "Debe indicar el número de jornadas.")
            return

        persona = self.ui.tl_txtPersona.text().strip()
        telefono = self.ui.tl_txtTelefono.text().strip()
        fecha = self.ui.tl_datFecha.date().toString("dd/MM/yyyy")
        ocupacion = self.ui.tl_spnOcupacion.value()

        tipo_reserva = self.ui.tl_cmbTipoReserva.currentData()
        tipo_reserva_id = tipo_reserva[0]
        tipo_cocina_id = self.ui.tl_cmbTipoCocina.currentData()

        jornadas = self.ui.tl_spnJornadas.value() if self.ui.tl_grpCongreso.isEnabled() else 0
        habitaciones = 1 if self.ui.tl_grpCongreso.isEnabled() and self.ui.tl_chkHabitaciones.isChecked() else 0

        datos = tl_Datos()
        datos.conectar()

        if self.reserva_id:
            resultado = datos.actualizar_reserva(
                self.reserva_id,
                tipo_reserva_id,
                self.salon_id,
                tipo_cocina_id,
                persona,
                telefono,
                fecha,
                ocupacion,
                jornadas,
                habitaciones
            )
        else:
            resultado = datos.insertar_reserva(
                tipo_reserva_id,
                self.salon_id,
                tipo_cocina_id,
                persona,
                telefono,
                fecha,
                ocupacion,
                jornadas,
                habitaciones
            )

        datos.cerrar()

        if resultado is True:
            QMessageBox.information(self, "Reserva creada", "La reserva se ha creado correctamente.")
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "Error al crear la reserva",
                "No se ha podido crear la reserva.\n\nMotivo:\n" + str(resultado)
            )
