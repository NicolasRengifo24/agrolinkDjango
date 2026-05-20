from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import json

from usuarios.models import Usuario, Transportista, Productor
from envios.models import Vehiculo
from envios.models import Envio
from pedidos.models import Compra, DetallesCompra
from productos.models import (
    Producto,
    CategoriaProducto,
    ProductoFinca
)
from productos.models import Finca


class InicioTransportistaTest(TestCase):

    def setUp(self):

        self.client = Client()

        # =========================
        # USER DJANGO
        # =========================
        self.auth_user = User.objects.create_user(
            username='transportista',
            password='123456'
        )

        # =========================
        # USUARIO TRANSPORTISTA
        # =========================
        self.usuario_transportista = Usuario.objects.create(
            nombre='Nicolas',
            nombre_usuario='nico2026',
            apellido='Garzon',
            correo='nico@test.com',
            ciudad='Chia',
            departamento='Cundinamarca',
            direccion='calle 1',
            cedula='123456789',
            telefono='3001234567',
            rol='TRANSPORTISTA',
            estado=True,
            user=self.auth_user
        )

        self.transportista = Transportista.objects.create(
            id_usuario=self.usuario_transportista,
            zonas_entrega='Bogotá'
        )

        # =========================
        # VEHICULO
        # =========================
        self.vehiculo = Vehiculo.objects.create(
            tipo_vehiculo='Camioneta',
            capacidad_carga=1000,
            placa_vehiculo='ABC123',
            id_transportista=self.transportista,
            estado='ACTIVO'
        )

        # =========================
        # PRODUCTOR
        # =========================
        self.productor_user = Usuario.objects.create(
            nombre='Jose',
            nombre_usuario='jose7',
            apellido='Muñoz',
            correo='jose@test.com',
            ciudad='Chia',
            departamento='Cundinamarca',
            direccion='vereda',
            cedula='999999',
            telefono='3111111111',
            rol='PRODUCTOR',
            estado=True
        )

        self.productor = Productor.objects.create(
            id_usuario=self.productor_user,
            tipo_cultivo='Verduras'
        )

        # =========================
        # CATEGORIA
        # =========================
        self.categoria = CategoriaProducto.objects.create(
            nombre_categoria='Verduras'
        )

        # =========================
        # PRODUCTO
        # =========================
        self.producto = Producto.objects.create(
            nombre_producto='Brócoli',
            descripcion_producto='Producto fresco',
            precio=5000,
            stock=20,
            peso_kg=5,
            id_categoria=self.categoria,
            id_usuario=self.productor
        )

        # =========================
        # FINCA
        # =========================
        self.finca = Finca.objects.create(
            nombre_finca='Finca Los Robles',
            direccion_finca='Vereda Chia',
            latitud=4.8760,
            longitud=-74.0748,
            ciudad='Chia',
            departamento='Cundinamarca',
            id_usuario=self.productor
        )

        # =========================
        # RELACION PRODUCTO-FINCA
        # =========================
        ProductoFinca.objects.create(
            id_producto=self.producto,
            id_finca=self.finca,
            cantidad_produccion=50
        )

        # =========================
        # CLIENTE
        # =========================
        self.cliente_user = Usuario.objects.create(
            nombre='Juan',
            nombre_usuario='juan123',
            apellido='Perez',
            correo='juan@test.com',
            ciudad='Bogotá',
            departamento='Cundinamarca',
            direccion='calle 10',
            cedula='888888',
            telefono='300000000',
            rol='CLIENTE',
            estado=True
        )

        from usuarios.models import Cliente

        self.cliente = Cliente.objects.create(
            id_usuario=self.cliente_user
        )

        # =========================
        # COMPRA
        # =========================
        self.compra = Compra.objects.create(
            subtotal=5000,
            impuestos=950,
            total=5950,
            estado='pagado',
            id_cliente=self.cliente,
            direccion_entrega='Bogotá',
            latitud_destino=4.6097,
            longitud_destino=-74.0817
        )

        # =========================
        # DETALLE COMPRA
        # =========================
        DetallesCompra.objects.create(
            id_compra=self.compra,
            id_producto=self.producto,
            cantidad=1,
            precio_unitario=5000,
            subtotal=5000
        )

        # =========================
        # ENVIO PENDIENTE
        # =========================
        self.envio = Envio.objects.create(
            estado_envio='pendiente',
            numero_seguimiento='ENV-001',
            id_compra=self.compra,
            peso_total_kg=5,
            distancia_km=20
        )

    def test_inicio_transportista(self):

        # LOGIN
        self.client.login(
            username='transportista',
            password='123456'
        )

        response = self.client.get(
            reverse('inicio_transportista')
        )

        # STATUS OK
        self.assertEqual(response.status_code, 200)

        # TEMPLATE
        self.assertTemplateUsed(
            response,
            'envios/envios_dashboard.html'
        )

        # CONTEXTO
        self.assertIn('envios', response.context)
        self.assertIn('envios_json', response.context)
        self.assertIn('vehiculos_activos', response.context)

        # VEHICULOS ACTIVOS
        vehiculos = response.context['vehiculos_activos']
        self.assertEqual(vehiculos.count(), 1)

        # JSON ENVIO
        envios_json = json.loads(
            response.context['envios_json']
        )

        self.assertEqual(len(envios_json), 1)

        envio_data = envios_json[0]

        self.assertEqual(
            envio_data['numero'],
            'ENV-001'
        )

        self.assertEqual(
            envio_data['nombre_finca'],
            'Finca Los Robles'
        )

        self.assertEqual(
            envio_data['peso'],
            5.0
        )