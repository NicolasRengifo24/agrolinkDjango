from django.urls import path
from . import views




urlpatterns = [
    path('transporte/', views.inicio, name='inicio'),
    path('vehiculos',views.mostrar_vehiculos, name = 'mostrar_vehiculos'), 
    
] 

