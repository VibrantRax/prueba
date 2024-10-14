import pymysql

class ConexionMySQL:

    @staticmethod
    def cconexion():
        """Establece la conexión a la base de datos MySQL."""
        try:
            conexion = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                db='db_escolar'
            )
            print("Conexión correcta")
            return conexion  # Devuelve la conexión establecida

        except pymysql.Error as error:
            print(f"Error al conectarse a la base de Datos: {error}")
            return None  # Retorna None si hay un error en la conexión