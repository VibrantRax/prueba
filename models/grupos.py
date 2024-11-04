from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql
import requests

# Clase que gestiona los grupos
class GruposMySQL:
    
    @staticmethod
    def mostrarGrupos():
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                #consulta MySQL
                    cursor.execute("SELECT grupo.*, salon.SalonID, salon.SalonNumero, edificio.EdificioID, edificio.EdificioNombre FROM `grupo` INNER JOIN salon on salon.SalonID = grupo.SalonID INNER JOIN edificio ON edificio.EdificioID = salon.EdificioID WHERE grupo.GrupoStatus = 'AC'")
                    miResultado = cursor.fetchall()

                    docentes_info = {}

                    response = requests.get('http://34.176.222.47:5000/docentes')
                    if response.status_code == 200:
                        docentes = response.json()
                        # Guardar en un diccionario para acceso rápido
                        for docente in docentes:
                            docentes_info[docente['DocenteId']] = {
                                "Nombre": docente['DocenteNombre'],
                                "PrimerApellido": docente['DocentePrimerApellido'],
                                "SegundoApellido": docente['DocenteSegundoApellido']
                            }

                    # Combinar la información de grupos con la de docentes
                    for grupo in miResultado:
                        docente_id = grupo['DocenteId']
                        if docente_id in docentes_info:
                            grupo['DocenteNombreCompleto'] = f"{docentes_info[docente_id]['Nombre']} {docentes_info[docente_id]['PrimerApellido']} {docentes_info[docente_id]['SegundoApellido']}"
                        else:
                            grupo['DocenteNombreCompleto'] = "Desconocido"
                    
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def mostrarGruposporID(id):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                # Consulta MySQL
                sql = """
                SELECT grupo.*, salon.SalonID, salon.SalonNumero, edificio.EdificioID, edificio.EdificioNombre 
                FROM `grupo` 
                INNER JOIN salon ON salon.SalonID = grupo.SalonID 
                INNER JOIN edificio ON edificio.EdificioID = salon.EdificioID 
                WHERE grupo.GrupoID = %s AND grupo.GrupoStatus = 'AC'
                """
                values = (id,)
                cursor.execute(sql, values)

                miResultado = cursor.fetchone()

                if not miResultado:
                    return None  # O manejar el caso donde no se encuentra el grupo

                # Obtener información de los docentes
                docentes_info = {}
                response = requests.get('http://34.176.222.47:5000/docentes')
                if response.status_code == 200:
                    docentes = response.json()
                    # Guardar en un diccionario para acceso rápido
                    for docente in docentes:
                        docentes_info[docente['DocenteId']] = {
                            "Nombre": docente['DocenteNombre'],
                            "PrimerApellido": docente['DocentePrimerApellido'],
                            "SegundoApellido": docente['DocenteSegundoApellido']
                        }

                # Combinar la información del grupo con la de docentes
                docente_id = miResultado['DocenteId']
                if docente_id in docentes_info:
                    miResultado['DocenteNombreCompleto'] = f"{docentes_info[docente_id]['Nombre']} {docentes_info[docente_id]['PrimerApellido']} {docentes_info[docente_id]['SegundoApellido']}"
                else:
                    miResultado['DocenteNombreCompleto'] = "Desconocido"

            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def ingresarGrupos(data, personal):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(GrupoID) FROM grupo")
                max_id = cursor.fetchone()['MAX(GrupoID)'] or 4000
                
                # Asignación de valores
                new_id = max_id + 1
                fechmodi = datetime.now()
                status = 'AC'

                # Consulta MySQL
                sql = """INSERT INTO grupo (GrupoID, DocenteId, GrupoNombre, SalonID, 
                                            GrupoFechaModificacion, GrupoStatus, 
                                            PersonalAdministrativoId) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                values = (new_id, data['DocenteId'], data['GrupoNombre'], data['SalonID'], fechmodi, status, personal)

                cursor.execute(sql, values)
                cone.commit()

                return new_id

        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")
            raise  # Lanza la excepción para que pueda ser manejada por el llamador

        finally:
            cursor.close()
            cone.close()


    @staticmethod
    def modificarGrupo(data, id, personal):
        try:
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql = """UPDATE grupo 
                        SET DocenteId = %s, GrupoNombre = %s, SalonID = %s, 
                            GrupoFechaModificacion = %s, PersonalAdministrativoId = %s 
                        WHERE GrupoID = %s"""
                values = (data['DocenteId'], data['GrupoNombre'], data['SalonID'], fechmodi, personal, id)

                cursor.execute(sql, values)
                cone.commit()

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def eliminarGrupo(id, personal):
        try:
            #asignacion de valores
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql = "UPDATE grupo SET GrupoFechaModificacion = %s, GrupoStatus = 'IN', PersonalAdministrativoId = %s WHERE GrupoID = %s"
                values = (fechmodi,personal,id)
                
                cursor.execute(sql, values)
                cone.commit()
                
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión