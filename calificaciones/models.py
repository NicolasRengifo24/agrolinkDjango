
from django.db import models
from productos.models import Producto
from django.contrib.auth.models import User

# app calificaciones
class Calificacion(models.Model):

    id_calificacion = models.AutoField(primary_key=True)

    # RELACIÓN CLAVE
    id_compra = models.ForeignKey('pedidos.Compra', on_delete=models.CASCADE, null = True, blank=True) 

    # calificaciones
    puntaje_producto = models.IntegerField(null=True, blank=True)
    puntaje_productor = models.IntegerField(null=True, blank=True)
    puntaje_transportista = models.IntegerField(null=True, blank=True)

    comentario = models.TextField(blank=True, null=True)

    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_calificacion'