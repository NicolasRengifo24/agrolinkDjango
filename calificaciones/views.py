from django.shortcuts import get_object_or_404, redirect, render
from .models import Calificacion
from productos.models import Producto
from django.db.models import Avg


def lista_productos_calificados(request):
    productos = Producto.objects.all().annotate(
        promedio=Avg('calificaciones__puntaje')  # 👈 ESTE ES EL CORRECTO
    )

    return render(request, 'calificaciones/lista.html', {
        'productos': productos
    })


def agregar_calificacion(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        puntaje = request.POST['puntaje']
        comentario = request.POST['comentario']

        Calificacion.objects.create(
            producto=producto,
            usuario=request.user,
            puntaje=puntaje,
            comentario=comentario
        )

        return redirect('lista_productos_calificados')

    return render(request, 'calificaciones/agregar.html', {'producto': producto})