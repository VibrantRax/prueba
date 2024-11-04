from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql
import requests

# Clase que gestiona la Alumno de las grupos 
class AlumnoMySQL:

    @staticmethod
    def mostrarAlumnos():
        try:

            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                #consulta MySQL
                    cursor.execute("SELECT alumnogrupo.*, grupo.GrupoID, grupo.GrupoNombre FROM alumnogrupo INNER JOIN grupo ON grupo.GrupoID = alumnogrupo.GrupoID WHERE alumnogrupo.AlumnoGrupoStatus = 'AC'")
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
    def mostrarAlumnosporID(id):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                # Consulta MySQL
                sql = """
                SELECT alumnogrupo.*, grupo.GrupoID, grupo.GrupoNombre 
                FROM alumnogrupo 
                INNER JOIN grupo ON grupo.GrupoID = alumnogrupo.GrupoID
                WHERE alumnogrupo.AlumnoGrupoID = %s AND alumnogrupo.AlumnoGrupoStatus = 'AC'
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
    def ingresarAlumnos(data, personal):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(AlumnoGrupoID) FROM alumnogrupo")
                max_id = cursor.fetchone()['MAX(AlumnoGrupoID)'] or 4000
                
                # Asignación de valores
                new_id = max_id + 1
                fechmodi = datetime.now()
                status = 'AC'

                #consulta MySQL
                sql = """INSERT INTO alumnogrupo (AlumnoGrupoID, AlumnoID,
                                                    GrupoID, AlumnoGrupoModificacion,
                                                    AlumnoGrupoStatus, PersonalAdministrativoId) 
                                    VALUES (%s, %s, %s, %s, %s, %s)"""
                values = (new_id, data['AlumnoID'], data['GrupoID'], fechmodi, status, personal)

                cursor.execute(sql, values)
                cone.commit()

                return new_id
            
        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def modificarAlumno(data, id, personal):
        try:
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql ="""UPDATE alumnogrupo 
                        SET AlumnoID = %s, GrupoID = %s, 
                            AlumnoGrupoModificacion = %s, PersonalAdministrativoId = %s 
                        WHERE AlumnoGrupoID = %s"""
                values = (data['AlumnoID'], data['GrupoID'], fechmodi, personal, id)

                cursor.execute(sql, values)
                cone.commit()

            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def eliminarAlumno(id, personal):
        try:
            #asignacion de valores
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql = "UPDATE alumnogrupo SET AlumnoGrupoModificacion = %s, AlumnoGrupoStatus = 'IN', PersonalAdministrativoId = %s WHERE AlumnoGrupoID = %s"
                values = (fechmodi,personal,id)
                
                cursor.execute(sql, values)
                cone.commit()
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión