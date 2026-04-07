from .models import Producto, ProductoFinca, CategoriaProducto
from pedidos.models import DetallesCompra
from django.shortcuts import render, redirect,get_object_or_404 
from django.contrib.auth.decorators import login_required
from .models import Producto, ProductoFinca, CategoriaProducto, Finca ,ImagenesProducto
from pedidos.models import DetallesCompra, Compra
from usuarios.models import Usuario
from django.db.models import Sum, Avg, Count
from calificaciones.models import Calificacion
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from django.db.models import Q
from usuarios.models import Productor
from django.urls import reverse



def inicio(request):

    # 👥 usuarios
    total_usuarios = Usuario.objects.count()

    # 📦 total productos
    total_productos = Producto.objects.count()

    # 📂 categorías
    categorias = CategoriaProducto.objects.all()
    categoria = request.GET.get('categoria')

    # 🔥 PRODUCTOS (CON ESTRELLAS)
    productos = Producto.objects.prefetch_related('imagenProducto').annotate(
        promedio_estrellas=Avg('calificaciones__puntaje'),
        total_calificaciones=Count('calificaciones')
    )

    # 🔎 filtro por categoría (AHORA SÍ FUNCIONA)
    total_usuarios = Usuario.objects.count()
    categorias = CategoriaProducto.objects.all()

    productos = Producto.objects.prefetch_related('imagenProducto')
    categoria = request.GET.get('categoria')
    if categoria:
        productos = productos.filter(id_categoria=categoria)

    # 🌱 productos por finca (LO TUYO ORIGINAL)
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

#@login_required
def lista_fincas(request):
    """Lista de fincas del productor"""
    
    fincas = Finca.objects.filter(id_usuario=request.user.usuario.productor)
    
    return render(request, 'finca/lista_fincas.html', {'fincas': fincas})


@login_required
def lista_productos(request):
    """Vista para listar los productos del productor actual"""
    try:
        productor = request.user.usuario.productor
        productos = Producto.objects.filter(id_usuario=productor)
    except (AttributeError, Productor.DoesNotExist):
        productos = []
        messages.warning(request, 'No tienes un perfil de productor asociado')
    
    categorias = CategoriaProducto.objects.all()
    
    # Aplicar filtros si existen
    ubicacion = request.GET.get('ubicacion', '')
    categoria_id = request.GET.get('categoriaId', 0)
    
    if ubicacion:
        productos = productos.filter(
            Q(id_usuario__id_usuario__ciudad__icontains=ubicacion) |
            Q(id_usuario__id_usuario__departamento__icontains=ubicacion)
        )
    
    if categoria_id and categoria_id != '0':
        productos = productos.filter(id_categoria_id=categoria_id)
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'ubicacion': ubicacion,
        'categoria_id': int(categoria_id) if categoria_id else 0,
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
        
        # Guardar imagen - Versión simplificada
        if 'imagenes' in request.FILES:
            imagen_file = request.FILES['imagenes']
            print(f"Guardando imagen: {imagen_file.name}, tamaño: {imagen_file.size}")
            
            # Siempre guardar como principal si es la primera/única
            ImagenesProducto.objects.create(
                id_producto=producto,
                url_imagen=imagen_file,
                es_principal=1
            )
            print("Imagen guardada exitosamente")
        else:
            print("No hay archivo de imagen en request.FILES")
        
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
    return render(request, 'ver_producto.html', context)


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
