from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from productos.models import (
    Producto,
    CategoriaProducto,
    Finca,
    ProductoFinca
)

from usuarios.models import Usuario, Productor, Cliente
from pedidos.models import Compra, DetallesCompra


class ProductosViewsTest(TestCase):

    def setUp(self):

        self.client = Client()

        # =====================================
        # USER DJANGO
        # =====================================

        self.user = User.objects.create_user(
            username='productor1',
            password='123456'
        )

        # =====================================
        # USUARIO PERSONALIZADO
        # =====================================

        self.usuario = Usuario.objects.create(
            user=self.user,
            nombre='Juan',
            apellido='Perez',
            nombre_usuario='productor1',
            correo='juan@test.com',
            telefono='3000000000',
            cedula='123456789',
            ciudad='Bogota',
            direccion='Calle 1',
            rol='PRODUCTOR'
        )

        # =====================================
        # PRODUCTOR
        # =====================================

        self.productor = Productor.objects.create(
            id_usuario=self.usuario,
            tipo_cultivo='Papa'
        )

        # =====================================
        # CATEGORIA
        # =====================================

        self.categoria = CategoriaProducto.objects.create(
            nombre_categoria='Verduras'
        )

        # =====================================
        # FINCA
        # =====================================

        self.finca = Finca.objects.create(
            id_usuario=self.productor,
            nombre_finca='Finca Test',
            direccion_finca='Calle 1',
            ciudad='Bogota',
            departamento='Cundinamarca',
            latitud=4.5,
            longitud=-74.1
        )

        # =====================================
        # PRODUCTO
        # =====================================

        self.producto = Producto.objects.create(
            id_usuario=self.productor,
            id_categoria=self.categoria,
            nombre_producto='Papa Criolla',
            descripcion_producto='Muy buena',
            precio=5000,
            stock=20,
            peso_kg=1
        )

        # =====================================
        # RELACION PRODUCTO FINCA
        # =====================================

        ProductoFinca.objects.create(
            id_producto=self.producto,
            id_finca=self.finca,
            cantidad_produccion=100
        )

    # =====================================
    # DETALLE PRODUCTO
    # =====================================

    def test_detalle_producto(self):

        url = reverse(
            'detalle_producto',
            args=[self.producto.id_producto]
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    # =====================================
    # LISTA PRODUCTOS LOGIN
    # =====================================

    def test_lista_productos_login(self):

        self.client.login(
            username='productor1',
            password='123456'
        )

        url = reverse('lista_productos')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    # =====================================
    # LISTA PRODUCTOS SIN LOGIN
    # =====================================

    def test_lista_productos_sin_login(self):

        url = reverse('lista_productos')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    # =====================================
    # CREAR FINCA GET
    # =====================================

    def test_crear_finca_get(self):

        self.client.login(
            username='productor1',
            password='123456'
        )

        url = reverse('crear_finca')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    # =====================================
    # CREAR FINCA POST
    # =====================================

    def test_crear_finca_post(self):

        self.client.login(
            username='productor1',
            password='123456'
        )

        url = reverse('crear_finca')

        response = self.client.post(url, {
            'nombre_finca': 'Nueva Finca',
            'direccion_finca': 'Calle 2',
            'ciudad': 'Bogota',
            'departamento': 'Cundinamarca',
            'latitud': '4.60',
            'longitud': '-74.20'
        })

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Finca.objects.filter(
                nombre_finca='Nueva Finca'
            ).exists()
        )

    # =====================================
    # VER PRODUCTO DETALLES JSON
    # =====================================

    

    # =====================================
    # ACTUALIZAR PRODUCTO POST
    # =====================================

    def test_actualizar_producto(self):

        self.client.login(
            username='productor1',
            password='123456'
        )

        url = reverse(
            'actualizar_producto',
            args=[self.producto.id_producto]
        )

        response = self.client.post(url, {
            'nombre_producto': 'Papa Nueva',
            'descripcion_producto': 'Editado',
            'precio': 9000,
            'stock': 50,
            'peso_kg': 2,
            'categoria': self.categoria.id_categoria
        })

        self.assertEqual(response.status_code, 200)

        self.producto.refresh_from_db()

        self.assertEqual(
            self.producto.nombre_producto,
            'Papa Nueva'
        )

    # =====================================
    # ELIMINAR PRODUCTO
    # =====================================

    def test_eliminar_producto(self):

        self.client.login(
            username='productor1',
            password='123456'
        )

        url = reverse(
            'eliminar_producto',
            args=[self.producto.id_producto]
        )

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Producto.objects.filter(
                id_producto=self.producto.id_producto
            ).exists()
        )

    # =====================================
    # VER PRODUCTO PRODUCTOR
    # =====================================


    # =====================================
    # BUSCAR PRODUCTOS
    # =====================================

    def test_buscar_productos(self):

        url = reverse('buscar_productos')

        response = self.client.get(url, {
            'ubicacion': 'Bogota',
            'categoriaId': self.categoria.id_categoria
        })

        self.assertIn(response.status_code, [200, 302])

    # =====================================
    # EDITAR FINCA
    # =====================================

    def test_editar_finca(self):

        self.client.login(
            username='productor1',
            password='123456'
        )

        url = reverse(
            'editar_finca',
            args=[self.finca.id_finca]
        )

        response = self.client.post(url, {
            'nombre_finca': 'Finca Editada',
            'direccion_finca': 'Nueva direccion',
            'ciudad': 'Medellin',
            'departamento': 'Antioquia',
            'latitud': '6.2',
            'longitud': '-75.5'
        })

        self.assertEqual(response.status_code, 302)

        self.finca.refresh_from_db()

        self.assertEqual(
            self.finca.nombre_finca,
            'Finca Editada'
        )
