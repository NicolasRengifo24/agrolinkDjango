# calificaciones/models.py

from django.db import models
from productos.models import Producto
from django.contrib.auth.models import User

class Calificacion(models.Model):
    id_calificacion = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE, 
        db_column='id_producto',
        related_name='calificaciones'
    )
    id_usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column='id_usuario'
    )
    puntaje = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    promedio = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'tb_calificacion'

    def __str__(self):
        return f"Calificación {self.id_calificacion}"