from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql
import requests

# Clase que gestiona las calificaciones
class CalificacionesMySQL:
    
    @staticmethod
    def mostrarCalificaciones():
        try:

            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                #consulta MySQL
                    cursor.execute("SELECT calificacion.* , materia.MateriaID, materia.MateriaNombre FROM calificacion INNER JOIN materia ON materia.MateriaID = calificacion.MateriaID WHERE calificacion.CalificacionStatus = 'AC'")
                    miResultado = cursor.fetchall()

                    alumnos_info = {}

                    response = requests.get('http://34.176.222.47:5000/alumnos')
                    if response.status_code == 200:
                        alumnos = response.json()
                        # Guardar en un diccionario para acceso rápido
                        for alumno in alumnos:
                            alumnos_info[alumno['AlumnoId']] = {
                                "Nombre": alumno['AlumnoNombre'],
                                "PrimerApellido": alumno['AlumnoPrimerApellido'],
                                "SegundoApellido": alumno['AlumnoSegundoApellido']
                            }

                    # Combinar la información de grupos con la de docentes
                    for alumno in miResultado:
                        alumno_id = alumno['AlumnoID']
                        if alumno_id in alumnos_info:
                            alumno['AlumnoNombreCompleto'] = f"{alumnos_info[alumno_id]['Nombre']} {alumnos_info[alumno_id]['PrimerApellido']} {alumnos_info[alumno_id]['SegundoApellido']}"
                        else:
                            alumno['AlumnoNombreCompleto'] = "Desconocido"
                    
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def mostrarCalificacionesporID(id):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                # Consulta MySQL
                sql = """
                SELECT calificacion.* , materia.MateriaID, materia.MateriaNombre
                FROM calificacion
                INNER JOIN materia ON materia.MateriaID = calificacion.MateriaID
                WHERE calificacion.CalificacionID = %s AND calificacion.CalificacionStatus = 'AC'
                """

                values = (id,)
                cursor.execute(sql, values)

                miResultado = cursor.fetchone()

                if not miResultado:
                    return None  # O manejar el caso donde no se encuentra el grupo

                # Obtener información de los alumnos
                alumnos_info = {}
                response = requests.get('http://34.176.222.47:5000/alumnos')
                if response.status_code == 200:
                    alumnos = response.json()
                    # Guardar en un diccionario para acceso rápido
                    for alumno in alumnos:
                        alumnos_info[alumno['AlumnoId']] = {
                            "Nombre": alumno['AlumnoNombre'],
                            "PrimerApellido": alumno['AlumnoPrimerApellido'],
                            "SegundoApellido": alumno['AlumnoSegundoApellido']
                        }

                # Combinar la información del grupo con la de alumnos
                alumno_id = miResultado['AlumnoID']
                if alumno_id in alumnos_info:
                    miResultado['AlumnoNombreCompleto'] = f"{alumnos_info[alumno_id]['Nombre']} {alumnos_info[alumno_id]['PrimerApellido']} {alumnos_info[alumno_id]['SegundoApellido']}"
                else:
                    miResultado['AlumnoNombreCompleto'] = "Desconocido"

            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def ingresarCalificacion(data, personal):
        try:

            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(CalificacionID) FROM calificacion")
                max_id = cursor.fetchone()['MAX(CalificacionID)'] or 4000
                
                # Asignación de valores
                new_id = max_id + 1
                fechmodi = datetime.now()
                status = 'AC'

                #consulta MySQL
                sql = """INSERT INTO calificacion (CalificacionID, AlumnoID, MateriaID, 
                                                    CalificacionDetalle, CalificacionFechaModificacion, 
                                                    CalificacionStatus, PersonalAdministrativoId) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                values = (new_id, data['AlumnoID'], data['MateriaID'], data['CalificacionDetalle'], fechmodi, status, personal)

                cursor.execute(sql, values)
                cone.commit()

                return new_id

        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def modificarCalificacion(data, id, personal):
        try:

            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql ="""UPDATE calificacion 
                    SET AlumnoID = %s, MateriaID = %s, CalificacionDetalle = %s, 
                        CalificacionFechaModificacion = %s, PersonalAdministrativoId = %s 
                    WHERE CalificacionID = %s"""
                values = (data['AlumnoID'], data['MateriaID'], data['CalificacionDetalle'], fechmodi, personal, id)

                cursor.execute(sql, values)
                cone.commit()

            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def eliminarCalificacion(id, personal):
        try:
        
            #asignacion de valores
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql = "UPDATE calificacion SET CalificacionFechaModificacion = %s, CalificacionStatus = 'IN', PersonalAdministrativoId = %s WHERE CalificacionID = %s"
                values = (fechmodi,personal,id)
                
                cursor.execute(sql, values)
                cone.commit()
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión
