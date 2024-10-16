from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from models.salones import SalonesMySQL
from models.edificios import EdificiosMySQL
from models.materias import MateriasMySQL
from models.reportes import ReportesMySQL
from models.grupo import GruposMySQL
from models.asignacion import AsignacionMySQL
from models.alumnos import AlumnoMySQL

app = Flask(__name__)
app.secret_key = "tu_secreto"  # Se requiere para usar flash

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


# Simulación de una base de datos de usuarios
usuarios = {
    'admin': generate_password_hash('adminpass'),  # Cambia 'adminpass' por la contraseña real
    'profesor': generate_password_hash('profesorpass'),
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in usuarios:
        return User(username)
    return None

# Cambia el nombre de la variable para evitar conflictos
asistencia_datos = [
    {"nombre": "Agustin Ramos", "14-Oct": "✔", "15-Oct": "✘", "16-Oct": "✔", "17-Oct": "R", "18-Oct": "✔"},
    {"nombre": "Sebastian Ramos", "14-Oct": "✔", "15-Oct": "✔", "16-Oct": "✔", "17-Oct": "R", "18-Oct": "✔"},
    {"nombre": "Jennifer Janice Jimenez Vidal", "14-Oct": "✔", "15-Oct": "✔", "16-Oct": "✔", "17-Oct": "J", "18-Oct": "✔"},
    {"nombre": "Jhon Doe", "14-Oct": "✔", "15-Oct": "✔", "16-Oct": "✔", "17-Oct": "✔", "18-Oct": "✔"},
    {"nombre": "Fernanda Rivera", "14-Oct": "✔", "15-Oct": "✔", "16-Oct": "✔", "17-Oct": "✔", "18-Oct": "✔"},
]

def generar_fechas(inicio, fin):
    """Genera una lista de fechas entre inicio y fin."""
    fechas = []
    fecha_actual = inicio
    while fecha_actual <= fin:
        fechas.append(fecha_actual.strftime('%d-%b'))
        fecha_actual += timedelta(days=1)
    return fechas


# Rutas

#inicio de sesion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = load_user(username)

        if user and check_password_hash(usuarios[username], password):
            login_user(user)
            return redirect(url_for('principal'))

        else:
            flash('Nombre de usuario o contraseña incorrectos.')
    
    return render_template('login.html', title="Inicio de Sesion")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))  # Esto busca una ruta con el nombre 'login'

#principal
@app.route('/principal', methods=['GET', 'POST'])
@login_required
def principal():
    return render_template('principal.html', username=current_user.id, active_page='inicio', title="Inicio")

#materias
@app.route('/materias', methods=['GET', 'POST'])
def materias():
    if request.method == 'POST':

        if 'guardar' in request.form:
            materia = request.form['materia']

            if not materia:
                flash("Faltan datos")
            else:
                MateriasMySQL.ingresarMaterias(materia)
                flash("Los datos fueron guardados.")
                return redirect(url_for('materias'))
        
        elif 'modificar' in request.form:
            id = request.form['id']
            materia = request.form['materia']

            if not id or not materia:
                flash("Faltan datos")
            else:
                MateriasMySQL.modificarMateria(id, materia)
                flash("Los datos fueron modificados.")
                return redirect(url_for('materias'))

        elif 'eliminar' in request.form:
            id = request.form['id']

            if not id:
                flash("Faltan datos")
            else:
                MateriasMySQL.eliminarMateria(id)
                flash("Los datos fueron eliminados.")
                return redirect(url_for('materias'))

    lista_materias = MateriasMySQL.mostrarMaterias()

    return render_template('materias.html', materias=lista_materias, username=current_user.id, active_page='materias', title="Materias")

#salones
@app.route('/salones', methods=['GET', 'POST'])
def salones():
    if request.method == 'POST':

        if 'guardar' in request.form:
            salon = request.form['salon']
            edificio_id = request.form['edificio']

            if not edificio_id or not salon:
                flash("Faltan datos")
            else:
                SalonesMySQL.ingresarSalon(salon, edificio_id)
                flash("Los datos fueron guardados.")
                return redirect(url_for('salones'))

        elif 'modificar' in request.form:
            salon = request.form['salon']
            edificio_id = request.form['edificioSelect']

            if not salon or not edificio_id:
                flash("Faltan datos")
            else:
                SalonesMySQL.modificarSalon(salon, edificio_id)
                flash("Los datos fueron modificados.")
                return redirect(url_for('salones'))

        elif 'eliminar' in request.form:
            salon = request.form['salon']

            if not id:
                flash("Faltan datos")
            else:
                SalonesMySQL.eliminarSalon(salon)
                flash("Los datos fueron eliminados.")
                return redirect(url_for('salones'))

    lista_salones = SalonesMySQL.mostrarSalones()
    lista_edificios = EdificiosMySQL.mostrarEdificios()

    return render_template('salones.html', salones=lista_salones, username=current_user.id, edificios=lista_edificios, active_page='salon', title="Salones")

#edificios
@app.route('/edificios', methods=['GET', 'POST'])
def edificios():
    if request.method == 'POST':

        if 'guardar' in request.form:
            edificio = request.form['edificio']

            if not edificio:
                flash("Faltan datos")
            else:
                EdificiosMySQL.ingresarEdifico(edificio)
                flash("Los datos fueron guardados.")
                return redirect(url_for('edificios'))
        
        elif 'modificar' in request.form:
            id = request.form['id']
            edificio = request.form['edificio']

            if not id or not edificio:
                flash("Faltan datos")
            else:
                EdificiosMySQL.modificarEdificio(id, edificio)
                flash("Los datos fueron modificados.")
                return redirect(url_for('edificios'))

        elif 'eliminar' in request.form:
            id = request.form['id']

            if not id:
                flash("Faltan datos")
            else:
                EdificiosMySQL.eliminarEdificio(id)
                flash("Los datos fueron eliminados.")
                return redirect(url_for('edificios'))

    lista_edificios = EdificiosMySQL.mostrarEdificios()
    return render_template('edificios.html', edificios=lista_edificios, username=current_user.id, active_page='edificios', title="Edificios")

#reportes 
@app.route('/reportes', methods=['GET', 'POST'])
def reportes():
    if request.method == 'POST':

        if 'guardar' in request.form:
            alumno = request.form['alumno']
            fecha = request.form['fecha']
            descripcion = request.form['descripcion']
            accion = request.form['accion']
            status = request.form['status']

            if not alumno or not fecha or not descripcion or not status:
                flash("Faltan datos")
            else:
                ReportesMySQL.ingresarReportes(alumno,fecha,descripcion,accion,status)
                flash("Los datos fueron guardados.")
                return redirect(url_for('reportes'))

        elif 'modificar' in request.form:
            id = request.form['id']
            alumno = request.form['alumno']
            fecha = request.form['fecha']
            descripcion = request.form['descripcion']
            accion = request.form['accion']
            status = request.form['estado']

            if not id or not alumno or not fecha or not descripcion or not status:
                flash("Faltan datos")
            else:
                ReportesMySQL.modificarReporte(id,alumno,fecha,descripcion,accion,status)
                flash("Los datos fueron modificados.")
                return redirect(url_for('reportes'))

        elif 'eliminar' in request.form:
            id = request.form['id']

            if not id:
                flash("Faltan datos")
            else:
                ReportesMySQL.eliminarReporte(id)
                flash("Los datos fueron eliminados.")
                return redirect(url_for('reportes'))


    lista_reportes_resueltos = ReportesMySQL.mostrarReportesResueltos()
    lista_reportes = ReportesMySQL.mostrarReportes()

    return render_template('reportes.html', username=current_user.id, resueltos = lista_reportes_resueltos, reportes = lista_reportes ,active_page='reporte', title="Reportes")

#grupos
@app.route('/grupos', methods=['GET', 'POST'])
def grupos():
    if request.method == 'POST':

        if 'guardar' in request.form:
            docente = request.form.get('docente')
            grupo = request.form['grupo']
            salon = request.form.get('salon')

            if not docente or not grupo or not salon:
                flash("Faltan datos")
            else:
                GruposMySQL.ingresarGrupos(docente, grupo, salon)
                flash("Los datos fueron guardados.")
                return redirect(url_for('grupos'))

        if 'modificar' in request.form:
            id = request.form['id']
            docente = request.form.get('docente')
            grupo = request.form['grupo']
            salon = request.form.get('salon')

            if not id or not docente or not grupo or not salon:
                flash("Faltan datos")
            else:
                GruposMySQL.modificarGrupo(docente, grupo, salon, id)
                flash("Los datos fueron modificados.")
                return redirect(url_for('grupos'))

        if 'eliminar' in request.form:
            id = request.form['id']

            if not id:
                flash("Faltan datos")
            else:
                GruposMySQL.eliminarGrupo(id)
                flash("Los datos fueron eliminados.")
                return redirect(url_for('grupos'))

    lista_salones = SalonesMySQL.mostrarSalones()
    lista_grupos = GruposMySQL.mostrarGrupos()

    return render_template('grupos.html', username=current_user.id, salones=lista_salones, grupos = lista_grupos, active_page='grupo', title="Grupos")

