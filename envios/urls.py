from django.urls import path
from . import views




urlpatterns = [
    path('transporte/', views.inicio_transportista, name='inicio_transportista'),
    
    
] 

