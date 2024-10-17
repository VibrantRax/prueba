from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona los horarios
class HorasMySQL:
    
    @staticmethod
    def mostrarHoras():
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            #consulta MySQL
            cursor.execute("SELECT HoraID, HoraInicio, HoraFin, HoraFechaModificacion FROM hora WHERE HoraStatus = 'AC'")
            miResultado = cursor.fetchall()
            cone.commit()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def ingresarHoras(inicio, fin):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            # Genera un nuevo ID para el grupo
            cursor.execute("SELECT COUNT(*) FROM hora")
            tids = cursor.fetchone()[0] + 1

            # Asignación de valores
            fechmodi = datetime.now()  
            admin = '0'


            #consulta MySQL
            sql = """INSERT INTO hora (HoraID, HoraInicio, HoraFin, 
                                        HoraFechaModificacion, HoraStatus, 
                                        PersonalAdministrativoId) 
                                VALUES (%s, %s, %s, %s, 'AC', %s)"""
            values = (tids, inicio, fin, fechmodi, admin)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Ahora hay {tids} registros en la tabla")

        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def modificarHora(inicio, fin, id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            
            # Asignación de valores
            fechmodi = datetime.now() 
            admin = '0'

            #consulta MySQL
            sql ="""UPDATE hora 
                    SET HoraInicio = %s, HoraFin = %s, 
                        HoraFechaModificacion = %s, PersonalAdministrativoId = %s 
                    WHERE HoraID = %s"""
            values = (inicio, fin, fechmodi, admin, id)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Hora con ID {id} fue actualizada.")

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def eliminarHora(id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            admin = "0"
            fechmodi = datetime.now()

            #consulta MySQL
            sql = "UPDATE hora SET HoraFechaModificacion = %s, HoraStatus = 'IN', PersonalAdministrativoId = %s WHERE HoraID = %s"
            values = (fechmodi,admin,id)
            
            cursor.execute(sql, values)
            cone.commit()
            print(f"Hora con ID {id} fue eliminada.")
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión