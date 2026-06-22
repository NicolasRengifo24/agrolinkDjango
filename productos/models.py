from django.db import models

# Create your models here.

class CategoriaProducto(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'tb_categorias_productos'

    def __str__(self):
        return f"{self.nombre_categoria}"




class Finca(models.Model):
    id_finca = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('usuarios.Productor', models.DO_NOTHING, db_column='id_usuario')
    nombre_finca = models.CharField(max_length=100, blank=True, null=True)
    direccion_finca = models.CharField(max_length=200, blank=True, null=True)
    certificado_bpa = models.CharField(db_column='certificado_BPA', max_length=200, blank=True, null=True)  # Field name made lowercase.
    certificado_mirfe = models.CharField(db_column='certificado_MIRFE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    certificado_mipe = models.CharField(db_column='certificado_MIPE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    registro_ica = models.CharField(db_column='registro_ICA', max_length=200, blank=True, null=True)  # Field name made lowercase.
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_fincas'
    
    def __str__(self):
        return self.nombre_finca

class TipoProducto(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    id_categoria = models.ForeignKey(CategoriaProducto, models.DO_NOTHING, db_column='id_categoria')
    descripcion_general = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_tipos_producto'

    def __str__(self):
        return self.nombre


class VariedadProducto(models.Model):
    id_variedad = models.AutoField(primary_key=True)
    id_tipo = models.ForeignKey(TipoProducto, models.CASCADE, db_column='id_tipo', related_name='variedades')
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'tb_variedades_producto'
        unique_together = ('id_tipo', 'nombre')

    def __str__(self):
        return f"{self.id_tipo.nombre} - {self.nombre}"


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('usuarios.Productor', models.DO_NOTHING, db_column='id_usuario')
    id_categoria = models.ForeignKey(CategoriaProducto, models.DO_NOTHING, db_column='id_categoria')
    id_tipo = models.ForeignKey(TipoProducto, models.DO_NOTHING, db_column='id_tipo', blank=True, null=True)
    id_variedad = models.ForeignKey(VariedadProducto, models.DO_NOTHING, db_column='id_variedad', blank=True, null=True)
    precio = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)
    nombre_producto = models.CharField(max_length=100)
    descripcion_producto = models.CharField(max_length=255, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.BooleanField(default=True)


    class Meta:
        managed = True
        db_table = 'tb_productos'

    def finca(self):
        pf = self.fincas.select_related('id_finca').first()
        return pf.id_finca if pf else None

    def __str__(self):
        return self.nombre_producto
    
    def imagen_principal_url(self):
        img = self.imagenProducto.filter(es_principal=1).first()
        return img.url_imagen.url if img else None




class ImagenesProducto(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, models.CASCADE, db_column='id_producto',related_name='imagenProducto')
    url_imagen = models.ImageField(upload_to='productos/')
    es_principal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_imagenes_productos'




class ProductoFinca(models.Model):
    id_producto_finca = models.AutoField(primary_key=True)
    id_finca = models.ForeignKey(Finca, models.CASCADE, db_column='id_finca',related_name='productos_finca' )
    id_producto = models.ForeignKey(Producto, models.CASCADE, db_column='id_producto',related_name='fincas'  )
    cantidad_produccion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_cosecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_productos_fincas'

    def __str__(self):
        return f"{self.id_finca.nombre_finca}"