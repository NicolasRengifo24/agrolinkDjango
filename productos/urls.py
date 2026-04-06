
from django.urls import path
from . import views




urlpatterns = [
    path('', views.inicio, name='inicio'),
    path("productos/", views.mostrar_productos, name="mostrar_productos"),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_carrito'),
    
    # fincas 
    path('fincas/', views.lista_fincas, name='lista_fincas'),
    path('fincas/crear/', views.crear_finca, name='crear_finca'),
    path('fincas/editar/<int:finca_id>/', views.editar_finca, name='editar_finca'),
] 



