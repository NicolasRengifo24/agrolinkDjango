from django.urls import path
from . import views
## api 
from django.urls import path
from .views import ciudades_cundinamarca_api




urlpatterns = [
    path('transporte/', views.inicio_transportista, name='inicio_transportista'),
    path('vehiculos/',views.mostrar_vehiculos, name = 'mostrar_vehiculos'), 
    path('vehiculos/agregar/', views.agregar_vehiculo, name='agregar_vehiculo'),
    path('vehiculos/cambiar-estado/<int:vehiculo_id>/', views.cambiar_estado_vehiculo, name='cambiar_estado_vehiculo'),
    path('vehiculos/eliminar/<int:vehiculo_id>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    path('mis-envios/', views.mis_envios, name='mis_envios'),
    path('aceptar-viaje/<int:envio_id>/', views.aceptar_viaje, name='aceptar_viaje'),
    path('cambiar-estado/<int:envio_id>/<str:nuevo_estado>/', views.cambiar_estado_envio,name='cambiar_estado_envio'),
    path('subir-foto-envio/<int:envio_id>/', views.subir_foto_envio, name='subir_foto_envio'),
    ## api ##
    path("api/cundinamarca/ciudades/",ciudades_cundinamarca_api, name="ciudades_cundinamarca_api"),    
    
    path('cargar-vehiculos-csv/', views.cargar_vehiculos_csv, name='cargar_vehiculos_csv'),

     #perfil
    path('perfil-transportista/', views.perfil_transportista, name='perfil_transportista'),
    path('editar-perfil-transportista/', views.editar_perfil_transportista, name='editar_perfil_transportista'),
    path('mis-notificaciones/', views.notificaciones_transportista, name='notificaciones_transportista'),
    path('mis-notificaciones/marcar/<int:notif_id>/', views.marcar_notif_transportista, name='marcar_notif_transportista'),
    
] 

