from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from .models import Compra, DetallesCompra
from usuarios.models import Cliente, Usuario
from pedidos.utils import obtener_compra_activa


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from decimal import Decimal

# Create your views here.


def carrito(request):

    usuario = request.user.usuario
    cliente = usuario.cliente

    compra = Compra.objects.filter(
        id_cliente=cliente,
        estado="carrito"
    ).first()

    detalles = DetallesCompra.objects.filter(id_compra=compra)

    return render(request, 'components/contenido_principal_carrito.html', {
        'compra': compra,
        'detalles': detalles
    })
    

def actualizar_carrito(request, detalle_id):
    detalle = get_object_or_404(DetallesCompra, id_detalle=detalle_id)
    
    nueva_cantidad = int(request.POST.get('cantidad',1))
    
    if nueva_cantidad <=0:
        messages.error(request, "cantidad invalida")
        return redirect('carrito')
    
    detalle.cantidad = nueva_cantidad
    detalle.subtotal = detalle.cantidad * detalle.precio_unitario
    detalle.save()
    
    messages.success(request, "Stock actualizado")
    return redirect('carrito')

def eliminar_del_carrito(request, detalle_id):
    detalle = get_object_or_404(DetallesCompra, id_detalle=detalle_id)
    detalle.delete()
    
    messages.success(request, "Producto eliminado del carrito")
    
    return redirect('carrito')