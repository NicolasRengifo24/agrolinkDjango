from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.carrito_compra, name= 'carrito_compra'),
]
