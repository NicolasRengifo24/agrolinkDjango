from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime



from .models import Usuario, Cliente, Productor, Asesor, Administrador,Transportista
from servicios.models import Servicio, Maquinas, Certificados

from pedidos.models import Compra, DetallesCompra
from django.http import JsonResponse
from envios.models import Envio
from servicios.models import Servicio
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password

from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm

from productos.models import Producto, ImagenesProducto, ProductoFinca,Finca
from . forms import ProductoForm, ImagenPrincipalForm, ProductoFincaForm, ProductoEditarForm





# proteccion de las vistas , solicitando el rol correspondiente para que 
# solo los usuarios administradores puedan acceder a las vistas 

from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login_view')

        try:
            usuario = request.user.usuario
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario sin perfil asignado")
            return redirect('home')

        if usuario.rol.upper() != "ADMINISTRADOR":
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


from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from usuarios.models import Usuario, Cliente, Productor, Transportista, Asesor, Administrador

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

        # Validar usuario existente
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect('mostrar_registro_usuarios')

        # 🔐 Crear usuario de Django
        user = User.objects.create_user(
            username=username,
            email=correo,
            password=password,
            first_name=nombre,
            last_name=apellido
        )

        # 👤 Crear usuario extendido
        usuario = Usuario.objects.create(
            user=user,
            nombre=nombre,
            apellido=apellido,
            nombre_usuario=username,
            correo=correo,
            cedula=documento,
            ciudad=ciudad,
            departamento=departamento,
            direccion=direccion,
            telefono=telefono,
            rol=rol,
            estado=True
        )

        # 🎯 CREAR SEGÚN EL ROL
        if rol == "CLIENTE":
            Cliente.objects.create(id_usuario=usuario)

        elif rol == "PRODUCTOR":
            Productor.objects.create(id_usuario=usuario)

        elif rol == "TRANSPORTISTA":
            Transportista.objects.create(id_usuario=usuario)

        elif rol == "ASESOR":
            Asesor.objects.create(id_usuario=usuario)

        elif rol == "ADMIN":
            Administrador.objects.create(id_usuario=usuario)

        messages.success(request, "Usuario registrado correctamente. Ya puedes iniciar sesión.")
        return redirect('login_view')

    return render(request, 'usuarios/registro.html')


# Navegacion vistas admin
#@admin_required
def dashboard_admin(request):
    return render(request, 'admin_usuarios/dashboard.html')
#@admin_required
def lista_productos_admin(request):
    return render(request, 'admin_productos/index.html')
#@admin_required
def list_usuarios_admin(request):
    return render(request,'admin_usuarios/dashboard.html')
#@admin_required
def lista_pedidos_admin(request):
    return render(request, 'admin_pedidos/pedidos.html')
#@admin_required
def lista_envios_admin(request):
    return render(request, 'admin_envios/envios.html')
#@admin_required
def lista_servicios_admin(request):
    return render(request, 'admin_servicios/servicios.html' )


# Metodos Admin
#@admin_required 
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
    
    
#@admin_required
def ver_lista_productos_admin(request):
    productos = Producto.objects.select_related('id_usuario', 'id_categoria').all()
    
    total_producto = Producto.objects.filter().count()
    stock_alto = Producto.objects.filter(stock__gte=100).count()
    stock_bajo = Producto.objects.filter(stock__lt=50).count()
    productores_activos= Producto.objects.values('id_usuario').distinct().count()
    
    context = {
        'productos': productos,
        'total_productos': total_producto,
        'stock_alto': stock_alto,
        'stock_bajo': stock_bajo,
        'productores_activos': productores_activos
    }
    
    return render(request, 'admin_productos/index.html', context )
    
def crear_producto_admin(request):
    producto_form = ProductoForm()
    imagen_form   = ImagenPrincipalForm()
    finca_form    = ProductoFincaForm()
    productores   = Productor.objects.all()

    if request.method == 'POST':
        producto_form = ProductoForm(request.POST)
        imagen_form   = ImagenPrincipalForm(request.POST, request.FILES)

        productor_id = request.POST.get('id_usuario')
        productor    = None
        if productor_id:
            try:
                productor = Productor.objects.get(pk=productor_id)
            except Productor.DoesNotExist:
                pass

        finca_form = ProductoFincaForm(request.POST, productor=productor, validate_finca=True)

        # Debug temporal — quitar después de resolver
        print("Producto errors:", producto_form.errors)
        print("Imagen errors:  ", imagen_form.errors)
        print("Finca errors:   ", finca_form.errors)

        if producto_form.is_valid() and imagen_form.is_valid() and finca_form.is_valid():

            # 1. Guardar producto
            producto_editado = producto_form.save()

            # 2. Guardar imagen solo si se subió una
            if request.FILES.get('url_imagen'):
                imagen             = imagen_form.save(commit=False)
                imagen.id_producto = producto_editado
                imagen.es_principal = 1
                imagen.save()

            # 3. Guardar relación producto ↔ finca
            producto_finca             = finca_form.save(commit=False)
            producto_finca.id_producto = producto_editado
            producto_finca.save()

            messages.success(request, f'Producto_editado "{Producto.nombre_producto}" creado exitosamente.')
            return redirect('ver_lista_productos_admin')

        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')

    context = {
        'form'       : producto_form,
        'imagen_form': imagen_form,
        'finca_form' : finca_form,
        'productores': productores,
        'fincas_json': _fincas_por_productor(),
    }
    return render(request, 'admin_productos/crear_producto.html', context)



def _fincas_por_productor():
    
        import json
        from collections import defaultdict

        resultado = defaultdict(list)
        fincas = Finca.objects.select_related('id_usuario').values(
            'id_finca', 'nombre_finca', 'departamento', 'ciudad', 'id_usuario'
        )
        for f in fincas:
            resultado[f['id_usuario']].append({
                
                'id': f['id_finca'],
                'nombre': f['nombre_finca'] or 'Sin nombre',
                'departamento': f['departamento'] or '',
                'ciudad': f['ciudad'] or '',
        })

        return json.dumps(resultado)

        




def editar_producto_admin(request, id):
    producto       = get_object_or_404(Producto, pk=id)   # ← objeto existente
    producto_finca = producto.fincas.select_related('id_finca').first()
    imagen_actual  = producto.imagenProducto.filter(es_principal=1).first()

    producto_form = ProductoEditarForm(instance=producto)
    finca_form    = ProductoFincaForm(instance=producto_finca, productor=producto.id_usuario)
    imagen_form   = ImagenPrincipalForm()

    if request.method == 'POST':
        producto_form = ProductoEditarForm(request.POST, instance=producto)
        finca_form    = ProductoFincaForm(
            request.POST,
            instance       = producto_finca,
            productor      = producto.id_usuario,
            validate_finca = True,
        )
        imagen_form = ImagenPrincipalForm(request.POST, request.FILES)
        
        
        print("POST data:", request.POST)
        print("Producto valid:", producto_form.is_valid())
        print("Producto errors:", producto_form.errors)
        print("Finca valid:", finca_form.is_valid())
        print("Finca errors:", finca_form.errors)
        print("Imagen valid:", imagen_form.is_valid())
        print("Imagen errors:", imagen_form.errors)

        if producto_form.is_valid() and finca_form.is_valid():

            producto_form.save()   # ← no reasignes la variable producto

            pf             = finca_form.save(commit=False)
            pf.id_producto = producto
            pf.save()

            if request.FILES.get('url_imagen'):
                if imagen_actual:
                    imagen_actual.url_imagen = request.FILES['url_imagen']
                    imagen_actual.save()
                else:
                    ImagenesProducto.objects.create(
                        id_producto  = producto,
                        url_imagen   = request.FILES['url_imagen'],
                        es_principal = 1,
                    )

            messages.success(request, f'Producto "{producto.nombre_producto}" actualizado exitosamente.')
            return redirect('ver_lista_productos_admin')

        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')

    context = {
        'producto'      : producto,
        'producto_finca': producto_finca,
        'imagen_actual' : imagen_actual,
        'form'          : producto_form,
        'imagen_form'   : imagen_form,
        'finca_form'    : finca_form,
        'fincas_json'   : _fincas_por_productor(),
    }
    return render(request, 'admin_productos/editar_producto.html', context)

def eliminar_Producto_admin(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    
    producto.delete()

    messages.success(request, "Producto eliminado correctamente")
    return redirect('ver_lista_productos_admin')



@admin_required
def ver_lista_pedidos_admin(request):

    compras = Compra.objects.select_related('id_cliente').prefetch_related('detallescompra_set')

    hoy = datetime.now()

    
    total_pedidos = Compra.objects.count()

    total_ventas = Compra.objects.aggregate(
        total=Sum('total')
    )['total'] or 0

    pedidos_mes = Compra.objects.filter(
        fecha_hora_compra__year=hoy.year,
        fecha_hora_compra__month=hoy.month
    ).count()

    ventas_mes = Compra.objects.filter(
        fecha_hora_compra__year=hoy.year,
        fecha_hora_compra__month=hoy.month
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    context = {
        'compras': compras,
        'total_pedidos': total_pedidos,
        'total_ventas': total_ventas,
        'pedidos_mes': pedidos_mes,
        'ventas_mes': ventas_mes
    }

    return render(request, 'admin_pedidos/pedidos.html', context)

def ver_detalle_compra_admin(request, id):
    compra = get_object_or_404(Compra.objects.select_related('id_cliente'),id_compra=id)
    
    detalles = DetallesCompra.objects.select_related('id_producto').filter(id_compra=compra.id_compra)
    
    
    
    context={ 'compra': compra, 'detalles': detalles}
    
    return render(request, 'admin_pedidos/detalle_compra.html', context)
    




@admin_required
def ver_lista_envio_admin(request):
    envios = Envio.objects.select_related(
        'id_compra',
        'id_transportista',
        'id_vehiculo'
    ).all()
    
    hoy = datetime.now()

    # 🔹 KPIs GENERALES
    total_envios = Envio.objects.count()

    envios_activos = Envio.objects.filter(
        estado_envio="en_camino"
    ).count()

    envios_entregados = Envio.objects.filter(
        estado_envio="entregado"
    ).count()

    envios_pendientes = Envio.objects.filter(
        estado_envio="pendiente"
    ).count()

    costo_total_envios = Envio.objects.aggregate(
        total=Sum('costo_total')
    )['total'] or 0

    
    envios_mes = Envio.objects.filter(
        fecha_salida__year=hoy.year,
        fecha_salida__month=hoy.month
    ).count()

    costo_envios_mes = Envio.objects.filter(
        fecha_salida__year=hoy.year,
        fecha_salida__month=hoy.month
    ).aggregate(
        total=Sum('costo_total')
    )['total'] or 0

    context = {
        'envios': envios,

        # KPIs
        'total_envios': total_envios,
        'envios_activos': envios_activos,
        'envios_entregados': envios_entregados,
        'envios_pendientes': envios_pendientes,
        'costo_total_envios': costo_total_envios,

        # KPIs del mes
        'envios_mes': envios_mes,
        'costo_envios_mes': costo_envios_mes
    }
    
    return render(request, 'admin_envios/envios.html', context )


def obtener_envio(request, id):
    envio = get_object_or_404(
        Envio.objects.select_related(
            'id_transportista__id_usuario',
            'id_vehiculo'
        ),
        id_envio=id
    )

    data = {
        "id_envio": envio.id_envio,
        "estado_envio": envio.estado_envio,
        "numero_seguimiento": envio.numero_seguimiento,
        "distancia_km": float(envio.distancia_km or 0),
        "peso_total_kg": float(envio.peso_total_kg or 0),

        "fecha_salida": str(envio.fecha_salida or ""),
        "fecha_entrega": str(envio.fecha_entrega or ""),

        "direccion_origen": envio.direccion_origen or "",
        "direccion_destino": envio.direccion_destino or "",

        "latitud_origen": envio.latitud_origen or 0,
        "longitud_origen": envio.longitud_origen or 0,
        "latitud_destino": envio.latitud_destino or 0,
        "longitud_destino": envio.longitud_destino or 0,

        "costo_base": float(envio.costo_base or 0),
        "costo_peso": float(envio.costo_peso or 0),
        "costo_total": float(envio.costo_total or 0),

        # 
        "transportista": (
            f"{envio.id_transportista.id_usuario.nombre} {envio.id_transportista.id_usuario.apellido}"
            if envio.id_transportista else ""
        ),

        "vehiculo": (
            f"{envio.id_vehiculo.tipo_vehiculo} - {envio.id_vehiculo.placa_vehiculo}"
            if envio.id_vehiculo else "No asignado"
        )
    }

    return JsonResponse(data)


@admin_required
def ver_lista_servicios_admin(request):
    servicios = Servicio.objects.select_related(
        'id_asesor',
        'id_asesor__id_usuario'
    ).all()

    # 🔹 KPIs
    total_servicios = Servicio.objects.count()

    servicios_activos = Servicio.objects.filter(
        estado__iexact="activo"
    ).count()

    servicios_inactivos = Servicio.objects.filter(
        estado__iexact="inactivo"
    ).count()

    context = {
        'servicios': servicios,

        # KPIs
        'total_servicios': total_servicios,
        'servicios_activos': servicios_activos,
        'servicios_inactivos': servicios_inactivos,
    }

    return render(request, 'admin_servicios/servicios.html', context)

def ver_servicio_detalle(request, id):

    servicio = get_object_or_404(Servicio, pk=id)

    maquinas = Maquinas.objects.filter(
        id_asesor=servicio.id_asesor
    )

    certificados = Certificados.objects.filter(
        id_usuario=servicio.id_asesor
    )

    return render(request, 'admin_servicios/ver_servicio_admin.html', {
        'servicio': servicio,
        'maquinas': maquinas,
        'certificados': certificados
    })


def cambiar_estado_servicio(request, servicio_id):
    
    servicio = get_object_or_404(Servicio.objects.select_related('id_asesor__id_usuario'), id_servicio=servicio_id)

    servicio.estado = servicio.id_asesor.id_usuario.estado  # True o False
    servicio.save()
    
    return redirect('ver_lista_servicios_admin')

def eliminar_servicio_admin(request, servicio_id):
    servicio = get_object_or_404(Servicio, id_servicio=servicio_id)
    servicio.delete()
    messages.success(request, "servicio eliminado correctamente")
    return redirect('ver_lista_servicios_admin')

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio/')
    


#admin crea usuario

#@admin_required
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

        #  Validación correcta
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect('crear_usuario')

        #  Crear User estándar (contraseña encriptada automáticamente)
        user = User.objects.create_user(
            username=username,
            email=correo,
            password=password,   # Django la encripta
            first_name=nombre,
            last_name=apellido
        )

        #  Crear Usuario extendido (datos adicionales)
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

        #  Crear según rol
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


def editar_usuario_admin(request, id):
    usuario = Usuario.objects.get(id_usuario=id)
    if request.method == 'POST':
        usuario.nombre=request.POST.get('txt_nombre')
        usuario.apellido=request.POST.get('txt_apellido')
        usuario.correo=request.POST.get('txt_correo')
        usuario.telefono=request.POST.get('txt_telefono')
        usuario.ciudad=request.POST.get('txt_ciudad')
        usuario.departamento=request.POST.get('txt_departamento')
        usuario.direccion=request.POST.get('txt_direccion')
        
        usuario.save()
        
        messages.success(request, "Usuario actualizado correctamente")
        return redirect('ver_listas_usuarios_admin')
    return render(request, 'admin_usuarios/editar_usuario.html', {'usuario': usuario})

def eliminar_usuario(request, id):
    usuario = Usuario.objects.get(id_usuario=id)

    Cliente.objects.filter(id_usuario=usuario).delete()
    Productor.objects.filter(id_usuario=usuario).delete()
    Transportista.objects.filter(id_usuario=usuario).delete()
    Asesor.objects.filter(id_usuario=usuario).delete()

    if usuario.user:
        usuario.user.delete()
    
    usuario.delete()

    messages.success(request, "Usuario eliminado correctamente")
    return redirect('ver_listas_usuarios_admin')


def ver_usuario(request, id):
    usuario =Usuario.objects.get(id_usuario=id)
    
    return render(request, 'admin_usuarios/ver_usuario.html', {'usuario': usuario})

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
                    return redirect('mostrar_productos') 
                # productos/inicio
                elif rol == 'ADMINISTRADOR':
                    return redirect('usuarios')

                elif rol == 'TRANSPORTISTA' :
                    return redirect('inicio_transportista')
                
                elif rol == 'PRODUCTOR':
                    return redirect('lista_productos')

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