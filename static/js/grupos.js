$(document).ready(function () {
    loadDocente();
    loadSalones();
    loadGrupos();
    
    function loadDocente() {
        $.get('/docentes', function (data) { 
            const docenteSelect = $('#DocenteId');
            docenteSelect.empty(); 
            docenteSelect.append(`<option value="">Selecciona un docente</option>`); // Opción por defecto
            data.forEach(function (docente) {
                docenteSelect.append(`<option value="${docente.DocenteId}">${docente.DocenteId} — ${docente.DocenteNombre} ${docente.DocentePrimerApellido} ${docente.DocenteSegundoApellido}</option>`);
            });
        }).fail(function (xhr) {
            console.error('Error al cargar los roles:', xhr.responseText);
        });
    }

    function loadSalones() {
        $.get('/salones', function (data) { 
            const docenteSelect = $('#SalonesId');
            docenteSelect.empty(); 
            docenteSelect.append(`<option value="">Selecciona un salon</option>`); // Opción por defecto
            data.forEach(function (salon) {
                docenteSelect.append(`<option value="${salon.SalonID}">${salon.SalonNumero}</option>`);
            });
        }).fail(function (xhr) {
            console.error('Error al cargar los roles:', xhr.responseText);
        });
    }

    function loadGrupos() {
        $.get('/grupos', function (data) {
            $('#gruposTableBody').empty(); // Limpiar la tabla existente
            data.forEach(function (grupo) {
                $('#gruposTableBody').append(`
                    <tr>
                        <td>${grupo.GrupoID}</td>
                        <td>${grupo.DocenteNombreCompleto}</td>
                        <td>${grupo.GrupoNombre}</td>
                        <td>${grupo.SalonNumero}</td>
                        <td>${grupo.EdificioNombre}</td>
                        <td>${grupo.GrupoFechaModificacion}</td>
                        <td>${grupo.GrupoStatus}</td>
                        <td>${grupo.PersonalAdministrativoId}</td>
                        <td>
                            <button class='btn btn-warning' onclick='editGrupo(${grupo.GrupoID})'><i class="fa-solid fa-pen-to-square"></i></button>
                            <button class='btn btn-danger' onclick='deleteGrupo(${grupo.GrupoID})'><i class="fa-solid fa-trash"></i></button>
                        </td>
                    </tr>`);
            });
            $('#gruposTable').removeClass('d-none'); // Mostrar la tabla
        }).fail(function (xhr) {
            console.error('Error al cargar el grupo:', xhr.responseText);
        });
    }

    $('#btnAddGrupo').on('click', function () {
        resetForm(); 
        $('#formContainer').removeClass('d-none'); 
    });

    $('#GrupoForm').on('submit', function (e) {
        e.preventDefault(); 
        
        const GrupoId = $('#GrupoId').val();
        const grupoData = {
            DocenteId: $('#DocenteId').val(),
            GrupoNombre: $('#GrupoNombre').val(),
            SalonID: $('#SalonesId').val(),
            PersonalAdministrativoId: "0"
        };
    
        if (GrupoId) { // Si existe un ID, es una actualización
            $.ajax({
                url: `/grupo/${GrupoId}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(grupoData),
                success: function () {
                    loadGrupos();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al actualizar el grupo.');
                }
            });
        } else { // Si no existe un ID, es una creación
            $.ajax({
                url: '/grupo',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(grupoData),
                success: function () {
                    loadGrupos();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al crear el grupo.');
                }
            });
        }
    });

    window.editGrupo = function (id) {
        $.get(`/grupos/${id}`, function (data) {
            $('#GrupoId').val(data.GrupoID);
            $('#DocenteId').val(data.DocenteId);
            $('#GrupoNombre').val(data.GrupoNombre); 
            $('#SalonesId').val(data.SalonID); 
            
            $('#formContainer').removeClass('d-none'); 
        }).fail(function () {
            alert('Error al cargar los datos del grupo.');
        });
    };

    window.deleteGrupo = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este salon?')) {
            $.ajax({
                url: `/salon/${id}`,
                type: 'DELETE',
                success: function () {
                    loadGrupos(); 
                },
                error: function (xhr) {
                    alert('Error al eliminar el grupo.');
                    console.error('Error:', xhr.responseText);
                }
            });
        }
    };

    function resetForm() {
        $('#GrupoId').val('');
        $('#DocenteId').val('');
        $('#GrupoNombre').val('');
        $('#SalonesId').val('');
        $('#formContainer').addClass('d-none'); 
    }

    $('#btnCancel').on('click', resetForm);
});