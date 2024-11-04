from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona los edificios
class EdificiosMySQL:

    @staticmethod
    def mostrarEdificios():
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                cursor.execute("SELECT * FROM edificio WHERE EdificioStatus = 'AC'")
                miResultado = cursor.fetchall()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def mostrarEdificiosporID(id):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql = "SELECT * FROM edificio WHERE EdificioID = %s AND EdificioStatus = 'AC'"
                values = (id)
                cursor.execute(sql, values)

                miResultado = cursor.fetchone()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def ingresarEdificio(data, personal):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(EdificioID) FROM edificio")
                max_id = cursor.fetchone()['MAX(EdificioID)'] or 4000
                
                #asigacion de valores
                new_id = max_id + 1
                fechmodi = datetime.now()
                status = 'AC'

                #consulta MySQL
                sql = """INSERT INTO edificio (EdificioID, EdificioNombre, 
                                                EdificioFechaModificacion, EdificioStatus, 
                                                PersonalAdministrativoId) 
                                    VALUES (%s, %s, %s, %s, %s, %s)"""
                values = (new_id, data['EdificioNombre'], fechmodi, status, personal)

                cursor.execute(sql, values)
                cone.commit()

                return new_id
        
        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión
    
    @staticmethod
    def modificarEdificio(data, id, personal):
        try:
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql ="""UPDATE edificio
                        SET EdificioNombre = %s,
                            EdificioFechaModificacion = %s, PersonalAdministrativoId = %s
                        WHERE EdificioID = %s"""
                values = (data['EdificioNombre'], fechmodi, personal, id)

                cursor.execute(sql, values)
                cone.commit()
        
        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def eliminarEdificio(id, personal):
        try:
            #asignacion de valores
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                sql = "UPDATE edificio SET EdificioStatus = 'IN', EdificioFechaModificacion = %s , PersonalAdministrativoId = %s WHERE edificio.EdificioID = %s"
                values = (fechmodi,personal,id)
                
                cursor.execute(sql, values)
                cone.commit()
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión