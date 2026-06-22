/* Panel de Control - Charts & interactividad */

document.addEventListener('DOMContentLoaded', function () {
    var csrfToken = getCookie('csrftoken');

    // ── Subir foto (AJAX, reutiliza patrón de mis_envios) ──
    document.querySelectorAll('.btn-subir-foto-panel').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var envioId = this.dataset.envioId;
            var tipo = this.dataset.tipo;
            var fileInput = document.getElementById('foto-input-' + envioId);

            if (!fileInput || !fileInput.files.length) {
                alert('Selecciona una foto primero');
                return;
            }

            var formData = new FormData();
            formData.append('tipo', tipo);
            formData.append('foto', fileInput.files[0]);

            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';

            fetch('/subir-foto-envio/' + envioId + '/', {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken },
                body: formData,
            })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error: ' + data.message);
                    btn.disabled = false;
                    btn.innerHTML = '<i class="bi bi-upload"></i>';
                }
            })
            .catch(function () {
                alert('Error de conexión');
                btn.disabled = false;
                btn.innerHTML = '<i class="bi bi-upload"></i>';
            });
        });
    });

    // ── Chart: Envíos por vehículo (barras agrupadas) ──
    var canvasVehiculo = document.getElementById('chartVehiculos');
    if (canvasVehiculo) {
        var dataVehiculo = canvasVehiculo.dataset.vehiculos;
        try {
            var dv = JSON.parse(dataVehiculo);
        } catch (e) { dv = null; }

        if (dv && dv.labels && dv.labels.length > 0) {
            new Chart(canvasVehiculo, {
                type: 'bar',
                data: {
                    labels: dv.labels,
                    datasets: [
                        {
                            label: 'Total Viajes',
                            data: dv.total,
                            backgroundColor: 'rgba(47, 107, 49, 0.7)',
                            borderColor: '#2f6b31',
                            borderWidth: 1,
                            borderRadius: 4,
                        },
                        {
                            label: 'Entregados',
                            data: dv.entregados,
                            backgroundColor: 'rgba(46, 204, 113, 0.7)',
                            borderColor: '#2ecc71',
                            borderWidth: 1,
                            borderRadius: 4,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: { usePointStyle: true, font: { size: 11 } },
                        },
                        tooltip: {
                            backgroundColor: '#1a3f2c',
                            titleColor: '#e9f5db',
                            bodyColor: '#fff',
                        },
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { stepSize: 1 },
                            grid: { color: 'rgba(0,0,0,0.05)' },
                        },
                        x: { grid: { display: false } },
                    },
                },
            });
        } else {
            canvasVehiculo.parentElement.innerHTML =
                '<div class="empty-fotos"><i class="bi bi-bar-chart"></i><p>Sin datos de vehículos</p></div>';
        }
    }

    // ── Chart: Ingresos por vehículo (barras) ──
    var canvasIngresos = document.getElementById('chartIngresos');
    if (canvasIngresos) {
        var dataIngresos = canvasIngresos.dataset.ingresos;
        try {
            var di = JSON.parse(dataIngresos);
        } catch (e) { di = null; }

        if (di && di.labels && di.labels.length > 0) {
            new Chart(canvasIngresos, {
                type: 'bar',
                data: {
                    labels: di.labels,
                    datasets: [{
                        label: 'Ingresos ($)',
                        data: di.ingresos,
                        backgroundColor: [
                            'rgba(47, 107, 49, 0.7)',
                            'rgba(52, 152, 219, 0.7)',
                            'rgba(243, 156, 18, 0.7)',
                            'rgba(155, 89, 182, 0.7)',
                            'rgba(46, 204, 113, 0.7)',
                            'rgba(231, 76, 60, 0.7)',
                        ],
                        borderColor: [
                            '#2f6b31', '#3498db', '#f39c12',
                            '#9b59b6', '#2ecc71', '#e74c3c',
                        ],
                        borderWidth: 1,
                        borderRadius: 4,
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: '#1a3f2c',
                            titleColor: '#e9f5db',
                            bodyColor: '#fff',
                            callbacks: {
                                label: function (ctx) {
                                    return '$' + ctx.parsed.y.toLocaleString('es-CO');
                                },
                            },
                        },
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(0,0,0,0.05)' },
                            ticks: {
                                callback: function (val) {
                                    return '$' + val.toLocaleString('es-CO');
                                },
                            },
                        },
                        x: { grid: { display: false } },
                    },
                },
            });
        } else {
            canvasIngresos.parentElement.innerHTML =
                '<div class="empty-fotos"><i class="bi bi-cash-stack"></i><p>Sin datos de ingresos</p></div>';
        }
    }
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
