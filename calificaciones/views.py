from django.shortcuts import get_object_or_404, redirect, render
from .models import Calificacion
from productos.models import Producto
from django.db.models import Avg, Count

def guardar_calificacion(request):
    if request.method == 'POST':
        
        compra_id = request.POST.get('compra_id')
        
         # evitar doble calificación
        if Calificacion.objects.filter(id_compra_id=compra_id).exists():
            return redirect('mis_pedidos')

        Calificacion.objects.create(
            id_compra_id=request.POST.get('compra_id'),
            puntaje_producto=request.POST.get('producto'),
            puntaje_productor=request.POST.get('productor'),
            puntaje_transportista=request.POST.get('transportista'),
            comentario=request.POST.get('comentario')
        )

    return redirect('mis_pedidos')