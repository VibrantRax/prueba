from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

class MateriasMySQL:

    @staticmethod
    def mostrarMaterias():
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            cursor.execute("SELECT MateriaID, MateriaNombre, MateriaFechaModificacion FROM materia WHERE MateriaStatus = 'AC'")
            miResultado = cursor.fetchall()
            cone.commit()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def ingresarMaterias(materia):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            cursor.execute("SELECT COUNT(*) FROM materia")
            tids = cursor.fetchone()[0] + 1
            
            nom = materia
            admin = "0"
            fechmodi = datetime.now()
            sql = """
                INSERT INTO materia 
                (MateriaID, MateriaNombre, MateriaFechaModificacion, MateriaStatus, PersonalAdministrativoId) 
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
    def modificarMateria(id, materia):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            nom = materia
            admin = "0"
            fechmodi = datetime.now()
            sql = "UPDATE materia SET MateriaNombre = %s, MateriaFechaModificacion = %s, PersonalAdministrativoId = %s WHERE MateriaID = %s"
            values = (nom, fechmodi, admin, id)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Materia con ID {id} fue actualizada.")
        
        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()
            cone.close()
    
    @staticmethod
    def eliminarMateria(id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            admin = "0"
            fechmodi = datetime.now()
            sql = "UPDATE materia SET MateriaStatus = 'IN', MateriaFechaModificacion = %s , PersonalAdministrativoId = %s WHERE materia.MateriaID = %s"
            values = (fechmodi,admin,id)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Materia con ID {id} fue eliminada.")
        
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión