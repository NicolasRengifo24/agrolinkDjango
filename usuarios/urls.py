from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    # Login y registro
    path('login/', views.login_view, name='login_view'),
    path('', views.inicio_usuarios, name='inicio_usuarios'),
    
    path('logout/', views.logout_view, name='logout_view'),
    
    # Google OAuth2
    path('google/completar-registro/', views.completar_registro_google, name='completar_registro_google'),
    path('google/guardar-registro/',   views.guardar_registro_google,   name='guardar_registro_google'),

    
    path('registro/', views.mostrar_registro_usuarios, name='mostrar_registro_usuarios'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    
    path('reset-password/', views.solicitar_codigo_recuperacion, name='solicitar_codigo_recuperacion'),
    path('verificar-codigo/', views.verificar_codigo_recuperacion, name='verificar_codigo_recuperacion'),
    path('nueva-contrasena/', views.establecer_nueva_contrasena, name='establecer_nueva_contrasena'),

    # Admin
    path('index_admin/', views.dashboard_admin, name='usuarios_admin'),
    path('usuario/', views.list_usuarios_admin, name='lista_usuarios_admin'),
    path('usuarios/', views.ver_listas_usuarios_admin, name='ver_listas_usuarios_admin'),
    path('productos_admin/', views.ver_lista_productos_admin, name='ver_lista_productos_admin'),
    
    path('envios_admin/', views.ver_lista_envio_admin, name='ver_lista_envios_admin'),
    
    
    path('crear_usuario/', views.crear_usuario_admin, name='crear_usuario'),
    path('editar_usuario/<int:id>/', views.editar_usuario_admin, name='editar_usuario'),
    path('eliminar_usuario/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('ver_usuario/<int:id>/', views.ver_usuario, name='ver_usuario'),
    
    path('productos_admin/',views.ver_lista_productos_admin, name= 'ver_lista_productos_admin'),
    path('formulario_producto_admin/', views.crear_producto_admin, name= 'crear_producto_admin'),
    path('productos_admin/<int:id>/editar/', views.editar_producto_admin, name='editar_producto_admin'),
    path('producto/<int:id>/eliminar/', views.eliminar_Producto_admin, name= 'eliminar_producto_admin'),
    
    path('pedidos_admin/', views.ver_lista_pedidos_admin, name='ver_lista_pedidos_admin'),
    path('compra/<int:id>/', views.ver_detalle_compra_admin, name= 'ver_detalle_compra'),
    path('envio/<int:id>/', views.obtener_envio, name='obtener_envio'),
    
    path('servicios_admin/', views.ver_lista_servicios_admin, name='ver_lista_servicios_admin'),
    path('servicio/<int:id>/', views.ver_servicio_detalle, name='ver_servicio'),
    path('servicios/cambiar_estado/<int:servicio_id>/', views.cambiar_estado_servicio, name='cambiar_estado_servicio'),
    path('servicios/eliminar/<int:servicio_id>/', views.eliminar_servicio_admin, name='eliminar_servicio_admin'),
    path('logout/', views.cerrar_sesion, name='logout'),

    # Reportes PDF
    path('reporte/inventario/', views.reporte_inventario_admin_pdf, name='reporte_inventario_admin_pdf'),
    path('reporte/pedidos/', views.reporte_pedidos_admin_pdf, name='reporte_pedidos_admin_pdf'),
    path('reporte/envios/', views.reporte_envios_admin_pdf, name='reporte_envios_admin_pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)