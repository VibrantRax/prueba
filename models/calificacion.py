from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona las calificaciones
class CalificacionesMySQL:
    
    @staticmethod
    def mostrarCalificaciones():
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            #consulta MySQL
            cursor.execute("SELECT calificacion.CalificacionID, calificacion.AlumnoID, materia.MateriaID, materia.MateriaNombre, calificacion.CalificacionDetalle, calificacion.CalificacionFechaModificacion FROM calificacion INNER JOIN materia ON materia.MateriaID = calificacion.CalificacionID WHERE calificacion.CalificacionStatus = 'AC'")
            miResultado = cursor.fetchall()
            cone.commit()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def ingresarCalificacion(alumno, materia, calificacion):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            # Genera un nuevo ID para el grupo
            cursor.execute("SELECT COUNT(*) FROM calificacion")
            tids = cursor.fetchone()[0] + 1

            # Asignación de valores
            fechmodi = datetime.now()  
            admin = '0'


            #consulta MySQL
            sql = """INSERT INTO calificacion (CalificacionID, AlumnoID, MateriaID, 
                                                CalificacionDetalle, CalificacionFechaModificacion, 
                                                CalificacionStatus, PersonalAdministrativoId) 
                                VALUES (%s, %s, %s, %s, %s, 'AC', %s)"""
            values = (tids, alumno, materia, calificacion, fechmodi, admin)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Ahora hay {tids} registros en la tabla")

        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def modificarCalificacion(alumno, materia, calificacion, id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            
            # Asignación de valores
            fechmodi = datetime.now() 
            admin = '0'


            #consulta MySQL
            sql ="""UPDATE calificacion 
                    SET AlumnoID = %s, MateriaID = %s, CalificacionDetalle = %s, 
                        CalificacionFechaModificacion = %s, PersonalAdministrativoId = %s 
                    WHERE CalificacionID = %s"""
            values = (alumno, materia, calificacion, fechmodi, admin, id)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Calificacion con ID {id} fue actualizada.")

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def eliminarCalificacion(id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            admin = "0"
            fechmodi = datetime.now()

            #consulta MySQL
            sql = "UPDATE calificacion SET CalificacionFechaModificacion = %s, CalificacionStatus = 'IN', PersonalAdministrativoId = %s WHERE CalificacionID = %s"
            values = (fechmodi,admin,id)
            
            cursor.execute(sql, values)
            cone.commit()
            print(f"Calificacion con ID {id} fue eliminada.")
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión


