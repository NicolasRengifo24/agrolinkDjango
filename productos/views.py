from django.shortcuts import render, redirect
from .models import Producto, ProductoFinca,CategoriaProducto
from pedidos.models import DetallesCompra, Compra
from usuarios.models import Usuario
from django.db.models import Sum


def inicio(request):
    total_usuarios = Usuario.objects.count()
    categorias = CategoriaProducto.objects.all()

    productos = Producto.objects.prefetch_related('imagenProducto')
    categoria = request.GET.get('categoria')
    if categoria:
        productos = productos.filter(id_categoria=categoria)

    productos_finca = ProductoFinca.objects.select_related(
        'id_finca', 'id_producto', 'id_finca__id_usuario'
    )

    producto_destacado = None
    finca_destacado = None
    total_productos = Producto.objects.count()

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

def mostrar_productos(request):
    productos = Producto.objects.all()
    return render(request, "productos/inicio.html", {"productos": productos})


def detalle_producto(request, id):
    producto = Producto.objects.prefetch_related('imagenProducto').filter(
        id_producto=id
    ).first()
    
    relacionados = []
    if producto and producto.id_categoria:
        relacionados = Producto.objects.prefetch_related('imagenProducto').filter(
            id_categoria=producto.id_categoria
        ).exclude(id_producto=producto.id_producto)[:4]  # limitar a 4 productos

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
    # 🧪 DEBUG (temporal)
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

    # 🔒 VALIDAR LOGIN
    if not request.user.is_authenticated:
        messages.warning(request, "Debe iniciar sesión como cliente")
        return redirect('login_view')

    # 🔒 VALIDAR QUE SEA CLIENTE
    try:
        usuario = request.user.usuario
        cliente = usuario.cliente
    except:
        messages.error(request, "Debe iniciar sesión como cliente")
        return redirect('login_view')
    

    # 📦 PRODUCTO
    producto = get_object_or_404(Producto, id_producto=producto_id)

    # 🔢 CANTIDAD
    cantidad = int(request.POST.get('cantidad', 1))

    # 🛒 CARRITO (Compra en estado carrito)
    compra, created = Compra.objects.get_or_create(
        id_cliente=cliente,
        estado="carrito",
        defaults={
            "subtotal": 0,
            "impuestos": 0,
            "total": 0
        }
    )

    # 📦 DETALLE
    detalle, created = DetallesCompra.objects.get_or_create(
        id_compra=compra,
        id_producto=producto,
        defaults={
            "cantidad": cantidad,
            "precio_unitario": producto.precio,
            "subtotal": producto.precio * cantidad
        }
    )

    # ➕ SI YA EXISTE → SUMA
    if not created:
        detalle.cantidad += cantidad
        detalle.precio_unitario = producto.precio
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario
        detalle.save()

    # 🔄 ACTUALIZAR TOTALES
    detalles = DetallesCompra.objects.filter(id_compra=compra)
    subtotal = sum(d.subtotal for d in detalles)
    impuestos = subtotal * Decimal('0.19')
    total = subtotal + impuestos

    compra.subtotal = subtotal
    compra.impuestos = impuestos
    compra.total = total
    compra.save()

    # ✅ MENSAJE
    messages.success(request, "Producto agregado al carrito")

    return redirect('carrito')



