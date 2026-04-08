var data = document.getElementById("envios-data").textContent;
var envios = JSON.parse(data);

// Crear mapa centrado en Colombia
var map = L.map('map').setView([4.7110, -74.0721], 6);

// Cargar mapa (OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);

// Recorrer envíos
envios.forEach(function (envio) {

    // Marcador origen
    if (envio.origen) {
        L.marker(envio.origen)
            .addTo(map)
            .bindPopup("Origen: " + envio.numero);
    }

    // Marcador destino
    if (envio.destino) {
        L.marker(envio.destino)
            .addTo(map)
            .bindPopup("Destino: " + envio.numero);
    }

});

// logica del modal 

var mapModal;
var markerGroup;

// Obtener datos
var data = document.getElementById("envios-data").textContent;
var envios = JSON.parse(data);

function abrirMapa(idEnvio) {

    var envio = envios.find(e => e.id == idEnvio);

    if (!envio) {
        console.error("Envio no encontrado");
        return;
    }

    var origen = envio.origen;
    var destino = envio.destino;

    var modalElement = document.getElementById('mapModal');
    var modal = new bootstrap.Modal(modalElement);

    modalElement.addEventListener('shown.bs.modal', function () {

    if (mapModal) {
        mapModal.remove();
    }

    // 🔥 1. CREAS EL MAPA
    mapModal = L.map('mapModalContainer').setView([4.7, -74], 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(mapModal);

    markerGroup = L.layerGroup().addTo(mapModal);

    if (origen) {
        L.marker(origen).addTo(markerGroup).bindPopup("Origen");
    }

    if (destino) {
        L.marker(destino).addTo(markerGroup).bindPopup("Destino");
    }

    if (origen && destino) {
        var ruta = [origen, destino];
        L.polyline(ruta).addTo(mapModal);
        mapModal.fitBounds(ruta, {
            padding: [50, 50],   // margen bonito
            maxZoom: 12          // 🔥 límite de zoom (clave)
        });
    }

    
    setTimeout(() => {
        mapModal.invalidateSize();
    }, 200);

}, { once: true });

    modal.show();
}
// logica para calcular la distancia usando la formula harvesine para calcular distancia entre doas puntos en el globo terraqueo


function calcularDistancia(origen, destino) {

    var R = 6371; // radio de la tierra en km

    var lat1 = origen[0] * Math.PI / 180;
    var lat2 = destino[0] * Math.PI / 180;

    var dLat = (destino[0] - origen[0]) * Math.PI / 180;
    var dLon = (destino[1] - origen[1]) * Math.PI / 180;

    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1) * Math.cos(lat2) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);

    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    var distancia = R * c;

    return distancia.toFixed(2);
}

