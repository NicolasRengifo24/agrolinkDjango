from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.carrito, name= 'carrito'),
    
    path('carrito/actualizar/<int:detalle_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:detalle_id>/', views.eliminar_del_carrito, name='eliminar_carrito'),
]
