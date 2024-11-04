$(document).ready(function () {
    loadEstudiantes();
    loadReportes();
    
    function loadEstudiantes() {
        $.get('/estudiantes', function (data) { 
            const estudianteSelect = $('#EstudianteId');
            estudianteSelect.empty(); 
            estudianteSelect.append(`<option value="">Selecciona un alumno</option>`);
            data.forEach(function (alumno) {
                estudianteSelect.append(`<option value="${alumno.AlumnoId}">${alumno.AlumnoId} — ${alumno.AlumnoNombre} ${alumno.AlumnoPrimerApellido} ${alumno.AlumnoSegundoApellido}</option>`);
            });
        }).fail(function (xhr) {
            console.error('Error al cargar los estudiantes:', xhr.responseText);
        });
    }

    function loadReportes() {
        $('#reportesSinResolverTableBody').empty();
        $('#reportesResueltosTableBody').empty();

        $.get('/reportes', function (data) {
            data.forEach(function (reporte) {
                const reporteRow = `
                    <tr>
                        <td>${reporte.ReporteID}</td>
                        <td>${reporte.AlumnoNombreCompleto}</td>
                        <td>${reporte.ReporteFecha}</td>
                        <td>${reporte.ReporteDescripcion}</td>
                        <td>${reporte.ReporteAccionTomada || 'Sin acción tomada'}</td>
                        <td>${reporte.ReporteFechaModificacion}</td>
                        <td>${reporte.PersonalAdministrativoId}</td>
                        <td>
                            <button class='btn btn-warning' onclick='editReporte(${reporte.ReporteID})'><i class="fa-solid fa-pen-to-square"></i></button>
                            <button class='btn btn-danger' onclick='deleteReporte(${reporte.ReporteID})'><i class="fa-solid fa-trash"></i></button>
                        </td>
                    </tr>`;

                if (reporte.ReporteStatus === "AN") {
                    $('#reportesSinResolverTableBody').append(reporteRow);
                    $('#reportesSinResolverTable').removeClass('d-none');
                } else if (reporte.ReporteStatus === "AC") {
                    $('#reportesResueltosTableBody').append(reporteRow);
                    $('#reportesResueltosTable').removeClass('d-none');
                }
            });
        }).fail(function (xhr) {
            console.error('Error al cargar los reportes:', xhr.responseText);
        });
    }

    $('#btnAddReporte').on('click', function () {
        resetForm(); 
        $('#formContainer').removeClass('d-none'); 
    });

    $('#reporteForm').on('submit', function (e) {
        e.preventDefault(); 
        
        const ReporteId = $('#ReporteId').val();
        const reporteData = {
            AlumnoID: $('#EstudianteId').val(),
            ReporteFecha: $('#ReporteFecha').val(),
            ReporteDescripcion: $('#ReporteDescripcion').val(),
            ReporteAccionTomada: $('#ReporteAccionTomada').val(),
            ReporteStatus: $('#ReporteStatus').val(),
            PersonalAdministrativoId: "0"
        };
    
        if (ReporteId) { // Si existe un ID, es una actualización
            $.ajax({
                url: `/reporte/${ReporteId}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(reporteData),
                success: function () {
                    loadReportes();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al actualizar el reporte.');
                    console.error('Error:', xhr.responseText);
                }
            });
        } else { // Si no existe un ID, es una creación
            $.ajax({
                url: '/reporte',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(reporteData),
                success: function () {
                    loadReportes();
                    resetForm();
                },
                error: function (xhr) {
                    alert('Error al crear el reporte.');
                    console.error('Error:', xhr.responseText);
                }
            });
        }
    });

    window.editReporte = function (id) {
        $.get(`/reportes/${id}`, function (data) {
            $('#ReporteId').val(data.ReporteID);
            $('#EstudianteId').val(data.AlumnoID);
            // Convertir la fecha al formato YYYY-MM-DD si es necesario
            const fechaReporte = new Date(data.ReporteFecha);
            const fechaFormateada = fechaReporte.toISOString().split('T')[0];
            $('#ReporteFecha').val(fechaFormateada);
            $('#ReporteDescripcion').val(data.ReporteDescripcion);
            $('#ReporteAccionTomada').val(data.ReporteAccionTomada); 
            $('#ReporteStatus').val(data.ReporteStatus);            
            $('#formContainer').removeClass('d-none'); 
        }).fail(function () {
            alert('Error al cargar los datos del reporte.');
        });
    };

    window.deleteReporte = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este reporte?')) {
            $.ajax({
                url: `/reportes/${id}`,
                type: 'DELETE',
                success: function () {
                    loadReportes(); 
                    alert('Reporte eliminado exitosamente.');
                },
                error: function (xhr) {
                    alert('Error al eliminar el reporte.');
                    console.error('Error:', xhr.responseText);
                }
            });
        }
    };

    function resetForm() {
        $('#ReporteId').val('');
        $('#EstudianteId').val('');
        $('#ReporteFecha').val('');
        $('#ReporteDescripcion').val('');
        $('#ReporteAccionTomada').val('');
        $('#ReporteStatus').val('');
        $('#formContainer').addClass('d-none'); 
    }

    $('#btnCancel').on('click', resetForm);
});
