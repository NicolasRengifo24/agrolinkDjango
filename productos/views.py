<<<<<<< HEAD
from django.shortcuts import render
from .models import Producto, ProductoFinca, CategoriaProducto
from pedidos.models import DetallesCompra
=======
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto, ProductoFinca, CategoriaProducto, Finca
from pedidos.models import DetallesCompra, Compra
>>>>>>> upstream/main
from usuarios.models import Usuario
from django.db.models import Sum, Avg, Count
from calificaciones.models import Calificacion



def inicio(request):
<<<<<<< HEAD

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
=======
    total_usuarios = Usuario.objects.count()
    categorias = CategoriaProducto.objects.all()

    productos = Producto.objects.prefetch_related('imagenProducto')
    categoria = request.GET.get('categoria')
>>>>>>> upstream/main
    if categoria:
        productos = productos.filter(id_categoria=categoria)

    # 🌱 productos por finca (LO TUYO ORIGINAL)
    productos_finca = ProductoFinca.objects.select_related(
        'id_finca', 'id_producto', 'id_finca__id_usuario'
    )

<<<<<<< HEAD
    # ⭐ destacado
=======
>>>>>>> upstream/main
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

<<<<<<< HEAD

# 🔁 tu función original (la dejamos por si la usas en rutas)
=======
>>>>>>> upstream/main
def mostrar_productos(request):
    productos = Producto.objects.prefetch_related('imagenProducto').annotate(
        promedio_estrellas=Avg('calificaciones__puntaje'),
        total_calificaciones=Count('calificaciones')
    )
    return render(request, "productos/inicio.html", {"productos": productos})


# 📄 DETALLE DE PRODUCTO (CON COMENTARIOS)
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
        ).exclude(id_producto=producto.id_producto)[:4]  # limitar a 4 productos

<<<<<<< HEAD
    # 💬 últimos 3 comentarios
    comentarios = Calificacion.objects.filter(
        producto=producto
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
=======
    categorias = CategoriaProducto.objects.all()
    
    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'relacionados' : relacionados,
        'categorias' : categorias,
        
    })



from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from pedidos.models import Compra, DetallesCompra
from productos.models import Producto
from decimal import Decimal

def agregar_al_carrito(request, producto_id):
    #  DEBUG (temporal)
    print("AUTH:", request.user.is_authenticated)
    print("USER:", request.user)

    try:
        usuario = request.user.usuario
        print("USUARIO OK:", usuario)
    except Exception as e:
        print("ERROR USUARIO:", e)

    try:
        cliente = request.user.usuario.cliente
        print("CLIENTE OK:", cliente)
    except Exception as e:
        print("ERROR CLIENTE:", e)

    #  VALIDAR LOGIN
    if not request.user.is_authenticated:
        messages.warning(request, "Debe iniciar sesión como cliente")
        return redirect('login_view')

    #  VALIDAR QUE SEA CLIENTE
    try:
        usuario = request.user.usuario
        cliente = usuario.cliente
    except:
        messages.error(request, "Debe iniciar sesión como cliente")
        return redirect('login_view')
    

    #  PRODUCTO
    producto = get_object_or_404(Producto, id_producto=producto_id)

    #  CANTIDAD
    cantidad = int(request.POST.get('cantidad', 1))

    #  CARRITO (Compra en estado carrito)
    compra, created = Compra.objects.get_or_create(
        id_cliente=cliente,
        estado="carrito",
        defaults={
            "subtotal": 0,
            "impuestos": 0,
            "total": 0
        }
    )

    #  DETALLE
    detalle, created = DetallesCompra.objects.get_or_create(
        id_compra=compra,
        id_producto=producto,
        defaults={
            "cantidad": cantidad,
            "precio_unitario": producto.precio,
            "subtotal": producto.precio * cantidad
        }
    )

    #  SI YA EXISTE → SUMA
    if not created:
        detalle.cantidad += cantidad
        detalle.precio_unitario = producto.precio
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario
        detalle.save()

    #  ACTUALIZAR TOTALES
    detalles = DetallesCompra.objects.filter(id_compra=compra)
    subtotal = sum(d.subtotal for d in detalles)
    impuestos = subtotal * Decimal('0.19')
    total = subtotal + impuestos

    compra.subtotal = subtotal
    compra.impuestos = impuestos
    compra.total = total
    compra.save()

    #  MENSAJE
    messages.success(request, "Producto agregado al carrito")

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


#@login_required
def editar_finca(request, finca_id):
    """Vista para editar una finca existente"""
    
    finca = get_object_or_404(Finca, id_finca=finca_id)
    
    # Verificar que el usuario sea el dueño de la finca
    if finca.id_usuario.id_usuario.id != request.user.usuario.id:
        messages.error(request, 'No tienes permiso para editar esta finca')
        return redirect('lista_fincas')
    
    if request.method == 'POST':
        # Actualizar datos
        finca.nombre_finca = request.POST.get('nombre_finca')
        finca.direccion_finca = request.POST.get('direccion_finca')
        finca.ciudad = request.POST.get('ciudad')
        finca.departamento = request.POST.get('departamento')
        
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')
        
        if latitud and longitud:
            finca.latitud = float(latitud)
            finca.longitud = float(longitud)
        
        finca.save()
        
        messages.success(request, 'Finca actualizada exitosamente')
        return redirect('lista_fincas')
    
    return render(request, 'finca/formulario_finca.html', {'finca': finca})


#@login_required
def lista_fincas(request):
    """Lista de fincas del productor"""
    
    fincas = Finca.objects.filter(id_usuario=request.user.usuario.productor)
    
    return render(request, 'finca/lista_fincas.html', {'fincas': fincas})
>>>>>>> upstream/main
