from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona la Alumno de las grupos 
class AlumnoMySQL:
 
    @staticmethod
    def mostrarAlumnos():
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            #consulta MySQL
            cursor.execute("SELECT alumnogrupo.AlumnoGrupoID, alumnogrupo.AlumnoID, grupo.GrupoID, grupo.GrupoNombre, alumnogrupo.AlumnoGrupoModificacion FROM alumnogrupo INNER JOIN grupo on grupo.GrupoID = alumnogrupo.GrupoID WHERE alumnogrupo.AlumnoGrupoStatus = 'AC'")
            miResultado = cursor.fetchall()
            cone.commit()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión
    
    @staticmethod
    def ingresarAlumnos(alumno, grupo):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            # Genera un nuevo ID para el alumno
            cursor.execute("SELECT COUNT(*) FROM alumnogrupo")
            tids = cursor.fetchone()[0] + 1

            # Asignación de valores
            fechmodi = datetime.now()
            admin = '0'

            #consulta MySQL
            sql = """INSERT INTO alumnogrupo (AlumnoGrupoID, AlumnoID,
                                                GrupoID, AlumnoGrupoModificacion,
                                                AlumnoGrupoStatus, PersonalAdministrativoId) 
                                VALUES (%s, %s, %s, %s, 'AC', %s)"""
            values = (tids, alumno, grupo, fechmodi, admin)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Ahora hay {tids} registros en la tabla")

        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def modificarAlumno(alumno, grupo, id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            
            # Asignación de valores
            fechmodi = datetime.now() 
            admin = '0'

            #consulta MySQL
            sql ="""UPDATE alumnogrupo 
                    SET AlumnoID = %s, GrupoID = %s, 
                        AlumnoGrupoModificacion = %s, PersonalAdministrativoId = %s 
                    WHERE AlumnoGrupoID = %s"""
            values = (alumno, grupo, fechmodi, admin, id)

            cursor.execute(sql, values)
            cone.commit()
            print(f"AlumnoGrupo con ID {id} fue actualizado.")

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def eliminarAlumno(id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            admin = "0"
            fechmodi = datetime.now()

            #consulta MySQL
            sql = "UPDATE alumnogrupo SET AlumnoGrupoModificacion = %s, AlumnoGrupoStatus = 'IN', PersonalAdministrativoId = %s WHERE AlumnoGrupoID = %s"
            values = (fechmodi,admin,id)

            cursor.execute(sql, values)
            cone.commit()
            print(f"AlumnoGrupo con ID {id} fue eliminado.")
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión