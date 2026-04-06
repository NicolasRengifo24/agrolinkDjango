// BUSCADOR
document.getElementById("searchInput")?.addEventListener("input", function(e){
    const texto = e.target.value.toLowerCase();
    const filas = document.querySelectorAll(".servicio-item");

    filas.forEach(fila => {
        fila.style.display = fila.textContent.toLowerCase().includes(texto) ? "" : "none";
    });
});


// CAMBIAR ESTADO
function cambiarEstado(id){
    if(confirm("¿Cambiar estado del servicio?")){
        console.log("Cambiar estado:", id);
    }
}


// ELIMINAR
function confirmarEliminarServicio(id){
    if(confirm("¿Eliminar servicio?")){
        console.log("Eliminar:", id);
    }
}