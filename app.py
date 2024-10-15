from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from datetime import datetime
from models.salones import SalonesMySQL
from models.edificios import EdificiosMySQL
from models.materias import MateriasMySQL
from models.reportes import ReportesMySQL
from models.grupo import GruposMySQL
from models.asignacion import AsignacionMySQL
from models.alumnos import AlumnoMySQL

app = Flask(__name__)
app.secret_key = "tu_secreto"  # Se requiere para usar flash

# Rutas

#inicio de sesion
@app.route('/')
def inicio_sesion():
    return render_template('inicio_sesion.html', title="Inicio de Sesion")

#principal
@app.route('/principal', methods=['GET', 'POST'])
def principal():
    return render_template('principal.html',active_page='inicio', title="Inicio")

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

    return render_template('materias.html', materias=lista_materias, active_page='materias', title="Materias")

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

    return render_template('salones.html', salones=lista_salones, edificios=lista_edificios, active_page='salon', title="Salones")

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
    return render_template('edificios.html', edificios=lista_edificios, active_page='edificios', title="Edificios")

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

    return render_template('reportes.html', resueltos = lista_reportes_resueltos, reportes = lista_reportes ,active_page='reporte', title="Reportes")

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

    return render_template('grupos.html', salones=lista_salones, grupos = lista_grupos, active_page='grupo', title="Grupos")

#asistencia
@app.route('/asistencias', methods=['GET', 'POST'])
def asistencias():
    if request.method == 'POST':
        pass

    return render_template('asistencias.html', active_page = 'asistencia', title="Asistencias")

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

    return render_template('asignaciones.html', grupos = lista_grupos, materias = lista_materias, asignaciones = lista_grupomaterias, active_page = 'asignacion' , title="Asignaciones")

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

    return render_template('alumnos.html', grupos = lista_grupos, alumnos = lista_alumnos, active_page = 'alumno', title="Alumnos")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)