from django.test import TestCase ,Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from decimal import Decimal
from productos.models import Producto,  CategoriaProducto
from usuarios.models import Usuario, Cliente , Productor 
from pedidos.models import Compra, DetallesCompra



class CarritoTest(TestCase):

    def setUp(self):
        self.client = Client()

        # USER
        self.user = User.objects.create_user(
            username='test',
            password='1234'
        )

        # USUARIO
        self.usuario = Usuario.objects.create(
            user=self.user,
            rol='CLIENTE'
        )

        # CLIENTE
        self.cliente = Cliente.objects.create(
            id_usuario=self.usuario
        )

        #
        self.productor = Productor.objects.create(
            id_usuario=self.usuario   
        )

        # CATEGORIA 
        self.categoria = CategoriaProducto.objects.create(
            nombre_categoria='Tuberculos'
        )

        # PRODUCTO 
        self.producto = Producto.objects.create(
            nombre_producto='Papa',
            precio=1000,
            id_usuario=self.productor,
            id_categoria=self.categoria
        )
        
                
    def test_usuario_no_logueado(self):
        response = self.client.post('/agregar/1/', {'cantidad': 2})

        self.assertEqual(response.status_code, 302)
        
            
    def test_agregar_producto(self):
        self.client.login(username='test', password='1234')

        url = reverse('agregar_carrito', args=[self.producto.id_producto])

        response = self.client.post(url, {'cantidad': -2})

        self.assertEqual(response.status_code, 302)

        compra = Compra.objects.get(id_cliente=self.cliente)
        detalle = DetallesCompra.objects.get(id_compra=compra)

        self.assertEqual(detalle.cantidad, 2)
        self.assertEqual(detalle.subtotal, 2000)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("agregado al carrito" in str(m) for m in messages))
        
        
        
    def test_sumar_producto_existente(self):
        self.client.login(username='test', password='1234')

        url = reverse('agregar_carrito', args=[self.producto.id_producto])

        # Primera vez
        self.client.post(url, {'cantidad': 2})

        # Segunda vez
        self.client.post(url, {'cantidad': 3})

        compra = Compra.objects.get(id_cliente=self.cliente)
        detalle = DetallesCompra.objects.get(id_compra=compra)

        self.assertEqual(detalle.cantidad, 5)
        
    def test_calculo_totales(self):
        self.client.login(username='test', password='1234')

        url = reverse('agregar_carrito', args=[self.producto.id_producto])

        self.client.post(url, {'cantidad': 2})

        compra = Compra.objects.get(id_cliente=self.cliente)

        self.assertEqual(compra.subtotal, 2000)
        self.assertEqual(compra.impuestos, Decimal('380.00'))
        self.assertEqual(compra.total, Decimal('2380.00'))
        
        
        
    def test_usuario_no_cliente(self):
        self.usuario.rol = 'ADMIN'
        self.usuario.save()

        self.client.login(username='test', password='1234')

        response = self.client.post(
            reverse('agregar_carrito', args=[self.producto.id_producto])
        )

        self.assertEqual(response.status_code, 302)
        
        
        
    def test_usuario_sin_cliente(self):
        self.cliente.delete()

        self.client.login(username='test', password='1234')

        response = self.client.post(
            reverse('agregar_carrito', args=[self.producto.id_producto])
        )

        self.assertEqual(response.status_code, 302)
        
        
    def test_cantidad_invalida(self):
        self.client.login(username='test', password='1234')

        response = self.client.post(
            reverse('agregar_carrito', args=[self.producto.id_producto]),
            {'cantidad': 'abc'}
        )

        self.assertEqual(response.status_code, 302)   
        
        
   