from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # Login y registro
    path('login/', views.login_view, name='login_view'),
    path('', views.inicio_usuarios, name='inicio_usuarios'),
    
    path('logout/', views.logout_view, name='logout_view'),

    
    path('registro/', views.mostrar_registro_usuarios, name='mostrar_registro_usuarios'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    
    path('reset-password/', views.reset_password, name='reset_password'),

    # Admin
    path('index_admin/', views.dashboard_admin, name='usuarios_admin'),
    path('usuario/', views.list_usuarios_admin, name='lista_usuarios_admin'),
    path('usuarios/', views.ver_listas_usuarios_admin, name='ver_listas_usuarios_admin'),
    path('productos_admin/', views.ver_lista_productos_admin, name='ver_lista_productos_admin'),
    path('pedidos_admin/', views.ver_lista_pedidos_admin, name='ver_lista_pedidos_admin'),
    path('envios_admin/', views.ver_lista_envio_admin, name='ver_lista_envios_admin'),
    path('servicios_admin/', views.ver_lista_servicios_admin, name='ver_lista_servicios_admin'),
    path('crear_usuario/', views.crear_usuario_admin, name='crear_usuario'),
    
    path('editar_usuario/<int:id>/', views.editar_usuario_admin, name='editar_usuario'),
    path('eliminar_usuario/<int:id>', views.eliminar_usuario, name='eliminar_usuario'),
    path('ver_usuario/<int:id>/', views.ver_usuario, name='ver_usuario'),
    
    path('productos_admin/',views.ver_lista_productos_admin, name= 'ver_lista_productos_admin'),
    path('formulario_producto_admin', views.crear_producto_admin, name= 'crear_producto_admin')
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)