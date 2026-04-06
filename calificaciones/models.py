from django.db import models
from productos.models import Producto
from django.contrib.auth.models import User

class Calificacion(models.Model):
<<<<<<< HEAD
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE, related_name='calificaciones')
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    puntaje = models.IntegerField()
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
=======
    id_calificacion = models.AutoField(primary_key=True)
    puntaje = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    promedio = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_calificacion'
>>>>>>> upstream/main
