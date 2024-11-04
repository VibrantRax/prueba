$(document).ready(function () {
    loadEstudiantes();
    loadMaterias();
    loadCalificaciones();
    
    function loadEstudiantes() {
        $.get('/estudiantes', function (data) { 
            const estudianteSelect = $('#EstudianteId');
            estudianteSelect.empty(); 
            estudianteSelect.append(`<option value="">Selecciona un alumno</option>`); // Opción por defecto
            data.forEach(function (alumno) {
                estudianteSelect.append(`<option value="${alumno.AlumnoId}">${alumno.AlumnoId} — ${alumno.AlumnoNombre} ${alumno.AlumnoPrimerApellido} ${alumno.AlumnoSegundoApellido}</option>`);
            });
        }).fail(function (xhr) {
            console.error('Error al cargar los estudiantes:', xhr.responseText);
        });
    }

    function loadMaterias() {
        $.get('/materias', function (data) { 
            const materiasSelect = $('#MateriaId');
            materiasSelect.empty(); 
            materiasSelect.append(`<option value="">Selecciona una materia</option>`); // Opción por defecto
            data.forEach(function (materia) {
                materiasSelect.append(`<option value="${materia.MateriaID}">${materia.MateriaNombre}</option>`);
            });
        }).fail(function (xhr) {
            console.error('Error al cargar las materias:', xhr.responseText);
        });
    }

    function loadCalificaciones() {
        $.get('/calificaciones', function (data) {
            $('#calificacionesTableBody').empty(); // Limpiar la tabla existente
            data.forEach(function (calificacion) {

                // Determina si está aprobado o no según la calificación
                const estadoAprobacion = calificacion.CalificacionDetalle >= 6 ? "<span class='text-success'>Aprobado</span>" : "<span class='text-danger'>Reprobado</span>";

                $('#calificacionesTableBody').append(`
                    <tr>
                        <td>${calificacion.CalificacionID}</td>
                        <td>${calificacion.AlumnoNombreCompleto}</td>
                        <td>${calificacion.MateriaNombre}</td>
                        <td>${calificacion.CalificacionDetalle}</td>
                        <td>${estadoAprobacion}</td> <!-- Columna de Aprobación -->
                        <td>${calificacion.CalificacionFechaModificacion}</td>
                        <td>${calificacion.CalificacionStatus}</td>
                        <td>${calificacion.PersonalAdministrativoId}</td>
                        <td>
                            <button class='btn btn-warning' onclick='editCalificacion(${calificacion.CalificacionID})'><i class="fa-solid fa-pen-to-square"></i></button>
                            <button class='btn btn-danger' onclick='deleteAlumno(${calificacion.CalificacionID})'><i class="fa-solid fa-trash"></i></button>
                        </td>
                    </tr>`);
            });
            $('#calificacionesTable').removeClass('d-none'); // Mostrar la tabla
        }).fail(function (xhr) {
            console.error('Error al cargar la calificacion:', xhr.responseText);
        });
    }

    $('#btnAddCalificacion').on('click', function () {
        resetForm(); 
        $('#formContainer').removeClass('d-none'); 
    });

    $('#CalificacionForm').on('submit', function (e) {
        e.preventDefault(); 
        
        const CalificacionId = $('#CalificacionId').val();
        const calificacionData = {
            AlumnoID: $('#EstudianteId').val(),
            MateriaID: $('#MateriaId').val(),
            CalificacionDetalle: $('#CalificacionDetalle').val(),
            PersonalAdministrativoId: "0"
        };
    
        if (CalificacionId) { // Si existe un ID, es una actualización
            $.ajax({
                url: `/calificacion/${CalificacionId}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(calificacionData),
                success: function () {
                    loadCalificaciones();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al actualizar la calificacion.');
                }
            });
        } else { // Si no existe un ID, es una creación
            $.ajax({
                url: '/calificacion',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(calificacionData),
                success: function () {
                    loadCalificaciones();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al crear la calificacion.');
                }
            });
        }
    });

    window.editCalificacion = function (id) {
        $.get(`/calificaciones/${id}`, function (data) {
            $('#CalificacionId').val(data.CalificacionID);
            $('#EstudianteId').val(data.AlumnoID);
            $('#MateriaId').val(data.MateriaID);
            $('#CalificacionDetalle').val(data.CalificacionDetalle); 
            $('#formContainer').removeClass('d-none'); 
        }).fail(function () {
            alert('Error al cargar los datos de la calificacion.');
        });
    };

    window.deleteAlumno = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar esta calificacion?')) {
            $.ajax({
                url: `/calificaciones/${id}`,
                type: 'DELETE',
                success: function () {
                    loadCalificaciones(); 
                },
                error: function (xhr) {
                    alert('Error al eliminar la calificacion.');
                    console.error('Error:', xhr.responseText);
                }
            });
        }
    };

    function resetForm() {
        $('#CalificacionId').val('');
        $('#EstudianteId').val('');
        $('#MateriaId').val('');
        $('#CalificacionDetalle').val('');
        $('#formContainer').addClass('d-none'); 
    }

    $('#btnCancel').on('click', resetForm);
});