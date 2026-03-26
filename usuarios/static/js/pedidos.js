// =============================
// BUSCADOR
// =============================
document.addEventListener("DOMContentLoaded", function(){

  const searchInput = document.getElementById('searchInput');

  if(searchInput){
    searchInput.addEventListener('input', function(e){
      const term = e.target.value.toLowerCase();

      document.querySelectorAll('.pedido-item').forEach(row => {
        row.style.display = row.textContent.toLowerCase().includes(term) ? '' : 'none';
      });
    });
  }

});


// =============================
// VER DETALLES
// =============================
function verDetallesPedido(id){

  document.getElementById('modalPedidoId').textContent = id;
  document.getElementById('modalClienteNombre').textContent = "Cliente Demo";
  document.getElementById('modalTotal').textContent = "$100.000";

  const modal = new bootstrap.Modal(document.getElementById('modalVerPedido'));
  modal.show();
}