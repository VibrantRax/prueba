from flask import Flask, jsonify, render_template, redirect, url_for, request, flash, session
import requests
from flask_cors import CORS
from models.alumnos import AlumnoMySQL
from models.asignaciones import AsignacionMySQL
from models.calificaciones import CalificacionesMySQL
from models.edificios import EdificiosMySQL
from models.grupos import GruposMySQL
from models.horarios import HorariosMySQL
from models.horas import HorasMySQL
from models.materias import MateriasMySQL
from models.reportes import ReportesMySQL
from models.salones import SalonesMySQL

app = Flask(__name__)
app.secret_key = "tu_secreto"  # Se requiere para usar flash
CORS(app)


url_docente = "http://34.176.222.47:5000/docentes"
url_estudiante = "http://34.176.222.47:5000/alumnos"
url_personal = 'http://34.176.222.47:5000/personal'

#------------------------------------------------------>Docentes<-----------------------------------------------------#

@app.route('/docentes', methods=['GET'])
def get_docentes():
    response = requests.get(url_docente)
    return jsonify(response.json()), 200

#---------------------------------------------------->Estudiantes<----------------------------------------------------#

@app.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    response = requests.get(url_estudiante)
    return jsonify(response.json()), 200

#------------------------------------------------------>Personal<-----------------------------------------------------#

response = requests.get(url_personal)

if response.status_code == 200:
    personal = response.json()
    # Filtra los datos necesarios (solo PersonalId, PersonalContrasena y PersonalNombre)
    filtered_data = [{ 
        'PersonalId': item['PersonalId'], 
        'PersonalContrasena': item['PersonalContrasena'],
        'PersonalNombre': item['PersonalNombre'],
        "PersonalRolDescripcion": item['PersonalRolDescripcion']
    } for item in personal]
    print("Datos de personal cargados correctamente.")

@app.route('/login', methods=['POST'])
def login():
    # Obtener los datos JSON enviados desde el frontend
    data = request.get_json()

    personal_id = data.get('personalId')
    personal_contrasena = data.get('personalContrasena')

    if not personal_id or not personal_contrasena:
        return jsonify({"status": "error", "message": "Faltan credenciales"}), 400

    # Compara los datos del formulario con los datos de la API
    for personal in filtered_data:
        # Convertir `personal_id` y `personal["PersonalId"]` a string para evitar problemas de comparación
        if str(personal['PersonalId']) == str(personal_id) and personal['PersonalContrasena'] == personal_contrasena:

            # Almacenar en sesión
            session['PersonalId'] = personal['PersonalId']
            session['PersonalNombre'] = personal['PersonalNombre']
            session['PersonalRolDescripcion'] = personal['PersonalRolDescripcion']
            
            return jsonify({"status": "success", "message": "Inicio de sesión exitoso", "redirect": url_for('principal')})
        
    return jsonify({"status": "error", "message": "Credenciales incorrectas"}), 401

#------------------------------------------------------>Alumnos<------------------------------------------------------#

# Crear un nuevo alumno
@app.route('/alumno', methods=['POST'])
def create_alumnos():

    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    id = AlumnoMySQL.ingresarAlumnos(data,personal)

    return jsonify({'message': 'Alumno creado', 'AlumnoID': id}), 201

# Leer todos los alumnos
@app.route('/alumnos', methods=['GET'])
def get_alumnos():

    alumnos = AlumnoMySQL.mostrarAlumnos()
    
    return jsonify(alumnos), 200

# Actualizar un alumno
@app.route('/alumno/<int:id>', methods=['PUT'])
def update_alumnos(id):

    #asignacion de valores
    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    AlumnoMySQL.modificarAlumno(data, id, personal)

    return jsonify({'message': 'Alumno actualizado'}), 200

# Eliminar edificio (ocultar)
@app.route('/edificio/<int:id>', methods=['DELETE'])
def delete_alumnos(id):

    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    AlumnoMySQL.eliminarAlumno(id, personal)

    return jsonify({'message': 'Alumno ocultado'}), 200

# Obtener un alumno por id
@app.route('/alumnos/<int:id>', methods=['GET'])
def get_alumno(id):

    alumnos = AlumnoMySQL.mostrarAlumnosporID(id)

    if alumnos:
        return jsonify(alumnos), 200
    else:
        return jsonify({'message': 'Alumno no encontrado'}), 404
    
#----------------------------------------------------->Asignacion<----------------------------------------------------#

# Crear una nueva asignacion
@app.route('/asignacion', methods=['POST'])
def create_asignaciones():

    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    id = AsignacionMySQL.ingresarAsignaciones(data,personal)

    return jsonify({'message': 'Asignacion creada', 'GrupoMateriaID': id}), 201

# Leer todas las asignaciones
@app.route('/asignaciones', methods=['GET'])
def get_asignaciones():

    asignaciones = AsignacionMySQL.mostrarAsignaciones()

    return jsonify(asignaciones), 200

# Actualizar una asignacion
@app.route('/asignacion/<int:id>', methods=['PUT'])
def update_asignaciones(id):

    #asignacion de valores
    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    AsignacionMySQL.modificarAsignacion(data, id, personal)

    return jsonify({'message': 'Asignacion actualizada'}), 200

# Eliminar asignacion (ocultar)
@app.route('/asignacion/<int:id>', methods=['DELETE'])
def delete_asignaciones(id):

    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    AsignacionMySQL.eliminarAsignacion(id, personal)

    return jsonify({'message': 'Asignacion ocultada'}), 200

# Obtener una asignacion por id
@app.route('/asignaciones/<int:id>', methods=['GET'])
def get_asignacion(id):

    asignaciones = AsignacionMySQL.mostrarAsignacionesporID(id)

    if asignaciones:
        return jsonify(asignaciones), 200
    else:
        return jsonify({'message': 'Asignacion no encontrada'}), 404
    
#--------------------------------------------------->Calificaiones<---------------------------------------------------#

# Crear una nueva asignacion
@app.route('/calificacion', methods=['POST'])
def create_calificaciones():

    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    id = CalificacionesMySQL.ingresarCalificacion(data,personal)

    return jsonify({'message': 'Calificacion creada', 'CalificacionID': id}), 201

# Leer todas las calificaciones
@app.route('/calificaciones', methods=['GET'])
def get_calificaciones():

    calificaciones = CalificacionesMySQL.mostrarCalificaciones()

    return jsonify(calificaciones), 200

# Actualizar una calificacion
@app.route('/calificacion/<int:id>', methods=['PUT'])
def update_calificaciones(id):

    #asignacion de valores
    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    CalificacionesMySQL.modificarCalificacion(data, id, personal)

    return jsonify({'message': 'Calificacion actualizada'}), 200

# Eliminar calificacion (ocultar)
@app.route('/calificacion/<int:id>', methods=['DELETE'])
def delete_calificaciones(id):

    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    CalificacionesMySQL.eliminarCalificacion(id, personal)

    return jsonify({'message': 'Calificacion ocultada'}), 200

# Obtener una asignacion por id
@app.route('/calificaciones/<int:id>', methods=['GET'])
def get_calificacion(id):

    calificaciones = CalificacionesMySQL.mostrarCalificacionesporID(id)

    if calificaciones:
        return jsonify(calificaciones), 200
    else:
        return jsonify({'message': 'Calificacion no encontrada'}), 404
    
#----------------------------------------------------->Edificios<-----------------------------------------------------#

# Crear un nuevo edificio
@app.route('/edificio', methods=['POST'])
def create_edificios():

    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    id = EdificiosMySQL.ingresarEdificio(data,personal)

    return jsonify({'message': 'Edificio creado', 'EdificoID': id}), 201

# Leer todos los edificios
@app.route('/edificios', methods=['GET'])
def get_edificios():

    edificios = EdificiosMySQL.mostrarEdificios()
        
    return jsonify(edificios), 200

