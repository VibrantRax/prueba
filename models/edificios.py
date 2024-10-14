from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona los edificios
class EdificiosMySQL:
    @staticmethod
    def mostrarEdificios():
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            cursor.execute("SELECT * FROM edificio WHERE EdificioStatus = 'AC'")
            miResultado = cursor.fetchall()
            cone.commit()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def ingresarEdifico(edifico):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            cursor.execute("SELECT COUNT(*) FROM edificio")
            tids = cursor.fetchone()[0] + 1
            
            nom = edifico
            admin = "0"
            fechmodi = datetime.now()
            sql = """
                INSERT INTO edificio 
                (EdificioID, EdificioNombre, EdificioFechaModificacion, EdificioStatus, PersonalAdministrativoId) 
                VALUES (%s, %s, %s, %s, %s);
            """
            values = (tids, nom, fechmodi, 'AC', admin)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Ahora hay {tids} registros en la tabla")
        
        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()
            cone.close()
    
    @staticmethod
    def modificarEdificio(id, edificio):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            nom = edificio
            admin = "0"
            fechmodi = datetime.now()
            sql = "UPDATE edificio SET EdificioNombre = %s, EdificioFechaModificacion = %s, PersonalAdministrativoId = %s WHERE EdificioID = %s"
            values = (nom, fechmodi, admin, id)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Edificio con ID {id} fue actualizado.")
        
        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def eliminarEdificio(id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            admin = "0"
            fechmodi = datetime.now()
            sql = "UPDATE edificio SET EdificioStatus = 'IN', EdificioFechaModificacion = %s , PersonalAdministrativoId = %s WHERE edificio.EdificioID = %s"
            values = (fechmodi,admin,id)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Edificio con ID {id} fue eliminado.")
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión