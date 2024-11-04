from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona los salones 
class SalonesMySQL:
    @staticmethod
    def mostrarSalones():
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                cursor.execute("SELECT salon.*, edificio.EdificioID, edificio.EdificioNombre FROM salon INNER JOIN edificio ON salon.EdificioID = edificio.EdificioID WHERE salon.SalonStatus = 'AC'")
                miResultado = cursor.fetchall()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def mostrarSalonesporID(id):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql = "SELECT salon.*, edificio.EdificioID, edificio.EdificioNombre FROM salon INNER JOIN edificio ON salon.EdificioID = edificio.EdificioID WHERE SalonID = %s AND SalonStatus = 'AC'"
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
    def ingresarSalon(data, personal):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(SalonID) FROM salon")
                max_id = cursor.fetchone()['MAX(SalonID)'] or 4000
                
                #asigacion de valores
                new_id = max_id + 1
                fechmodi = datetime.now()
                status = 'AC'

                #consulta MySQL
                sql ="""INSERT INTO salon (SalonID, SalonNumero, EdificioID, 
                                            SalonFechaModificacion, SalonStatus, 
                                            PersonalAdministrativoId) 
                                    VALUES (%s, %s, %s, %s, %s, %s);"""
                values = (new_id, data['SalonNumero'], data['EdificioID'], fechmodi, status, personal)

                cursor.execute(sql, values)
                cone.commit()

                return new_id
        
        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión
    
    @staticmethod
    def modificarSalon(data, id, personal):
        try:
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql ="""UPDATE salon 
                        SET SalonNumero = %s, EdificioID = %s, 
                            SalonFechaModificacion = %s, PersonalAdministrativoId = %s 
                        WHERE SalonID = %s"""
                values = (data['SalonNumero'], data['EdificioID'], fechmodi, personal, id)

                cursor.execute(sql, values)
                cone.commit()
        
        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def eliminarSalon(id, personal):
        try:
            #asignacion de valores
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                #consulta MySQL
                sql = "UPDATE salon SET SalonStatus = 'IN', SalonFechaModificacion = %s , PersonalAdministrativoId = %s WHERE salon.SalonID = %s"
                values = (fechmodi,personal,id)
                
                cursor.execute(sql, values)
                cone.commit()
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión