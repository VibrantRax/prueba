$(document).ready(function () {
    loadEdificios();
    loadSalones(); 

    function loadEdificios() {
        $.get('/edificios', function (data) { 
            const edificioSelect = $('#EdificiosId');
            edificioSelect.empty(); 
            edificioSelect.append(`<option value="">Selecciona un edificio</option>`); // Opción por defecto
            data.forEach(function (edificio) {
                edificioSelect.append(`<option value="${edificio.EdificioID}">${edificio.EdificioNombre}</option>`);
            });
        }).fail(function (xhr) {
            console.error('Error al cargar los roles:', xhr.responseText);
        });
    }

    function loadSalones() {
        $.get('/salones', function (data) {
            $('#salonesTableBody').empty(); // Limpiar la tabla existente
            data.forEach(function (salon) {
                $('#salonesTableBody').append(`
                    <tr>
                        <td>${salon.SalonID}</td>
                        <td>${salon.SalonNumero}</td>
                        <td>${salon.EdificioNombre || 'Sin Edificio'}</td>
                        <td>${salon.SalonFechaModificacion}</td>
                        <td>${salon.SalonStatus}</td>
                        <td>${salon.PersonalAdministrativoId}</td>
                        <td>
                            <button class='btn btn-warning' onclick='editSalon(${salon.SalonID})'><i class="fa-solid fa-pen-to-square"></i></button>
                            <button class='btn btn-danger' onclick='deleteSalon(${salon.SalonID})'><i class="fa-solid fa-trash"></i></button>
                        </td>
                    </tr>`);
            });
            $('#salonesTable').removeClass('d-none'); // Mostrar la tabla
        }).fail(function (xhr) {
            console.error('Error al cargar el salon:', xhr.responseText);
        });
    }

    $('#btnAddSalon').on('click', function () {
        resetForm(); 
        $('#formContainer').removeClass('d-none'); 
    });

    $('#salonForm').on('submit', function (e) {
        e.preventDefault(); 
        
        const salonId = $('#salonId').val();
        const salonData = {
            SalonNumero: $('#SalonNumero').val(),
            EdificioID: $('#EdificiosId').val(),
            PersonalAdministrativoId: "0"
        };
    
        if (salonId) { // Si existe un ID, es una actualización
            $.ajax({
                url: `/salon/${salonId}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(salonData),
                success: function () {
                    loadSalones();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al actualizar el salon.');
                }
            });
        } else { // Si no existe un ID, es una creación
            $.ajax({
                url: '/salon',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(salonData),
                success: function () {
                    loadSalones();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al crear el salon.');
                }
            });
        }
    });

    window.editSalon = function (id) {
        $.get(`/salones/${id}`, function (data) {
            $('#salonId').val(data.SalonID);
            $('#SalonNumero').val(data.SalonNumero);
            $('#EdificiosId').val(data.EdificioID); 
            
            $('#formContainer').removeClass('d-none'); 
        }).fail(function () {
            alert('Error al cargar los datos del salon.');
        });
    };

    window.deleteSalon = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este salon?')) {
            $.ajax({
                url: `/salones/${id}`,
                type: 'DELETE',
                success: function () {
                    loadSalones(); 
                },
                error: function (xhr) {
                    alert('Error al eliminar el salon.');
                    console.error('Error:', xhr.responseText);
                }
            });
        }
    };

    function resetForm() {
        $('#salonId').val('');
        $('#SalonNumero').val('');
        $('#EdificiosId').val('');
        $('#formContainer').addClass('d-none'); 
    }

    $('#btnCancel').on('click', resetForm);
});