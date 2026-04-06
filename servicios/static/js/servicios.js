//Buscador Funcionalidad para filtrar los servicios en la tabla de servicios.html
document.getElementById("searchInput").addEventListener("keyup", function() {

    let filtro = this.value.toLowerCase();
    let filas = document.querySelectorAll(".servicio-item");

filas.forEach(fila => {
    let texto = fila.innerText.toLowerCase();
    fila.style.display = texto.includes(filtro) ? "" : "none";
    });
});