$(document).ready(function () {
    loadGrupos();
    loadMaterias();
    loadAsignaciones(); 

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

    function loadAsignaciones() {
        $.get('/asignaciones', function (data) {
            $('#asignacionTableBody').empty(); // Limpiar la tabla existente
            data.forEach(function (asignacion) {
                $('#asignacionTableBody').append(`
                    <tr>
                        <td>${asignacion.GrupoMateriaID}</td>
                        <td>${asignacion.GrupoNombre}</td>
                        <td>${asignacion.MateriaNombre || 'Sin Edificio'}</td>
                        <td>${asignacion.GrupoMateriaFechaModificacion}</td>
                        <td>${asignacion.GrupoMateriaStatus}</td>
                        <td>${asignacion.PersonalAdministrativoId}</td>
                        <td>
                            <button class='btn btn-warning' onclick='editAsignacion(${asignacion.GrupoMateriaID})'><i class="fa-solid fa-pen-to-square"></i></button>
                            <button class='btn btn-danger' onclick='deleteAsignacion(${asignacion.GrupoMateriaID})'><i class="fa-solid fa-trash"></i></button>
                        </td>
                    </tr>`);
            });
            $('#asignacionTable').removeClass('d-none'); // Mostrar la tabla
        }).fail(function (xhr) {
            console.error('Error al cargar la asignacion:', xhr.responseText);
        });
    }

    $('#btnAddAsignacion').on('click', function () {
        resetForm(); 
        $('#formContainer').removeClass('d-none'); 
    });

    $('#asignacionForm').on('submit', function (e) {
        e.preventDefault(); 
        
        const asignacionId = $('#asignacionId').val();
        const asignacionData = {
            GrupoID: $('#GrupoId').val(),
            MateriaID: $('#MateriaId').val(),
            PersonalAdministrativoId: "0"
        };
    
        if (asignacionId) { // Si existe un ID, es una actualización
            $.ajax({
                url: `/asignacion/${asignacionId}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(asignacionData),
                success: function () {
                    loadAsignaciones();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al actualizar la asignacion.');
                }
            });
        } else { // Si no existe un ID, es una creación
            $.ajax({
                url: '/asignacion',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(asignacionData),
                success: function () {
                    loadAsignaciones();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al crear la asignacion.');
                }
            });
        }
    });

    window.editAsignacion = function (id) {
        $.get(`/asignaciones/${id}`, function (data) {
            $('#asignacionId').val(data.GrupoMateriaID);
            $('#GrupoId').val(data.GrupoID);
            $('#MateriaId').val(data.MateriaID); 
            
            $('#formContainer').removeClass('d-none'); 
        }).fail(function () {
            alert('Error al cargar los datos de la asignacion.');
        });
    };

    window.deleteAsignacion = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar esta asignacion?')) {
            $.ajax({
                url: `/asignacion/${id}`,
                type: 'DELETE',
                success: function () {
                    loadAsignaciones(); 
                },
                error: function (xhr) {
                    alert('Error al eliminar la asignacion.');
                    console.error('Error:', xhr.responseText);
                }
            });
        }
    };

    function resetForm() {
        $('#asignacionId').val('');
        $('#GrupoId').val('');
        $('#MateriaId').val('');
        $('#formContainer').addClass('d-none'); 
    }

    $('#btnCancel').on('click', resetForm);
});