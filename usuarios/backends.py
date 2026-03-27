from django.contrib.auth.backends import BaseBackend
from .models import Usuario
from django.contrib.auth.hashers import check_password

class UsuarioBackend(BaseBackend):
    def authenticate(self, request, nombre_usuario=None, contrasena=None, **kwargs):
        try:
            usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)
            if check_password(contrasena, usuario.contrasena_usuario):
                return usuario
        except Usuario.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
        
'''
quí usamos check_password para comparar la contraseña encriptada.
Si aún guardas contraseñas en texto plano, deberías migrar a make_password y check_password para mayor seguridad.

'''
