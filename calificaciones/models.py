from django.db import models
from productos.models import Producto
from django.contrib.auth.models import User

class Calificacion(models.Model):
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    puntaje = models.IntegerField()
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)