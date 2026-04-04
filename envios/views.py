from django.shortcuts import render , redirect, get_object_or_404
from django.http import JsonResponse
from .models import Envio , Vehiculo
from productos.models import Producto,Finca
from usuarios.models import Usuario , Transportista
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

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
    

@login_required
def mostrar_vehiculos(request):
    try:
        usuario_obj = Usuario.objects.get(user=request.user)
        transportista_obj = Transportista.objects.get(id_usuario=usuario_obj)
        vehiculos = Vehiculo.objects.filter(id_transportista=transportista_obj)
    except (Usuario.DoesNotExist, Transportista.DoesNotExist):
        vehiculos = Vehiculo.objects.none()
        messages.warning(request, "No tienes perfil de transportista")
    
    return render(request, 'vehiculos/vehiculos_dashboard.html', {
        'vehiculos': vehiculos,
    })
    
    
@login_required
def agregar_vehiculo(request):
    if request.method == 'POST':
        # Obtener el transportista actual
        try:
            usuario_obj = Usuario.objects.get(user=request.user)
            transportista_obj = Transportista.objects.get(id_usuario=usuario_obj)
        except (Usuario.DoesNotExist, Transportista.DoesNotExist):
            messages.error(request, "No tienes permisos de transportista")
            return redirect('mostrar_vehiculos')
        
        # Obtener datos del formulario
        tipo_vehiculo = request.POST.get('tipo_vehiculo')
        placa_vehiculo = request.POST.get('placa_vehiculo')
        capacidad_carga = request.POST.get('capacidad_carga')
        
        # Validar datos
        if not tipo_vehiculo or not placa_vehiculo:
            messages.error(request, "Por favor completa los campos obligatorios")
            return redirect('mostrar_vehiculos')
        
        # Crear el vehículo
        try:
            vehiculo = Vehiculo.objects.create(
                id_transportista=transportista_obj,
                tipo_vehiculo=tipo_vehiculo,
                placa_vehiculo=placa_vehiculo.upper(),  # Convertir a mayúsculas
                capacidad_carga=capacidad_carga if capacidad_carga else 0
            )
            messages.success(request, f"Vehículo {placa_vehiculo} registrado exitosamente")
        except Exception as e:
            messages.error(request, f"Error al registrar vehículo: {str(e)}")
        
        return redirect('mostrar_vehiculos')
    
    return redirect('mostrar_vehiculos')
    
    

@login_required
def cambiar_estado_vehiculo(request, vehiculo_id):
    """Cambia el estado del vehículo (AJAX)"""
    
    if request.method == 'POST':
        try:
            usuario_obj = Usuario.objects.get(user=request.user)
            transportista_obj = Transportista.objects.get(id_usuario=usuario_obj)
            
            vehiculo = get_object_or_404(
                Vehiculo, 
                id_vehiculo=vehiculo_id, 
                id_transportista=transportista_obj
            )
            
            # Cambiar estado
            if vehiculo.estado == 'ACTIVO':
                vehiculo.estado = 'SUSPENDIDO'
                mensaje = f"Vehículo {vehiculo.placa_vehiculo} suspendido"
            else:
                vehiculo.estado = 'ACTIVO'
                mensaje = f"Vehículo {vehiculo.placa_vehiculo} activado"
            
            vehiculo.save()
            
            return redirect('mostrar_vehiculos')
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
def eliminar_vehiculo(request, vehiculo_id):
    """Elimina un vehículo"""
    
    if request.method == 'POST':
        try:
            # Verificar el usuario
            usuario_obj = Usuario.objects.get(user=request.user)
            transportista_obj = Transportista.objects.get(id_usuario=usuario_obj)
            
            # Buscar el vehículo y verificar que pertenece al transportista
            vehiculo = get_object_or_404(
                Vehiculo, 
                id_vehiculo=vehiculo_id, 
                id_transportista=transportista_obj
            )
            
            placa = vehiculo.placa_vehiculo
            vehiculo.delete()
            
            messages.success(request, f"Vehículo {placa} eliminado correctamente")
            
        except Usuario.DoesNotExist:
            messages.error(request, "Perfil de usuario no encontrado")
        except Transportista.DoesNotExist:
            messages.error(request, "No tienes permisos de transportista")
        except Exception as e:
            messages.error(request, f"Error al eliminar: {str(e)}")
    
    return redirect('mostrar_vehiculos')


@login_required
def mis_envios(request):
    """Vista para mostrar los envíos del transportista"""
    # Tu lógica aquí
    return render(request, 'envios/mis_envios.html')