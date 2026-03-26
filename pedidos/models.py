from django.db import models
from usuarios.models import Cliente
# Create your models here.

class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey('usuarios.Cliente', models.DO_NOTHING, db_column='id_cliente')
    fecha_hora_compra = models.DateTimeField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2)
    valor_envio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    direccion_entrega = models.CharField(max_length=200, blank=True, null=True)
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_compras'


class DetallesCompra(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_compra = models.ForeignKey(Compra, models.DO_NOTHING, db_column='id_compra')
    id_producto = models.ForeignKey('productos.Producto', models.DO_NOTHING, db_column='id_producto')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_detalles_compra'