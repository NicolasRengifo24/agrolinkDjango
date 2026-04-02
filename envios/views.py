from django.shortcuts import render
from .models import Envio , Vehiculo
from productos.models import Producto,Finca
from usuarios.models import Usuario

import json

# Create your views here.
def inicio_transportista(request):
    
    envios = Envio.objects.select_related(
        "id_compra__id_cliente",
        "id_vehiculo",
        "id_transportista"
    ).all()
    
    data_envios = []

    for envio in envios:
        if envio.latitud_origen and envio.longitud_origen:
            data_envios.append({
                "id" : envio.id_envio,
                "origen": [envio.latitud_origen, envio.longitud_origen],
                "destino": [envio.latitud_destino, envio.longitud_destino],
                "numero": envio.numero_seguimiento
            })



    return render(request, 'envios/envios_dashboard.html',{
    'envios' : envios,
    'envios_json' : json.dumps(data_envios),

    })
    

def mostrar_vehiculos(request) :
        
    vehiculos = Vehiculo.objects.all()
    
    return render(request, 'vehiculos/vehiculos_dashboard.html',{
        'vehiculos' : vehiculos,
    })
    
    