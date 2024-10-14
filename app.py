from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from datetime import datetime
from models.salones import SalonesMySQL
from models.edificios import EdificiosMySQL
from models.materias import MateriasMySQL
from models.reportes import ReportesMySQL
from models.grupo import GruposMySQL

app = Flask(__name__)
app.secret_key = "tu_secreto"  # Se requiere para usar flash

# Rutas

#inicio de sesion
@app.route('/')
def inicio_sesion():
    return render_template('inicio_sesion.html',)

#principal
@app.route('/principal', methods=['GET', 'POST'])
def principal():
    return render_template('principal.html',active_page='inicio')

#materias
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

    return render_template('materias.html', materias=lista_materias, active_page='materias')

#salones
@app.route('/salones', methods=['GET', 'POST'])
def salones():

    if request.method == 'POST':
        if 'guardar' in request.form:

            salon = request.form['salon']
            edificio_id = request.form['edificio']

            if not edificio_id:
                flash("Por favor ingrese el nombre del edificio.")
            elif not salon:
                flash("Por favor ingrese el salon")
            else:
                SalonesMySQL.ingresarSalon(salon, edificio_id)
                flash("Los datos fueron guardados.")

        elif 'modificar' in request.form:
            salon = request.form['salon']
            edificio_id = request.form['edificioSelect']
            if not salon or not edificio_id:
                flash("Falta ID o Materia.")
            else:
                SalonesMySQL.modificarSalon(salon, edificio_id)
                flash("Los datos fueron modificados.")

        elif 'eliminar' in request.form:
            salon = request.form['salon']
            if not id:
                flash("Falta ID")
            else:
                SalonesMySQL.eliminarSalon(salon)

    lista_salones = SalonesMySQL.mostrarSalones()
    lista_edificios = EdificiosMySQL.mostrarEdificios()

    return render_template('salones.html', salones=lista_salones, edificios=lista_edificios, active_page='salon')

#edificios
@app.route('/edificios', methods=['GET', 'POST'])
def edificios():
    if request.method == 'POST':
        if 'guardar' in request.form:
            edificio = request.form['edificio']
            if not edificio:
                flash("Por favor ingrese el nombre del edificio.")
            else:
                EdificiosMySQL.ingresarEdifico(edificio)
                flash("Los datos fueron guardados.")
        
        elif 'modificar' in request.form:
            id = request.form['id']
            edificio = request.form['edificio']
            if not id or not edificio:
                flash("Falta ID o Edificio.")
            else:
                # Actualiza el edificio con el ID real
                EdificiosMySQL.modificarEdificio(id, edificio)
                flash("Los datos fueron modificados.")

        elif 'eliminar' in request.form:
            id = request.form['id']
            if not id:
                flash("Falta ID")
            else:
                # Ingresar lógica para eliminar edificio
                EdificiosMySQL.eliminarEdificio(id)
                flash("El edificio fue eliminado.")

    lista_edificios = EdificiosMySQL.mostrarEdificios()
    return render_template('edificios.html', edificios=lista_edificios, active_page='edificios')

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
                flash("Los datos fueron guardados.")

        elif 'eliminar' in request.form:
            id = request.form['id']
            if not id:
                flash("Falta ID")
            else:
                ReportesMySQL.eliminarReporte(id)
                flash("El reporte fue eliminado.")

    lista_reportes_resueltos = ReportesMySQL.mostrarReportesResueltos()
    lista_reportes = ReportesMySQL.mostrarReportes()

    return render_template('reportes.html', resueltos = lista_reportes_resueltos, reportes = lista_reportes ,active_page='reporte')

#grupos
@app.route('/grupos', methods=['GET', 'POST'])
def grupos():
    if request.method == 'POST':
        pass

    lista_salones = SalonesMySQL.mostrarSalones()
    lista_grupos = GruposMySQL.mostrarGrupos()

    return render_template('grupos.html', salones=lista_salones, grupos = lista_grupos, active_page='grupo')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)