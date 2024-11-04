$(document).ready(function () {
    // Cargar las materias al inicio
    loadMaterias();

    function loadMaterias(){
        $.get('/materias', function (data) {
            $('#materiasTableBody').empty(); // Limpia el contenido de la tabla
            data.forEach(function (materia) {
                $('#materiasTableBody').append(`
                    <tr>
                        <td>${materia.MateriaID}</td>
                        <td>${materia.MateriaNombre}</td>
                        <td>${materia.MateriaFechaModificacion}</td>
                        <td>${materia.MateriaStatus}</td>
                        <td>${materia.PersonalAdministrativoId}</td>
                        <td>
                            <button class='btn btn-warning' onclick='editMateria(${materia.MateriaID})'><ion-icon name="create"></ion-icon></button>
                            <button class='btn btn-danger' onclick='deleteMateria(${materia.MateriaID})'><ion-icon name="trash"></ion-icon></button>
                        </td>
                    </tr>`);
            });
            $('#materiasTable').removeClass('d-none');
        });
    }

    $('#btnAddMateria').on('click', function () {
        resetForm(); 
        $('#formContainer').removeClass('d-none'); 
    });

    $('#materiaForm').on('submit', function (e) {
        e.preventDefault(); 
        
        const materiaId = $('#materiaId').val();
        const materiaData = {
            MateriaNombre: $('#MateriaNombre').val(),
            PersonalAdministrativoId: "0" 
        };

        if (materiaId) {
            $.ajax({
                url: `/materia/${materiaId}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(materiaData),
                success: function () {
                    loadMaterias();
                    resetForm();
                },
                error: function (xhr, status, error) {
                    console.error('Error al actualizar la materia:', xhr.responseText);
                    alert('Error al actualizar la materia. Ver consola para más detalles.');
                }
            });
        } else {
            $.ajax({
                url: '/materia',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(materiaData),
                success: function () {
                    loadMaterias();
                    resetForm();
                },
                error: function (xhr) {
                    console.error('Error al crear la materia:', xhr.responseText);
                    alert('Error al crear la materia. Ver consola para más detalles.');
                }
            });
        }
    });

    window.editMateria = function (id) {
        $.get(`/materias/${id}`, function (data) {
            console.log(data);  // Muestra la respuesta en la consola para verificar
    
            // Verifica si 'data' contiene los campos esperados
            if (data && data.MateriaID) {
                $('#materiaId').val(data.MateriaID);
                $('#MateriaNombre').val(data.MateriaNombre);
                $('#formContainer').removeClass('d-none');
            } else {
                alert('Materia no encontrada.');
            }
        }).fail(function (xhr) {
            console.error('Error al cargar los datos de la materia:', xhr.responseText);
            alert('Error al cargar los datos de la materia.');
        });
    };
    

    window.deleteMateria = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar esta materia?')) {
            $.ajax({
                url: `/materias/${id}`,
                type: 'DELETE',
                success: function () {
                    loadMaterias();
                }
            });
        }
    };

    function resetForm() {
        $('#materiaId').val('');
        $('#MateriaNombre').val('');
        $('#formContainer').addClass('d-none'); 
    }

    $('#btnCancel').on('click', resetForm);
});
