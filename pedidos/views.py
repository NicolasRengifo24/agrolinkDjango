from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings          
from .models import Compra, DetallesCompra
from calificaciones.models import Calificacion
from usuarios.models import Cliente, Usuario
from envios.models import Envio
from decimal import Decimal
import time
import requests

# Create your views here.



@login_required
def carrito(request):

    usuario = request.user.usuario

    #  VALIDAR QUE SEA CLIENTE
    if usuario.rol.upper() != "CLIENTE":
        messages.error(request, "Solo los clientes pueden acceder al carrito")
        return redirect('mostrar_productos')

    #  Obtener cliente de forma segura
    try:
        cliente = usuario.cliente
    except:
        messages.error(request, "Este usuario no tiene perfil de cliente")
        return redirect('inicio')

    # 1 Buscar compra activa (carrito)
    compra = Compra.objects.filter(
        id_cliente=cliente,
        estado="carrito"
    ).first()

    # 2️ Detalles
    detalles = DetallesCompra.objects.filter(id_compra=compra) if compra else []
    
    # contador del carrito 
    cart_count = sum(det.cantidad for det in detalles)

    # 3️ Referencia única para ePayco
    referencia_unica = None
    if compra:
        referencia_unica = f"compra_{compra.id_compra}_{int(time.time())}"

    return render(request, 'components/contenido_principal_carrito.html', {
    'compra': compra,
    'detalles': detalles,
    'total': compra.total if compra else 0,
    'subtotal': compra.subtotal if compra else 0,
    'ref_pago': referencia_unica,
    'epayco_key': settings.EPAYCO_PUBLIC_KEY,
    'total_epayco': f"{compra.total:.2f}" if compra else '0.00',

    
    'url_respuesta': f"{settings.NGROK_URL}/respuesta-pago/",
    'url_confirmacion': f"{settings.NGROK_URL}/confirmacion-pago/",
    'cart_count': cart_count,
})
    

def actualizar_carrito(request, detalle_id):
    detalle = get_object_or_404(DetallesCompra, id_detalle=detalle_id)
    
    nueva_cantidad = int(request.POST.get('cantidad', 1))
    
    if nueva_cantidad <= 0:
        messages.error(request, "Cantidad inválida")
        return redirect('carrito')
    
    # ✅ ACTUALIZAR CANTIDAD
    detalle.cantidad = nueva_cantidad
    
    # ✅ ACTUALIZAR SUBTOTAL (MUY IMPORTANTE)
    detalle.subtotal = nueva_cantidad * detalle.id_producto.precio
    
    detalle.save()

    # 🔥 RECALCULAR COMPRA COMPLETA
    detalles = DetallesCompra.objects.filter(id_compra=detalle.id_compra)

    subtotal = sum(d.subtotal for d in detalles)
    impuestos = subtotal * Decimal('0.19')
    total = subtotal + impuestos

    compra = detalle.id_compra
    compra.subtotal = subtotal
    compra.impuestos = impuestos
    compra.total = total
    compra.save()

    messages.success(request, "Cantidad actualizada correctamente")
    return redirect('carrito')


def eliminar_del_carrito(request, detalle_id):
    detalle = get_object_or_404(DetallesCompra, id_detalle=detalle_id)
    detalle.delete()
    detalles = DetallesCompra.objects.filter(id_compra=detalle.id_compra)

    subtotal = sum(d.subtotal for d in detalles)
    impuestos = subtotal * Decimal('0.19')
    total = subtotal + impuestos

    compra = detalle.id_compra
    compra.subtotal = subtotal
    compra.impuestos = impuestos
    compra.total = total
    compra.save()    
    
    messages.success(request, "Producto eliminado del carrito")
    
    return redirect('carrito')


# el corazon del funcionamiento de epayco ----NoTOCAR----
def respuesta_pago(request):
    return render(request, "components/epayco_respuesta.html", {
        "data": request.GET
    })
    
    

