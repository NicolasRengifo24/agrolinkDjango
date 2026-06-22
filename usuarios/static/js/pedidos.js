document.addEventListener("DOMContentLoaded", function(){

  const searchInput = document.getElementById('searchInput');

  if(searchInput){
    searchInput.addEventListener('input', function(e){
      const term = e.target.value.toLowerCase().trim();

      document.querySelectorAll('.pedido-item').forEach(row => {
        if(term === ''){
          row.style.display = '';
          return;
        }
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
      });
    });
  }

});