#asistencia
@app.route('/asistencias', methods=['GET', 'POST'])
@login_required
def asistencias():
    # Fechas predeterminadas (si no se selecciona ninguna)
    inicio_default = datetime(2024, 10, 14)
    fin_default = datetime(2024, 10, 18)

    if request.method == 'POST':
        # Obtener las fechas seleccionadas en el formulario
        inicio_str = request.form.get('inicio')
        fin_str = request.form.get('fin')

        # Convertir las fechas a objetos datetime
        if inicio_str and fin_str:
            inicio = datetime.strptime(inicio_str, '%Y-%m-%d')
            fin = datetime.strptime(fin_str, '%Y-%m-%d')

            # Validar si la diferencia es mayor a 15 días
            diferencia = (fin - inicio).days
            if diferencia > 10:
                flash('El rango de fechas no puede ser mayor a 10 días.', 'danger')
                inicio = inicio_default
                fin = fin_default
        else:
            inicio = inicio_default
            fin = fin_default
    else:
        inicio = inicio_default
        fin = fin_default

    # Generar la lista de fechas a mostrar
    fechas = generar_fechas(inicio, fin)

    return render_template('asistencias.html', asistencias=asistencia_datos, fechas=fechas, inicio=inicio.strftime('%Y-%m-%d'), fin=fin.strftime('%Y-%m-%d'), username=current_user.id, active_page='asistencia', title="Asistencias")


#asignacion de materias
@app.route('/asignaciones', methods = ['GET', "POST"])
def asignaciones():
    if request.method == 'POST':

        if 'guardar' in request.form:
            grupo = request.form.get('grupo')
            materia = request.form.get('materia')

            if not grupo or not materia:
                flash("Faltan datos")
            else:
                AsignacionMySQL.ingresarAsignaciones(grupo, materia)
                flash("Los datos fueron guardados.")
                return redirect(url_for('asignaciones'))

        if 'modificar' in request.form:
            id = request.form['id']
            grupo = request.form.get('grupo')
            materia = request.form.get('materia')

            if not id or not grupo or not materia:
                flash("Faltan datos")
            else:
                AsignacionMySQL.modificarAsignacion(grupo, materia, id)
                flash("Los datos fueron modificados.")
                return redirect(url_for('asignaciones'))

        if 'eliminar' in request.form:
            id = request.form['id']

            if not id:
                flash("Faltan datos")
            else:
                AsignacionMySQL.eliminarAsignacion(id)
                flash("Los datos fueron eliminados.")
                return redirect(url_for('asignaciones'))


    lista_grupos = GruposMySQL.mostrarGrupos()
    lista_materias = MateriasMySQL.mostrarMaterias()
    lista_grupomaterias = AsignacionMySQL.mostrarAsignaciones()

    return render_template('asignaciones.html', username=current_user.id, grupos = lista_grupos, materias = lista_materias, asignaciones = lista_grupomaterias, active_page = 'asignacion' , title="Asignaciones")

#alumnos
@app.route('/alumnos', methods = ['GET', "POST"])
def alumnos():
    if request.method == 'POST':
        
        if 'guardar' in request.form:
            alumno = request.form.get('alumno')
            grupo = request.form.get('grupo')

            if not alumno or not grupo:
                flash("Faltan datos")
            else:
                AlumnoMySQL.ingresarAlumnos(alumno, grupo)
                flash("Los datos fueron guardados.")
                return redirect(url_for('alumnos'))
            
        if 'modificar' in request.form:
            id = request.form['id']
            alumno = request.form.get('alumno')
            grupo = request.form.get('grupo')

            if not alumno or not grupo or not id:
                flash("Faltan datos")
            else:
                AlumnoMySQL.modificarAlumno(alumno, grupo, id)
                flash("Los datos fueron modificados.")
                return redirect(url_for('alumnos'))
            
        if 'eliminar' in request.form:
            id = request.form['id']

            if not id:
                flash("Faltan datos")
            else:
                AlumnoMySQL.eliminarAlumno(id)
                flash("Los datos fueron eliminados.")
                return redirect(url_for('alumnos'))
        
    lista_grupos = GruposMySQL.mostrarGrupos()
    lista_alumnos = AlumnoMySQL.mostrarAlumnos()

    return render_template('alumnos.html', username=current_user.id, grupos = lista_grupos, alumnos = lista_alumnos, active_page = 'alumno', title="Alumnos")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)