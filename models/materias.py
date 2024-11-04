from datetime import datetime
from .conexion import ConexionMySQL  # Importa la clase de conexión
import pymysql

# Clase que gestiona las materias
class MateriasMySQL:

    @staticmethod
    def mostrarMaterias():
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                cursor.execute("SELECT * FROM materia WHERE MateriaStatus = 'AC'")
                miResultado = cursor.fetchall()

            return miResultado

        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def mostrarMateriasporID(id):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql = "SELECT * FROM materia WHERE MateriaID = %s AND MateriaStatus = 'AC'"
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
    def ingresarMaterias(data, personal):
        try:
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                cursor.execute("SELECT MAX(MateriaID) FROM materia")
                max_id = cursor.fetchone()['MAX(MateriaID)'] or 4000
                
                #asigacion de valores
                new_id = max_id + 1
                fechmodi = datetime.now()
                status = 'AC'

                #consulta MySQL
                sql = """INSERT INTO materia (MateriaID, MateriaNombre, 
                                                MateriaFechaModificacion, MateriaStatus, 
                                                PersonalAdministrativoId) 
                                    VALUES (%s, %s, %s, %s, %s)"""
                values = (new_id, data['MateriaNombre'], fechmodi, status, personal)
                
                cursor.execute(sql, values)
                cone.commit()

                return new_id  # Retorna el ID de la nueva materia creada

        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def modificarMateria(data,id, personal):
        try:
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:

                #consulta MySQL
                sql ="""UPDATE materia 
                        SET MateriaNombre = %s, MateriaFechaModificacion = %s, 
                            PersonalAdministrativoId = %s WHERE MateriaID = %s"""
                values = (data['MateriaNombre'], fechmodi, personal, id)

                cursor.execute(sql, values)
                cone.commit()

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión

    @staticmethod
    def eliminarMateria(id, personal):
        try:

            #asignacion de valores
            fechmodi = datetime.now()
            cone = ConexionMySQL.cconexion()
            with cone.cursor() as cursor:
                #consulta MySQL
                sql = "UPDATE materia SET MateriaStatus = 'IN', MateriaFechaModificacion = %s , PersonalAdministrativoId = %s WHERE materia.MateriaID = %s"
                values = (fechmodi,personal,id)
                
                cursor.execute(sql, values)
                cone.commit()

        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")

        finally:
            cursor.close()  # Cerrar el cursor
            cone.close()  # Cerrar la conexión