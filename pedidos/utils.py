
from .models import Compra
from decimal import Decimal

def obtener_compra_activa(usuario):
    compra, created = Compra.objects.get_or_create(
        id_cliente=usuario,
        estado='carrito',
        defaults={
            'subtotal': 0,
            'impuestos': 0,
            'valor_envio': 0,
            'total': 0
        }
    )
    return compra  

from usuarios.models import Cliente

def obtener_cliente_prueba():
    return Cliente.objects.first()