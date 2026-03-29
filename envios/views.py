from django.shortcuts import render
from .models import Envio
from productos.models import Producto,Finca
from usuarios.models import Usuario

# Create your views here.
def inicio(request):
    
    envios = Envio.objects.select_related(
        "id_compra__id_cliente",
        "id_vehiculo",
        "id_transportista"
    ).all()



    return render(request, 'envios/envios_dashboard.html',{
    'envios' : envios,

    })
    
    
    