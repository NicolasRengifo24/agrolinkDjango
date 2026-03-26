let mapa;
let marcador;

function verEnvio(id){

  // abrir modal
  const modal = new bootstrap.Modal(document.getElementById('modalEnvio'));
  modal.show();

  setTimeout(() => {

    // coordenadas ejemplo (Bogotá)
    let lat = 4.6097;
    let lng = -74.0817;

    // crear mapa
    mapa = L.map('mapaEnvio').setView([lat, lng], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap'
    }).addTo(mapa);

    // marcador repartidor
    marcador = L.marker([lat, lng]).addTo(mapa)
      .bindPopup("Repartidor en camino 🚚")
      .openPopup();

    // SIMULACIÓN MOVIMIENTO (tipo Uber)
    simularMovimiento();

  }, 300);
}