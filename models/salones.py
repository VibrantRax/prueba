from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona los salones 
class SalonesMySQL:
    @staticmethod
    def mostrarSalones():
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            cursor.execute("SELECT salon.SalonID, edificio.EdificioNombre, edificio.EdificioID, salon.SalonFechaModificacion FROM salon INNER JOIN edificio ON salon.EdificioID = edificio.EdificioID WHERE salon.SalonStatus = 'AC'")
            miResultado = cursor.fetchall()
            cone.commit()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()
            cone.close()
    
    @staticmethod
    def ingresarSalon(salon, edificio_id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            cursor.execute("SELECT COUNT(*) FROM salon")
            tids = cursor.fetchone()[0] + 1
            
            salon = salon
            edi = edificio_id
            admin = "0"
            fechmodi = datetime.now()
            sql = """
                INSERT INTO salon
                (SalonID, EdificioID, SalonFechaModificacion, SalonStatus, PersonalAdministrativoId) 
                VALUES (%s, %s, %s, %s, %s);
            """
            values = (salon, edi, fechmodi, 'AC', admin)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Ahora hay {tids} registros en la tabla")
        
        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()
            cone.close()
    
    @staticmethod
    def modificarSalon(salon, edificio_id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            salon = salon
            edi = edificio_id
            admin = "0"
            fechmodi = datetime.now()
            sql = "UPDATE salon SET EdificioID = %s, SalonFechaModificacion = %s, PersonalAdministrativoId = %s WHERE SalonID = %s"
            values = (edi, fechmodi, admin, salon)
            cursor.execute(sql, values)
            cone.commit()
            print(f"El salon {salon} fue actualizado.")
        
        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def eliminarSalon(salon):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            admin = "0"
            fechmodi = datetime.now()
            sql = "UPDATE salon SET SalonStatus = 'IN', SalonFechaModificacion = %s , PersonalAdministrativoId = %s WHERE salon.SalonID = %s"
            values = (fechmodi,admin,salon)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Salon con numero {salon} fue eliminado.")
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión