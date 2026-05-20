from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from servicios.models import Servicio
from usuarios.models import Usuario, Asesor


class AsesorServiciosViewTest(TestCase):

    def setUp(self):

        self.client = Client()

        # =====================================
        # USER DJANGO
        # =====================================

        self.user = User.objects.create_user(
            username='asesor1',
            password='123456'
        )

        # =====================================
        # USUARIO PERSONALIZADO
        # =====================================

        self.usuario = Usuario.objects.create(
            user=self.user,
            nombre_usuario='asesor1',
            rol='ASESOR',
            correo='asesor@test.com',
            telefono='3001234567',
            ciudad='Bogota',
            cedula='123456789'
        )

        # =====================================
        # ASESOR
        # =====================================

        self.asesor = Asesor.objects.create(
            id_usuario=self.usuario
        )

        # =====================================
        # SERVICIO
        # =====================================

        self.servicio = Servicio.objects.create(
            id_asesor=self.asesor,
            categoria='Riego',
            descripcion='Servicio de riego',
            estado='ACTIVO'
        )

        self.url = reverse('asesor_servicios')

    # =====================================
    # GET EXITOSO
    # =====================================

    def test_get_asesor_servicios(self):

        self.client.login(
            username='asesor1',
            password='123456'
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            'servicios/asesor.html'
        )

        self.assertContains(
            response,
            'Servicio de riego'
        )

    # =====================================
    # REDIRECCION SIN LOGIN
    # =====================================

    def test_sin_login(self):

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    # =====================================
    # REDIRECCION SI NO ES ASESOR
    # =====================================

    def test_usuario_no_asesor(self):

        user2 = User.objects.create_user(
            username='cliente1',
            password='123456'
        )

        Usuario.objects.create(
            user=user2,
            nombre_usuario='cliente1',
            rol='CLIENTE',
            correo='cliente@test.com',
            telefono='3001111111',
            ciudad='Bogota',
            cedula='999999999'
        )

        self.client.login(
            username='cliente1',
            password='123456'
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    # =====================================
    # CREAR SERVICIO
    # =====================================

    def test_crear_servicio(self):

        self.client.login(
            username='asesor1',
            password='123456'
        )

        response = self.client.post(self.url, {
            'categoria': 'Maquinaria',
            'descripcion': 'Tractor disponible',
            'estado': 'ACTIVO'
        })

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Servicio.objects.filter(
                descripcion='Tractor disponible'
            ).exists()
        )

    # =====================================
    # EDITAR SERVICIO
    # =====================================

    def test_editar_servicio(self):

        self.client.login(
            username='asesor1',
            password='123456'
        )

        response = self.client.post(self.url, {
            'id_servicio': self.servicio.id_servicio,
            'categoria': 'Fumigacion',
            'descripcion': 'Servicio actualizado',
            'estado': 'INACTIVO'
        })

        self.assertEqual(response.status_code, 302)

        self.servicio.refresh_from_db()

        self.assertEqual(
            self.servicio.descripcion,
            'Servicio actualizado'
        )

        self.assertEqual(
            self.servicio.estado,
            'INACTIVO'
        )

    # =====================================
    # ELIMINAR SERVICIO
    # =====================================

    def test_eliminar_servicio(self):

        self.client.login(
            username='asesor1',
            password='123456'
        )

        response = self.client.post(self.url, {
            'eliminar_id': self.servicio.id_servicio
        })

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Servicio.objects.filter(
                id_servicio=self.servicio.id_servicio
            ).exists()
        )

    # =====================================
    # EDITAR SERVICIO INEXISTENTE
    # =====================================

    def test_editar_servicio_inexistente(self):

        self.client.login(
            username='asesor1',
            password='123456'
        )

        response = self.client.post(self.url, {
            'id_servicio': 9999,
            'categoria': 'X',
            'descripcion': 'No existe',
            'estado': 'ACTIVO'
        })

        self.assertEqual(response.status_code, 302)

    # =====================================
    # ELIMINAR SERVICIO INEXISTENTE
    # =====================================

    def test_eliminar_servicio_inexistente(self):

        self.client.login(
            username='asesor1',
            password='123456'
        )

        response = self.client.post(self.url, {
            'eliminar_id': 9999
        })

        self.assertEqual(response.status_code, 302)

    # =====================================
    # CREAR SERVICIO CAMPOS VACIOS
    # =====================================

    def test_crear_servicio_campos_vacios(self):

        self.client.login(
            username='asesor1',
            password='123456'
        )

        response = self.client.post(self.url, {
            'categoria': '',
            'descripcion': '',
            'estado': ''
        })

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Servicio.objects.filter(
                descripcion=''
            ).exists()
        )