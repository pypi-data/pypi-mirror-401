import sqlite3


class RTB_BaseDatos:

    def __init__(self, ruta_bd):
        self.ruta_bd = ruta_bd
        self.conexion = None
        self.puntero = None

    # Conectar a la base de datos
    def conectar(self):
        try:
            self.conexion = sqlite3.connect(self.ruta_bd)
            self.conexion.row_factory = sqlite3.Row
            return self.conexion
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    # Cerrar la conexión a la base de datos
    def cerrar(self):
        if self.conexion:
            self.conexion.close()
            self.conexion = None

    # Obtener lista de salones
    def getSalones(self):
        conn = self.conectar()
        if not conn:
            return []
        try:
            puntero = conn.cursor()
            puntero.execute("SELECT salon_id, nombre FROM salones")
            salones = puntero.fetchall()
            return salones
        finally:
            self.cerrar()

    # Obtener reservas por ID de salón
    def getReservasPorSalon(self, salon_id):
        conn = self.conectar()
        if not conn:
            return []
        try:
            puntero = conn.cursor()
            consulta = """
                SELECT
                    r.reserva_id, r.fecha, r.persona, r.telefono, tr.nombre
                FROM reservas r
                JOIN tipos_reservas tr ON r.tipo_reserva_id = tr.tipo_reserva_id
                WHERE r.salon_id = ?
                ORDER BY r.fecha DESC
            """
            puntero.execute(consulta, (salon_id,))
            reservas = puntero.fetchall()
            return reservas

        except Exception as e:
            print(f"Error en getReservasPorSalon: {e}")
            return []
        finally:
            self.cerrar()

    # Obtener datos de una reserva por su ID
    def getReservasPorId(self, reserva_id):
        conn = self.conectar()
        if not conn:
            return None
        try:
            puntero = conn.cursor()
            consulta = """
                SELECT
                    r.persona,
                    r.telefono,
                    r.fecha,
                    tr.nombre AS tipo_reserva,  
                    r.ocupacion,
                    tc.nombre AS tipo_cocina,   
                    r.jornadas,
                    r.habitaciones,
                    r.salon_id,
                    r.tipo_reserva_id,
                    r.tipo_cocina_id
                FROM
                    reservas r
                INNER JOIN
                    tipos_reservas tr ON r.tipo_reserva_id = tr.tipo_reserva_id
                INNER JOIN
                    tipos_cocina tc ON r.tipo_cocina_id = tc.tipo_cocina_id
                WHERE
                    r.reserva_id = ?
            """
            puntero.execute(consulta, (reserva_id,))
            reserva = puntero.fetchone()
            return reserva
        except Exception as e:
            print(f"Error en getReservasPorId para ID {reserva_id}: {e}")
            return None
        finally:
            self.cerrar()

    # Obtener el ID del tipo de cocina por su nombre
    def getTipoCocinaId(self, nombre_cocina):
        conn = self.conectar()
        if not conn:
            return None
        try:
            puntero = conn.cursor()
            puntero.execute(
                "SELECT tipo_cocina_id FROM tipos_cocina WHERE nombre = ?",
                (nombre_cocina,),
            )
            resultado = puntero.fetchone()
            return resultado[0] if resultado else None
        except sqlite3.Error as e:
            print(f"Error al buscar TipoCocina ID: {e}")
            return None
        finally:
            self.cerrar()

    # Obtener el ID del tipo de reserva por su nombre
    def getTipoReservaId(self, nombre_reserva):
        conn = self.conectar()
        if not conn:
            return None
        try:
            puntero = conn.cursor()
            puntero.execute(
                "SELECT tipo_reserva_id FROM tipos_reservas WHERE nombre = ?",
                (nombre_reserva,),
            )
            resultado = puntero.fetchone()
            return resultado[0] if resultado else None
        except sqlite3.Error as e:
            print(f"Error al buscar TipoReserva ID: {e}")
            return None
        finally:
            self.cerrar()

    # Obtener el ID del salón por su nombre
    def getSalonId(self, nombre_salon):
        conn = self.conectar()
        if not conn:
            return None
        try:
            puntero = conn.cursor()
            puntero.execute(
                "SELECT salon_id FROM salones WHERE nombre = ?", (nombre_salon,)
            )
            resultado = puntero.fetchone()
            return resultado[0] if resultado else None
        except sqlite3.Error as e:
            print(f"Error al buscar Salón ID: {e}")
            return None
        finally:
            self.cerrar()

    # Obtener lista de tipos de reservas
    def getListaTiposReservas(self):
        conn = self.conectar()
        if not conn:
            return []
        try:
            puntero = conn.cursor()
            puntero.execute(
                "SELECT tipo_reserva_id, nombre FROM tipos_reservas ORDER BY nombre ASC"
            )
            return puntero.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener lista de tipos de reservas: {e}")
            return []
        finally:
            self.cerrar()

    # Obtener lista de tipos de cocina
    def getListaTiposCocina(self):
        conn = self.conectar()
        if not conn:
            return []
        try:
            puntero = conn.cursor()
            puntero.execute(
                "SELECT tipo_cocina_id, nombre FROM tipos_cocina ORDER BY nombre ASC"
            )
            return puntero.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener lista de tipos de cocina: {e}")
            return []
        finally:
            self.cerrar()

    # Verificar si una fecha está disponible para una reserva en un salón específico
    def verificarFechaDisponible(self, fecha, salon_id, reserva_id_actual=None):
        conn = self.conectar()
        if not conn:
            return False

        try:
            puntero = conn.cursor()
            if reserva_id_actual is not None:
                puntero.execute(
                    "SELECT COUNT(*) as count FROM reservas WHERE fecha = ? AND salon_id = ? AND reserva_id != ?",
                    (fecha, salon_id, reserva_id_actual),
                )
            else:
                puntero.execute(
                    "SELECT COUNT(*) as count FROM reservas WHERE fecha = ? AND salon_id = ?",
                    (fecha, salon_id),
                )
            resultado = puntero.fetchone()
            return resultado[0] == 0
        except sqlite3.Error as e:
            print(f"Error al verificar disponibilidad de fecha: {e}")
            return False
        finally:
            self.cerrar()

    # Guardar nueva reserva en la base de datos
    def guardarNuevaReserva(self, datos_para_bd):
        conn = self.conectar()
        if not conn:
            return False

        consulta = """
            INSERT INTO reservas (
                tipo_reserva_id, salon_id, tipo_cocina_id, persona, 
                telefono, fecha, ocupacion, habitaciones, jornadas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        valores = (
            datos_para_bd["tipo_reserva_id"],
            datos_para_bd["salon_id"],
            datos_para_bd["tipo_cocina_id"],
            datos_para_bd["nombre"],
            datos_para_bd["telefono"],
            datos_para_bd["fecha"],
            datos_para_bd["ocupacion"],
            datos_para_bd["habitaciones"],
            datos_para_bd["jornadas"],
        )

        try:
            conn.execute(consulta, valores)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al guardar nueva reserva: {e}")
            return False
        finally:
            self.cerrar()

    # Actualizar reserva existente en la base de datos
    def actualizarReserva(self, datos_para_bd):
        conn = self.conectar()
        if not conn:
            return False

        consulta = """
            UPDATE reservas SET 
                tipo_reserva_id = ?, 
                salon_id = ?, 
                tipo_cocina_id = ?, 
                persona = ?, 
                telefono = ?, 
                fecha = ?, 
                ocupacion = ?, 
                habitaciones = ?, 
                jornadas = ?
            WHERE reserva_id = ?
        """

        valores = (
            datos_para_bd["tipo_reserva_id"],
            datos_para_bd["salon_id"],
            datos_para_bd["tipo_cocina_id"],
            datos_para_bd["nombre"],
            datos_para_bd["telefono"],
            datos_para_bd["fecha"],
            datos_para_bd["ocupacion"],
            datos_para_bd["habitaciones"],
            datos_para_bd["jornadas"],
            datos_para_bd["reserva_id"],
        )

        try:
            conn.execute(consulta, valores)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al actualizar reserva ID {datos_para_bd['reserva_id']}: {e}")
            return False
        finally:
            self.cerrar()
