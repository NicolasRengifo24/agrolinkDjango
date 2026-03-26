from django.db import models



# Create your models here.


class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    id_transportista = models.ForeignKey('usuarios.Transportista', models.DO_NOTHING, db_column='id_transportista')
    tipo_vehiculo = models.CharField(max_length=50, blank=True, null=True)
    capacidad_carga = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    documento_propiedad = models.CharField(max_length=250, blank=True, null=True)
    placa_vehiculo = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_vehiculos'



class Envio(models.Model):
    id_envio = models.AutoField(primary_key=True)
    id_compra = models.ForeignKey('pedidos.Compra', models.DO_NOTHING, db_column='id_compra', blank=True, null=True)
    id_vehiculo = models.ForeignKey('Vehiculo', models.DO_NOTHING, db_column='id_vehiculo', blank=True, null=True)
    id_transportista = models.ForeignKey('usuarios.Transportista', models.DO_NOTHING, db_column='id_transportista', blank=True, null=True)
    estado_envio = models.CharField(max_length=50, blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)
    fecha_entrega = models.DateField(blank=True, null=True)
    numero_seguimiento = models.CharField(max_length=50, blank=True, null=True)
    direccion_origen = models.CharField(max_length=300, blank=True, null=True)
    direccion_destino = models.CharField(max_length=300, blank=True, null=True)
    latitud_origen = models.FloatField(blank=True, null=True)
    longitud_origen = models.FloatField(blank=True, null=True)
    latitud_destino = models.FloatField(blank=True, null=True)
    longitud_destino = models.FloatField(blank=True, null=True)
    distancia_km = models.FloatField(blank=True, null=True)
    peso_total_kg = models.FloatField(blank=True, null=True)
    costo_base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    costo_peso = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tarifa_por_km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tarifa_por_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_envios'



