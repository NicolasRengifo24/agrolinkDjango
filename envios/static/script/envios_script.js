// script de la interfaz de envio

// Funcionalidad para aceptar viajes
document.querySelectorAll('.btn-aceptar').forEach(btn => {
    btn.addEventListener('click', function () {
        const card = this.closest('.card-viaje');
        card.querySelector('.badge-estado').className = 'badge bg-secondary badge-estado mb-2';
        card.querySelector('.badge-estado').textContent = 'Aceptado';
        this.disabled = true;
        this.innerHTML = '<i class="fas fa-check-circle me-2"></i>Viaje aceptado';

        // Aquí iría la lógica para enviar la aceptación al servidor
        console.log('Viaje aceptado:', card.querySelector('h5').textContent);
    });
});

const slider = document.querySelector('.peso-slider');
const valueDisplay = document.querySelector('.valor-peso');

if (slider) {
slider.addEventListener('input', function () {
    valueDisplay.textContent = this.value + ' kg';

    // Cambia el color del badge según el valor
    const value = parseInt(this.value);
    valueDisplay.classList.remove('bg-primary', 'bg-warning', 'bg-danger');

    if (value > 10000) {
        valueDisplay.classList.add('bg-danger');
    } else if (value > 5000) {
        valueDisplay.classList.add('bg-warning');
    } else {
        valueDisplay.classList.add('bg-primary');
    }
});
}

// Función para abrir el modal y cargar los datos del viaje
function abrirModalAceptarViaje(envioId, origen, destino, distancia, peso) {
    // Guardar el ID del envío
    document.getElementById('envio_id').value = envioId;

    // Mostrar información en el modal
    document.getElementById('modal-origen').textContent = origen || 'No especificado';
    document.getElementById('modal-destino').textContent = destino || 'No especificado';
    document.getElementById('modal-distancia').textContent = distancia ? `${distancia} km` : 'No calculada';
    document.getElementById('modal-peso').textContent = peso ? `${peso} kg` : 'No especificado';

    // Calcular costo estimado
    if (distancia && peso) {
        const costoKm = distancia * 3000;
        const costoPeso = peso * 200;
        const costoTotal = costoKm + costoPeso;
        document.getElementById('costo_total_estimado').textContent =
            `$${costoTotal.toLocaleString('es-CO')}`;
    }

    // Configurar fecha mínima de entrega (fecha recolección + 1 día)
    const fechaRecoleccion = document.getElementById('fecha_recoleccion');
    const fechaEntrega = document.getElementById('fecha_entrega_estimada');

    fechaRecoleccion.addEventListener('change', function () {
        const fechaRec = new Date(this.value);
        const fechaMinEntrega = new Date(fechaRec);
        fechaMinEntrega.setDate(fechaRec.getDate() + 1);

        const fechaMinStr = fechaMinEntrega.toISOString().split('T')[0];
        fechaEntrega.min = fechaMinStr;

        if (fechaEntrega.value && fechaEntrega.value < fechaMinStr) {
            fechaEntrega.value = fechaMinStr;
        }
    });

    // Abrir el modal
    const modal = new bootstrap.Modal(document.getElementById('aceptarViajeModal'));
    modal.show();
}

// Manejar el envío del formulario
document.getElementById('formAceptarViaje').addEventListener('submit', function (e) {
    e.preventDefault();

    const envioId = document.getElementById('envio_id').value;
    const vehiculoId = document.getElementById('vehiculo_id').value;
    const fechaRecoleccion = document.getElementById('fecha_recoleccion').value;
    const fechaEntrega = document.getElementById('fecha_entrega_estimada').value;

    // Validaciones
    if (!vehiculoId) {
        alert('Por favor selecciona un vehículo');
        return;
    }

    if (!fechaRecoleccion || !fechaEntrega) {
        alert('Por favor selecciona ambas fechas');
        return;
    }

    // Validar que la fecha de entrega sea posterior a la de recolección
    if (new Date(fechaEntrega) <= new Date(fechaRecoleccion)) {
        alert('La fecha de entrega debe ser posterior a la fecha de recolección');
        return;
    }

    // Enviar petición
    fetch(`/aceptar-viaje/${envioId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'vehiculo_id': vehiculoId,
            'fecha_recoleccion': fechaRecoleccion,
            'fecha_entrega_estimada': fechaEntrega
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload(); // Recargar para actualizar la lista
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al aceptar el viaje');
    });
}

// Función para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
