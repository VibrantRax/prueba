from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona los horarios
class HorasMySQL:
    
    @staticmethod
    def mostrarHoras():
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                #consulta MySQL
                cursor.execute("SELECT * FROM hora WHERE HoraStatus = 'AC'")
                miResultado = cursor.fetchall()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def mostrarHorasporID(id):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql = "SELECT * FROM hora WHERE HoraID = %s AND HoraStatus = 'AC'"
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
    def ingresarHoras(data, personal):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(HoraID) FROM hora")
                max_id = cursor.fetchone()['MAX(HoraID)'] or 4000
                
                #asigacion de valores
                new_id = max_id + 1
                fechmodi = datetime.now()
                status = 'AC'

                #consulta MySQL
                sql = """INSERT INTO hora (HoraID, HoraInicio, HoraFin, 
                                                HoraFechaModificacion, HoraStatus, 
                                                PersonalAdministrativoId) 
                                        VALUES (%s, %s, %s, %s, %s, %s)"""
                values = (new_id, data['HoraInicio'], data['HoraFin'], fechmodi, status, personal)

                cursor.execute(sql, values)
                cone.commit()

            return new_id

        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def modificarHora(data, id, personal):
        try:
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql ="""UPDATE hora 
                        SET HoraInicio = %s, HoraFin = %s, 
                            HoraFechaModificacion = %s, PersonalAdministrativoId = %s 
                        WHERE HoraID = %s"""
                values = (data['HoraInicio'], data['HoraFin'], fechmodi, personal, id)

                cursor.execute(sql, values)
                cone.commit()

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def eliminarHora(id, personal):
        try:
            #asignacion de valores
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql = "UPDATE hora SET HoraFechaModificacion = %s, HoraStatus = 'IN', PersonalAdministrativoId = %s WHERE HoraID = %s"
                values = (fechmodi,personal,id)
                
                cursor.execute(sql, values)
                cone.commit()
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión