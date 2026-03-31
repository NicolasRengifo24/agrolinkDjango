// Función para obtener el CSRF token de Django
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

function cambiarEstado(servicioId, boton) {
    fetch(`/servicios/cambiar_estado/${servicioId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Muy importante para Django
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({}) // No necesitamos enviar datos extra
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizamos la celda del estado del servicio
            const fila = boton.closest('tr');
            fila.querySelector('td:nth-child(4)').innerText = data.nuevo_estado;
        } else {
            alert('Error al cambiar el estado');
        }
    })
    .catch(error => console.error('Error:', error));
}
