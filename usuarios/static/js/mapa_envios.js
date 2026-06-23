let mapa;
let marcadorOrigen;
let marcadorDestino;
let lineaRuta;

function verEnvio(id) {

    fetch(`/envio/${id}/`)
    .then(response => response.json())
    .then(envio => {

        // 🔹 DATOS
        document.getElementById("envioId").innerText = envio.id_envio;
        document.getElementById("envioEstado").innerText = envio.estado_envio || "—";
        document.getElementById("envioTracking").innerText = envio.numero_seguimiento || "—";
        document.getElementById("envioDistancia").innerText = envio.distancia_km || 0;
        document.getElementById("envioPeso").innerText = envio.peso_total_kg || 0;

        document.getElementById("envioSalida").innerText = envio.fecha_salida || "—";
        document.getElementById("envioEntrega").innerText = envio.fecha_entrega || "—";

        document.getElementById("envioOrigen").innerText = envio.direccion_origen || "—";
        document.getElementById("envioDestino").innerText = envio.direccion_destino || "—";

        document.getElementById("envioTransportista").innerText = envio.transportista || "—";
        document.getElementById("envioVehiculo").innerText = envio.vehiculo || "—";

        document.getElementById("envioCostoBase").innerText = envio.costo_base || 0;
        document.getElementById("envioCostoPeso").innerText = envio.costo_peso || 0;
        document.getElementById("envioCostoTotal").innerText = envio.costo_total || 0;

        // 🔹 FOTOS
        const fotoCarga = document.getElementById('envioFotoCarga');
        const fotoDescarga = document.getElementById('envioFotoDescarga');
        const fotoCargaEmpty = document.getElementById('fotoCargaEmpty');
        const fotoDescargaEmpty = document.getElementById('fotoDescargaEmpty');

        if (envio.foto_carga_url) {
            fotoCarga.src = envio.foto_carga_url;
            fotoCarga.style.display = 'block';
            fotoCargaEmpty.style.display = 'none';
        } else {
            fotoCarga.style.display = 'none';
            fotoCargaEmpty.style.display = 'block';
        }

        if (envio.foto_descarga_url) {
            fotoDescarga.src = envio.foto_descarga_url;
            fotoDescarga.style.display = 'block';
            fotoDescargaEmpty.style.display = 'none';
        } else {
            fotoDescarga.style.display = 'none';
            fotoDescargaEmpty.style.display = 'block';
        }

        // 🔹 ABRIR MODAL
        let modal = new bootstrap.Modal(document.getElementById('modalEnvio'));
        modal.show();

        setTimeout(() => {

            if (!envio.latitud_origen || !envio.latitud_destino) return;

            // 🔥 SOLUCIÓN ERROR MAPA DUPLICADO
            if (mapa) {
                mapa.remove();
                mapa = null;
            }

            mapa = L.map('mapaEnvio').setView(
                [envio.latitud_origen, envio.longitud_origen], 13
            );

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap'
            }).addTo(mapa);

            marcadorOrigen = L.marker([envio.latitud_origen, envio.longitud_origen])
                .addTo(mapa)
                .bindPopup("Origen");

            marcadorDestino = L.marker([envio.latitud_destino, envio.longitud_destino])
                .addTo(mapa)
                .bindPopup("Destino");

            lineaRuta = L.polyline([
                [envio.latitud_origen, envio.longitud_origen],
                [envio.latitud_destino, envio.longitud_destino]
            ]).addTo(mapa);

            mapa.fitBounds(lineaRuta.getBounds());

        }, 300);

    })
    .catch(error => {
        console.error("Error cargando envío:", error);
    });
}