from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns =[
    path('registro/', views.mostrar_registro_usuarios, name='registrar'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    # urls admin
    path('index_admin/', views.dashboard_admin, name= 'usuarios_admin'),
    path('usuario/',views.list_usuarios_admin, name= 'lista_usuarios_admin'),
    
    
    path('usuarios/', views.ver_listas_usuarios_admin, name='ver_listas_usuarios_admin'),
    path('productos_admin/',views.ver_lista_productos_admin, name= 'ver_lista_productos_admin'),
    path('pedidos_admin/', views.ver_lista_pedidos_admin, name= 'ver_lista_pedidos_admin'),
    path('envios_admin/', views.ver_lista_envio_admin, name= 'ver_lista_envios_admin'),
    path('servicios_admin/', views.ver_lista_servicios_admin, name= 'ver_lista_servicios_admin'),
    path('crear_usuario/', views.crear_usuario_admin, name= 'crear_usuario'),
    
    
]