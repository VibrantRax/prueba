from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from datetime import datetime

app = Flask(__name__)
app.secret_key = "tu_secreto"  # Se requiere para usar flash

class ConexionMySQL:

    @staticmethod
    def cconexion():
        """Establece la conexión a la base de datos MySQL."""
        try:
            conexion = pymysql.connect(
                host="34.47.10.132",
                user="admin",
                password="12345",
                db='db_escolar'
            )
            print("Conexión correcta")
            return conexion  # Devuelve la conexión establecida

        except pymysql.Error as error:
            print(f"Error al conectarse a la base de Datos: {error}")
            return None  # Retorna None si hay un error en la conexión

# Clase que gestiona los edificios
class EdificiosMySQL:
    @staticmethod
    def mostrarEdificios():
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            cursor.execute("SELECT * FROM edificio WHERE EdificioStatus = 'AC'")
            miResultado = cursor.fetchall()
            cone.commit()
            return miResultado
        
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")

        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def ingresarEdifico(edifico):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            cursor.execute("SELECT COUNT(*) FROM edificio")
            tids = cursor.fetchone()[0] + 1
            
            nom = edifico
            admin = "0"
            fechmodi = datetime.now()
            sql = """
                INSERT INTO edificio 
                (EdificioID, EdificioNombre, EdificioFechaModificacion, EdificioStatus, PersonalAdministrativoId) 
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
    def obtenerEdificioPorId(id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            cursor.execute("SELECT EdificioID, EdificioNombre FROM edificio WHERE EdificioID = %s", (id,))
            edificio = cursor.fetchone()
            cone.commit()
            return edificio
        
        except pymysql.Error as error:
            print(f"Error al obtener los datos del edificio: {error}")

        finally:
            cursor.close()
            cone.close()


# Clase que gestiona las materias
class MateriasMySQL:

    @staticmethod
    def mostrarMaterias():
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            cursor.execute("SELECT MateriaID, MateriaNombre FROM materia WHERE MateriaStatus = 'AC'")
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
    
    @staticmethod
    def obtenerMateriaPorId(id):
        try:
            cone = ConexionMySQL.cconexion()
            cursor = cone.cursor()
            cursor.execute("SELECT MateriaID, MateriaNombre FROM materia WHERE MateriaID = %s", (id,))
            materia = cursor.fetchone()
            cone.commit()
            return materia
        
        except pymysql.Error as error:
            print(f"Error al obtener los datos de la materia: {error}")

        finally:
            cursor.close()
            cone.close()


# Rutas
@app.route('/')
def inicio_sesion():
    return render_template('inicio_sesion.html')

@app.route('/materias', methods=['GET', 'POST'])
def materias():
    if request.method == 'POST':
        if 'guardar' in request.form:
            materia = request.form['materia']
            if not materia:
                flash("Por favor ingrese la materia.")
            else:
                MateriasMySQL.ingresarMaterias(materia)
                flash("Los datos fueron guardados.")
        
        elif 'modificar' in request.form:
            id = request.form['id']
            materia = request.form['materia']
            if not id or not materia:
                flash("Falta ID o Materia.")
            else:
                MateriasMySQL.modificarMateria(id, materia)
                flash("Los datos fueron modificados.")

        elif 'eliminar' in request.form:
            id = request.form['id']
            if not id:
                flash("Falta ID")
            else:
                MateriasMySQL.eliminarMateria(id)

    lista_materias = MateriasMySQL.mostrarMaterias()

    # Recuperar una materia por su ID si se especifica
    materia_editar = None
    if 'id' in request.args:
        materia_editar = MateriasMySQL.obtenerMateriaPorId(request.args.get('id'))

    return render_template('materias.html', materias=lista_materias, materia_editar=materia_editar)



@app.route('/edificios', methods=['GET', 'POST'])
def edificios():
    if request.method == 'POST':
        if 'guardar' in request.form:
            edificio = request.form['edificio']
            if not edificio:
                flash("Por favor ingrese el nombre del edificio.")
            else:
                # Ingresar lógica para guardar edificio
                EdificiosMySQL.ingresarEdifico(edificio)
                flash("Los datos fueron guardados.")
        
        elif 'modificar' in request.form:
            id = request.form['id']
            edificio = request.form['edificio']
            if not id or not edificio:
                flash("Falta ID o Edificio.")
            else:
                # Ingresar lógica para modificar edificio
                flash("Los datos fueron modificados.")

        elif 'eliminar' in request.form:
            id = request.form['id']
            if not id:
                flash("Falta ID")
            else:
                # Ingresar lógica para eliminar edificio
                flash("El edificio fue eliminado.")
        
        elif 'limpiar' in request.form:
            pass

    lista_edificios = EdificiosMySQL.mostrarEdificios()

    # Recuperar un edificio por su ID si se especifica
    edificio_editar = None
    if 'id' in request.args:
        edificio_editar = EdificiosMySQL.obtenerEdificioPorId(request.args.get('id'))

    return render_template('edificios.html', edificios=lista_edificios, edificio_editar=edificio_editar)


if __name__ == '__main__':
    app.run(debug=True)
