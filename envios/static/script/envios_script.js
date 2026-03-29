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