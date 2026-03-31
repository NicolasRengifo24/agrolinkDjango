from django.shortcuts import render
from .models import Producto, ProductoFinca, CategoriaProducto
from pedidos.models import DetallesCompra
from usuarios.models import Usuario
from django.db.models import Sum, Avg, Count
from calificaciones.models import Calificacion


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


# 📄 DETALLE DE PRODUCTO (CON COMENTARIOS)
def detalle_producto(request, id):
    producto = Producto.objects.prefetch_related('imagenProducto').filter(
        id_producto=id
    ).annotate(
        promedio_estrellas=Avg('calificaciones__puntaje'),
        total_calificaciones=Count('calificaciones')
    ).first()

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