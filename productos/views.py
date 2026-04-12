from datetime import timedelta

from django.http import JsonResponse
from envios.models import Envio
from .models import Producto, ProductoFinca, CategoriaProducto 
from pedidos.models import DetallesCompra 
from django.shortcuts import render, redirect,get_object_or_404 
from django.contrib.auth.decorators import login_required
from .models import Producto, ProductoFinca, CategoriaProducto, Finca ,ImagenesProducto
from pedidos.models import DetallesCompra, Compra
from usuarios.models import Usuario
from django.db.models import Prefetch, Sum, Avg, Count, Max
from calificaciones.models import Calificacion
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from django.db.models import Q , F
from usuarios.models import Productor
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.db.models.functions import TruncDate
from django.utils.timezone import now




def inicio(request):

    # 👥 usuarios
    total_usuarios = Usuario.objects.count()

    # 📦 total productos
    total_productos = Producto.objects.count()

    # 📂 categorías
    categorias = CategoriaProducto.objects.all()
    categoria = request.GET.get('categoria')

    #  PRODUCTOS (CON ESTRELLAS)
    productos = Producto.objects.prefetch_related('imagenProducto').annotate(
        promedio_estrellas=Avg('calificaciones__puntaje'),
        total_calificaciones=Count('calificaciones')
    )

    #  filtro por categoría 
    total_usuarios = Usuario.objects.count()
    categorias = CategoriaProducto.objects.all()

    productos = Producto.objects.prefetch_related('imagenProducto')
    categoria = request.GET.get('categoria')
    if categoria:
        productos = productos.filter(id_categoria=categoria)

    # productos por finca
    productos_finca = ProductoFinca.objects.select_related(
        'id_finca', 'id_producto', 'id_finca__id_usuario'
    )

    # ⭐ destacado
    producto_destacado = None
    finca_destacado = None

    producto_destacado_data = (
        DetallesCompra.objects
        .values('id_producto')
        .annotate(total_vendido=Sum('cantidad'))
        .order_by('-total_vendido')
        .first()
    )

    if producto_destacado_data:
        producto_destacado = Producto.objects.prefetch_related('imagenProducto').filter(
            id_producto=producto_destacado_data['id_producto']
        ).annotate(
            promedio_estrellas=Avg('calificaciones__puntaje'),
            total_calificaciones=Count('calificaciones')
        ).first()

    if producto_destacado:
        pf = ProductoFinca.objects.select_related('id_finca').filter(
            id_producto=producto_destacado
        ).first()
        if pf:
            finca_destacado = pf.id_finca

    return render(request, 'productos/inicio.html', {
        'productos': productos,
        'productos_finca': productos_finca,
        'destacado': producto_destacado,
        'finca_destacado': finca_destacado,
        'categorias': categorias,
        'total_usuarios': total_usuarios,
        'total_productos': total_productos,
    })


# 🔁 tu función original (la dejamos por si la usas en rutas)
def mostrar_productos(request):
    productos = Producto.objects.prefetch_related('imagenProducto').annotate(
        promedio_estrellas=Avg('calificaciones__puntaje'),
        total_calificaciones=Count('calificaciones')
    )
    return render(request, "productos/inicio.html", {"productos": productos})


def detalle_producto(request, id):
    producto = Producto.objects.prefetch_related('imagenProducto').filter(
        id_producto=id
    ).annotate(
        promedio_estrellas=Avg('calificaciones__puntaje'),
        total_calificaciones=Count('calificaciones')
    ).first()
    
    relacionados = []
    if producto and producto.id_categoria:
        relacionados = Producto.objects.prefetch_related('imagenProducto').filter(
            id_categoria=producto.id_categoria
        ).exclude(id_producto=producto.id_producto)[:4]

    # CORREGIDO: usar id_producto en lugar de producto
    comentarios = Calificacion.objects.filter(
        id_producto=producto
    ).order_by('-fecha')[:3]

    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'comentarios': comentarios
    })


# 📋 lista simple (también corregida)
def lista_productos(request):
    productos = Producto.objects.all().annotate(
        promedio_estrellas=Avg('calificaciones__puntaje'),
        total_calificaciones=Count('calificaciones')
    )
    return render(request, "productos/lista.html", {"productos": productos})
    categorias = CategoriaProducto.objects.all()
    
    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'relacionados' : relacionados,
        'categorias' : categorias,
        
    })




def agregar_al_carrito(request, producto_id):
    # VALIDAR LOGIN
    if not request.user.is_authenticated:
        messages.warning(request, "Debe iniciar sesión como cliente")
        return redirect('login_view')

    # VALIDAR QUE SEA CLIENTE (CORREGIDO)
    try:
        usuario = request.user.usuario
        rol = usuario.rol.upper()
        
        # Aceptar tanto 'CLIENTE' como 'ROLE_CLIENTE'
        if rol not in ['CLIENTE', 'ROLE_CLIENTE']:
            messages.error(request, "Debe iniciar sesión como cliente")
            return redirect('login_view')
        
        # Verificar que tenga perfil de cliente
        if not hasattr(usuario, 'cliente'):
            messages.error(request, "Su usuario no tiene perfil de cliente")
            return redirect('login_view')
            
        cliente = usuario.cliente
        
    except Exception as e:
        print(f"Error al obtener cliente: {e}")
        messages.error(request, "Error con su perfil de cliente")
        return redirect('login_view')

    # PRODUCTO
    producto = get_object_or_404(Producto, id_producto=producto_id)

    # CANTIDAD
    cantidad = int(request.POST.get('cantidad', 1))

    # CARRITO (Compra en estado carrito)
    compra, created = Compra.objects.get_or_create(
        id_cliente=cliente,
        estado="carrito",
        defaults={
            "subtotal": 0,
            "impuestos": 0,
            "total": 0
        }
    )

    # DETALLE
    detalle, created = DetallesCompra.objects.get_or_create(
        id_compra=compra,
        id_producto=producto,
        defaults={
            "cantidad": cantidad,
            "precio_unitario": producto.precio,
            "subtotal": producto.precio * cantidad
        }
    )

    # SI YA EXISTE → SUMA
    if not created:
        detalle.cantidad += cantidad
        detalle.precio_unitario = producto.precio
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario
        detalle.save()

    # ACTUALIZAR TOTALES
    detalles = DetallesCompra.objects.filter(id_compra=compra)
    subtotal = sum(d.subtotal for d in detalles)
    impuestos = subtotal * Decimal('0.19')
    total = subtotal + impuestos

    compra.subtotal = subtotal
    compra.impuestos = impuestos
    compra.total = total
    compra.save()

    messages.success(request, f"{producto.nombre_producto} agregado al carrito")
    return redirect('carrito')


#@login_required
def crear_finca(request):
    """Vista para crear una nueva finca con selección de ubicación en mapa"""
    
    # Verificar que el usuario sea productor
    if request.user.usuario.rol.upper() != "PRODUCTOR":
        messages.error(request, "Solo los productores pueden registrar fincas")
        return redirect('inicio')
    
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_finca = request.POST.get('nombre_finca')
        direccion_finca = request.POST.get('direccion_finca')
        ciudad = request.POST.get('ciudad')
        departamento = request.POST.get('departamento')
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')
        
        # Validaciones
        if not nombre_finca:
            messages.error(request, 'El nombre de la finca es obligatorio')
            return render(request, 'finca/formulario_finca.html')
        
        if not latitud or not longitud:
            messages.error(request, 'Debes seleccionar la ubicación de la finca en el mapa')
            return render(request, 'finca/formulario_finca.html')
        
        try:
            # Crear finca
            finca = Finca.objects.create(
                id_usuario=request.user.usuario.productor,
                nombre_finca=nombre_finca,
                direccion_finca=direccion_finca,
                ciudad=ciudad,
                departamento=departamento,
                latitud=float(latitud),
                longitud=float(longitud)
            )
            
            messages.success(request, f'¡Finca "{nombre_finca}" registrada exitosamente!')
            return redirect('lista_fincas')  # Redirige a la lista de fincas
            
        except Exception as e:
            messages.error(request, f'Error al guardar la finca: {str(e)}')
            return render(request, 'finca/formulario_finca.html')
    
    # GET: mostrar formulario vacío
    return render(request, 'finca/formulario_finca.html')






@login_required
def editar_finca(request, finca_id):
    finca = get_object_or_404(Finca, id_finca=finca_id)
    
    # Verificar que el usuario tenga perfil de productor
    if not hasattr(request.user, 'usuario'):
        messages.error(request, 'Tu cuenta no tiene un perfil de usuario asociado')
        return redirect('lista_fincas')
    
    try:
        productor_actual = request.user.usuario.productor
    except ObjectDoesNotExist:
        messages.error(request, 'Tu perfil de usuario no tiene rol de productor')
        return redirect('lista_fincas')
    
    # Comparar productores
    if finca.id_usuario != productor_actual:
        messages.error(request, 'No tienes permiso para editar esta finca')
        return redirect('lista_fincas')
    
    if request.method == 'POST':
        # Actualizar datos
        finca.nombre_finca = request.POST.get('nombre_finca')
        finca.direccion_finca = request.POST.get('direccion_finca')
        finca.ciudad = request.POST.get('txt_ciudad')
        finca.departamento = request.POST.get('txt_departamento')
        
        # Procesar coordenadas
        latitud = request.POST.get('latitud', '').strip()
        longitud = request.POST.get('longitud', '').strip()
        
        if latitud and longitud:
            try:
                finca.latitud = float(latitud.replace(',', '.'))
                finca.longitud = float(longitud.replace(',', '.'))
            except ValueError:
                pass
        
        finca.save()
        messages.success(request, 'Finca actualizada exitosamente')
        return redirect('lista_fincas')
    
    return render(request, 'finca/formulario_finca.html', {'finca': finca})

#@login_required
def lista_fincas(request):
    """Lista de fincas del productor"""
    
    fincas = Finca.objects.filter(id_usuario=request.user.usuario.productor)
    
    return render(request, 'finca/lista_fincas.html', {'fincas': fincas})



@login_required
def lista_productos(request):
    """Vista para listar los productos del productor actual"""
    
    # Obtener parámetros de filtro desde GET
    ubicacion = request.GET.get('ubicacion', '')
    categoria_id_str = request.GET.get('categoriaId', '0')
    
    # Convertir categoria_id a entero de forma segura
    try:
        categoria_id = int(categoria_id_str)
    except (ValueError, TypeError):
        categoria_id = 0
    
    # Obtener productos del productor actual
    try:
        productor = request.user.usuario.productor
        productos = Producto.objects.filter(id_usuario=productor)
    except (AttributeError, Productor.DoesNotExist):
        productos = Producto.objects.none()  # QuerySet vacío en lugar de lista vacía
        messages.warning(request, 'No tienes un perfil de productor asociado')
    
    # Obtener todas las categorías para el filtro
    categorias = CategoriaProducto.objects.all()
    
    # Aplicar filtros
    if ubicacion:
        productos = productos.filter(
            Q(fincas__id_finca__ciudad__icontains=ubicacion) |
            Q(fincas__id_finca__departamento__icontains=ubicacion)
        ).distinct()  # distinct() para evitar duplicados por la relación many-to-many
    
    if categoria_id > 0:  # Solo filtrar si es mayor que 0
        productos = productos.filter(id_categoria_id=categoria_id)
    
    # Ordenar productos (opcional)
    productos = productos.order_by('-id_producto')  # Los más recientes primero
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'ubicacion': ubicacion,
        'categoria_id': categoria_id,  # Ya es un entero
    }
    
    return render(request, 'productos/lista_productos.html', context)




@login_required
@login_required
def crear_producto(request):
    try:
        productor = request.user.usuario.productor
    except (AttributeError, Productor.DoesNotExist):
        messages.error(request, 'No tienes permiso para crear productos')
        return redirect('inicio')
    
    if request.method == 'POST':
        print("=== POST RECIBIDO ===")
        
        # Crear producto
        producto = Producto(
            id_usuario=productor,
            id_categoria_id=request.POST.get('categoria'),
            nombre_producto=request.POST.get('nombre_producto'),
            descripcion_producto=request.POST.get('descripcion_producto') or '',
            precio=request.POST.get('precio') or 0,
            stock=request.POST.get('stock') or 0,
            peso_kg=request.POST.get('peso_kg') or None,
        )
        producto.save()
        
        # Guardar imagen
        if 'imagenes' in request.FILES:
            imagen_file = request.FILES['imagenes']
            ImagenesProducto.objects.create(
                id_producto=producto,
                url_imagen=imagen_file,
                es_principal=1
            )
        
        # 🔥 IMPORTANTE: Crear la relación con la finca
        finca_id = request.POST.get('fincaIds')
        if finca_id:
            from productos.models import ProductoFinca
            ProductoFinca.objects.create(
                id_producto=producto,
                id_finca_id=finca_id,
                cantidad_produccion=0,
                fecha_cosecha=None
            )
            print(f"✅ Producto asociado a finca ID: {finca_id}")
        else:
            print("⚠️ No se seleccionó ninguna finca")
        
        messages.success(request, 'Producto creado exitosamente')
        return redirect('lista_productos')
    
    context = {
        'categorias': CategoriaProducto.objects.all(),
        'fincas_productor': Finca.objects.filter(id_usuario=productor),
        'productor_nombre': f"{productor.id_usuario.nombre} {productor.id_usuario.apellido}",
    }
    return render(request, 'productos/crear_producto.html', context)

@login_required
def buscar_productos(request):
    """Vista para buscar productos del productor"""
    ubicacion = request.GET.get('ubicacion', '')
    categoria_id = request.GET.get('categoriaId', 0)
    return redirect(f"{reverse('lista_productos')}?ubicacion={ubicacion}&categoriaId={categoria_id}")


@login_required
def ver_producto(request, producto_id):
    """Vista para ver detalle de un producto (productor)"""
    producto = get_object_or_404(Producto, id_producto=producto_id)
    
    # Verificar permiso
    try:
        productor = request.user.usuario.productor
        es_propietario = (producto.id_usuario == productor)
    except (AttributeError, Productor.DoesNotExist):
        es_propietario = False
    
    if not es_propietario:
        messages.error(request, 'No tienes permiso para ver este producto')
        return redirect('lista_productos')
    
    imagenes = producto.imagenProducto.all()
    
    context = {
        'producto': producto,
        'imagenes': imagenes,
        'imagen_principal': imagenes.filter(es_principal=1).first(),
    }
    return render(request, 'productos/detalle_producto.html', context)


def ver_producto_detalles(request, producto_id):
    """Vista para obtener los detalles de un producto en JSON"""
    try:
        producto = get_object_or_404(Producto, id_producto=producto_id)
        
        # Obtener fincas asociadas
        fincas_asociadas = ProductoFinca.objects.filter(id_producto=producto).select_related('id_finca')
        
        fincas_data = []
        for pf in fincas_asociadas:
            fincas_data.append({
                'nombre_finca': pf.id_finca.nombre_finca,
                'cantidad_produccion': str(pf.cantidad_produccion) if pf.cantidad_produccion else 'N/A',
                'fecha_cosecha': pf.fecha_cosecha.strftime('%d/%m/%Y') if pf.fecha_cosecha else None
            })
        
        producto_data = {
            'id_producto': producto.id_producto,
            'nombre_producto': producto.nombre_producto,
            'descripcion_producto': producto.descripcion_producto,
            'precio': str(producto.precio) if producto.precio else '0',
            'stock': producto.stock,
            'peso_kg': str(producto.peso_kg) if producto.peso_kg else '0',
            'categoria': producto.id_categoria.nombre_categoria if producto.id_categoria else 'Sin categoría',
            'imagen_principal': producto.imagen_principal_url(),
            'fincas': fincas_data
        }
        
        return JsonResponse({
            'success': True,
            'producto': producto_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
        
        
        

def editar_producto_form(request, producto_id):
    """Vista para obtener el formulario de edición en HTML"""
    try:
        producto = get_object_or_404(Producto, id_producto=producto_id)
        categorias = CategoriaProducto.objects.all()
        
        # Renderizar el formulario HTML
        form_html = render_to_string('productos/editar_producto_form.html', {
            'producto': producto,
            'categorias': categorias
        })
        
        return JsonResponse({
            'success': True,
            'form_html': form_html
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@csrf_exempt
def actualizar_producto(request, producto_id):
    """Vista para actualizar el producto via AJAX"""
    if request.method == 'POST':
        try:
            producto = get_object_or_404(Producto, id_producto=producto_id)
            
            # Actualizar campos
            producto.nombre_producto = request.POST.get('nombre_producto')
            producto.descripcion_producto = request.POST.get('descripcion_producto')
            producto.precio = request.POST.get('precio')
            producto.stock = request.POST.get('stock')
            producto.peso_kg = request.POST.get('peso_kg')
            producto.id_categoria_id = request.POST.get('categoria')
            
            producto.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Producto actualizado correctamente'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required
def editar_producto(request, producto_id):
    """Vista para editar un producto existente"""
    producto = get_object_or_404(Producto, id_producto=producto_id)
    categorias = CategoriaProducto.objects.all()
    
    # Verificar permiso
    try:
        productor = request.user.usuario.productor
        if producto.id_usuario != productor:
            messages.error(request, 'No tienes permiso para editar este producto')
            return redirect('lista_productos')
    except (AttributeError, Productor.DoesNotExist):
        messages.error(request, 'No tienes permiso para editar productos')
        return redirect('lista_productos')
    
    if request.method == 'POST':
        try:
            # Actualizar SOLO los campos que existen
            producto.id_categoria_id = request.POST.get('categoria')
            producto.nombre_producto = request.POST.get('nombre_producto')
            producto.descripcion_producto = request.POST.get('descripcion_producto')
            producto.precio = request.POST.get('precio')
            producto.stock = request.POST.get('stock')
            producto.peso_kg = request.POST.get('peso_kg') or None
            producto.save()
            
            # Manejar nuevas imágenes
            nuevas_imagenes = request.FILES.getlist('nuevas_imagenes')
            for img in nuevas_imagenes:
                ImagenesProducto.objects.create(
                    id_producto=producto,
                    url_imagen=img,
                    es_principal=0
                )
            
            # Eliminar imágenes seleccionadas
            imagenes_eliminar = request.POST.getlist('eliminar_imagenes')
            for img_id in imagenes_eliminar:
                try:
                    imagen = ImagenesProducto.objects.get(id_imagen=img_id, id_producto=producto)
                    imagen.delete()
                except ImagenesProducto.DoesNotExist:
                    pass
            
            # Actualizar imagen principal
            imagen_principal_id = request.POST.get('imagen_principal')
            if imagen_principal_id:
                producto.imagenProducto.update(es_principal=0)
                ImagenesProducto.objects.filter(id_imagen=imagen_principal_id, id_producto=producto).update(es_principal=1)
            
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('lista_productos')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el producto: {str(e)}')
    
    # Obtener imágenes para el formulario
    imagenes = producto.imagenProducto.all()
    imagen_principal = imagenes.filter(es_principal=1).first()
    
    context = {
        'producto': producto,
        'categorias': categorias,
        'imagenes': imagenes,
        'imagen_principal': imagen_principal,
    }
    return render(request, 'editar_producto.html', context)


@login_required
def eliminar_producto(request, producto_id):
    """Vista para eliminar un producto"""
    producto = get_object_or_404(Producto, id_producto=producto_id)
    
    # Verificar permiso
    try:
        productor = request.user.usuario.productor
        if producto.id_usuario != productor:
            messages.error(request, 'No tienes permiso para eliminar este producto')
            return redirect('lista_productos')
    except (AttributeError, Productor.DoesNotExist):
        messages.error(request, 'No tienes permiso para eliminar productos')
        return redirect('lista_productos')
    
    if request.method == 'POST':
        try:
            nombre_producto = producto.nombre_producto
            producto.delete()
            messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente')
        except Exception as e:
            messages.error(request, f'Error al eliminar el producto: {str(e)}')
    
    return redirect('lista_productos')

 





def mis_ventas(request):

    usuario_id = request.user.usuario.id_usuario  # 🔥 CLAVE

    # 🔹 PRODUCTOS
    productos = Producto.objects.filter(id_usuario_id=usuario_id)

    # 🔹 RESUMEN DE VENTAS
    ventas = (
        DetallesCompra.objects
        .filter(id_producto__id_usuario_id=usuario_id)
        .values('id_producto__id_producto', 'id_producto__nombre_producto')
        .annotate(
            total_vendido=Sum('cantidad'),
            total_ingresos=Sum('subtotal'),
            total_ventas=Count('id_compra', distinct=True),
            ultima_venta=Max('id_compra__fecha_hora_compra')
        )
    )

    # 🔹 PEDIDOS POR ALISTAR
    pedidos_alistar = (
        Compra.objects
        .filter(detallescompra__id_producto__id_usuario_id=usuario_id)
        .select_related('id_cliente__id_usuario')
        .prefetch_related(
            Prefetch(
                'detallescompra_set',
                queryset=DetallesCompra.objects.select_related('id_producto')
            )
        )
        .distinct()
        .order_by('-fecha_hora_compra')
    )

    # 🔹 ENVÍOS
    envios = Envio.objects.filter(
        id_compra__in=pedidos_alistar.values_list('id_compra', flat=True)
    )

    envios_dict = {
        e.id_compra.id_compra: e for e in envios if e.id_compra
    }

    for p in pedidos_alistar:
        p.envio = envios_dict.get(p.id_compra)

    # 🔹 GRÁFICA GENERAL
    ventas_chart = (
        DetallesCompra.objects
        .filter(id_producto__id_usuario_id=usuario_id)
        .values('id_producto__nombre_producto')
        .annotate(total_ingresos=Sum('subtotal'))
    )

    # 🔹 ÚLTIMOS 7 DÍAS
    hoy = now().date()
    hace_7_dias = hoy - timedelta(days=7)

    ultimos_7_dias_qs = (
        DetallesCompra.objects
        .filter(
            id_producto__id_usuario_id=usuario_id,
            id_compra__fecha_hora_compra__date__gte=hace_7_dias
        )
        .values('id_compra__fecha_hora_compra__date')
        .annotate(total=Sum('subtotal'))
        .order_by('id_compra__fecha_hora_compra__date')
    )

    ultimos_7_dias = [
        {
            "fecha": str(x["id_compra__fecha_hora_compra__date"]),
            "total": float(x["total"] or 0)
        }
        for x in ultimos_7_dias_qs
    ]

    # 🔹 KPIs
    base = DetallesCompra.objects.filter(
        id_producto__id_usuario_id=usuario_id
    )

    kpis_raw = base.aggregate(
        ingresos=Sum('subtotal'),
        unidades=Sum('cantidad'),
        ordenes=Count('id_compra', distinct=True),
        ticket_promedio=Avg('subtotal')
    )

    kpis = {
        'ingresos': kpis_raw['ingresos'] or 0,
        'unidades': kpis_raw['unidades'] or 0,
        'ordenes': kpis_raw['ordenes'] or 0,
        'ticket_promedio': kpis_raw['ticket_promedio'] or 0,
    }

    context = {
        'productos': productos,
        'ventas': ventas,
        'ventas_chart': list(ventas_chart),
        'pedidos_alistar': pedidos_alistar,
        'ultimos_7_dias': ultimos_7_dias,
        'kpis': kpis
    }

    return render(request, 'productos/mis_ventas.html', context)

def detalle_ventas_producto(request, producto_id):
    try:
        # 🔹 1. Traer detalles del producto
        detalles = (
            DetallesCompra.objects
            .filter(id_producto__id_producto=producto_id)
            .select_related('id_compra', 'id_producto')
            .order_by('-id_compra__fecha_hora_compra')
        )

        # 🔹 2. Renderizar HTML del modal
        html = render_to_string(
            'productos/detalle_ventas.html',
            {'detalles': detalles},
            request=request
        )

        # 🔹 3. Datos para gráfica (ventas por día)
        ventas_por_dia = (
    DetallesCompra.objects
    .filter(id_producto__id_producto=producto_id)
    .annotate(fecha=TruncDate('id_compra__fecha_hora_compra'))
    .values('fecha')
    .annotate(total=Sum('subtotal'))
    .order_by('fecha')
)

        # 🔹 4. Convertir a lista para JSON
        data_grafica = [
            {
               'fecha': v['fecha'].strftime('%Y-%m-%d'),
                'total': float(v['total'])
            }
            for v in ventas_por_dia
        ]

        return JsonResponse({
            'success': True,
            'html': html,
            'grafica': data_grafica
        })
    except Exception as e:
        print("❌ ERROR detalle ventas:", str(e))

        return JsonResponse({
            'success': False,
            'error': str(e)
        })


'''
def dashboard_productor(request):
    print("🔥 ENTRÉ A DASHBOARD_PRODUCTOR")

    productor = request.user.usuario.productor
    
    print("PRODUCTOR:", productor)
    print("TIPO:", type(productor))

    # 📊 FECHAS
    hoy = now().date()
    hace_7_dias = hoy - timedelta(days=7)
    hace_30_dias = hoy - timedelta(days=30)

    base = DetallesCompra.objects.filter(
    id_producto__id_usuario=productor.id_usuario
    )
    
    print("BASE COUNT:", base.count())

    # 💰 KPIs
    kpis = base.aggregate(
    ingresos=Sum('subtotal'),
    unidades=Sum('cantidad'),
    ordenes=Count('id_compra', distinct=True),
    ticket_promedio=Avg('subtotal')
)

    kpis = {
        'ingresos': kpis['ingresos'] or 0,
        'unidades': kpis['unidades'] or 0,
        'ordenes': kpis['ordenes'] or 0,
        'ticket_promedio': kpis['ticket_promedio'] or 0,
    }

    # 📈 ingresos últimos 7 días
    ultimos_7_dias_qs = (
    DetallesCompra.objects
    .filter(
        id_producto__id_usuario_id=productor.id_usuario
    )
    .values('id_compra__fecha_hora_compra__date')
    .annotate(total=Sum('subtotal'))
    .order_by('id_compra__fecha_hora_compra__date')
    )

    ultimos_7_dias = [
        {
            "fecha": str(x["id_compra__fecha_hora_compra__date"]),
            "total": float(x["total"] or 0)
        }
        for x in ultimos_7_dias_qs
    ]

    print("DEBUG DASHBOARD FINAL:", ultimos_7_dias)

    # 📦 productos top
    top_productos = (
        base.values('id_producto__nombre_producto')
        .annotate(
            unidades=Sum('cantidad'),
            ingresos=Sum('subtotal')
        )
        .order_by('-ingresos')[:5]
    )

    # 🚚 estados de pedidos
    estados = (
        Compra.objects.filter(
            detallescompra__id_producto__id_usuario=productor
        )
        .values('estado')
        .annotate(total=Count('id_compra'))
    )

    # 🚨 pedidos pendientes
    pendientes = Compra.objects.filter(
    detallescompra__id_producto__id_usuario_id=productor.id_usuario,
    estado='Pendiente'
    ).count()
    
    
    
    

    return render(request, 'productos/dashboard_pro.html', {
    'kpis': kpis,
    'ultimos_7_dias': ultimos_7_dias,
    'top_productos': list(top_productos),
    'estados': list(estados),
    'pendientes': pendientes
})
'''

