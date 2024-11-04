$(document).ready(function () {
    loadEstudiantes();
    loadGrupos();
    loadAlumnos();
    
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

    function loadGrupos() {
        $.get('/grupos', function (data) { 
            const grupoSelect = $('#GrupoId');
            grupoSelect.empty(); 
            grupoSelect.append(`<option value="">Selecciona un grupo</option>`); // Opción por defecto
            data.forEach(function (grupo) {
                grupoSelect.append(`<option value="${grupo.GrupoID}">${grupo.GrupoNombre}</option>`);
            });
        }).fail(function (xhr) {
            console.error('Error al cargar los grupos:', xhr.responseText);
        });
    }

    function loadAlumnos() {
        $.get('/alumnos', function (data) {
            $('#alumnosTableBody').empty(); // Limpiar la tabla existente
            data.forEach(function (alumno) {
                $('#alumnosTableBody').append(`
                    <tr>
                        <td>${alumno.AlumnoGrupoID}</td>
                        <td>${alumno.AlumnoNombreCompleto}</td>
                        <td>${alumno.GrupoNombre}</td>
                        <td>${alumno.AlumnoGrupoModificacion}</td>
                        <td>${alumno.AlumnoGrupoStatus}</td>
                        <td>${alumno.PersonalAdministrativoId}</td>
                        <td>
                            <button class='btn btn-warning' onclick='editAlumno(${alumno.AlumnoGrupoID})'><i class="fa-solid fa-pen-to-square"></i></button>
                            <button class='btn btn-danger' onclick='deleteAlumno(${alumno.AlumnoGrupoID})'><i class="fa-solid fa-trash"></i></button>
                        </td>
                    </tr>`);
            });
            $('#alumnosTable').removeClass('d-none'); // Mostrar la tabla
        }).fail(function (xhr) {
            console.error('Error al cargar el alumno:', xhr.responseText);
        });
    }

    $('#btnAddAlumno').on('click', function () {
        resetForm(); 
        $('#formContainer').removeClass('d-none'); 
    });

    $('#AlumnoForm').on('submit', function (e) {
        e.preventDefault(); 
        
        const AlumnosId = $('#AlumnosId').val();
        const alumnoData = {
            AlumnoID: $('#EstudianteId').val(),
            GrupoID: $('#GrupoId').val(),
            PersonalAdministrativoId: "0"
        };
    
        if (AlumnosId) { // Si existe un ID, es una actualización
            $.ajax({
                url: `/alumno/${AlumnosId}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(alumnoData),
                success: function () {
                    loadAlumnos();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al actualizar el alumno.');
                }
            });
        } else { // Si no existe un ID, es una creación
            $.ajax({
                url: '/alumno',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(alumnoData),
                success: function () {
                    loadAlumnos();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al crear el alumno.');
                }
            });
        }
    });

    window.editAlumno = function (id) {
        $.get(`/alumnos/${id}`, function (data) {
            $('#AlumnosId').val(data.AlumnoGrupoID);
            $('#EstudianteId').val(data.AlumnoID);
            $('#GrupoId').val(data.GrupoID); 
            $('#formContainer').removeClass('d-none'); 
        }).fail(function () {
            alert('Error al cargar los datos del alumno.');
        });
    };

    window.deleteAlumno = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este alumno?')) {
            $.ajax({
                url: `/alumnos/${id}`,
                type: 'DELETE',
                success: function () {
                    loadAlumnos(); 
                },
                error: function (xhr) {
                    alert('Error al eliminar el alumno.');
                    console.error('Error:', xhr.responseText);
                }
            });
        }
    };

    function resetForm() {
        $('#AlumnosId').val('');
        $('#EstudianteId').val('');
        $('#GrupoId').val('');
        $('#formContainer').addClass('d-none'); 
    }

    $('#btnCancel').on('click', resetForm);
});