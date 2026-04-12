
from django.urls import path
from . import views
from .views import lista_productos




urlpatterns = [
    # cliente
    path('', views.inicio, name='inicio_cliente'),
    
    path("productos/", views.mostrar_productos, name="mostrar_productos"),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('', lista_productos, name='lista_productos'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_carrito'),
    
    # fincas 
    path('fincas/', views.lista_fincas, name='lista_fincas'),
    path('fincas/crear/', views.crear_finca, name='crear_finca'),
    path('fincas/editar/<int:finca_id>/', views.editar_finca, name='editar_finca'),
    
    #productos - productor
    path('productor/productos/', views.lista_productos, name='lista_productos'),
    path('productor/productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productor/productos/buscar/', views.buscar_productos, name='buscar_productos'),
    path('productor/productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    
    
    path('productos/<int:producto_id>/detalles/', views.ver_producto_detalles, name='ver_producto_detalles'),
    path('productos/<int:producto_id>/editar-form/', views.editar_producto_form, name='editar_producto_form'),
    path('productos/<int:producto_id>/actualizar/', views.actualizar_producto, name='actualizar_producto'),
    path('productor/mis-ventas/', views.mis_ventas, name='mis_ventas'),
    path('ventas/detalle/<int:producto_id>/', views.detalle_ventas_producto),
    
    # reporte 
    path('productor/reporte/pdf/', views.reporte_ventas_pdf, name='reporte_pdf'),
    
    
    
] 



