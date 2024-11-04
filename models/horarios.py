from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona los horarios
class HorariosMySQL:
    
    @staticmethod
    def mostrarHorarios():
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                #consulta MySQL
                    cursor.execute("SELECT horario.*, materia.MateriaID, materia.MateriaNombre, hora.HoraID, hora.HoraInicio, hora.HoraFin FROM horario INNER JOIN materia ON materia.MateriaID = horario.MateriaID INNER JOIN hora ON hora.HoraID = horario.HoraID WHERE horario.HorarioStatus = 'AC'")
                    miResultado = cursor.fetchall()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def mostrarHorariosporID(id):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql = "SELECT horario.*, materia.MateriaID, materia.MateriaNombre, hora.HoraID, hora.HoraInicio, hora.HoraFin FROM horario INNER JOIN materia ON materia.MateriaID = horario.MateriaID INNER JOIN hora ON hora.HoraID = horario.HoraID WHERE HorarioID = %s AND HorarioStatus = 'AC'"
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
    def ingresarHorarios(data, personal):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(HorarioID) FROM horario")
                max_id = cursor.fetchone()['MAX(HorarioID)'] or 4000
                
                #asigacion de valores
                new_id = max_id + 1
                fechmodi = datetime.now()
                status = 'AC'

                #consulta MySQL
                sql = """INSERT INTO horario (HorarioID, MateriaID, HorarioDiaSemana, 
                                                HoraID, HorarioFechaModificacion, 
                                                HorarioStatus, PersonalAdministrativoId) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                values = (new_id, data['MateriaID'], data['HorarioDiaSemana'], data['HoraID'], fechmodi, status, personal)

                cursor.execute(sql, values)
                cone.commit()

                return new_id

        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def modificarHorario(data, id, personal):
        try:
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql ="""UPDATE horario 
                        SET MateriaID = %s, HorarioDiaSemana = %s, HoraID = %s, 
                            HorarioFechaModificacion = %s, PersonalAdministrativoId = %s 
                        WHERE HorarioID = %s""" 
                values = ( data['MateriaID'], data['HorarioDiaSemana'], data['HoraID'], fechmodi, personal, id)

                cursor.execute(sql, values)
                cone.commit()

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def eliminarHorario(id, personal):
        try:
            #asignacion de valores
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql = "UPDATE horario SET HorarioFechaModificacion = %s, HorarioStatus = 'IN', PersonalAdministrativoId = %s WHERE HorarioID = %s"
                values = (fechmodi,personal,id)
                
                cursor.execute(sql, values)
                cone.commit()
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión
