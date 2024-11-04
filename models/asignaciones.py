from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona la asignacion de las materias 
class AsignacionMySQL:

    @staticmethod
    def mostrarAsignaciones():
        try:

            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                cursor.execute("SELECT grupomateria.*, grupo.GrupoID, grupo.GrupoNombre, materia.MateriaID, materia.MateriaNombre FROM grupomateria INNER JOIN materia ON materia.MateriaID = grupomateria.MateriaID INNER JOIN grupo ON grupo.GrupoID = grupomateria.GrupoID WHERE grupomateria.GrupoMateriaStatus = 'AC'")
                miResultado = cursor.fetchall()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def mostrarAsignacionesporID(id):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql = "SELECT grupomateria.*, grupo.GrupoID, grupo.GrupoNombre, materia.MateriaID, materia.MateriaNombre FROM grupomateria INNER JOIN materia ON materia.MateriaID = grupomateria.MateriaID INNER JOIN grupo ON grupo.GrupoID = grupomateria.GrupoID WHERE grupomateria.GrupoMateriaID = %s AND grupomateria.GrupoMateriaStatus = 'AC'"
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
    def ingresarAsignaciones(data, personal):
        try:

            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(GrupoMateriaID) FROM grupomateria")
                max_id = cursor.fetchone()['MAX(GrupoMateriaID)'] or 4000
                
                #asigacion de valores
                new_id = max_id + 1
                fechmodi = datetime.now()
                status = 'AC'

                #consulta MySQL
                sql = """INSERT INTO grupomateria (GrupoMateriaID, GrupoID, 
                                                    MateriaID, GrupoMateriaFechaModificacion, 
                                                    GrupoMateriaStatus, PersonalAdministrativoId) 
                                    VALUES (%s, %s, %s, %s, %s, %s)"""
                values = (new_id, data['GrupoID'], data['MateriaID'], fechmodi, status, personal)

                cursor.execute(sql, values)
                cone.commit()

                return new_id

        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def modificarAsignacion(data, id, personal):
        try:

            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql ="""UPDATE grupomateria 
                        SET GrupoID = %s, MateriaID = %s, 
                            GrupoMateriaFechaModificacion = %s, PersonalAdministrativoId = %s 
                        WHERE GrupoMateriaID = %s;"""
                values = (data['GrupoID'], data['MateriaID'], fechmodi, personal, id)

                cursor.execute(sql, values)
                cone.commit()

            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def eliminarAsignacion(id, personal):
        try:
            
            #asignacion de valores
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                #consulta MySQL
                sql = "UPDATE grupomateria SET GrupoMateriaFechaModificacion = %s, GrupoMateriaStatus = 'IN', PersonalAdministrativoId = %s WHERE GrupoMateriaID = %s"
                values = (fechmodi,personal,id)
                
                cursor.execute(sql, values)
                cone.commit()

        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión