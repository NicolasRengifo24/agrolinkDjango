/* Dashboard Transportista - Chart.js initialization */

document.addEventListener('DOMContentLoaded', function () {
    // ── Earnings Line Chart ──
    var earningsCanvas = document.getElementById('chartEarnings');
    if (earningsCanvas) {
        var earningsData = earningsCanvas.dataset.ganancias || '[]';
        try {
            var meses = JSON.parse(earningsData);
        } catch (e) {
            console.warn('Error parsing earnings data', e);
            meses = [];
        }

        if (meses.length > 0) {
            new Chart(earningsCanvas, {
                type: 'line',
                data: {
                    labels: meses.map(function(m) { return m.mes; }),
                    datasets: [{
                        label: 'Ganancias ($)',
                        data: meses.map(function(m) { return m.total; }),
                        borderColor: '#2f6b31',
                        backgroundColor: 'rgba(47, 107, 49, 0.08)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: '#2f6b31',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                    }]
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
                            padding: 12,
                            cornerRadius: 8,
                            callbacks: {
                                label: function(ctx) {
                                    return '$' + ctx.parsed.y.toLocaleString('es-CO');
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(0,0,0,0.05)' },
                            ticks: {
                                callback: function(val) { return '$' + val.toLocaleString('es-CO'); }
                            }
                        },
                        x: {
                            grid: { display: false }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    }
                }
            });
        } else {
            earningsCanvas.parentElement.innerHTML =
                '<div class="chart-empty"><i class="bi bi-graph-up"></i><p class="mb-0">Aún no hay datos de ganancias</p></div>';
        }
    }

    // ── Trips by Status Donut Chart ──
    var donutCanvas = document.getElementById('chartStatus');
    if (donutCanvas) {
        var statusData = donutCanvas.dataset.status || '[]';
        try {
            var estados = JSON.parse(statusData);
        } catch (e) {
            console.warn('Error parsing status data', e);
            estados = [];
        }

        var colorMap = {
            'Entregado': '#2ecc71',
            'En_Transito': '#3498db',
            'Asignado': '#f39c12',
            'Pendiente': '#95a5a6',
            'Cancelado': '#e74c3c'
        };
        var labelMap = {
            'Entregado': 'Entregados',
            'En_Transito': 'En tránsito',
            'Asignado': 'Asignados',
            'Pendiente': 'Pendientes',
            'Cancelado': 'Cancelados'
        };

        if (estados.length > 0) {
            new Chart(donutCanvas, {
                type: 'doughnut',
                data: {
                    labels: estados.map(function(e) {
                        return labelMap[e.estado] || e.estado;
                    }),
                    datasets: [{
                        data: estados.map(function(e) { return e.count; }),
                        backgroundColor: estados.map(function(e) {
                            return colorMap[e.estado] || '#95a5a6';
                        }),
                        borderWidth: 2,
                        borderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '65%',
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 14,
                                usePointStyle: true,
                                font: { size: 12 }
                            }
                        },
                        tooltip: {
                            backgroundColor: '#1a3f2c',
                            titleColor: '#e9f5db',
                            bodyColor: '#fff',
                            padding: 12,
                            cornerRadius: 8,
                            callbacks: {
                                label: function(ctx) {
                                    var total = ctx.dataset.data.reduce(function(a, b) { return a + b; }, 0);
                                    var pct = ((ctx.parsed / total) * 100).toFixed(1);
                                    return ctx.label + ': ' + ctx.parsed + ' (' + pct + '%)';
                                }
                            }
                        }
                    }
                }
            });
        } else {
            donutCanvas.parentElement.innerHTML =
                '<div class="chart-empty"><i class="bi bi-pie-chart"></i><p class="mb-0">Aún no hay envíos</p></div>';
        }
    }
});
