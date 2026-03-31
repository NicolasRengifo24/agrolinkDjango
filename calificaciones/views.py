from django.shortcuts import get_object_or_404, redirect, render
from .models import Calificacion
from productos.models import Producto
from django.db.models import Avg, Count


# 📋 LISTA DE PRODUCTOS CON CALIFICACIONES
def lista_productos_calificados(request):
    productos = Producto.objects.annotate(
        promedio_estrellas=Avg('calificaciones__puntaje'),
        total_calificaciones=Count('calificaciones')
    )

    return render(request, 'calificaciones/lista.html', {
        'productos': productos
    })


# ➕ AGREGAR CALIFICACIÓN
def agregar_calificacion(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)

    if request.method == 'POST':
        puntaje = request.POST.get('puntaje')
        comentario = request.POST.get('comentario')

        Calificacion.objects.create(
            producto=producto,
            usuario=request.user,
            puntaje=puntaje,
            comentario=comentario
        )

        return redirect('lista_productos_calificados')

    return render(request, 'calificaciones/agregar.html', {
        'producto': producto
    })


# 🔍 DETALLE CON COMENTARIOS (OPCIONAL PERO RECOMENDADO)
def detalle_calificaciones(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)

    comentarios = producto.calificaciones.all().order_by('-fecha')[:3]

    promedio = producto.calificaciones.aggregate(
        promedio=Avg('puntaje')
    )['promedio']

    total = producto.calificaciones.count()

    return render(request, 'calificaciones/detalle.html', {
        'producto': producto,
        'comentarios': comentarios,
        'promedio': promedio,
        'total': total
    })