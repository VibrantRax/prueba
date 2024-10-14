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
            cursor.execute("SELECT GrupoID, DocenteID, GrupoNombre, SalonID FROM grupo WHERE GrupoStatus = 'AC'")
            miResultado = cursor.fetchall()
            cone.commit()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()
            cone.close()