import sqlite3
import os


class tl_Datos:
    """
    Clase de acceso a datos.
    Crea la base de datos a partir del script SQL si no existe.
    """

    def __init__(self):
        self.ruta_sql = "bbdd/reservas.sql"
        self.ruta_bd = "bbdd/reservas.sqlite"
        self.conexion = None

    def conectar(self):
        """
        Conecta con la base de datos.
        Si no existe, la crea usando el script SQL.
        """
        crear_bd = not os.path.exists(self.ruta_bd)

        self.conexion = sqlite3.connect(self.ruta_bd)

        if crear_bd:
            self._crear_bd_desde_sql()

    
    def obtener_salones(self):
        """
        Devuelve todos los salones.
        """
        consulta = "SELECT salon_id, nombre FROM salones ORDER BY nombre"
        cursor = self.conexion.cursor()
        cursor.execute(consulta)
        return cursor.fetchall()
    
    
    def obtener_reservas_por_salon(self, salon_id):
        """
        Devuelve las reservas de un salón ordenadas por fecha descendente.
        """
        consulta = """
            SELECT r.reserva_id,
                r.fecha,
                r.persona,
                r.telefono,
                tr.nombre
            FROM reservas r
            JOIN tipos_reservas tr
                ON r.tipo_reserva_id = tr.tipo_reserva_id
            WHERE r.salon_id = ?
            ORDER BY r.fecha DESC
        """
        cursor = self.conexion.cursor()
        cursor.execute(consulta, (salon_id,))
        return cursor.fetchall()


    def _crear_bd_desde_sql(self):
        """
        Crea la base de datos ejecutando el script SQL.
        """
        with open(self.ruta_sql, "r", encoding="utf-8") as f:
            sql_script = f.read()

        cursor = self.conexion.cursor()
        cursor.executescript(sql_script)
        self.conexion.commit()


    def cerrar(self):
        if self.conexion:
            self.conexion.close()


    def obtener_tipos_reserva(self):
        """
        Devuelve todos los tipos de reserva.
        """
        consulta = """
            SELECT tipo_reserva_id, nombre, requiere_jornadas, requiere_habitaciones
            FROM tipos_reservas
            ORDER BY nombre
        """
        cursor = self.conexion.cursor()
        cursor.execute(consulta)
        return cursor.fetchall()


    def obtener_tipos_cocina(self):
        """
        Devuelve todos los tipos de cocina.
        """
        consulta = """
            SELECT tipo_cocina_id, nombre
            FROM tipos_cocina
            ORDER BY nombre
        """
        cursor = self.conexion.cursor()
        cursor.execute(consulta)
        return cursor.fetchall()
    

    def insertar_reserva(
        self,
        tipo_reserva_id,
        salon_id,
        tipo_cocina_id,
        persona,
        telefono,
        fecha,
        ocupacion,
        jornadas,
        habitaciones
    ):
        """
        Inserta una nueva reserva en la base de datos.
        """
        try:
            consulta = """
                INSERT INTO reservas (
                    tipo_reserva_id,
                    salon_id,
                    tipo_cocina_id,
                    persona,
                    telefono,
                    fecha,
                    ocupacion,
                    jornadas,
                    habitaciones
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor = self.conexion.cursor()
            cursor.execute(
                consulta,
                (
                    tipo_reserva_id,
                    salon_id,
                    tipo_cocina_id,
                    persona,
                    telefono,
                    fecha,
                    ocupacion,
                    jornadas,
                    habitaciones
                )
            )
            self.conexion.commit()
            return True

        except Exception as e:
            mensaje = str(e)

            # Error de clave única: mismo salón + misma fecha
            if "UNIQUE constraint failed" in mensaje:
                return "El salón ya está reservado para la fecha seleccionada."

            # Cualquier otro error
            return "Se ha producido un error al guardar la reserva."
        

    def obtener_reserva_por_id(self, reserva_id):
        """
        Devuelve una reserva por su ID.
        """
        consulta = """
            SELECT
                reserva_id,
                tipo_reserva_id,
                tipo_cocina_id,
                persona,
                telefono,
                fecha,
                ocupacion,
                jornadas,
                habitaciones
            FROM reservas
            WHERE reserva_id = ?
        """
        cursor = self.conexion.cursor()
        cursor.execute(consulta, (reserva_id,))
        return cursor.fetchone()
    

    def actualizar_reserva(
        self,
        reserva_id,
        tipo_reserva_id,
        salon_id,
        tipo_cocina_id,
        persona,
        telefono,
        fecha,
        ocupacion,
        jornadas,
        habitaciones
    ):
        try:
            consulta = """
                UPDATE reservas
                SET
                    tipo_reserva_id = ?,
                    salon_id = ?,
                    tipo_cocina_id = ?,
                    persona = ?,
                    telefono = ?,
                    fecha = ?,
                    ocupacion = ?,
                    jornadas = ?,
                    habitaciones = ?
                WHERE reserva_id = ?
            """
            cursor = self.conexion.cursor()
            cursor.execute(
                consulta,
                (
                    tipo_reserva_id,
                    salon_id,
                    tipo_cocina_id,
                    persona,
                    telefono,
                    fecha,
                    ocupacion,
                    jornadas,
                    habitaciones,
                    reserva_id
                )
            )
            self.conexion.commit()
            return True

        except Exception as e:
            mensaje = str(e)
            if "UNIQUE constraint failed" in mensaje:
                return "El salón ya está reservado para la fecha seleccionada."
            return "No se ha podido actualizar la reserva."




