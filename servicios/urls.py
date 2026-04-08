from django.urls import path
from . import views

urlpatterns = [
    # 🔹 ASESOR
    path('asesor/', views.asesor_servicios, name='asesor_servicios'),
    path('maquinas/', views.maquinas_asesor, name='maquinas_asesor'),

    # 🔹 CLIENTE
    path('servicios/', views.servicios_cliente, name='servicios_cliente'),
]