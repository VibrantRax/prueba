from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona los grupos
class GruposMySQL:
    
    @staticmethod
    def mostrarGrupos():
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            #consulta MySQL
            cursor.execute("SELECT GrupoID, DocenteID, GrupoNombre, SalonID FROM grupo WHERE GrupoStatus = 'AC'")
            miResultado = cursor.fetchall()
            cone.commit()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def ingresarGrupos(docente, grupo, salon):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            # Genera un nuevo ID para el grupo
            cursor.execute("SELECT COUNT(*) FROM grupo")
            tids = cursor.fetchone()[0] + 1

            # Asignación de valores
            fechmodi = datetime.now()  
            admin = '0'


            #consulta MySQL
            sql = """INSERT INTO grupo (GrupoID, DocenteId, GrupoNombre, SalonID, 
                                                GrupoFechaModificacion, GrupoStatus, 
                                                PersonalAdministrativoId) 
                                VALUES (%s, %s, %s, %s, %s, 'AC', %s)"""
            values = (tids, docente, grupo, salon, fechmodi, admin)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Ahora hay {tids} registros en la tabla")

        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def modificarGrupo(docente, grupo, salon, id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            
            # Asignación de valores
            fechmodi = datetime.now() 
            admin = '0'


            #consulta MySQL
            sql = """UPDATE grupo 
                     SET DocenteId = %s, GrupoNombre = %s, SalonID = %s, 
                         GrupoFechaModificacion = %s, PersonalAdministrativoId = %s 
                     WHERE GrupoID = %s"""
            values = (docente, grupo, salon, fechmodi, admin, id)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Grupo con ID {id} fue actualizado.")

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def eliminarGrupo(id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            admin = "0"
            fechmodi = datetime.now()

            #consulta MySQL
            sql = "UPDATE grupo SET GrupoFechaModificacion = %s, GrupoStatus = 'IN', PersonalAdministrativoId = %s WHERE GrupoID = %s"
            values = (fechmodi,admin,id)
            
            cursor.execute(sql, values)
            cone.commit()
            print(f"Grupo con ID {id} fue eliminado.")
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión





    