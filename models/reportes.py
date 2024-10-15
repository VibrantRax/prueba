from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona los reportes
class ReportesMySQL:

    @staticmethod
    def mostrarReportesResueltos():
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            #consulta MySQL
            cursor.execute("SELECT ReporteID, AlumnoID, ReporteFecha, ReporteDescripcion, ReporteAccionTomada, ReporteFechaModificacion, ReporteStatus FROM reporte WHERE ReporteStatus = 'AC'")
            miResultado = cursor.fetchall()
            cone.commit()
            return miResultado

        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def mostrarReportes():
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            #consulta MySQL
            cursor.execute("SELECT ReporteID, AlumnoID, ReporteFecha, ReporteDescripcion, ReporteAccionTomada, ReporteFechaModificacion, ReporteStatus FROM reporte WHERE ReporteStatus = 'AN'")
            miResultado = cursor.fetchall()
            cone.commit()
            return miResultado

        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def ingresarReportes(alumno, fecha, descripcion, accion, status):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            # Genera un nuevo ID para el reporte
            cursor.execute("SELECT COUNT(*) FROM reporte")
            tids = cursor.fetchone()[0] + 1

            # Asignación de valores
            fechmodi = datetime.now() 
            admin = '0'

            #consulta MySQL
            sql = """INSERT INTO reporte (ReporteID, AlumnoID, ReporteFecha, ReporteDescripcion, 
                                           ReporteAccionTomada, ReporteFechaModificacion, 
                                           ReporteStatus, PersonalAdministrativoId) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (tids, alumno, fecha, descripcion, accion or "Sin acción tomada", fechmodi, status, admin)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Ahora hay {tids} registros en la tabla")

        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión
    
    @staticmethod
    def modificarReporte(id,alumno,fecha,descripcion,accion,status):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            # Asignación de valores
            fechmodi = datetime.now() 
            admin = '0'

            #consulta MySQL
            sql ="""UPDATE reporte 
                    SET ReporteFecha = %s, ReporteDescripcion = %s, 
                        ReporteAccionTomada = %s, ReporteFechaModificacion = %s, 
                        ReporteStatus = %s, PersonalAdministrativoId = %s 
                    WHERE ReporteID = %s"""
            values = (fecha, descripcion, accion or "Sin acción tomada", fechmodi, status, admin,id)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Reporte con ID {id} fue actualizado.")

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def eliminarReporte(id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            admin = "0"
            fechmodi = datetime.now()

            #consulta MySQL
            sql = "UPDATE reporte SET ReporteFechaModificacion = %s, ReporteStatus = 'IN', PersonalAdministrativoId = %s WHERE ReporteID = %s"
            values = (fechmodi,admin,id)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Reporte con ID {id} fue eliminado.")

        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión