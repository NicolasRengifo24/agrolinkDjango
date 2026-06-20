from datetime import timedelta

from django.http import JsonResponse
from envios.models import Envio 
from servicios.models import Servicio
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




from django.db.models import Avg, Count, Sum, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def inicio(request):

    busqueda = request.GET.get('busqueda')

    total_usuarios = Usuario.objects.count()
    total_productos = Producto.objects.filter(estado=True).count()
    categorias = CategoriaProducto.objects.all()

    categoria_f = request.GET.get('categoria')
    ubicacion = request.GET.get('ubicacion')
    precio_min = request.GET.get('precioMin')
    precio_max = request.GET.get('precioMax')

    productos = Producto.objects.prefetch_related('imagenProducto').filter(estado=True)

    servicios_busqueda = None

    if busqueda:
        servicios_busqueda = Servicio.objects.filter(
            estado='ACTIVO'
        ).filter(
            Q(categoria__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

        productos = productos.filter(
            Q(nombre_producto__icontains=busqueda) |
            Q(descripcion_producto__icontains=busqueda) |
            Q(fincas__id_finca__ciudad__icontains=busqueda) |
            Q(fincas__id_finca__departamento__icontains=busqueda)
        )

    if categoria_f:
        productos = productos.filter(id_categoria=categoria_f)

    if ubicacion:
        productos = productos.filter(
            Q(fincas__id_finca__ciudad__icontains=ubicacion) |
            Q(fincas__id_finca__departamento__icontains=ubicacion)
        )

    if precio_min:
        productos = productos.filter(precio__gte=precio_min)

    if precio_max:
        productos = productos.filter(precio__lte=precio_max)

    productos = productos.distinct()

    promedios = Calificacion.objects.values(
        'id_compra__detallescompra__id_producto'
    ).annotate(
        promedio=Avg('puntaje_producto')
    )

    promedios_dict = {}
    for item in promedios:
        producto_id = item['id_compra__detallescompra__id_producto']
        promedios_dict[producto_id] = item['promedio']

    conteos = Calificacion.objects.values('id_compra__detallescompra__id_producto').annotate(
        total=Count('id_calificacion')
    )

    conteos_dict = {}
    for item in conteos:
        producto_id = item['id_compra__detallescompra__id_producto']
        conteos_dict[producto_id] = item['total']

    page = request.GET.get('page', 1)
    paginator = Paginator(productos, 8)
    try:
        productos_page = paginator.page(page)
    except PageNotAnInteger:
        productos_page = paginator.page(1)
    except EmptyPage:
        productos_page = paginator.page(paginator.num_pages)

    for producto in productos_page:
        producto.promedio_estrellas = promedios_dict.get(producto.id_producto, 0)
        producto.total_calificaciones = conteos_dict.get(producto.id_producto, 0)

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
            id_producto=producto_destacado_data['id_producto'], estado=True
        ).first()

    if producto_destacado:
        pf = ProductoFinca.objects.select_related('id_finca').filter(
            id_producto=producto_destacado
        ).first()
        if pf:
            finca_destacado = pf.id_finca

    productos_finca = ProductoFinca.objects.select_related(
        'id_finca', 'id_producto', 'id_finca__id_usuario'
    )

    ubicaciones = Finca.objects.values_list('ciudad', flat=True).distinct()
    ubicaciones = [u for u in ubicaciones if u]

    departamentos = Finca.objects.values_list('departamento', flat=True).distinct()
    departamentos = [d for d in departamentos if d]

    total_entregados = Envio.objects.filter(estado_envio__iexact='entregado').count()
    total_envios = Envio.objects.count()
    porcentaje_entregas = round((total_entregados / total_envios) * 100, 1) if total_envios > 0 else 0
    calificacion_promedio = Calificacion.objects.aggregate(avg=Avg('puntaje_producto'))['avg'] or 0

    return render(request, 'productos/inicio.html', {
        'productos': productos_page,
        'page_obj': productos_page,
        'productos_finca': productos_finca,
        'destacado': producto_destacado,
        'finca_destacado': finca_destacado,
        'categorias': categorias,
        'total_usuarios': total_usuarios,
        'total_productos': total_productos,
        'ubicaciones': ubicaciones,
        'departamentos': departamentos,
        'busqueda': busqueda,
        'servicios_busqueda': servicios_busqueda,
        'total_entregados': total_entregados,
        'porcentaje_entregas': porcentaje_entregas,
        'calificacion_promedio': calificacion_promedio,
    })    


def cargar_productos_pagina(request):
    busqueda = request.GET.get('busqueda', '')
    categoria_f = request.GET.get('categoria', '')
    ubicacion = request.GET.get('ubicacion', '')
    precio_min = request.GET.get('precioMin', '')
    precio_max = request.GET.get('precioMax', '')
    page = request.GET.get('page', 1)

    productos = Producto.objects.prefetch_related('imagenProducto').filter(estado=True)

    if busqueda:
        productos = productos.filter(
            Q(nombre_producto__icontains=busqueda) |
            Q(descripcion_producto__icontains=busqueda) |
            Q(fincas__id_finca__ciudad__icontains=busqueda) |
            Q(fincas__id_finca__departamento__icontains=busqueda)
        )

    if categoria_f:
        productos = productos.filter(id_categoria=categoria_f)

    if ubicacion:
        productos = productos.filter(
            Q(fincas__id_finca__ciudad__icontains=ubicacion) |
            Q(fincas__id_finca__departamento__icontains=ubicacion)
        )

    if precio_min:
        productos = productos.filter(precio__gte=precio_min)

    if precio_max:
        productos = productos.filter(precio__lte=precio_max)

    productos = productos.distinct()

    promedios = Calificacion.objects.values(
        'id_compra__detallescompra__id_producto'
    ).annotate(promedio=Avg('puntaje_producto'))
    promedios_dict = {i['id_compra__detallescompra__id_producto']: i['promedio'] for i in promedios}

    conteos = Calificacion.objects.values(
        'id_compra__detallescompra__id_producto'
    ).annotate(total=Count('id_calificacion'))
    conteos_dict = {i['id_compra__detallescompra__id_producto']: i['total'] for i in conteos}

    paginator = Paginator(productos, 8)
    try:
        productos_page = paginator.page(page)
    except PageNotAnInteger:
        productos_page = paginator.page(1)
    except EmptyPage:
        productos_page = paginator.page(paginator.num_pages)

    for producto in productos_page:
        producto.promedio_estrellas = promedios_dict.get(producto.id_producto, 0)
        producto.total_calificaciones = conteos_dict.get(producto.id_producto, 0)

    cards_html = render_to_string(
        'components/productos_grid.html',
        {'productos': productos_page},
        request=request
    )
    pagination_html = render_to_string(
        'components/pagination.html',
        {'page_obj': productos_page},
        request=request
    )

    return JsonResponse({
        'cards_html': cards_html,
        'pagination_html': pagination_html,
    })


def mostrar_productos(request):
    productos = Producto.objects.prefetch_related('imagenProducto').filter(estado=True).annotate(
        promedio_estrellas=Avg('calificaciones__puntaje'),
        total_calificaciones=Count('calificaciones')
    ).distinct()
    page = request.GET.get('page', 1)
    paginator = Paginator(productos, 8)
    try:
        productos_page = paginator.page(page)
    except PageNotAnInteger:
        productos_page = paginator.page(1)
    except EmptyPage:
        productos_page = paginator.page(paginator.num_pages)
    return render(request, "productos/inicio.html", {"productos": productos_page, "page_obj": productos_page})






def detalle_producto(request, id):
    producto = Producto.objects.prefetch_related('imagenProducto').filter(
        id_producto=id, estado=True
    ).first()

    if producto and producto.id_categoria:
        relacionados = Producto.objects.prefetch_related('imagenProducto').filter(
            id_categoria=producto.id_categoria, estado=True
        ).exclude(id_producto=producto.id_producto)[:4]

    # ⭐ estadísticas
    stats = Calificacion.objects.filter(
        id_compra__detallescompra__id_producto=producto
    ).aggregate(
        promedio=Avg('puntaje_producto'),
        total=Count('id_calificacion')
    )

    producto.promedio_estrellas = stats["promedio"] or 0
    producto.total_calificaciones = stats["total"] or 0

    # ⭐ comentarios (IMPORTANTE)
    calificaciones = Calificacion.objects.filter(
        id_compra__detallescompra__id_producto=producto
    ).select_related('id_compra')

    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'relacionados': relacionados,
        'calificaciones': calificaciones
    })
    

@login_required
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
    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except (ValueError, TypeError):
        messages.error(request, "Cantidad inválida")
        return redirect('carrito')  

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
        finca.ciudad = request.POST.get('ciudad')
        finca.departamento = request.POST.get('departamento')
        
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

@login_required
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
        productos = Producto.objects.none()
        productor = None
        messages.warning(request, 'No tienes un perfil de productor asociado')
    
    # Verificar si el productor tiene fincas registradas
    tiene_fincas = False
    if productor is not None:
        tiene_fincas = Finca.objects.filter(id_usuario=productor).exists()
    
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
        'categoria_id': categoria_id,
        'tiene_fincas': tiene_fincas,
    }
    
    return render(request, 'productos/lista_productos.html', context)



@login_required
def crear_producto(request):
    try:
        productor = request.user.usuario.productor
    except (AttributeError, Productor.DoesNotExist):
        messages.error(request, 'No tienes permiso para crear productos')
        return redirect('inicio')
    
    if request.method == 'POST':
        print("=== POST RECIBIDO ===")

        finca_id = request.POST.get('fincaId')
        if not finca_id:
            messages.error(request, 'Debes seleccionar una finca de producción')
            return redirect('crear_producto')
        
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
        from productos.models import ProductoFinca
        ProductoFinca.objects.create(
            id_producto=producto,
            id_finca_id=finca_id,
            cantidad_produccion=0,
            fecha_cosecha=None
        )
        print(f"✅ Producto asociado a finca ID: {finca_id}")
        
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
        
        messages.success(request, 'Producto editado exitosamente')
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
    
    top_productos = (
        DetallesCompra.objects
        .filter(id_producto__id_usuario_id=usuario_id)
        .values(
            'id_producto__id_producto',
            'id_producto__nombre_producto'
        )
        .annotate(
            unidades=Sum('cantidad'),
            ingresos=Sum('subtotal')
        )
        .order_by('-ingresos')[:5]
    )

    #  PEDIDOS POR ALISTAR
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

    # ENVÍOS
    envios = Envio.objects.filter(
        id_compra__in=pedidos_alistar.values_list('id_compra', flat=True)
    )
    
        # 1. Pedidos sin envío
    pedidos_sin_envio = Compra.objects.filter(
        detallescompra__id_producto__id_usuario_id=usuario_id,
        envio__isnull=True
    ).distinct().count()

    # 2. Envíos sin transportista
    envios_sin_transportista = Envio.objects.filter(
        id_compra__detallescompra__id_producto__id_usuario_id=usuario_id,
        id_transportista__isnull=True
    ).distinct().count()

    #  TOTAL REAL
    pendientes_logistica = pedidos_sin_envio + envios_sin_transportista

    envios_dict = {
        e.id_compra.id_compra: e for e in envios if e.id_compra
    }

    for p in pedidos_alistar:
        p.envio = envios_dict.get(p.id_compra)

    #  GRÁFICA GENERAL
    ventas_chart = (
        DetallesCompra.objects
        .filter(id_producto__id_usuario_id=usuario_id)
        .values('id_producto__nombre_producto')
        .annotate(total_ingresos=Sum('subtotal'))
    )

    #  GRÁFICA DE VENTAS POR FECHA (con filtro opcional)
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    ventas_grafica_qs = (
        DetallesCompra.objects
        .filter(id_producto__id_usuario_id=usuario_id)
    )

    if fecha_desde:
        ventas_grafica_qs = ventas_grafica_qs.filter(
            id_compra__fecha_hora_compra__date__gte=fecha_desde
        )
    if fecha_hasta:
        ventas_grafica_qs = ventas_grafica_qs.filter(
            id_compra__fecha_hora_compra__date__lte=fecha_hasta
        )

    ventas_grafica_qs = (
        ventas_grafica_qs
        .values('id_compra__fecha_hora_compra__date')
        .annotate(total=Sum('subtotal'))
        .order_by('id_compra__fecha_hora_compra__date')
    )

    ventas_grafica = [
        {
            "fecha": str(x["id_compra__fecha_hora_compra__date"]),
            "total": float(x["total"] or 0)
        }
        for x in ventas_grafica_qs
    ]

    #  KPIs
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
        'pendientes': pendientes_logistica,

    }

    context = {
        'productos': productos,
        'ventas': ventas,
        'ventas_chart': list(ventas_chart),
        'pedidos_alistar': pedidos_alistar,
        'ventas_grafica': ventas_grafica,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'kpis': kpis,
        'top_productos': list(top_productos),
    }

    return render(request, 'productos/mis_ventas.html', context)

def detalle_ventas_producto(request, producto_id):
    try:
        #  1. Traer detalles del producto
        detalles = (
            DetallesCompra.objects
            .filter(id_producto__id_producto=producto_id)
            .select_related('id_compra', 'id_producto')
            .order_by('-id_compra__fecha_hora_compra')
        )

        #  2. Renderizar HTML del modal
        html = render_to_string(
            'productos/detalle_ventas.html',
            {'detalles': detalles},
            request=request
        )

        #  3. Datos para gráfica (ventas por día)
        ventas_por_dia = (
    DetallesCompra.objects
    .filter(id_producto__id_producto=producto_id)
    .annotate(fecha=TruncDate('id_compra__fecha_hora_compra'))
    .values('fecha')
    .annotate(total=Sum('subtotal'))
    .order_by('fecha')
    )

        #  4. Convertir a lista para JSON
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


# esto es Para el reporte 

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from datetime import datetime
from django.db.models import Sum

def reporte_ventas_pdf(request):

    usuario = request.user.usuario
    productor = usuario.productor
    usuario_id = usuario.id_usuario

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas_agrolink.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()

    elementos = []

    # =========================
    #  HEADER
    # =========================
    elementos.append(Paragraph("📊 REPORTE PROFESIONAL - AGROLINK", styles['Title']))
    elementos.append(Spacer(1, 12))

    #  PRODUCTOR
    elementos.append(Paragraph("👤 Información del Productor", styles['Heading2']))
    elementos.append(Spacer(1, 8))

    elementos.append(Paragraph(f"Nombre: {usuario.nombre} {usuario.apellido}", styles['Normal']))
    elementos.append(Paragraph(f"Correo: {usuario.correo}", styles['Normal']))
    elementos.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))

    elementos.append(Spacer(1, 20))

    # =========================
    #  FINCAS
    # =========================
    fincas = Finca.objects.filter(id_usuario_id=usuario_id)

    elementos.append(Paragraph("🌱 Fincas Registradas", styles['Heading2']))
    elementos.append(Spacer(1, 10))

    if fincas.exists():
        data_fincas = [["Nombre", "Ciudad", "Departamento"]]

        for f in fincas:
            data_fincas.append([
                f.nombre_finca or "N/A",
                f.ciudad or "N/A",
                f.departamento or "N/A"
            ])

        tabla = Table(data_fincas)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elementos.append(tabla)
    else:
        elementos.append(Paragraph("No hay fincas registradas", styles['Normal']))

    elementos.append(Spacer(1, 20))

    # =========================
    #  PRODUCTOS
    # =========================
    productos = Producto.objects.filter(
        id_usuario_id=usuario_id
    ).prefetch_related('fincas__id_finca')

    elementos.append(Paragraph("📦 Productos", styles['Heading2']))
    elementos.append(Spacer(1, 10))

    data_productos = [["Producto", "Precio", "Stock", "Kg/Unidad", "Finca"]]

    for p in productos:
        finca = p.finca()

        data_productos.append([
            p.nombre_producto,
            f"${int(p.precio or 0):,}",
            p.stock or 0,
            f"{p.peso_kg or 0} kg",
            finca.nombre_finca if finca else "No asignada"
        ])

    tabla = Table(data_productos)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 20))

    # =========================
    #  VENTAS
    # =========================
    ventas = (
        DetallesCompra.objects
        .filter(id_producto__id_usuario_id=usuario_id)
        .values(
            'id_producto__nombre_producto',
            'id_producto__id_producto'
        )
        .annotate(
            total=Sum('subtotal'),
            unidades=Sum('cantidad')
        )
        .order_by('-total')
    )

    elementos.append(Paragraph("💰 Ingresos por Producto", styles['Heading2']))
    elementos.append(Spacer(1, 10))

    data_ventas = [["Producto", "Unidades", "Kg/Unidad", "Total Kg", "Ingresos", "Finca"]]

    #  MAPA DE PRODUCTOS (optimización)
    productos_map = {
        p.id_producto: p for p in productos
    }

    for v in ventas:
        producto = productos_map.get(v['id_producto__id_producto'])
        finca = producto.finca() if producto else None

        peso_unitario = float(producto.peso_kg or 0) if producto else 0
        total_kg = peso_unitario * (v['unidades'] or 0)

        data_ventas.append([
            v['id_producto__nombre_producto'],
            v['unidades'],
            f"{peso_unitario} kg",
            f"{int(total_kg):,} kg",
            f"${int(v['total'] or 0):,}",
            finca.nombre_finca if finca else "No asignada"
        ])

    tabla = Table(data_ventas)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 20))

    # =========================
    #  TOP PRODUCTO
    # =========================
    top = ventas.first()

    if top:
        producto = productos_map.get(top['id_producto__id_producto'])
        finca = producto.finca() if producto else None

        elementos.append(Paragraph("🏆 Producto Más Vendido", styles['Heading2']))
        elementos.append(Spacer(1, 10))

        elementos.append(Paragraph(f"Producto: {top['id_producto__nombre_producto']}", styles['Normal']))
        elementos.append(Paragraph(f"Unidades: {top['unidades']}", styles['Normal']))
        elementos.append(Paragraph(f"Ingresos: ${int(top['total'] or 0):,}", styles['Normal']))
        elementos.append(Paragraph(f"Finca: {finca.nombre_finca if finca else 'No asignada'}", styles['Normal']))

    elementos.append(Spacer(1, 20))

    # =========================
    #  TOTALES
    # =========================
    totales = DetallesCompra.objects.filter(
        id_producto__id_usuario_id=usuario_id
    ).aggregate(
        ingresos=Sum('subtotal'),
        unidades=Sum('cantidad')
    )

    elementos.append(Paragraph("📊 Totales Generales", styles['Heading2']))
    elementos.append(Spacer(1, 10))

    elementos.append(Paragraph(
        f"Ingresos Totales: ${int(totales['ingresos'] or 0):,}",
        styles['Normal']
    ))

    elementos.append(Paragraph(
        f"Unidades Vendidas: {totales['unidades'] or 0}",
        styles['Normal']
    ))

    # =========================
    #  GENERAR PDF
    # =========================
    doc.build(elementos)

    return response

#Perfil-Productor

@login_required
def perfil_productor(request):
    usuario = request.user.usuario
    productor = Productor.objects.get(id_usuario=usuario)

    productos_count = Producto.objects.filter(id_usuario=productor, estado=True).count()

    ventas_count = DetallesCompra.objects.filter(
        id_producto__id_usuario=productor
    ).count()

    # Comentarios recibidos en sus productos
    comentarios = Calificacion.objects.filter(
        id_compra__detallescompra__id_producto__id_usuario=productor
    ).exclude(
        comentario__isnull=True
    ).exclude(
        comentario__exact=''
    ).select_related(
        'id_compra'
    ).order_by('-fecha')[:10]

    # Calificación promedio del productor
    promedio = Calificacion.objects.filter(
        id_compra__detallescompra__id_producto__id_usuario=productor
    ).aggregate(promedio=Avg('puntaje_producto'))['promedio'] or 0

    total_comentarios = comentarios.count()

    if usuario.rol == 'PRODUCTOR':
        url_volver = 'lista_productos'
    else:
        url_volver = 'mostrar_productos'

    context = {
        'productor': productor,
        'es_dueno': True,
        'url_volver': url_volver,
        'productos': productos_count,
        'ventas': ventas_count,
        'comentarios': comentarios,
        'promedio': round(promedio, 1),
        'total_comentarios': total_comentarios,
    }

    return render(request, 'components/perfil_productor.html', context)

@login_required
def editar_perfil_productor(request):
    if request.method == "POST":
        try:
            usuario = request.user.usuario
            productor = Productor.objects.get(id_usuario=usuario)

            correo = request.POST.get("correo")
            cedula = request.POST.get("cedula")

            # VALIDACIÓN UNIQUE
            if Usuario.objects.filter(
                Q(correo=correo) | Q(cedula=cedula)
            ).exclude(id_usuario=usuario.id_usuario).exists():

                messages.error(request, "Correo o cédula ya en uso")
                return redirect('perfil_productor')

            # Datos
            usuario.nombre = request.POST.get("nombre")
            usuario.apellido = request.POST.get("apellido")
            usuario.correo = correo
            usuario.telefono = request.POST.get("telefono")
            usuario.cedula = request.POST.get("cedula")
            usuario.direccion = request.POST.get("direccion")

            if 'foto_perfil' in request.FILES:
                usuario.foto_perfil = request.FILES['foto_perfil']

            productor.tipo_cultivo = request.POST.get("tipo_cultivo")

            usuario.save()
            productor.save()

            messages.success(request, "Perfil actualizado correctamente")

        except Exception as e:
            print("ERROR:", e)
            messages.error(request, "Error al actualizar")

    return redirect('perfil_productor')   


    #CLIENTE VE EL PERFIL DE PRODUCTOR 

def ver_perfil_productor(request, id):

    productor = get_object_or_404(Productor, id_usuario=id)

    es_dueno = False

    if request.user.is_authenticated:
        usuario = request.user.usuario

        if hasattr(usuario, 'productor'):
            if usuario.productor.id_usuario.id_usuario == id:
                es_dueno = True


    productos_count = Producto.objects.filter(id_usuario=productor, estado=True).count()
    
    ventas_count = DetallesCompra.objects.filter(
        id_producto__id_usuario=productor
    ).count()

    if request.user.is_authenticated:
        url_volver = 'mostrar_productos'
    else:
        url_volver = 'mostrar_productos'    

    return render(request, 'components/perfil_productor.html', {
        'productor': productor,
        'es_dueno': es_dueno,
        'productos': productos_count,
        'ventas': ventas_count,
        'url_volver': url_volver,
    })