# Actualizar un edificio
@app.route('/edificio/<int:id>', methods=['PUT'])
def update_edificios(id):

    #asignacion de valores
    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    EdificiosMySQL.modificarEdificio(data, id, personal)

    return jsonify({'message': 'Edificio actualizado'}), 200

# Eliminar edificio (ocultar)
@app.route('/edificio/<int:id>', methods=['DELETE'])
def delete_edificios(id):

    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    EdificiosMySQL.eliminarEdificio(id, personal)

    return jsonify({'message': 'Edificio ocultado'}), 200

# Obtener un edificio por id
@app.route('/edificios/<int:id>', methods=['GET'])
def get_edificio(id):

    edificios = EdificiosMySQL.mostrarEdificiosporID(id)

    if edificios:
        return jsonify(edificios), 200
    else:
        return jsonify({'message': 'Edificio no encontrado'}), 404
    
#------------------------------------------------------->Grupos<------------------------------------------------------#

# Crear un nuevo grupo
@app.route('/grupo', methods=['POST'])
def create_grupos():

    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión 
    id = GruposMySQL.ingresarGrupos(data,personal)
    
    return jsonify({'message': 'Grupo creado', 'GrupoID': id}), 201

# Leer todos los grupos
@app.route('/grupos', methods=['GET'])
def get_grupos():

    grupos = GruposMySQL.mostrarGrupos()
    
    return jsonify(grupos)

# Actualizar un grupo
@app.route('/grupo/<int:id>', methods=['PUT'])
def update_grupos(id):

    #asignacion de valores
    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    GruposMySQL.modificarGrupo(data, id, personal)

    return jsonify({'message': 'Grupo actualizado'}), 200

# Eliminar grupo (ocultar)
@app.route('/grupo/<int:id>', methods=['DELETE'])
def delete_grupos(id):

    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    GruposMySQL.eliminarGrupo(id, personal)

    return jsonify({'message': 'Grupo ocultado'}), 200

# Obtener un grupo por id
@app.route('/grupos/<int:id>', methods=['GET'])
def get_grupo(id):
    
    grupos = GruposMySQL.mostrarGruposporID(id)

    if grupos:
        return jsonify(grupos), 200
    else:
        return jsonify({'message': 'Grupo no encontrado'}), 404

#------------------------------------------------------>Horarios<-----------------------------------------------------#

# Crear un nuevo horario
@app.route('/horario', methods=['POST'])
def create_horarios():

    data = request.json 
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    id = HorariosMySQL.ingresarHorarios(data,personal)
    
    return jsonify({'message': 'Horario creadao', 'HorarioID': id}), 201

# Leer todas los horarios
@app.route('/horarios', methods=['GET'])
def get_horarios():

    horarios = HorariosMySQL.mostrarHorarios()
        
    return jsonify(horarios), 200

# Actualizar un horario
@app.route('/horario/<int:id>', methods=['PUT'])
def update_horarios(id):

    #asignacion de valores
    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    HorariosMySQL.modificarHorario(data,id, personal)

    return jsonify({'message': 'Horario actualizado'}), 200

# Eliminar horario (ocultar)
@app.route('/horario/<int:id>', methods=['DELETE'])
def delete_horarios(id):

    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    HorariosMySQL.eliminarHorario(id, personal)

    return jsonify({'message': 'Horario ocultado'}), 200

# Obtener un horario por id
@app.route('/horarios/<int:id>', methods=['GET'])
def get_horario(id):
    
    horarios = HorariosMySQL.mostrarHorariosporID(id)

    if horarios:
        return jsonify(horarios), 200
    else:
        return jsonify({'message': 'Horario no encontrado'}), 404

#------------------------------------------------------->Horas<-------------------------------------------------------#

# Crear una nueva hora
@app.route('/hora', methods=['POST'])
def create_horas():

    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    id = HorasMySQL.ingresarHoras(data,personal)
    
    return jsonify({'message': 'Hora creada', 'HoraID': id}), 201

