from django.db import models
from productos.models import Producto
from usuarios.models import Usuario

class Calificacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='calificaciones')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntaje = models.IntegerField()  # 1 a 5
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.puntaje}"