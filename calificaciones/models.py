from django.db import models

# Create your models here.
class Calificacion(models.Model):
    id_calificacion = models.AutoField(primary_key=True)
    puntaje = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    promedio = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_calificacion'