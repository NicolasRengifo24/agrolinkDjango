from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    nombre_usuario = models.CharField(unique=True, max_length=100)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(unique=True, max_length=100)
    ciudad = models.CharField(max_length=50)
    departamento = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    cedula = models.CharField(unique=True, max_length=20)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    estado = models.BooleanField(default=True)
    rol = models.CharField(max_length=50)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)

    class Meta:
        managed = True  
        db_table = 'tb_usuarios'

    def __str__(self):
        return f"{self.nombre} ({self.rol})"



class Transportista(models.Model):
    id_usuario = models.OneToOneField(Usuario, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    
    zonas_entrega = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_transportistas'



class Productor(models.Model):
    id_usuario = models.OneToOneField(Usuario, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    
    tipo_cultivo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_productores'

    def __str__(self):
        return f"{self.id_usuario.nombre} - {self.tipo_cultivo}"


class Cliente(models.Model):
    id_usuario = models.OneToOneField(Usuario, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    
    preferencias = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_clientes'


class Asesor(models.Model):
    id_usuario = models.OneToOneField(Usuario, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    
    tipo_asesoria = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tb_asesores'



class Administrador(models.Model):
    id_usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        primary_key=True
    )

    class Meta:
        managed = True
        db_table = 'tb_administradores'


class Notificacion(models.Model):
    TIPOS = [
        ('SOLICITUD_VEHICULO', 'Solicitud de vehículo'),
        ('APROBACION_VEHICULO', 'Vehículo aprobado'),
        ('RECHAZO_VEHICULO', 'Vehículo rechazado'),
    ]

    id_notificacion = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50, choices=TIPOS)
    mensaje = models.TextField()
    destino = models.ForeignKey(
        Usuario, models.CASCADE,
        db_column='destino',
        related_name='notificaciones'
    )
    id_vehiculo = models.ForeignKey(
        'envios.Vehiculo', models.SET_NULL,
        db_column='id_vehiculo',
        null=True, blank=True
    )
    leido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'tb_notificaciones'

    def __str__(self):
        return f"[{self.tipo}] {self.mensaje[:60]}"