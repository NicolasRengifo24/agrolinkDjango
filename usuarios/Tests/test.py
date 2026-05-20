from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from usuarios.models import (
    Usuario,
    Cliente,
    Productor,
    Transportista,
    Asesor
)

# ========================
# PRUEBAS LOGIN
# ========================

class LoginViewTest(TestCase):

    def setUp(self):

        self.client = Client()
        self.password = "test1234"

        # Usuario auth_user
        self.user = User.objects.create_user(
            username="jeison",
            password=self.password
        )

        # Usuario extendido
        self.usuario = Usuario.objects.create(
            user=self.user,
            nombre="Jeison",
            apellido="Leon",
            nombre_usuario="jeison",
            correo="jeison@test.com",
            ciudad="Bogotá",
            departamento="Cundinamarca",
            direccion="Calle 1",
            cedula="10000001",
            telefono="3120000000",
            rol="CLIENTE",
            estado=True
        )

        # Perfil cliente
        Cliente.objects.create(
            id_usuario=self.usuario,
            preferencias="Orgánico"
        )

    # LOGIN EXITOSO CLIENTE
    def test_login_cliente(self):

        response = self.client.post(reverse('login_view'), {
            'username': 'jeison',
            'password': self.password
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mostrar_productos'))

    # LOGIN INVÁLIDO
    def test_login_invalido(self):

        response = self.client.post(reverse('login_view'), {
            'username': 'jeison',
            'password': 'incorrecta'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Credenciales inválidas")

    # USUARIO SIN PERFIL
    def test_usuario_sin_perfil(self):

        User.objects.create_user(
            username="sinperfil",
            password="123456"
        )

        response = self.client.post(reverse('login_view'), {
            'username': 'sinperfil',
            'password': '123456'
        })

        self.assertEqual(response.status_code, 302)

    # LOGIN ADMIN
    def test_login_admin(self):

        self.usuario.rol = "ADMINISTRADOR"
        self.usuario.save()

        response = self.client.post(reverse('login_view'), {
            'username': 'jeison',
            'password': self.password
        })

        self.assertRedirects(
            response,
            reverse('ver_listas_usuarios_admin')
        )

    # LOGIN TRANSPORTISTA
    def test_login_transportista(self):

        self.usuario.rol = "TRANSPORTISTA"
        self.usuario.save()

        Transportista.objects.create(
            id_usuario=self.usuario,
            zonas_entrega="Bogotá"
        )

        response = self.client.post(reverse('login_view'), {
            'username': 'jeison',
            'password': self.password
        })

        self.assertRedirects(
            response,
            reverse('inicio_transportista')
        )

    # LOGIN PRODUCTOR
    def test_login_productor(self):

        self.usuario.rol = "PRODUCTOR"
        self.usuario.save()

        Productor.objects.create(
            id_usuario=self.usuario,
            tipo_cultivo="Hidroponía"
        )

        response = self.client.post(reverse('login_view'), {
            'username': 'jeison',
            'password': self.password
        })

        self.assertRedirects(
            response,
            reverse('lista_productos')
        )

    # LOGIN ASESOR
    def test_login_asesor(self):

        self.usuario.rol = "ASESOR"
        self.usuario.save()

        Asesor.objects.create(
            id_usuario=self.usuario,
            tipo_asesoria="Riego"
        )

        response = self.client.post(reverse('login_view'), {
            'username': 'jeison',
            'password': self.password
        })

        self.assertRedirects(
            response,
            reverse('asesor_servicios')
        )

    # ROL DESCONOCIDO
    def test_rol_desconocido(self):

        self.usuario.rol = "HACKER"
        self.usuario.save()

        response = self.client.post(reverse('login_view'), {
            'username': 'jeison',
            'password': self.password
        })

        self.assertEqual(response.status_code, 302)


# ========================
# CREAR USUARIO
# ========================

class CrearUsuarioAdminTest(TestCase):

    def setUp(self):

        self.client = Client()
        self.url = reverse('crear_usuario')

        self.data_base = {
            'txt_nombre': 'Nicolas',
            'txt_apellido': 'Perez',
            'txt_nombreUsuario': 'nicolas2026',
            'txt_correo': 'nicolas1@gmail.com',
            'txt_contrasena': 'Nico2026',
            'txt_telefono': '3127654387',
            'txt_documento': '100086534',
            'txt_ciudad': 'Bogota',
            'txt_departamento': 'Cundinamarca',
            'txt_direccion': 'calle 12',
        }

    # CREAR CLIENTE
    def test_crear_usuario_cliente(self):

        data = self.data_base.copy()

        data.update({
            'txt_nombreUsuario': 'cliente_test_1',
            'txt_correo': 'cliente@test.com',
            'txt_documento': '123456789',
            'role': 'CLIENTE',
            'txt_preferencias': 'Orgánico'
        })

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        usuario = Usuario.objects.get(
            nombre_usuario='cliente_test_1'
        )

        self.assertEqual(usuario.rol, 'CLIENTE')

        self.assertTrue(
            Cliente.objects.filter(
                id_usuario=usuario
            ).exists()
        )

    # USUARIO DUPLICADO
    def test_usuario_duplicado(self):

        User.objects.create_user(
            username='cliente_test_duplicado',
            password='123456'
        )

        data = self.data_base.copy()

        data.update({
            'txt_nombreUsuario': 'cliente_test_duplicado',
            'txt_correo': 'duplicado@test.com',
            'txt_documento': '999999999',
            'role': 'CLIENTE'
        })

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            User.objects.filter(
                username='cliente_test_duplicado'
            ).count(),
            1
        )

    # CREAR PRODUCTOR
    def test_crear_usuario_productor(self):

        data = self.data_base.copy()

        data.update({
            'txt_nombreUsuario': 'prod123',
            'txt_correo': 'prod@test.com',
            'txt_documento': '88888888',
            'role': 'PRODUCTOR',
            'txt_tipoCultivo': 'Hidroponía'
        })

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        usuario = Usuario.objects.get(
            nombre_usuario='prod123'
        )

        self.assertEqual(usuario.rol, 'PRODUCTOR')

        self.assertTrue(
            Productor.objects.filter(
                id_usuario=usuario
            ).exists()
        )

    # GET FORMULARIO
    def test_get_renderiza_formulario(self):

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            'admin_usuarios/registrar_usuario.html'
        )