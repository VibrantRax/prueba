$(document).ready(function () {
    // Cargar los edificios al inicio
    loadEdificios();

    function loadEdificios(){
        $.get('/edificios', function (data) {
            $('#edificiosTableBody').empty(); // Limpia el contenido de la tabla
            data.forEach(function (edificio) {
                $('#edificiosTableBody').append(`
                    <tr>
                        <td>${edificio.EdificioID}</td>
                        <td>${edificio.EdificioNombre}</td>
                        <td>${edificio.EdificioFechaModificacion}</td>
                        <td>${edificio.EdificioStatus}</td>
                        <td>${edificio.PersonalAdministrativoId}</td>
                        <td>
                            <button class='btn btn-warning' onclick='editEdificio(${edificio.EdificioID})'><ion-icon name="create"></ion-icon></button>
                            <button class='btn btn-danger' onclick='deleteEdificio(${edificio.EdificioID})'><ion-icon name="trash"></ion-icon></button>
                        </td>
                    </tr>`);
            });
            $('#edificiosTable').removeClass('d-none');
        });
    }

    $('#btnAddEdificio').on('click', function () {
        resetForm(); 
        $('#formContainer').removeClass('d-none'); 
    });

    $('#edificioForm').on('submit', function (e) {
        e.preventDefault(); 
        
        const edificioId = $('#edificioId').val();
        const edificioData = {
            EdificioNombre: $('#EdificioNombre').val(),
            PersonalAdministrativoId: "0" 
        };

        if (edificioId) {
            $.ajax({
                url: `/edificio/${edificioId}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(edificioData),
                success: function () {
                    loadEdificios();
                    resetForm();
                },
                error: function (xhr, status, error) {
                    console.error('Error al actualizar el edificio:', xhr.responseText);
                    alert('Error al actualizar el edificio. Ver consola para más detalles.');
                }
            });
        } else {
            $.ajax({
                url: '/edificio',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(edificioData),
                success: function () {
                    loadEdificios();
                    resetForm();
                },
                error: function (xhr) {
                    console.error('Error al crear el edificio:', xhr.responseText);
                    alert('Error al crear el edificio. Ver consola para más detalles.');
                }
            });
        }
    });

    window.editEdificio = function (id) {
        $.get(`/edificios/${id}`, function (data) {
            console.log(data);
            
            // Verifica si 'data' contiene los campos esperados
            if (data && data.EdificioID) {  // Verifica que data contenga el ID del edificio
                $('#edificioId').val(data.EdificioID); // Asigna el ID al campo oculto
                $('#EdificioNombre').val(data.EdificioNombre); // Asigna el nombre al campo
                $('#formContainer').removeClass('d-none'); // Muestra el formulario
            } else {
                alert('Edificio no encontrado.'); // Mensaje de error si no se encuentra el edificio
            }
        }).fail(function (xhr) {
            console.error('Error al cargar los datos del edificio:', xhr.responseText);
            alert('Error al cargar los datos del edificio.');
        });
    };

    window.deleteEdificio = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este edificio?')) {
            $.ajax({
                url: `/edificios/${id}`,
                type: 'DELETE',
                success: function () {
                    loadEdificios();
                }
            });
        }
    };

    function resetForm() {
        $('#edificioId').val('');
        $('#EdificioNombre').val('');
        $('#formContainer').addClass('d-none'); 
    }

    $('#btnCancel').on('click', resetForm);
});
