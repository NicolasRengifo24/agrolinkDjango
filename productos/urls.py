
from django.urls import path
from . import views




urlpatterns = [
    path('', views.inicio, name='inicio'),
    path("productos/", views.mostrar_productos, name="mostrar_productos"),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
] 



