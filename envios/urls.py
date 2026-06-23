from django.urls import path
from . import views
from .views import ciudades_cundinamarca_api




urlpatterns = [
    path('transporte/', views.inicio_transportista, name='inicio_transportista'),
    path('vehiculos/',views.mostrar_vehiculos, name = 'mostrar_vehiculos'), 
    path('vehiculos/agregar/', views.agregar_vehiculo, name='agregar_vehiculo'),
    path('vehiculos/cambiar-estado/<int:vehiculo_id>/', views.cambiar_estado_vehiculo, name='cambiar_estado_vehiculo'),
    path('vehiculos/editar/<int:vehiculo_id>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:vehiculo_id>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    path('mis-envios/', views.mis_envios, name='mis_envios'),
    path('aceptar-viaje/<int:envio_id>/', views.aceptar_viaje, name='aceptar_viaje'),
    path('cambiar-estado/<int:envio_id>/<str:nuevo_estado>/', views.cambiar_estado_envio,name='cambiar_estado_envio'),
    path('subir-foto-envio/<int:envio_id>/', views.subir_foto_envio, name='subir_foto_envio'),
    path('verificar-fotos-pendientes/', views.verificar_fotos_pendientes, name='verificar_fotos_pendientes'),
    ## api ##
    path("api/cundinamarca/ciudades/",ciudades_cundinamarca_api, name="ciudades_cundinamarca_api"),    
    
    path('cargar-vehiculos-csv/', views.cargar_vehiculos_csv, name='cargar_vehiculos_csv'),

     #perfil
    path('perfil-transportista/', views.perfil_transportista, name='perfil_transportista'),
    path('editar-perfil-transportista/', views.editar_perfil_transportista, name='editar_perfil_transportista'),
    path('mis-notificaciones/', views.notificaciones_transportista, name='notificaciones_transportista'),
    path('mis-notificaciones/marcar/<int:notif_id>/', views.marcar_notif_transportista, name='marcar_notif_transportista'),

    # panel de control
    path('panel-control/', views.panel_control, name='panel_control_transportista'),
    path('reporte-envios-csv/', views.reporte_envios_csv, name='reporte_envios_csv'),
    path('reporte-ingresos-csv/', views.reporte_ingresos_csv, name='reporte_ingresos_csv'),
    path('reporte-envios-excel/', views.reporte_envios_excel, name='reporte_envios_excel'),
    path('reporte-ingresos-excel/', views.reporte_ingresos_excel, name='reporte_ingresos_excel'),
    path('reporte-envios-pdf/', views.reporte_envios_pdf, name='reporte_envios_pdf'),
    path('reporte-ingresos-pdf/', views.reporte_ingresos_pdf, name='reporte_ingresos_pdf'),
] 

