let mapa;
let marcador;

function verEnvio(id){

  // abrir modal
  const modal = new bootstrap.Modal(document.getElementById('modalEnvio'));
  modal.show();

  // Cargar datos reales del envío
  fetch('/envio/' + id + '/')
    .then(r => r.json())
    .then(data => {
      document.getElementById('envioId').textContent = data.id_envio;
      document.getElementById('envioEstado').textContent = data.estado_envio;
      document.getElementById('envioTracking').textContent = data.numero_seguimiento || 'Sin código';
      document.getElementById('envioDistancia').textContent = data.distancia_km;
      document.getElementById('envioPeso').textContent = data.peso_total_kg;
      document.getElementById('envioSalida').textContent = data.fecha_salida || '—';
      document.getElementById('envioEntrega').textContent = data.fecha_entrega || '—';
      document.getElementById('envioTransportista').textContent = data.transportista || 'No asignado';
      document.getElementById('envioVehiculo').textContent = data.vehiculo || 'No asignado';
      document.getElementById('envioOrigen').textContent = data.direccion_origen || '—';
      document.getElementById('envioDestino').textContent = data.direccion_destino || '—';

      // Formatear costos COP
      var formatCOP = function(n) {
        return '$' + Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
      };
      document.getElementById('envioCostoBase').textContent = formatCOP(data.costo_base);
      document.getElementById('envioCostoPeso').textContent = formatCOP(data.costo_peso);
      document.getElementById('envioCostoTotal').textContent = formatCOP(data.costo_total);
    })
    .catch(() => {
      document.getElementById('envioEstado').textContent = 'Error al cargar';
    });

  setTimeout(() => {
    let lat = 4.6097;
    let lng = -74.0817;
    mapa = L.map('mapaEnvio').setView([lat, lng], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap'
    }).addTo(mapa);
    marcador = L.marker([lat, lng]).addTo(mapa)
      .bindPopup("Repartidor en camino 🚚")
      .openPopup();
    simularMovimiento();
  }, 300);
}

// ── FILTROS ──
document.addEventListener("DOMContentLoaded", function(){

  function filtrarEnvios(){
    var term = (document.getElementById('searchEnvio').value || '').toLowerCase().trim();
    var estado = document.getElementById('estadoFilter').value;
    var fecha = document.getElementById('fechaFilter').value;

    document.querySelectorAll('.pedido-item').forEach(function(row){
      var mostrar = true;

      if(term !== '' && !row.textContent.toLowerCase().includes(term)){
        mostrar = false;
      }

      if(mostrar && estado !== ''){
        var celdaEstado = row.querySelector('td:nth-child(5) .badge-envio');
        if(!celdaEstado || celdaEstado.textContent.trim() !== estado){
          mostrar = false;
        }
      }

      if(mostrar && fecha !== ''){
        // no hay columna de fecha visible, se salta
      }

      row.style.display = mostrar ? '' : 'none';
    });
  }

  document.getElementById('searchEnvio').addEventListener('input', filtrarEnvios);
  document.getElementById('estadoFilter').addEventListener('change', filtrarEnvios);
  document.getElementById('btnFiltrar').addEventListener('click', filtrarEnvios);

});