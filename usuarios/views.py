from django.shortcuts import render , redirect
from django.contrib import messages
from .models import Usuario, Cliente, Productor, Asesor, Administrador,Transportista
from productos.models import Producto
from pedidos.models import Compra
from envios.models import Envio
from servicios.models import Servicio
#  Esto Es Navegacion
def inicio_usuarios(request):
    return render(request,'usuarios/login.html')


def mostrar_registro_usuarios(request):
    return render(request,'usuarios/register.html')



# Esto Son Metodos 

def login(request):
    if request.method=='POST':
        cedula = request.POST.get("txt_documento")
        contrasena = request.POST.get("txt_clave")

        usuario = Usuario.objects.filter(cedula = cedula,contrasena = contrasena).first()

        if usuario is not None:
            return redirect('inicio.html')
        else: 
            return redirect('register.html')




def registrar_usuario(request):
    if request.method == 'POST':

        # 🔹 datos base
        nombre = request.POST.get("txt_nombre")
        apellido = request.POST.get("txt_apellido")
        documento = request.POST.get("txt_documento")  
        nombreUsuario = request.POST.get("txt_nombreUsuario")
        correo = request.POST.get("txt_correo")
        contrasena = request.POST.get("txt_contrasena")
        telefono = request.POST.get("txt_telefono")
        ciudad = request.POST.get("txt_ciudad")
        departamento = request.POST.get("txt_departamento")
        direccion = request.POST.get("txt_direccion")
        rol = request.POST.get("role")

        # 1. CREAR USUARIO (OBLIGATORIO)
        usuario = Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            nombre_usuario=nombreUsuario,
            telefono=telefono,
            departamento=departamento,
            ciudad=ciudad,
            correo=correo,
            contrasena_usuario=contrasena,
            direccion=direccion,
            cedula=documento,
            rol=rol
        )

        # 2. CREAR SEGÚN ROL
        if rol == "CLIENTE":
            Cliente.objects.create(
                id_usuario=usuario,
                preferencias=request.POST.get("txt_preferencias")
            )

        elif rol == "PRODUCTOR":
            Productor.objects.create(
                id_usuario=usuario,
                tipo_cultivo=request.POST.get("txt_tipoCultivo")
            )

        elif rol == "TRANSPORTISTA":
            Transportista.objects.create(
                id_usuario=usuario,
                zonas_entrega=request.POST.get("txt_zonasEntrega")
            )

        elif rol == "SERVICIO":
            Asesor.objects.create(
                id_usuario=usuario,
                tipo_asesoria=request.POST.get("txt_tipoAsesoria")
            )

    return redirect('mostrar_registro_usuarios')




# Navegacion vistas admin
def dashboard_admin(request):
    return render(request, 'admin_usuarios/dashboard.html')

def lista_productos_admin(request):
    return render(request, 'admin_productos/index.html')

def list_usuarios_admin(request):
    return render(request,'admin_usuarios/dashboard.html')

def lista_pedidos_admin(request):
    return render(request, 'admin_pedidos/pedidos.html')

def lista_envios_admin(request):
    return render(request, 'admin_envios/envios.html')

def lista_servicios_admin(request):
    return render(request, 'admin_servicios/servicios.html' )


# Metodos Admin 
def ver_listas_usuarios_admin(request):
    #tablas por rol de usuarios
    clientes = Cliente.objects.select_related('id_usuario').all()
    productores = Productor.objects.select_related('id_usuario').all()
    transportistas = Transportista.objects.select_related('id_usuario').all()
    asesores = Asesor.objects.select_related('id_usuario').all()
    
    #conteo de usuarios
    total_clientes =Cliente.objects.filter(id_usuario__estado=True).count()
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
    
def ver_lista_productos_admin(request):
    productos = Producto.objects.select_related('id_usuario', 'id_categoria').all()
    
    return render(request, 'admin_productos/index.html', {'productos': productos})

def ver_lista_pedidos_admin(request):
    compras = Compra.objects.select_related('id_cliente' 'id_compra'). all()
    
    return render(request, 'admin_pedidos/pedidos.html', {'compras': compras})

def ver_lista_envio_admin(request):
    envios = Envio.objects.select_related(
        'id_compra',
        'id_transportista'
    ).all()
    return render(request, 'admin_envios/envios.html')

def ver_lista_servicios_admin(request):
    servicios = Servicio.objects.select_related(
        'id_asesor',
        'id_asesor__id_usuario'
    ).all()
    
    return render(request, 'admin_servicios/servicios.html', {'servicios': servicios})


#admin crea usuario
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

        # Validación básica
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect('registrar_usuario')

        # Crear usuario
        usuario = Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            username=username,
            correo=correo,
            telefono=telefono,
            documento=documento,
            ciudad=ciudad,
            departamento=departamento,
            direccion=direccion,
            rol=rol
        )

        # ⚠️ IMPORTANTE: guardar contraseña encriptada
        

        messages.success(request, "Usuario registrado correctamente")
        return redirect('ver_listas_usuarios_admin')  # o donde quieras redirigir

    return render(request, 'admin_usuarios/registrar_usuario.html')