@csrf_exempt
def confirmacion_pago(request):
    print("====================================")
    print("🔥 WEBHOOK EPAYCO LLAMADO")
    print("Método:", request.method)

    if request.method == "POST":
        data = request.POST
        print("📦 DATA RECIBIDA:", data)

        ref = data.get("x_ref_payco")
        estado = data.get("x_cod_transaction_state")
        factura = data.get("x_id_invoice")

        try:
            compra_id = int(factura.split("_")[1])
            compra = Compra.objects.get(id_compra=compra_id)
            print("✅ Compra encontrada:", compra.id_compra)
        except Exception as e:
            print("❌ ERROR buscando compra:", str(e))
            return JsonResponse({"status": "error compra no encontrada"})

        if estado == "1":  # ✅ PAGO APROBADO
            print("💰 PAGO APROBADO")

            # 🔥 EVITAR DUPLICADOS (webhook puede llamarse varias veces)
            if Envio.objects.filter(id_compra=compra).exists():
                print("⚠️ Envío ya existe para esta compra")
                return JsonResponse({"status": "ok"})

            compra.estado = "pagado"
            compra.metodo_pago = "epayco"
            compra.save()
            
            # ========================================
    # 🔥 RESTAR STOCK DE PRODUCTOS
    # ========================================
    detalles = compra.detallescompra_set.all()
    for detalle in detalles:
        producto = detalle.id_producto
        if producto.stock is not None:
            if producto.stock >= detalle.cantidad:
                producto.stock -= detalle.cantidad
                producto.save()
                print(f"📉 Stock actualizado: {producto.nombre_producto} → {producto.stock}")
            else:
                print(f"⚠️ Stock insuficiente para {producto.nombre_producto}")

            # ========================================
            # 🔥 CREAR ENVÍO
            # ========================================

            detalles = compra.detallescompra_set.all()

            if not detalles.exists():
                print("❌ No hay detalles en la compra")
                return JsonResponse({"status": "error", "message": "No hay productos en la compra"})

            primer_detalle = detalles.first()
            producto = primer_detalle.id_producto

            # 📍 ORIGEN (finca)
            lat_origen = None
            lng_origen = None
            direccion_origen = ""
            nombre_finca = ""

            from productos.models import ProductoFinca
            producto_finca = ProductoFinca.objects.filter(id_producto=producto).first()

            if producto_finca and producto_finca.id_finca:
                finca = producto_finca.id_finca
                lat_origen = finca.latitud
                lng_origen = finca.longitud
                direccion_origen = finca.direccion_finca or finca.nombre_finca
                nombre_finca = finca.nombre_finca
                print(f"📍 Origen: {nombre_finca} - Lat: {lat_origen}, Lng: {lng_origen}")
            else:
                print("❌ No se encontró finca para el producto")

            # 📍 DESTINO (desde compra)
            lat_destino = compra.latitud_destino
            lng_destino = compra.longitud_destino
            direccion_destino = compra.direccion_entrega

            # 📏 DISTANCIA (desde detalles)
            distancia_km = float(primer_detalle.distancia_km or 0)
            print(f"📏 Distancia desde detalles: {distancia_km} km")

            # 📦 PESO TOTAL
            peso_total_kg = 0
            for detalle in detalles:
                peso_producto = float(detalle.id_producto.peso_kg or 0)
                peso_total_kg += float(detalle.cantidad) * peso_producto

            print(f"📦 Peso total: {peso_total_kg} kg")

            # 💰 COSTOS
            tarifa_por_km = 3000
            tarifa_por_kg = 200

            costo_distancia = float(distancia_km) * tarifa_por_km
            costo_peso = peso_total_kg * tarifa_por_kg
            costo_total = costo_distancia + costo_peso

            print(f"💰 Costos - Distancia: ${costo_distancia:,.0f}, Peso: ${costo_peso:,.0f}, Total: ${costo_total:,.0f}")

            # 🔢 NÚMERO DE SEGUIMIENTO
            import random
            import string
            from datetime import datetime

            fecha_actual = datetime.now().strftime('%Y%m%d')
            random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            numero_seguimiento = f"AGRO-{fecha_actual}-{random_chars}"

            # 🚚 CREAR ENVÍO (🔥 CORREGIDO)
            envio = Envio.objects.create(
                id_compra=compra,
                estado_envio="pendiente",
                numero_seguimiento=numero_seguimiento,

                direccion_origen=direccion_origen,
                direccion_destino=direccion_destino,

                latitud_origen=lat_origen,
                longitud_origen=lng_origen,
                latitud_destino=lat_destino,
                longitud_destino=lng_destino,

                distancia_km=distancia_km,
                peso_total_kg=peso_total_kg,

                tarifa_por_km=tarifa_por_km,
                tarifa_por_kg=tarifa_por_kg,

                # 🔥 CORREGIDO AQUÍ
                costo_base=costo_distancia,
                costo_peso=costo_peso,
                costo_total=costo_total
            )

            print(f"🚚 Envío creado correctamente - ID: {envio.id_envio}")

        elif estado == "2":
            print("❌ PAGO RECHAZADO")
            compra.estado = "rechazado"
            compra.save()

        elif estado == "3":
            print("⏳ PAGO PENDIENTE")
            compra.estado = "pendiente"
            compra.save()

        elif estado == "11":
            print("🚫 PAGO CANCELADO")
            compra.estado = "cancelado"
            compra.save()

        else:
            print("⚠️ ESTADO DESCONOCIDO:", estado)

        print("====================================")
        return JsonResponse({"status": "ok"})

    print("⚠️ Método no permitido")
    return JsonResponse({"error": "metodo no permitido"})

# Función auxiliar para calcular distancia (fallback)
def calcular_distancia(lat1, lng1, lat2, lng2):
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Radio de la tierra en km
    
    lat1_rad = radians(float(lat1))
    lat2_rad = radians(float(lat2))
    delta_lat = radians(float(lat2) - float(lat1))
    delta_lng = radians(float(lng2) - float(lng1))
    
    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c



# Función para calcular distancia usando la fórmula de Haversine
def calcular_distancia(lat1, lng1, lat2, lng2):
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Radio de la tierra en km
    
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lng = radians(lng2 - lng1)
    
    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c


#pedidos del usuario

#@login_required
@login_required
def mis_pedidos(request):

    usuario = request.user.usuario

    # Validar que sea cliente
    if usuario.rol.upper() != "CLIENTE":
        return redirect('inicio')

    cliente = usuario.cliente

    compras = Compra.objects.filter(
        id_cliente=cliente
    ).exclude(estado="carrito").order_by('-fecha_hora_compra')
    
    # 🔥 compras que necesitan calificación
    compras_sin_calificar = compras.filter(
        envio__estado_envio='ENTREGADO'
    ).exclude(
        id_compra__in=Calificacion.objects.values_list('id_compra_id', flat=True)
    )

    pedidos = []
    
    compras_sin_calificar_ids = set(
        compras_sin_calificar.values_list('id_compra', flat=True)
    )
    
    for pedido in pedidos:
        pedido.necesita_calificacion = pedido.compra.id_compra in compras_sin_calificar_ids

    for compra in compras:
        detalles = DetallesCompra.objects.filter(id_compra=compra)
        envio = Envio.objects.filter(id_compra=compra).first()  # 🔥 AQUÍ

        pedidos.append({
            "compra": compra,
            "detalles": detalles,
            "envio": envio
        })

    return render(request, "pedidos/mis_pedidos.html", {
        "pedidos": pedidos,
        'compras_sin_calificar' : compras_sin_calificar,
    })    
    

