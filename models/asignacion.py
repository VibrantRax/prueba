from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona la asignacion de las materias 
class AsignacionMySQL:
 
    @staticmethod
    def mostrarAsignaciones():
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            #consulta MySQL
            cursor.execute("SELECT grupomateria.GrupoID, grupo.GrupoID, grupo.GrupoNombre, materia.MateriaID, materia.MateriaNombre, grupomateria.GrupoMateriaFechaModificacion FROM grupomateria INNER JOIN grupo on grupo.GrupoID = grupomateria.GrupoID INNER JOIN materia on materia.MateriaID = grupomateria.MateriaID WHERE grupomateria.GrupoMateriaStatus = 'AC'")
            miResultado = cursor.fetchall()
            cone.commit()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión
    
    @staticmethod
    def ingresarAsignaciones(grupo, materia):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

            # Genera un nuevo ID para la asignacion
            cursor.execute("SELECT COUNT(*) FROM grupomateria")
            tids = cursor.fetchone()[0] + 1

            # Asignación de valores
            fechmodi = datetime.now()
            admin = '0'

            #consulta MySQL
            sql = """INSERT INTO grupomateria (GrupoMateriaID, GrupoID, 
                                                MateriaID, GrupoMateriaFechaModificacion, 
                                                GrupoMateriaStatus, PersonalAdministrativoId) 
                                VALUES (%s, %s, %s, %s, 'AC', %s)"""  
            values = (tids, grupo, materia, fechmodi, admin)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Ahora hay {tids} registros en la tabla")

        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def modificarAsignacion(grupo, materia, id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            
            # Asignación de valores
            fechmodi = datetime.now() 
            admin = '0'

            #consulta MySQL
            sql ="""UPDATE grupomateria 
                    SET GrupoID = %s, MateriaID = %s, 
                        GrupoMateriaFechaModificacion = %s, PersonalAdministrativoId = %s 
                    WHERE GrupoMateriaID = %s;"""
            values = (grupo, materia, fechmodi, admin, id)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Asignacion con ID {id} fue actualizada.")

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def eliminarAsignacion(id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            admin = "0"
            fechmodi = datetime.now()

            #consulta MySQL
            sql = "UPDATE grupomateria SET GrupoMateriaFechaModificacion = %s, GrupoMateriaStatus = 'IN', PersonalAdministrativoId = %s WHERE GrupoMateriaID = %s"
            values = (fechmodi,admin,id)

            cursor.execute(sql, values)
            cone.commit()
            print(f"Asignacion con ID {id} fue eliminada.")
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión
