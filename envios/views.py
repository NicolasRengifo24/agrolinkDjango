from django.shortcuts import render , redirect, get_object_or_404
from django.http import JsonResponse
from .models import Envio , Vehiculo
from productos.models import Producto,Finca
from usuarios.models import Usuario , Transportista
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

import json
from datetime import datetime
import random
import string

# Create your views here.
@login_required
def inicio_transportista(request):
    
    envios = Envio.objects.select_related(
        "id_compra__id_cliente",
        "id_vehiculo",
        "id_transportista"
    ).filter(id_transportista__isnull=True,estado_envio="pendiente").order_by('-id_envio')
    
    # Obtener vehículos activos del transportista actual
    vehiculos_activos = []
    if request.user.is_authenticated:
        try:
            usuario_obj = Usuario.objects.get(user=request.user)
            transportista_obj = Transportista.objects.get(id_usuario=usuario_obj)
            vehiculos_activos = Vehiculo.objects.filter(
                id_transportista=transportista_obj,
                estado='ACTIVO'
            )
        except (Usuario.DoesNotExist, Transportista.DoesNotExist):
            pass
    
    data_envios = []
    for envio in envios:
        # Inicializar variables
        lat_origen = None
        lng_origen = None
        direccion_origen = ""
        nombre_finca = ""
        
        # Obtener coordenadas de destino de la compra
        lat_destino = None
        lng_destino = None
        direccion_destino = envio.id_compra.direccion_entrega or ""
        
        if envio.id_compra.latitud_destino and envio.id_compra.longitud_destino:
            lat_destino = float(envio.id_compra.latitud_destino)
            lng_destino = float(envio.id_compra.longitud_destino)
        
        # Obtener coordenadas de origen (finca del productor)
        detalles = envio.id_compra.detallescompra_set.all()
        if detalles.exists():
            primer_detalle = detalles.first()
            producto = primer_detalle.id_producto
            
            print(f"DEBUG - Producto: {producto.nombre_producto}")
            
            # CORREGIDO: Obtener la finca a través de ProductoFinca
            # La relación es: Producto -> ProductoFinca (related_name='fincas') -> Finca (id_finca)
            producto_finca_rel = producto.fincas.first()  # Esto es ProductoFinca
            if producto_finca_rel:
                finca = producto_finca_rel.id_finca  # Esto es la Finca
                print(f"DEBUG - Finca encontrada: {finca}")
                if finca:
                    nombre_finca = finca.nombre_finca or ""
                    direccion_origen = finca.direccion_finca or nombre_finca
                    if finca.latitud and finca.longitud:
                        lat_origen = float(finca.latitud)
                        lng_origen = float(finca.longitud)
                        print(f"DEBUG - Coordenadas finca: {lat_origen}, {lng_origen}")
                    else:
                        print(f"DEBUG - Finca sin coordenadas")
                else:
                    print(f"DEBUG - No hay finca en ProductoFinca")
            else:
                print(f"DEBUG - No hay ProductoFinca para este producto")
        
        # Solo agregar a data_envios si tenemos coordenadas de origen y destino
        if lat_origen and lng_origen and lat_destino and lng_destino:
            data_envios.append({
                "id": envio.id_envio,
                "origen": [lat_origen, lng_origen],
                "destino": [lat_destino, lng_destino],
                "numero": envio.numero_seguimiento or f"ENV-{envio.id_envio}",
                "direccion_origen": direccion_origen,
                "direccion_destino": direccion_destino,
                "nombre_finca": nombre_finca,
                "peso": float(envio.peso_total_kg or 0),
                "distancia": float(envio.distancia_km or 0)
            })
        else:
            print(f"DEBUG - Envío {envio.id_envio} sin coordenadas: origen={lat_origen}, destino={lat_destino}")

    import json
    envios_json = json.dumps(data_envios)
    
    return render(request, 'envios/envios_dashboard.html', {
        'envios': envios,
        'envios_json': envios_json,
        'vehiculos_activos': vehiculos_activos,
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

    try:
        # Obtener usuario y transportista
        usuario_obj = Usuario.objects.get(user=request.user)
        transportista_obj = Transportista.objects.get(id_usuario=usuario_obj)

    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado")
        return redirect('inicio')

    except Transportista.DoesNotExist:
        messages.error(request, "No tienes perfil de transportista")
        return redirect('inicio')

    # 🔥 ESTA ES LA CLAVE
    envios = Envio.objects.select_related(
        'id_compra__id_cliente__id_usuario',
        'id_vehiculo'
    ).filter(
        id_transportista=transportista_obj
    ).order_by('-id_envio')

    print("🚚 Envios encontrados:", envios.count())  # DEBUG

    return render(request, 'envios/mis_envios_dashboard.html', {
        'envios': envios
    })
    
    
@login_required
def aceptar_viaje(request, envio_id):
    """Acepta un viaje y asigna vehículo, fechas y número de seguimiento"""
    
    if request.method == 'POST':
        try:
            # Obtener el transportista actual
            usuario_obj = Usuario.objects.get(user=request.user)
            transportista_obj = Transportista.objects.get(id_usuario=usuario_obj)
            
            # Obtener el envío
            envio = get_object_or_404(Envio, id_envio=envio_id)
            
            # Verificar que el envío esté disponible (no asignado)
            if envio.id_transportista:
                return JsonResponse({
                    'success': False,
                    'message': 'Este envío ya fue asignado a otro transportista'
                }, status=400)
            
            # Obtener datos del formulario
            vehiculo_id = request.POST.get('vehiculo_id')
            fecha_recoleccion = request.POST.get('fecha_recoleccion')
            fecha_entrega_estimada = request.POST.get('fecha_entrega_estimada')
            
            # Validar que se seleccionó un vehículo
            if not vehiculo_id:
                return JsonResponse({
                    'success': False,
                    'message': 'Debes seleccionar un vehículo'
                }, status=400)
            
            # Obtener el vehículo y verificar que pertenece al transportista
            vehiculo = get_object_or_404(
                Vehiculo, 
                id_vehiculo=vehiculo_id, 
                id_transportista=transportista_obj
            )
            
            # Validar que el vehículo no esté suspendido
            if vehiculo.estado != 'ACTIVO':
                return JsonResponse({
                    'success': False,
                    'message': f'El vehículo {vehiculo.placa_vehiculo} está suspendido. No puede ser asignado.'
                }, status=400)
            
            # Validar fechas
            if not fecha_recoleccion or not fecha_entrega_estimada:
                return JsonResponse({
                    'success': False,
                    'message': 'Debes seleccionar ambas fechas'
                }, status=400)
            
            # Generar número de seguimiento único
            numero_seguimiento = generar_numero_seguimiento()
            
            # Calcular costo total
            distancia_km = envio.distancia_km or 0
            peso_total_kg = envio.peso_total_kg or 0
            
            # Tarifas
            tarifa_por_km = 3000  # $3,000 por km
            tarifa_por_kg = 200   # $200 por kg
            
            costo_distancia = distancia_km * tarifa_por_km
            costo_peso = peso_total_kg * tarifa_por_kg
            costo_total = costo_distancia + costo_peso
            
            # Actualizar el envío
            envio.id_transportista = transportista_obj
            envio.id_vehiculo = vehiculo
            envio.estado_envio = 'Asignado'
            envio.fecha_salida = fecha_recoleccion
            envio.fecha_entrega = fecha_entrega_estimada
            envio.numero_seguimiento = numero_seguimiento
            envio.tarifa_por_km = tarifa_por_km
            envio.tarifa_por_kg = tarifa_por_kg
            envio.costo_total = costo_total
            envio.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Viaje aceptado exitosamente. Número de seguimiento: {numero_seguimiento}',
                'numero_seguimiento': numero_seguimiento,
                'costo_total': f'{costo_total:,.0f}'
            })
            
        except Vehiculo.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Vehículo no encontrado o no te pertenece'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al aceptar el viaje: {str(e)}'
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

def generar_numero_seguimiento():
    """Genera un número de seguimiento único"""
    while True:
        # Formato: AGRO-YYYYMMDD-XXXXX
        fecha_actual = datetime.now().strftime('%Y%m%d')
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        numero = f"AGRO-{fecha_actual}-{random_chars}"
        
        # Verificar que no exista
        if not Envio.objects.filter(numero_seguimiento=numero).exists():
            return numero
        
        
@login_required
def cambiar_estado_envio(request, envio_id, nuevo_estado):

    try:
        usuario_obj = Usuario.objects.get(user=request.user)
        transportista_obj = Transportista.objects.get(id_usuario=usuario_obj)

        envio = get_object_or_404(Envio, id_envio=envio_id)

        # 🔐 Seguridad: solo su propio envío
        if envio.id_transportista != transportista_obj:
            messages.error(request, "No tienes permiso para este envío")
            return redirect('mis_envios')

        # 🔄 Validar transición lógica
        if envio.estado_envio == "Asignado" and nuevo_estado == "En_Transito":
            envio.estado_envio = "En_Transito"

        elif envio.estado_envio == "En_Transito" and nuevo_estado == "Entregado":
            envio.estado_envio = "Entregado"

        else:
            messages.warning(request, "Cambio de estado no permitido")
            return redirect('mis_envios')

        envio.save()

        messages.success(request, f"Estado actualizado a {envio.estado_envio}")

    except Exception as e:
        messages.error(request, f"Error: {str(e)}")

    return redirect('mis_envios')



######### Esto es para el Api #######
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import UbicacionService

@api_view(['GET'])
def ciudades_cundinamarca_api(request):
    ciudades = UbicacionService.obtener_ciudades_cundinamarca()
    return Response({
        "success": True,
        "data": ciudades
    })