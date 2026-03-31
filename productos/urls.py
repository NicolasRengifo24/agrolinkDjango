
from django.urls import path
from . import views
from .views import lista_productos




urlpatterns = [
    path('', views.inicio, name='inicio'),
    path("productos/", views.mostrar_productos, name="mostrar_productos"),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('', lista_productos, name='lista_productos'),
] 



