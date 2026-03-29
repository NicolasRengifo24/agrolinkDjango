from django.urls import path
from . import views




urlpatterns = [
    path('transporte/', views.inicio, name='inicio'),
    
    
] 

