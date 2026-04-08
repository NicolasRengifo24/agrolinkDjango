from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings          
from .models import Compra, DetallesCompra
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

    #  NUEVO
    'url_respuesta': f"{settings.NGROK_URL}/respuesta-pago/",
    'url_confirmacion': f"{settings.NGROK_URL}/confirmacion-pago/",
})
    

def actualizar_carrito(request, detalle_id):
    detalle = get_object_or_404(DetallesCompra, id_detalle=detalle_id)
    
    nueva_cantidad = int(request.POST.get('cantidad',1))
    
    if nueva_cantidad <=0:
        messages.error(request, "cantidad invalida")
        return redirect('carrito')
    
    messages.success(request, "Stock actualizado")
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

        print("📦 DATA RECIBIDA:")
        print(data)

        ref = data.get("x_ref_payco")
        estado = data.get("x_cod_transaction_state")
        factura = data.get("x_id_invoice")

        print("🔎 ref_payco:", ref)
        print("🔎 estado:", estado)
        print("🔎 factura:", factura)

        try:
            compra_id = int(factura.split("_")[1])
            compra = Compra.objects.get(id_compra=compra_id)
            print("✅ Compra encontrada:", compra.id_compra)
        except Exception as e:
            print("❌ ERROR buscando compra:", str(e))
            return JsonResponse({"status": "error compra no encontrada"})

        # 🔥 VALIDAR ESTADO
        if estado == "1":  # APROBADO
            print("💰 PAGO APROBADO")

            compra.estado = "pagado"
            compra.metodo_pago = "epayco"
            compra.save()

            # 🚚 CREAR ENVÍO
            Envio.objects.create(
                id_compra=compra,
                estado_envio="pendiente",
                direccion_destino=compra.direccion_entrega
            )

            print("🚚 Envío creado correctamente")

        elif estado == "2":
            print("❌ PAGO RECHAZADO")
            compra.estado = "rechazado"
            compra.save()

        elif estado == "3":
            print("⏳ PAGO PENDIENTE")
            compra.estado = "pendiente"
            compra.save()
            
        elif estado == "11":
            print("PAGO CANCELADO POR EL USUARIO")
            compra.estado = "cancelado"
            compra.save()    

        else:
            print("⚠️ ESTADO DESCONOCIDO:", estado)

        print("====================================")
        return JsonResponse({"status": "ok"})

    print("⚠️ Método no permitido")
    return JsonResponse({"error": "metodo no permitido"})



#pedidos del usuario

#@login_required
def mis_pedidos(request):

    usuario = request.user.usuario

    # Validar que sea cliente
    if usuario.rol.upper() != "CLIENTE":
        return redirect('inicio')

    cliente = usuario.cliente

    compras = Compra.objects.filter(
        id_cliente=cliente
    ).exclude(estado="carrito").order_by('-fecha_hora_compra')

    pedidos = []

    for compra in compras:
        detalles = DetallesCompra.objects.filter(id_compra=compra)

        pedidos.append({
            "compra": compra,
            "detalles": detalles
        })

    return render(request, "pedidos/mis_pedidos.html", {
        "pedidos": pedidos
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
    
    # Si ya tiene coordenadas guardadas, mostrarlas en el mapa
    latitud_existente = compra.latitud_destino
    longitud_existente = compra.longitud_destino
    direccion_existente = compra.direccion_entrega
    
    if request.method == 'POST':
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')
        direccion = request.POST.get('direccion', '')
        
        if not latitud or not longitud:
            messages.error(request, 'Debes seleccionar una ubicación en el mapa')
            return render(request, 'pedidos/seleccionar_destino.html', {
                'compra': compra,
                'latitud_existente': latitud_existente,
                'longitud_existente': longitud_existente,
                'direccion_existente': direccion_existente,
            })
        
        try:
            # Guardar coordenadas en la compra
            compra.latitud_destino = float(latitud)
            compra.longitud_destino = float(longitud)
            compra.direccion_entrega = direccion
            compra.save()
            
            messages.success(request, '📍 Ubicación de destino guardada correctamente')
            return redirect('carrito')
            
        except Exception as e:
            messages.error(request, f'Error al guardar la ubicación: {str(e)}')
    
    return render(request, 'pedidos/seleccionar_destino.html', {
        'compra': compra,
        'latitud_existente': latitud_existente,
        'longitud_existente': longitud_existente,
        'direccion_existente': direccion_existente,
    })