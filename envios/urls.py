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
    ## api ##
    path("api/cundinamarca/ciudades/",ciudades_cundinamarca_api, name="ciudades_cundinamarca_api"),    
    
    path('cargar-vehiculos-csv/', views.cargar_vehiculos_csv, name='cargar_vehiculos_csv'),
    
] 

