from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.carrito, name= 'carrito'),
    
    path('ajax/actualizar/', views.ajax_actualizar_detalle, name='ajax_actualizar'),
    path('ajax/eliminar/', views.ajax_eliminar_detalle, name='ajax_eliminar'),
]
