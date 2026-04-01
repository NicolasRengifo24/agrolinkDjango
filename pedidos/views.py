from django.shortcuts import render, redirect
from .models import Compra, DetallesCompra
from usuarios.models import Cliente, Usuario
from pedidos.utils import obtener_compra_activa

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from decimal import Decimal

# Create your views here.


def carrito(request):
    cliente_prueba = Cliente.objects.first()
    compra = obtener_compra_activa(cliente_prueba)
    detalles = DetallesCompra.objects.filter(id_compra=compra)

    subtotal = sum(d.subtotal for d in detalles)
    envio = compra.valor_envio or 0
    total = compra.total

    return render(request, 'components/contenido_principal_carrito.html', {
        'detalles': detalles,
        'compra': compra,
        'subtotal': subtotal,
        'envio': envio,
        'total': total
    })
    




@require_POST
def ajax_actualizar_detalle(request):
    producto_id = request.POST.get('producto_id')
    cantidad = int(request.POST.get('cantidad'))

    compra = obtener_compra_activa(request.user.cliente)

    detalle = DetallesCompra.objects.get(
        id_compra=compra,
        id_producto_id=producto_id
    )

    detalle.cantidad = cantidad
    detalle.subtotal = Decimal(cantidad) * detalle.precio_unitario
    detalle.save()

    # recalcular compra
    detalles = DetallesCompra.objects.filter(id_compra=compra)
    subtotal = sum(d.subtotal for d in detalles)

    compra.subtotal = subtotal
    compra.impuestos = subtotal * Decimal('0.19')
    compra.total = subtotal + compra.impuestos + (compra.valor_envio or 0)
    compra.save()

    return JsonResponse({
        'ok': True,
        'subtotal_item': float(detalle.subtotal),
        'total': float(compra.total)
    })

@require_POST
def ajax_eliminar_detalle(request):
    producto_id = request.POST.get('producto_id')

    compra = obtener_compra_activa(request.user.cliente)

    DetallesCompra.objects.filter(
        id_compra=compra,
        id_producto_id=producto_id
    ).delete()

    detalles = DetallesCompra.objects.filter(id_compra=compra)
    subtotal = sum(d.subtotal for d in detalles)

    compra.subtotal = subtotal
    compra.impuestos = subtotal * Decimal('0.19')
    compra.total = subtotal + compra.impuestos + (compra.valor_envio or 0)
    compra.save()

    return JsonResponse({
        'ok': True,
        'total': float(compra.total)
    })    