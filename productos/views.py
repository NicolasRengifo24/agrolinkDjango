from django.shortcuts import render
from .models import Producto, ProductoFinca,CategoriaProducto
from pedidos.models import DetallesCompra
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
