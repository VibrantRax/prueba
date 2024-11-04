$(document).ready(function () {
    // Cargar las materias al inicio
    loadHoras();

    function loadHoras(){
        $.get('/horas', function (data) {
            $('#horasTableBody').empty(); // Limpia el contenido de la tabla
            data.forEach(function (hora) {
                $('#horasTableBody').append(`
                    <tr>
                        <td>${hora.HoraID}</td>
                        <td>${hora.HoraInicio}</td>
                        <td>${hora.HoraFin}</td>
                        <td>${hora.HoraFechaModificacion}</td>
                        <td>${hora.HoraStatus}</td>
                        <td>${hora.PersonalAdministrativoId}</td>
                        <td>
                            <button class='btn btn-warning' onclick='editHora(${hora.HoraID})'><ion-icon name="create"></ion-icon></button>
                            <button class='btn btn-danger' onclick='deleteHora(${hora.HoraID})'><ion-icon name="trash"></ion-icon></button>
                        </td>
                    </tr>`);
            });
            $('#horasTable').removeClass('d-none');
        });
    }

    $('#btnAddHora').on('click', function () {
        resetForm(); 
        $('#formContainer').removeClass('d-none'); 
    });

    $('#horaForm').on('submit', function (e) {
        e.preventDefault(); 
        
        const horaId = $('#horaId').val();
        const horaData = {
            HoraInicio: $('#textoHoraInicio').val(),
            HoraFin: $('#textoHoraFin').val(),
            PersonalAdministrativoId: "0" 
        };

        if (horaId) {
            $.ajax({
                url: `/hora/${horaId}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(horaData),
                success: function () {
                    loadHoras();
                    resetForm();
                },
                error: function (xhr, status, error) {
                    console.error('Error al actualizar la hora:', xhr.responseText);
                    alert('Error al actualizar la hora. Ver consola para más detalles.');
                }
            });
        } else {
            $.ajax({
                url: '/hora',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(horaData),
                success: function () {
                    loadHoras();
                    resetForm();
                },
                error: function (xhr) {
                    console.error('Error al crear la hora:', xhr.responseText);
                    alert('Error al crear la hora. Ver consola para más detalles.');
                }
            });
        }
    });

    window.editHora = function (id) {
        $.get(`/horas/${id}`, function (data) {
            const hora = Array.isArray(data) ? data[0] : data;
            
            if (hora) {
                // Rellena los campos ocultos con los valores recibidos
                $('#horaId').val(hora.HoraID);
                $('#textoHoraInicio').val(hora.HoraInicio);
                $('#textoHoraFin').val(hora.HoraFin);
                
                // Llama a convertirAHora para actualizar los inputs visibles
                convertirAHora('HoraInicio', 'textoHoraInicio');
                convertirAHora('HoraFin', 'textoHoraFin');
                
                $('#formContainer').removeClass('d-none');
            } else {
                alert('No se encontraron datos para esta hora.');
            }
        }).fail(function (xhr) {
            console.error('Error al cargar los datos de la hora:', xhr.responseText);
            alert('Error al cargar los datos de la hora.');
        });
    };    

    window.deleteHora = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar esta hora?')) {
            $.ajax({
                url: `/horas/${id}`,
                type: 'DELETE',
                success: function () {
                    loadHoras();
                }
            });
        }
    };

    function resetForm() {
        $('#horaId').val('');
        $('#textoHoraInicio').val('');
        $('#textoHoraFin').val('');
        $('#HoraInicio').val('');
        $('#HoraFin').val('');
        $('#formContainer').addClass('d-none'); 
    }

    $('#btnCancel').on('click', resetForm);
});
