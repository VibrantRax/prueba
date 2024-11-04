$(document).ready(function () {
    loadMaterias();
    loadHoras();
    loadHorarios(); 

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

    function loadHoras() {
        $.get('/horas', function (data) { 
            const horasSelect = $('#HoraId');
            horasSelect.empty(); 
            horasSelect.append(`<option value="">Selecciona una hora</option>`); // Opción por defecto
            data.forEach(function (hora) {
                horasSelect.append(`<option value="${hora.HoraID}">${hora.HoraInicio} — ${hora.HoraFin}</option>`);
            });
        }).fail(function (xhr) {
            console.error('Error al cargar las horas:', xhr.responseText);
        });
    }

    function loadHorarios() {
        $.get('/horarios', function (data) {
            $('#horariosTableBody').empty(); // Limpiar la tabla existente
            data.forEach(function (horario) {
                $('#horariosTableBody').append(`
                    <tr>
                        <td>${horario.HorarioID}</td>
                        <td>${horario.MateriaNombre}</td>
                        <td>${horario.HorarioDiaSemana}</td>
                        <td>${horario.HoraInicio} — ${horario.HoraFin}</td>
                        <td>${horario.HorarioFechaModificacion}</td>
                        <td>${horario.HorarioStatus}</td>
                        <td>${horario.PersonalAdministrativoId}</td>
                        <td>
                            <button class='btn btn-warning' onclick='editHorario(${horario.HorarioID})'><i class="fa-solid fa-pen-to-square"></i></button>
                            <button class='btn btn-danger' onclick='deleteHorario(${horario.HorarioID})'><i class="fa-solid fa-trash"></i></button>
                        </td>
                    </tr>`);
            });
            $('#horariosTable').removeClass('d-none'); // Mostrar la tabla
        }).fail(function (xhr) {
            console.error('Error al cargar el horario:', xhr.responseText);
        });
    }

    $('#btnAddHorario').on('click', function () {
        resetForm(); 
        $('#formContainer').removeClass('d-none'); 
    });

    $('#horarioForm').on('submit', function (e) {
        e.preventDefault(); 
        
        const horarioId = $('#horarioId').val();
        const horarioData = {
            MateriaID: $('#MateriaId').val(),
            HorarioDiaSemana: $('#SemanaDia').val(),
            HoraID: $('#HoraId').val(),
            PersonalAdministrativoId: "0"
        };
    
        if (horarioId) { // Si existe un ID, es una actualización
            $.ajax({
                url: `/horario/${horarioId}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(horarioData),
                success: function () {
                    loadHorarios();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al actualizar el horario.');
                }
            });
        } else { // Si no existe un ID, es una creación
            $.ajax({
                url: '/horario',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(horarioData),
                success: function () {
                    loadHorarios();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al crear el horario.');
                }
            });
        }
    });

    window.editHorario = function (id) {
        $.get(`/horarios/${id}`, function (data) {
            $('#horarioId').val(data.HorarioID);
            $('#MateriaId').val(data.MateriaID);
            $('#SemanaDia').val(data.HorarioDiaSemana);
            $('#HoraId').val(data.HoraID);
            
            $('#formContainer').removeClass('d-none'); 
        }).fail(function () {
            alert('Error al cargar los datos del horario.');
        });
    };

    window.deleteHorario = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este horario?')) {
            $.ajax({
                url: `/horarios/${id}`,
                type: 'DELETE',
                success: function () {
                    loadHorarios(); 
                },
                error: function (xhr) {
                    alert('Error al eliminar el horario.');
                    console.error('Error:', xhr.responseText);
                }
            });
        }
    };

    function resetForm() {
        $('#horarioId').val('');
        $('#MateriaId').val('');
        $('#SemanaDia').val('');
        $('#HoraId').val('');
        $('#formContainer').addClass('d-none'); 
    }

    $('#btnCancel').on('click', resetForm);
});