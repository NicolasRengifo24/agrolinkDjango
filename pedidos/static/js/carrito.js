function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// 🔄 ACTUALIZAR CANTIDAD
document.addEventListener('change', function(e){
    if(e.target.classList.contains('cantidad-input')){

        let productoId = e.target.dataset.id;
        let cantidad = e.target.value;

        fetch(URL_ACTUALIZAR, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `producto_id=${productoId}&cantidad=${cantidad}`
        })
        .then(res => res.json())
        .then(data => {
            if(data.ok){
                document.getElementById(`subtotal-${productoId}`).innerText =
                    "$ " + data.subtotal_item;

                document.getElementById("total-general").innerText =
                    "$ " + data.total;
            }
        });
    }
});


// ❌ ELIMINAR PRODUCTO
document.addEventListener('click', function(e){
    if(e.target.closest('.eliminar-btn')){

        let btn = e.target.closest('.eliminar-btn');
        let productoId = btn.dataset.id;

        fetch(URL_ELIMINAR, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `producto_id=${productoId}`
        })
        .then(res => res.json())
        .then(data => {
            if(data.ok){
                btn.closest('.card').remove();

                document.getElementById("total-general").innerText =
                    "$ " + data.total;
            }
        });
    }
});