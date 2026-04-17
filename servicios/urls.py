from django.urls import path
from . import views

urlpatterns = [
    # 🔹 ASESOR
    path('asesor/', views.asesor_servicios, name='asesor_servicios'),
    path('maquinas/', views.maquinas_asesor, name='maquinas_asesor'),
    path('servicio/<int:id>/', views.detalles_servicios, name='detalle_servicio'),
    
    path('servicios/', views.lista_servicios, name='lista_servicios'),  # 🔥 ESTA ES LA CLAVE
    #perfil asesor
    path('asesor/perfil/', views.perfil_asesor, name='perfil_asesor'),
    path('asesor/editar/', views.editar_perfil_asesor, name='editar_perfil_asesor'),

]