# Leer todas las horas
@app.route('/horas', methods=['GET'])
def get_horas():

    horas = HorasMySQL.mostrarHoras()
        
    return jsonify(horas), 200

# Actualizar una hora
@app.route('/hora/<int:id>', methods=['PUT'])
def update_horas(id):

    #asignacion de valores
    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    HorasMySQL.modificarHora(data,id, personal)

    return jsonify({'message': 'Hora actualizada'}), 200

# Eliminar hora (ocultar)
@app.route('/hora/<int:id>', methods=['DELETE'])
def delete_horas(id):

    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    HorasMySQL.eliminarHora(id, personal)

    return jsonify({'message': 'Hora ocultada'}), 200

# Obtener una hora por id
@app.route('/horas/<int:id>', methods=['GET'])
def get_hora(id):

    horas = HorasMySQL.mostrarHorasporID(id)

    if horas:
        return jsonify(horas), 200
    else:
        return jsonify({'message': 'Hora no encontrada'}), 404

#------------------------------------------------------>Materias<-----------------------------------------------------#
# Crear una nueva materia
@app.route('/materia', methods=['POST'])
def create_materias():

    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    id = MateriasMySQL.ingresarMaterias(data,personal)

    return jsonify({'message': 'Materia creada', 'MateriaID': id}), 201

# Leer todas las materias
@app.route('/materias', methods=['GET'])
def get_materias():

    materias = MateriasMySQL.mostrarMaterias()

    return jsonify(materias), 200

# Actualizar una materia
@app.route('/materia/<int:id>', methods=['PUT'])
def update_materias(id):

    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    MateriasMySQL.modificarMateria(data,id, personal)

    return jsonify({'message': 'Materia actualizada'}), 200

# Eliminar materia (ocultar)
@app.route('/materia/<int:id>', methods=['DELETE'])
def delete_materias(id):

    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    MateriasMySQL.eliminarMateria(id, personal)
    
    return jsonify({'message': 'Materia ocultada'}), 200

# Obtener una materia por id
@app.route('/materias/<int:id>', methods=['GET'])
def get_materia(id):

    materias = MateriasMySQL.mostrarMateriasporID(id)

    if materias:
        return jsonify(materias), 200
    else:
        return jsonify({'message': 'Materia no encontrada'}), 404
    
#------------------------------------------------------>Reportes<-----------------------------------------------------#

# Crear un nuevo reporte
@app.route('/reporte', methods=['POST'])
def create_reportes():

    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    id = ReportesMySQL.ingresarReportes(data,personal)

    return jsonify({'message': 'Reporte creado', 'ReporteID': id}), 201

# Leer todas los reportes
@app.route('/reportes', methods=['GET'])
def get_reportes():

    reportes = ReportesMySQL.mostrarReportes()

    return jsonify(reportes), 200

# Actualizar un reporte
@app.route('/reporte/<int:id>', methods=['PUT'])
def update_reportes(id):

    #asignacion de valores
    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    ReportesMySQL.modificarReporte(data, id, personal)

    return jsonify({'message': 'Reporte actualizado'}), 200

# Eliminar reporte (ocultar)
@app.route('/reporte/<int:id>', methods=['DELETE'])
def delete_reportes(id):

    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    ReportesMySQL.eliminarReporte(id, personal)

    return jsonify({'message': 'Reporte ocultado'}), 200

# Obtener un reporte por id
@app.route('/reportes/<int:id>', methods=['GET'])
def get_reporte(id):

    reportes = ReportesMySQL.mostrarReportesporID(id)

    if reportes:
        return jsonify(reportes), 200
    else:
        return jsonify({'message': 'Reporte no encontrado'}), 404

#------------------------------------------------------>Salones<------------------------------------------------------#
# Crear un nuevo salon
@app.route('/salon', methods=['POST'])
def create_salones():

    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    id = SalonesMySQL.ingresarSalon(data,personal)

    return jsonify({'message': 'Salon creado', 'SalonID': id}), 201

