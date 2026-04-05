from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.carrito, name= 'carrito'),
    
    path('carrito/actualizar/<int:detalle_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:detalle_id>/', views.eliminar_del_carrito, name='eliminar_carrito'),
    # pedidos/urls.py
    path('respuesta-pago/', views.respuesta_pago, name='respuesta_pago'),
    path('confirmacion-pago/', views.confirmacion_pago, name='confirmacion_pago'),
    
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),

    
]
