from django.db import models


# Create your models here.
class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    id_asesor = models.ForeignKey('usuarios.Asesor', models.DO_NOTHING, db_column='id_asesor')
    categoria = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_servicios'



class Maquinas(models.Model):
    id_maquina = models.AutoField(primary_key=True)
    id_asesor = models.ForeignKey('usuarios.Asesor', models.DO_NOTHING, db_column='id_asesor')
    tipo_maquina = models.CharField(max_length=50)
    documento_propiedad = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    registro_rnma = models.CharField(db_column='registro_RNMA', max_length=200, blank=True, null=True)  # Field name made lowercase.
    tarjeta_registro_maquinaria = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_maquinas'


class Certificados(models.Model):
    id_certificado = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('usuarios.Asesor', models.DO_NOTHING, db_column='id_usuario')
    tipo_certificado = models.CharField(max_length=100)
    descripcion_cert = models.CharField(max_length=255)
    fecha_expedicion = models.DateField()

    class Meta:
        managed = True
        db_table = 'tb_certificados'