# Leer todas los salones
@app.route('/salones', methods=['GET'])
def get_salones():

    salones = SalonesMySQL.mostrarSalones()

    return jsonify(salones), 200

# Actualizar un salon
@app.route('/salon/<int:id>', methods=['PUT'])
def update_salones(id):

    #asignacion de valores
    data = request.json
    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    SalonesMySQL.modificarSalon(data, id, personal)

    return jsonify({'message': 'Salon actualizado'}), 200

# Eliminar salon (ocultar)
@app.route('/salon/<int:id>', methods=['DELETE'])
def delete_salones(id):

    personal = session.get('PersonalId')  # Obtener el PersonalId de la sesión
    SalonesMySQL.eliminarSalon(id, personal)

    return jsonify({'message': 'Salon ocultado'}), 200

# Obtener un salon por id
@app.route('/salones/<int:id>', methods=['GET'])
def get_salon(id):

    salones = SalonesMySQL.mostrarSalonesporID(id)

    if salones:
        return jsonify(salones), 200
    else:
        return jsonify({'message': 'Salon no encontrado'}), 404

#------------------------------------------------------->Rutas<-------------------------------------------------------#
@app.route('/')
def home():
    return render_template('login.html', title="Login")

@app.route('/principal')
def principal():
    if 'PersonalId' not in session:
        return redirect('/')
    
    foto = str(session.get('PersonalId')) 
    return render_template('principal.html', active_page='inicio', title="Inicio", foto = foto)

@app.route('/alumno')
def alumnos():
    if 'PersonalId' not in session:
        return redirect('/')
    
    foto = str(session.get('PersonalId'))
    return render_template('alumnos.html', active_page='alumno', title="Alumnos", foto = foto)

@app.route('/asignacion')
def asignaciones():
    if 'PersonalId' not in session:
        return redirect('/')
    
    foto = str(session.get('PersonalId'))
    return render_template('asignaciones.html', active_page='asignacion', title="Asignaciones", foto = foto)

@app.route('/calificacion')
def calificaciones():
    if 'PersonalId' not in session:
        return redirect('/')
    
    foto = str(session.get('PersonalId'))
    return render_template('calificaciones.html', active_page='calificacion', title="Calificaciones", foto = foto)

@app.route('/edificio')
def edificios():
    if 'PersonalId' not in session:
        return redirect('/')
    
    foto = str(session.get('PersonalId'))
    return render_template('edificios.html', active_page='edificios', title="Edificios", foto = foto)

@app.route('/grupo')
def grupos():
    if 'PersonalId' not in session:
        return redirect('/')
    
    foto = str(session.get('PersonalId'))
    return render_template('grupos.html', active_page='grupo', title="Grupos", foto = foto)

@app.route('/horario')
def horarios():
    if 'PersonalId' not in session:
        return redirect('/')
    
    foto = str(session.get('PersonalId'))
    return render_template('horarios.html', active_page='horario', title="Horarios", foto = foto)

@app.route('/hora')
def horas():
    if 'PersonalId' not in session:
        return redirect('/')
    
    foto = str(session.get('PersonalId'))
    return render_template('horas.html', active_page='horas', title="Horas", foto = foto)

@app.route('/materia')
def materias():
    if 'PersonalId' not in session:
        return redirect('/')
    
    foto = str(session.get('PersonalId'))
    return render_template('materias.html', active_page='materias', title="Materias", foto = foto)

@app.route('/reporte')
def reportes():
    if 'PersonalId' not in session:
        return redirect('/')
    
    foto = str(session.get('PersonalId'))
    return render_template('reportes.html', active_page='reporte', title="Reportes", foto = foto)

@app.route('/salon')
def salones():
    if 'PersonalId' not in session:
        return redirect('/')
    
    foto = str(session.get('PersonalId'))
    return render_template('salones.html', active_page='salon', title="Salones", foto = foto)

@app.route('/logout')
def logout():
    session.clear()  # Limpiar toda la sesión
    return redirect('/')  # Redirigir a la página de inicio de sesión

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)