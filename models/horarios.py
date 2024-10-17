from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona los horarios
class HorariosMySQL:
    
    @staticmethod
    def mostrarHorarios():
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            #consulta MySQL
            cursor.execute("SELECT horario.HorarioID, materia.MateriaID, materia.MateriaNombre, horario.HorarioDiaSemana, hora.HoraID, hora.HoraInicio, hora.HoraFin, horario.HorarioFechaModificacion  FROM horario INNER JOIN materia ON materia.MateriaID = horario.MateriaID INNER JOIN hora ON hora.HoraID = horario.HoraID WHERE horario.HorarioStatus = 'AC'")
            miResultado = cursor.fetchall()
            cone.commit()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def ingresarHorarios(materia, dia, hora):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            # Genera un nuevo ID para el grupo
            cursor.execute("SELECT COUNT(*) FROM horario")
            tids = cursor.fetchone()[0] + 1

            # Asignación de valores
            fechmodi = datetime.now()  
            admin = '0'


            #consulta MySQL
            sql = """INSERT INTO horario (HorarioID, MateriaID, HorarioDiaSemana, 
                                            HoraID, HorarioFechaModificacion, 
                                            HorarioStatus, PersonalAdministrativoId) 
                                VALUES (%s, %s, %s, %s, %s, 'AC', %s)"""
            values = (tids, materia, dia, hora, fechmodi, admin)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Ahora hay {tids} registros en la tabla")

        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def modificarHorario(materia, dia, hora, id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            
            # Asignación de valores
            fechmodi = datetime.now() 
            admin = '0'


            #consulta MySQL
            sql ="""UPDATE horario 
                    SET MateriaID = %s, HorarioDiaSemana = %s, HoraID = %s, 
                        HorarioFechaModificacion = %s, PersonalAdministrativoId = %s 
                    WHERE HorarioID = %s""" 
            values = (materia, dia, hora, fechmodi, admin, id)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Horario con ID {id} fue actualizado.")

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def eliminarHorario(id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            admin = "0"
            fechmodi = datetime.now()

            #consulta MySQL
            sql = "UPDATE horario SET HorarioFechaModificacion = %s, HorarioStatus = 'IN', PersonalAdministrativoId = %s WHERE HorarioID = %s"
            values = (fechmodi,admin,id)
            
            cursor.execute(sql, values)
            cone.commit()
            print(f"Horario con ID {id} fue eliminado.")
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión
