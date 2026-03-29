from django.shortcuts import render , redirect
from django.contrib import messages
from .models import Usuario, Cliente, Productor, Asesor, Administrador,Transportista
from productos.models import Producto
from pedidos.models import Compra
from envios.models import Envio
from servicios.models import Servicio
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm



# proteccion de las vistas , solicitando el rol correspondiente para que 
# solo los usuarios administradores puedan acceder a las vistas 

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_view')
        if not hasattr(request.user, 'usuario') or request.user.usuario.rol.upper() != "ADMINISTRADOR":
            messages.error(request, "Acceso restringido solo para administradores.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# pagina publica 
def home(request):
    return render(request, 'inicio.html')




#  Esto Es Navegacion
@login_required
def inicio_cliente(request):
    return render(request,'inicio.html')


def inicio_usuarios(request):
    return render(request,'usuarios/login.html')


def mostrar_registro_usuarios(request):
    return render(request,'usuarios/register.html')



# Esto Son Metodos 


def registrar_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('txt_nombre')
        apellido = request.POST.get('txt_apellido')
        username = request.POST.get('txt_nombreUsuario')
        correo = request.POST.get('txt_correo')
        password = request.POST.get('txt_contrasena')
        telefono = request.POST.get('txt_telefono')
        documento = request.POST.get('txt_documento')
        ciudad = request.POST.get('txt_ciudad')
        departamento = request.POST.get('txt_departamento')
        direccion = request.POST.get('txt_direccion')
        rol = request.POST.get('role')

        # Validar que no exista el usuario en auth_user
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect('mostrar_registro_usuarios')

        # Crear User estándar (contraseña encriptada automáticamente)
        user = User.objects.create_user(
            username=username,
            email=correo,
            password=password,
            first_name=nombre,
            last_name=apellido
        )

        # Crear Usuario extendido con todos los campos obligatorios
        Usuario.objects.create(
            user=user,
            nombre=nombre,
            apellido=apellido,
            nombre_usuario=username,   # <- campo único
            correo=correo,
            cedula=documento,
            ciudad=ciudad,
            departamento=departamento,
            direccion=direccion,
            telefono=telefono,
            rol=rol,
            estado=True
        )

        messages.success(request, "Usuario registrado correctamente. Ya puedes iniciar sesión.")
        return redirect('login_view')

    return render(request, 'usuarios/registro.html')


# Navegacion vistas admin
@admin_required
def dashboard_admin(request):
    return render(request, 'admin_usuarios/dashboard.html')
@admin_required
def lista_productos_admin(request):
    return render(request, 'admin_productos/index.html')
@admin_required
def list_usuarios_admin(request):
    return render(request,'admin_usuarios/dashboard.html')
@admin_required
def lista_pedidos_admin(request):
    return render(request, 'admin_pedidos/pedidos.html')
@admin_required
def lista_envios_admin(request):
    return render(request, 'admin_envios/envios.html')
@admin_required
def lista_servicios_admin(request):
    return render(request, 'admin_servicios/servicios.html' )


# Metodos Admin
@admin_required 
def ver_listas_usuarios_admin(request):
    #tablas por rol de usuarios
    clientes = Cliente.objects.select_related('id_usuario').all()
    productores = Productor.objects.select_related('id_usuario').all()
    transportistas = Transportista.objects.select_related('id_usuario').all()
    asesores = Asesor.objects.select_related('id_usuario').all()
    
    #conteo de usuarios
    total_clientes =Cliente.objects.filter().count()
    total_productores = Productor.objects.filter(id_usuario__estado=True).count()
    total_transportistas=Transportista.objects.filter(id_usuario__estado=True).count()
    total_asesores=Asesor.objects.filter(id_usuario__estado=True).count()
    
    return render(request, 'admin_usuarios/dashboard.html', {
        'clientes': clientes,
        'productores': productores,
        'transportistas': transportistas,
        'asesores': asesores,
        
        'total_clientes':total_clientes,
        'total_productores':total_productores,
        'total_transportistas': total_transportistas,
        'total_asesores': total_asesores,
    })
@admin_required
def ver_lista_productos_admin(request):
    productos = Producto.objects.select_related('id_usuario', 'id_categoria').all()
    
    return render(request, 'admin_productos/index.html', {'productos': productos})
@admin_required
def ver_lista_pedidos_admin(request):
    compras = Compra.objects.select_related('id_cliente' 'id_compra'). all()
    
    return render(request, 'admin_pedidos/pedidos.html', {'compras': compras})
@admin_required
def ver_lista_envio_admin(request):
    envios = Envio.objects.select_related(
        'id_compra',
        'id_transportista'
    ).all()
    return render(request, 'admin_envios/envios.html')
@admin_required
def ver_lista_servicios_admin(request):
    servicios = Servicio.objects.select_related(
        'id_asesor',
        'id_asesor__id_usuario'
    ).all()
    
    return render(request, 'admin_servicios/servicios.html', {'servicios': servicios})


#admin crea usuario

@admin_required
def crear_usuario_admin(request):
    if request.method == 'POST':
        nombre = request.POST.get('txt_nombre')
        apellido = request.POST.get('txt_apellido')
        username = request.POST.get('txt_nombreUsuario')
        correo = request.POST.get('txt_correo')
        password = request.POST.get('txt_contrasena')
        telefono = request.POST.get('txt_telefono')
        documento = request.POST.get('txt_documento')
        ciudad = request.POST.get('txt_ciudad')
        departamento = request.POST.get('txt_departamento')
        direccion = request.POST.get('txt_direccion')
        rol = request.POST.get('role')

        # ✅ Validación correcta
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect('crear_usuario')

        # ✅ Crear User estándar (contraseña encriptada automáticamente)
        user = User.objects.create_user(
            username=username,
            email=correo,
            password=password,   # Django la encripta
            first_name=nombre,
            last_name=apellido
        )

        # ✅ Crear Usuario extendido (datos adicionales)
        usuario = Usuario.objects.create(
            user=user,
            nombre=nombre,
            apellido=apellido,
            nombre_usuario=username,   # <- aquí llenas el campo único
            correo=correo,
            cedula=documento,
            ciudad=ciudad,
            departamento=departamento,
            direccion=direccion,
            telefono=telefono,
            rol=rol,
            estado=True
        )

        # ✅ Crear según rol
        if rol.upper() == "CLIENTE":
            Cliente.objects.create(
                id_usuario=usuario,
                preferencias=request.POST.get("txt_preferencias")
            )
        elif rol.upper() == "PRODUCTOR":
            Productor.objects.create(
                id_usuario=usuario,
                tipo_cultivo=request.POST.get("txt_tipoCultivo")
            )
        elif rol.upper() == "TRANSPORTISTA":
            Transportista.objects.create(
                id_usuario=usuario,
                zonas_entrega=request.POST.get("txt_zonasEntrega")
            )
        elif rol.upper() == "SERVICIO":
            Asesor.objects.create(
                id_usuario=usuario,
                tipo_asesoria=request.POST.get("txt_tipoAsesoria")
            )

        messages.success(request, "Usuario registrado correctamente")
        return redirect('ver_listas_usuarios_admin')

    return render(request, 'admin_usuarios/registrar_usuario.html')

# esto es el login , la autenticacion de cada usuario 



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                try:
                    usuario = Usuario.objects.get(user=user)
                except Usuario.DoesNotExist:
                    messages.error(request, "No se encontró información extendida del usuario")
                    return redirect('login_view')

                rol = usuario.rol.upper()
                messages.success(request, f"Login correcto. Rol detectado: {rol}")
                print(f"ROL DETECTADO: '{usuario.rol}'")

                if rol == 'CLIENTE':
                    return redirect('inicio')             # productos/inicio
                elif rol == 'ADMINISTRADOR':
                    return redirect('inicio_usuarios')    # usuarios/inicio_usuarios
                else:
                    messages.error(request, f"Rol desconocido: {rol}")
                    return redirect('login_view')
            else:
                messages.error(request, "Credenciales inválidas")
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    logout(request)   # elimina la sesión del usuario
    return redirect('inicio_usuarios')


def reset_password(request):
    return render(request, 'usuarios/reset_password.html')