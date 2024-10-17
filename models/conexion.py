import pymysql

class ConexionMySQL:

    @staticmethod
    def cconexion():
        """Establece la conexión a la base de datos MySQL."""
        try:
            conexion = pymysql.connect(
                host="34.95.55.194",
                user="uvp",
                password="x43!0oPao",
                db='db_escolar'
            )
            print("Conexión correcta")
            return conexion  # Devuelve la conexión establecida

        except pymysql.Error as error:
            print(f"Error al conectarse a la base de Datos: {error}")
            return None  # Retorna None si hay un error en la conexión