@login_required
def seleccionar_destino(request):
    """Vista para que el cliente seleccione su ubicación de entrega en el mapa"""
    
    usuario = request.user.usuario
    
    # Validar que sea cliente
    if usuario.rol.upper() != "CLIENTE":
        messages.error(request, "Solo los clientes pueden seleccionar destino")
        return redirect('inicio')
    
    try:
        cliente = usuario.cliente
    except:
        messages.error(request, "Perfil de cliente no encontrado")
        return redirect('inicio')
    
    # Buscar compra activa en carrito
    compra = Compra.objects.filter(
        id_cliente=cliente,
        estado="carrito"
    ).first()
    
    if not compra:
        messages.warning(request, "No tienes productos en el carrito")
        return redirect('carrito')
    
    # Obtener coordenadas de origen (finca del producto)
    detalles = compra.detallescompra_set.all()
    lat_origen = None
    lng_origen = None
    peso_total = 0
    
    if detalles.exists():
        primer_detalle = detalles.first()
        producto = primer_detalle.id_producto
        
        # Obtener peso total
        for detalle in detalles:
            peso_producto = float(detalle.id_producto.peso_kg or 0)
            peso_total += float(detalle.cantidad) * peso_producto
        
        # Obtener finca
        from productos.models import ProductoFinca
        producto_finca = ProductoFinca.objects.filter(id_producto=producto).first()
        if producto_finca and producto_finca.id_finca:
            finca = producto_finca.id_finca
            lat_origen = finca.latitud
            lng_origen = finca.longitud
    
    # Valores existentes
    latitud_existente = compra.latitud_destino
    longitud_existente = compra.longitud_destino
    direccion_existente = compra.direccion_entrega
    distancia_existente = getattr(compra, 'distancia_km', 0)
    
    if request.method == 'POST':
        latitud = request.POST.get('latitud') or compra.latitud_destino
        longitud = request.POST.get('longitud') or compra.longitud_destino
        direccion = request.POST.get('direccion', '')
        distancia = request.POST.get('distancia', '0')
        
        print(f"📍 POST - Lat: {latitud}, Lng: {longitud}")
        print(f"📍 Distancia recibida: {distancia} km")
        
        if latitud is None or longitud is None:
            messages.error(request, 'Debes seleccionar una ubicación en el mapa')
            return render(request, 'pedidos/seleccionar_destino.html', {
                'compra': compra,
                'latitud_existente': latitud_existente,
                'longitud_existente': longitud_existente,
                'direccion_existente': direccion_existente,
                'distancia_existente': distancia_existente,
                'lat_origen': lat_origen,
                'lng_origen': lng_origen,
                'peso_total': peso_total,
            })
        
        try:
            # Normalizar coordenadas
            latitud_normalizada = str(latitud).replace(',', '.')
            longitud_normalizada = str(longitud).replace(',', '.')
            distancia_normalizada = str(distancia).replace(',', '.') if distancia else '0'
            
            # Guardar en la COMPRA (para que el webhook pueda acceder)
            compra.latitud_destino = float(latitud_normalizada)
            compra.longitud_destino = float(longitud_normalizada)
            compra.direccion_entrega = direccion
            # Guardar distancia en los detalles
            detalles = compra.detallescompra_set.all()

            for detalle in detalles:
                 detalle.distancia_km = float(distancia_normalizada)
                 detalle.save()

            print(f"✅ Distancia guardada en detalles: {distancia_normalizada} km")  # ← Guardar distancia en la compra
            compra.save()
            
            print(f"✅ Datos guardados en compra {compra.id_compra}")
            print(f"Distancia detalle: {detalle.distancia_km} km")
            print(f"   Latitud: {compra.latitud_destino}")
            print(f"   Longitud: {compra.longitud_destino}")
            
            messages.success(request, f'📍 Ubicación guardada. Distancia: {distancia_normalizada} km')
            return redirect('carrito')
            
        except Exception as e:
            print("❌ ERROR REAL:", str(e))
            messages.error(request, f'Error al guardar: {str(e)}')
    
    return render(request, 'pedidos/seleccionar_destino.html', {
        'compra': compra,
        'latitud_existente': latitud_existente,
        'longitud_existente': longitud_existente,
        'direccion_existente': direccion_existente,
        'distancia_existente': distancia_existente,
        'lat_origen': lat_origen,
        'lng_origen': lng_origen,
        'peso_total': peso_total,
    })
    
    
    
    