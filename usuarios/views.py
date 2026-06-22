from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter



from .models import Usuario, Cliente, Productor, Asesor, Administrador, Transportista, Notificacion
from servicios.models import Servicio, Maquinas, Certificados

from pedidos.models import Compra, DetallesCompra
from django.http import JsonResponse
from envios.models import Envio, Vehiculo
from servicios.models import Servicio
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password

from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import random

from .forms import LoginForm, RegistroUsuarioForm


from productos.models import Producto, ImagenesProducto, ProductoFinca, Finca, CategoriaProducto
from. forms import ProductoForm, ImagenesProducto, ImagenPrincipalForm, ProductoFincaForm, ProductoEditarForm




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
    form = RegistroUsuarioForm()
    return render(request,'usuarios/register.html', {'form': form})



# Esto Son Metodos 


from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from usuarios.models import Usuario, Cliente, Productor, Transportista, Asesor, Administrador

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            # Acceder a los datos validados
            nombre = form.cleaned_data['txt_nombre']
            apellido = form.cleaned_data['txt_apellido']
            username = form.cleaned_data['txt_nombreUsuario']
            correo = form.cleaned_data['txt_correo']
            password = form.cleaned_data['txt_contrasena']
            telefono = form.cleaned_data['txt_telefono']
            documento = form.cleaned_data['txt_documento']
            ciudad = form.cleaned_data['txt_ciudad']
            departamento = form.cleaned_data['txt_departamento']
            tipo = form.cleaned_data['txt_direccion_tipo']
            n1 = form.cleaned_data['txt_direccion_numero1']
            letra = form.cleaned_data.get('txt_direccion_letra', '') or ''
            n2 = form.cleaned_data['txt_direccion_numero2']
            n3 = form.cleaned_data['txt_direccion_numero3']
            direccion = f"{tipo} {n1}{letra} # {n2}-{n3}"
            rol = form.cleaned_data['role']

            # Crear usuario base de Django
            user = User.objects.create_user(
                username=username,
                email=correo,
                password=password,
                first_name=nombre,
                last_name=apellido
            )

            # Crear usuario extendido
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

            # Crear según el rol
            if rol == "CLIENTE":
                Cliente.objects.create(id_usuario=usuario)
            elif rol == "PRODUCTOR":
                Productor.objects.create(id_usuario=usuario)
            elif rol == "TRANSPORTISTA":
                Transportista.objects.create(id_usuario=usuario)
            elif rol == "ASESOR":
                Asesor.objects.create(id_usuario=usuario)
            elif rol == "ADMINISTRADOR":
                Administrador.objects.create(id_usuario=usuario)

            messages.success(request, "Usuario registrado correctamente. Ya puedes iniciar sesión.")
            return redirect('login_view')
        else:
            
            return render(request, 'usuarios/register.html', {'form': form})
    else:
        form = RegistroUsuarioForm()

    return render(request, 'usuarios/register.html', {'form': form})


#google auth2

def completar_registro_google(request):
    """
    Vista que muestra el formulario para completar
    los datos faltantes después del login con Google.
    Si el usuario ya tiene perfil, redirige directo.
    """

    # Verificar que venga de Google
    google_correo = request.session.get('google_correo')
    if not google_correo:
        messages.error(request, "Acceso no válido")
        return redirect('login_view')

    # Si ya tiene perfil de Usuario extendido, redirigir según rol
    try:
        usuario = request.user.usuario
        rol = usuario.rol.upper()

        if rol == 'CLIENTE':
            return redirect('mostrar_productos')
        elif rol == 'ADMINISTRADOR':
            return redirect('ver_listas_usuarios_admin')
        elif rol == 'TRANSPORTISTA':
            return redirect('inicio_transportista')
        elif rol == 'PRODUCTOR':
            return redirect('lista_productos')
        elif rol == 'ASESOR':
            return redirect('asesor_servicios')

    except Exception:
        # No tiene perfil todavía → mostrar formulario
        pass

    # Pasar datos de Google y datos previos del formulario al template
    form_data = request.session.pop('google_form_data', {})
    context = {
        'google_nombre'  : request.session.get('google_nombre', ''),
        'google_apellido': request.session.get('google_apellido', ''),
        'google_correo'  : request.session.get('google_correo', ''),
        'google_foto'    : request.session.get('google_foto', ''),
        'form_data'      : form_data,
    }

    return render(request, 'usuarios/completar_registro_google.html', context)


def guardar_registro_google(request):
    """
    Procesa el formulario de completar registro con Google.
    Crea el Usuario extendido y el perfil según el rol elegido.
    """

    if request.method != 'POST':
        return redirect('completar_registro_google')

    # Verificar sesión de Google
    google_correo = request.session.get('google_correo')
    if not google_correo:
        messages.error(request, "Sesión expirada, intenta de nuevo")
        return redirect('login_view')

    # Recoger datos del formulario
    nombre      = request.POST.get('nombre', '').strip()
    apellido    = request.POST.get('apellido', '').strip()
    username    = request.POST.get('username', '').strip()
    cedula      = request.POST.get('cedula', '').strip()
    telefono    = request.POST.get('telefono', '').strip()
    ciudad      = request.POST.get('ciudad', '').strip()
    departamento = request.POST.get('departamento', 'Cundinamarca').strip()
    tipo_dir    = request.POST.get('direccion_tipo', '').strip()
    n1          = request.POST.get('direccion_numero1', '').strip()
    letra       = request.POST.get('direccion_letra', '').strip()
    n2          = request.POST.get('direccion_numero2', '').strip()
    n3          = request.POST.get('direccion_numero3', '').strip()
    direccion   = f"{tipo_dir} {n1}{letra} # {n2}-{n3}" if all([tipo_dir, n1, n2, n3]) else ''
    rol         = request.POST.get('rol', '').strip().upper()

    # Guardar datos para preservar en el formulario en caso de error
    request.session['google_form_data'] = {
        'nombre': nombre, 'apellido': apellido, 'username': username,
        'cedula': cedula, 'telefono': telefono, 'ciudad': ciudad,
        'departamento': departamento, 'tipo_dir': tipo_dir,
        'n1': n1, 'letra': letra, 'n2': n2, 'n3': n3, 'rol': rol,
    }

    # Validaciones básicas
    if not all([nombre, apellido, username, cedula, ciudad, tipo_dir, n1, n2, n3, rol]):
        messages.error(request, "Por favor completa todos los campos obligatorios")
        return redirect('completar_registro_google')

    # Verificar que el username no exista
    if User.objects.filter(username=username).exists():
        messages.error(request, "Ese nombre de usuario ya está en uso")
        return redirect('completar_registro_google')

    # Verificar que la cédula no exista
    if Usuario.objects.filter(cedula=cedula).exists():
        messages.error(request, "Esa cédula ya está registrada")
        return redirect('completar_registro_google')

    try:
        # Actualizar el User de Django con el username
        user = request.user
        user.username   = username
        user.first_name = nombre
        user.last_name  = apellido
        user.email      = google_correo
        user.save()

        # Crear Usuario extendido
        usuario = Usuario.objects.create(
            user         = user,
            nombre       = nombre,
            apellido     = apellido,
            nombre_usuario = username,
            correo       = google_correo,
            cedula       = cedula,
            ciudad       = ciudad,
            departamento = departamento,
            direccion    = direccion,
            telefono     = telefono,
            rol          = rol,
            estado       = True
        )

        # Crear perfil según rol
        if rol == 'CLIENTE':
            Cliente.objects.create(
                id_usuario   = usuario,
                preferencias = request.POST.get('preferencias', 'Sin preferencias')
            )
        elif rol == 'PRODUCTOR':
            Productor.objects.create(
                id_usuario   = usuario,
                tipo_cultivo = request.POST.get('tipo_cultivo', '')
            )
        elif rol == 'TRANSPORTISTA':
            Transportista.objects.create(
                id_usuario    = usuario,
                zonas_entrega = request.POST.get('zonas_entrega', '')
            )
        elif rol == 'ASESOR':
            Asesor.objects.create(
                id_usuario    = usuario,
                tipo_asesoria = request.POST.get('tipo_asesoria', '')
            )

        # Limpiar sesión de Google
        for key in ['google_nombre', 'google_apellido', 'google_correo',
                    'google_foto', 'google_user_id', 'google_form_data']:
            request.session.pop(key, None)

        messages.success(request, f"¡Bienvenido a Agrolink, {nombre}!")

        # Redirigir según rol
        if rol == 'CLIENTE':
            return redirect('mostrar_productos')
        elif rol == 'ADMINISTRADOR':
            return redirect('ver_listas_usuarios_admin')
        elif rol == 'TRANSPORTISTA':
            return redirect('inicio_transportista')
        elif rol == 'PRODUCTOR':
            return redirect('lista_productos')
        elif rol == 'ASESOR':
            return redirect('asesor_servicios')
        else:
            return redirect('mostrar_productos')

    except Exception as e:
        messages.error(request, f"Error al guardar el registro: {str(e)}")
        return redirect('completar_registro_google')

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
    productores = Productor.objects.select_related('id_usuario').prefetch_related('finca_set').all()
    transportistas = Transportista.objects.select_related('id_usuario').all()
    asesores = Asesor.objects.select_related('id_usuario').all()
    
    #conteo de usuarios
    total_clientes =Cliente.objects.filter().count()
    total_productores = Productor.objects.filter(id_usuario__estado=True).count()
    total_transportistas=Transportista.objects.filter(id_usuario__estado=True).count()
    total_asesores=Asesor.objects.filter(id_usuario__estado=True).count()
    
    #notificaciones no leidas para el admin
    try:
        usuario_admin = Usuario.objects.get(user=request.user)
        notificaciones_no_leidas = Notificacion.objects.filter(destino=usuario_admin, leido=False).count()
    except Usuario.DoesNotExist:
        notificaciones_no_leidas = 0
    
    return render(request, 'admin_usuarios/dashboard.html', {
        'clientes': clientes,
        'productores': productores,
        'transportistas': transportistas,
        'asesores': asesores,
        
        'total_clientes':total_clientes,
        'total_productores':total_productores,
        'total_transportistas': total_transportistas,
        'total_asesores': total_asesores,
        
        'notificaciones_no_leidas': notificaciones_no_leidas,
    })
    
    
#@admin_required
def ver_lista_productos_admin(request):
    productos = Producto.objects.select_related('id_usuario', 'id_categoria').all()
    categorias = CategoriaProducto.objects.all()
    
    total_producto = Producto.objects.filter().count()
    stock_alto = Producto.objects.filter(stock__gte=100).count()
    stock_bajo = Producto.objects.filter(stock__lt=50).count()
    productores_activos= Producto.objects.values('id_usuario').distinct().count()
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'total_productos': total_producto,
        'stock_alto': stock_alto,
        'stock_bajo': stock_bajo,
        'productores_activos': productores_activos
    }
    
    return render(request, 'admin_productos/index.html', context )
    
@login_required
def crear_producto_admin(request):

    producto_form = ProductoForm()
    imagen_form   = ImagenPrincipalForm()
    finca_form    = ProductoFincaForm()
    productores   = Productor.objects.all()

    if request.method == 'POST':

        producto_form = ProductoForm(request.POST)
        imagen_form   = ImagenPrincipalForm(request.POST, request.FILES)

        # Obtener productor seleccionado
        productor_id = request.POST.get('id_usuario')
        productor = None

        if productor_id:
            try:
                productor = Productor.objects.get(pk=productor_id)
            except Productor.DoesNotExist:
                productor = None

        # Formulario finca
        finca_form = ProductoFincaForm(
            request.POST,
            productor=productor,
            validate_finca=True
        )

        # Debug temporal
        print("Producto errors:", producto_form.errors)
        print("Imagen errors:", imagen_form.errors)
        print("Finca errors:", finca_form.errors)

        # Validaciones
        if (
            producto_form.is_valid() and
            imagen_form.is_valid() and
            finca_form.is_valid()
        ):

            # =========================
            # 1. Guardar producto
            # =========================
            producto_creado = producto_form.save()

            # =========================
            # 2. Guardar imagen
            # =========================
            if request.FILES.get('url_imagen'):

                imagen = imagen_form.save(commit=False)
                imagen.id_producto = producto_creado
                imagen.es_principal = 1
                imagen.save()

            # =========================
            # 3. Guardar relación finca
            # =========================
            producto_finca = finca_form.save(commit=False)
            producto_finca.id_producto = producto_creado
            producto_finca.save()

            # =========================
            # Mensaje éxito
            # =========================
            messages.success(
                request,
                f'Producto "{producto_creado.nombre_producto}" creado exitosamente.'
            )

            return redirect('ver_lista_productos_admin')

        else:
            messages.error(
                request,
                'Por favor corrige los errores del formulario.'
            )

    context = {
        'form': producto_form,
        'imagen_form': imagen_form,
        'finca_form': finca_form,
        'productores': productores,
        'fincas_json': _fincas_por_productor(),
    }

    return render(
        request,
        'admin_productos/crear_producto.html',
        context
    )



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

def toggle_estado_producto_admin(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    producto.estado = not producto.estado
    producto.save()
    accion = "inhabilitado" if not producto.estado else "habilitado"
    messages.success(request, f"Producto {producto.nombre_producto} {accion} correctamente")
    return redirect('ver_lista_productos_admin')



@admin_required
def ver_lista_pedidos_admin(request):

    compras = Compra.objects.select_related('id_cliente__id_usuario').prefetch_related('detallescompra_set').order_by('-fecha_hora_compra')

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
        'id_transportista__id_usuario',
        'id_vehiculo'
    ).all().order_by('-fecha_salida')
    
    hoy = datetime.now()

    # 🔹 KPIs GENERALES
    total_envios = Envio.objects.count()

    envios_activos = Envio.objects.filter(
        estado_envio="En_Transito"
    ).count()

    envios_entregados = Envio.objects.filter(
        estado_envio="Entregado"
    ).count()

    envios_pendientes = Envio.objects.filter(
        estado_envio="Asignado"
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
        'costo_envios': costo_total_envios,

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

        "costo_base": int(float(envio.costo_base or 0)),
        "costo_peso": int(float(envio.costo_peso or 0)),
        "costo_total": int(float(envio.costo_total or 0)),

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

    #  KPIs
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
    servicio = get_object_or_404(Servicio, id_servicio=servicio_id)

    # Cambiar el estado propio del servicio
    if servicio.estado == "activo":
        servicio.estado = "inactivo"
    else:
        servicio.estado = "activo"

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
        elif rol.upper() == "ASESOR":
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

def toggle_estado_usuario(request, id):
    usuario = get_object_or_404(Usuario, id_usuario=id)
    usuario.estado = not usuario.estado
    usuario.save()
    accion = "bloqueado" if not usuario.estado else "desbloqueado"
    messages.success(request, f"Usuario {usuario.nombre} {usuario.apellido} {accion} correctamente")
    return redirect('ver_listas_usuarios_admin')


def ver_usuario(request, id):
    usuario = Usuario.objects.get(id_usuario=id)
    
    vehiculos = None
    if usuario.rol == 'TRANSPORTISTA':
        try:
            transportista = Transportista.objects.get(id_usuario=usuario)
            vehiculos = Vehiculo.objects.filter(id_transportista=transportista)
        except Transportista.DoesNotExist:
            pass
    
    fincas = None
    if usuario.rol == 'PRODUCTOR':
        try:
            productor = Productor.objects.get(id_usuario=usuario)
            fincas = Finca.objects.filter(id_usuario=productor)
        except Productor.DoesNotExist:
            pass
    
    return render(request, 'admin_usuarios/ver_usuario.html', {
        'usuario': usuario,
        'vehiculos': vehiculos,
        'fincas': fincas,
    })


# Notificaciones admin
@login_required
def listar_notificaciones(request):
    try:
        usuario_obj = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        return redirect('login_view')

    notificaciones = Notificacion.objects.filter(destino=usuario_obj).order_by('-fecha_creacion')
    no_leidas = notificaciones.filter(leido=False).count()

    return render(request, 'admin_usuarios/notificaciones.html', {
        'notificaciones': notificaciones,
        'no_leidas': no_leidas,
    })


@login_required
def marcar_notificacion_leida(request, notif_id):
    notificacion = get_object_or_404(Notificacion, id_notificacion=notif_id)
    notificacion.leido = True
    notificacion.save()
    return redirect('listar_notificaciones')


@login_required
def aprobar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id_vehiculo=vehiculo_id, estado='PENDIENTE')
    vehiculo.estado = 'ACTIVO'
    vehiculo.save()

    transportista = vehiculo.id_transportista
    Notificacion.objects.create(
        tipo='APROBACION_VEHICULO',
        mensaje=f"Tu vehículo {vehiculo.placa_vehiculo} ha sido aprobado por el administrador.",
        destino=transportista.id_usuario,
        id_vehiculo=vehiculo
    )

    notif_pendientes = Notificacion.objects.filter(
        id_vehiculo=vehiculo, tipo='SOLICITUD_VEHICULO', leido=False
    )
    notif_pendientes.update(leido=True)

    messages.success(request, f"Vehículo {vehiculo.placa_vehiculo} aprobado correctamente")
    return redirect('listar_notificaciones')


@login_required
def rechazar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id_vehiculo=vehiculo_id, estado='PENDIENTE')
    vehiculo.estado = 'RECHAZADO'
    vehiculo.save()

    transportista = vehiculo.id_transportista
    Notificacion.objects.create(
        tipo='RECHAZO_VEHICULO',
        mensaje=f"Tu vehículo {vehiculo.placa_vehiculo} ha sido rechazado por el administrador.",
        destino=transportista.id_usuario,
        id_vehiculo=vehiculo
    )

    notif_pendientes = Notificacion.objects.filter(
        id_vehiculo=vehiculo, tipo='SOLICITUD_VEHICULO', leido=False
    )
    notif_pendientes.update(leido=True)

    messages.success(request, f"Vehículo {vehiculo.placa_vehiculo} rechazado")
    return redirect('listar_notificaciones')


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

                if not usuario.estado:
                    logout(request)
                    messages.error(request, "Tu cuenta está bloqueada. Contacta al administrador.")
                    return redirect('login_view')

                rol = usuario.rol.upper()
                messages.success(request, f"Login correcto. Rol detectado: {rol}")
                print(f"ROL DETECTADO: '{usuario.rol}'")

                if rol == 'CLIENTE':
                    return redirect('mostrar_productos') 
                # productos/inicio
                elif rol == 'ADMINISTRADOR':
                    return redirect('ver_listas_usuarios_admin')

                elif rol == 'TRANSPORTISTA' :
                    return redirect('inicio_transportista')
                
                elif rol == 'PRODUCTOR':
                    return redirect('lista_productos')
                
                elif rol == 'ASESOR' : 
                    return redirect('asesor_servicios')

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


def solicitar_codigo_recuperacion(request):
    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip()
        if not correo:
            messages.error(request, "Por favor ingresa tu correo electrónico")
            return render(request, 'usuarios/Recuperar_password.html', {'paso': 'email'})

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            messages.error(request, "No se encontró una cuenta con ese correo")
            return render(request, 'usuarios/Recuperar_password.html', {'paso': 'email'})

        codigo = str(random.randint(100000, 999999))
        request.session['codigo_recuperacion'] = codigo
        request.session['correo_recuperacion'] = correo
        request.session['usuario_id'] = usuario.id_usuario

        try:
            send_mail(
                'Código de recuperación - AgroLink',
                f'Tu código de verificación es: {codigo}\n\nEste código expira en 10 minutos.',
                settings.EMAIL_HOST_USER,
                [correo],
                fail_silently=False,
            )
            messages.success(request, "Se ha enviado un código de verificación a tu correo")
        except Exception as e:
            messages.error(request, f"Error al enviar el correo: {str(e)}")
            return render(request, 'usuarios/Recuperar_password.html', {'paso': 'email'})

        return render(request, 'usuarios/Recuperar_password.html', {'paso': 'codigo', 'correo': correo})

    return render(request, 'usuarios/Recuperar_password.html', {'paso': 'email'})


def verificar_codigo_recuperacion(request):
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo', '').strip()
        codigo_session = request.session.get('codigo_recuperacion')

        if not codigo_ingresado:
            messages.error(request, "Por favor ingresa el código de verificación")
            return render(request, 'usuarios/Recuperar_password.html', {
                'paso': 'codigo',
                'correo': request.session.get('correo_recuperacion', '')
            })

        if codigo_ingresado == codigo_session:
            return render(request, 'usuarios/Recuperar_password.html', {
                'paso': 'nueva_contrasena',
                'correo': request.session.get('correo_recuperacion', '')
            })
        else:
            messages.error(request, "El código ingresado es incorrecto")
            return render(request, 'usuarios/Recuperar_password.html', {
                'paso': 'codigo',
                'correo': request.session.get('correo_recuperacion', '')
            })

    return redirect('solicitar_codigo_recuperacion')


def establecer_nueva_contrasena(request):
    if request.method == 'POST':
        nueva_contrasena = request.POST.get('nueva_contrasena', '').strip()
        confirmar_contrasena = request.POST.get('confirmar_contrasena', '').strip()

        if not nueva_contrasena or not confirmar_contrasena:
            messages.error(request, "Por favor completa todos los campos")
            return render(request, 'usuarios/Recuperar_password.html', {
                'paso': 'nueva_contrasena',
                'correo': request.session.get('correo_recuperacion', '')
            })

        if nueva_contrasena != confirmar_contrasena:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, 'usuarios/Recuperar_password.html', {
                'paso': 'nueva_contrasena',
                'correo': request.session.get('correo_recuperacion', '')
            })

        if len(nueva_contrasena) < 8:
            messages.error(request, "La contraseña debe tener al menos 8 caracteres")
            return render(request, 'usuarios/Recuperar_password.html', {
                'paso': 'nueva_contrasena',
                'correo': request.session.get('correo_recuperacion', '')
            })

        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "Sesión expirada, solicita un nuevo código")
            return redirect('solicitar_codigo_recuperacion')

        try:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
            user = usuario.user
            if user:
                user.set_password(nueva_contrasena)
                user.save()
                messages.success(request, "Contraseña actualizada correctamente. Ya puedes iniciar sesión")

                del request.session['codigo_recuperacion']
                del request.session['correo_recuperacion']
                del request.session['usuario_id']

                return redirect('login_view')
            else:
                messages.error(request, "Error al actualizar la contraseña")
                return render(request, 'usuarios/Recuperar_password.html', {
                    'paso': 'nueva_contrasena',
                    'correo': request.session.get('correo_recuperacion', '')
                })
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
            return redirect('solicitar_codigo_recuperacion')

    return redirect('solicitar_codigo_recuperacion')


# ============================================================
#  REPORTES PDF - ADMIN
# ============================================================

def reporte_inventario_admin_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario_agrolink.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    elementos = []

    # Header
    elementos.append(Paragraph("AGROLINK - Reporte de Inventario", styles['Title']))
    elementos.append(Spacer(1, 8))
    elementos.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elementos.append(Spacer(1, 16))

    # Resumen
    total_productos = Producto.objects.count()
    stock_alto = Producto.objects.filter(stock__gte=100).count()
    stock_bajo = Producto.objects.filter(stock__lt=50).count()
    productores_activos = Producto.objects.values('id_usuario').distinct().count()

    elementos.append(Paragraph("Resumen", styles['Heading2']))
    data_resumen = [
        ["Indicador", "Valor"],
        ["Total Productos", str(total_productos)],
        ["Stock Alto (≥100)", str(stock_alto)],
        ["Stock Bajo (<50)", str(stock_bajo)],
        ["Productores Activos", str(productores_activos)],
    ]
    t = Table(data_resumen, colWidths=[250, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2f6b31')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8e2')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8faf7')),
    ]))
    elementos.append(t)
    elementos.append(Spacer(1, 20))

    # Productos por categoría
    elementos.append(Paragraph("Productos por Categoría", styles['Heading2']))
    elementos.append(Spacer(1, 8))

    productos = Producto.objects.select_related('id_categoria', 'id_usuario__id_usuario').all()
    data = [["Producto", "Categoría", "Stock", "Precio", "Productor"]]
    for p in productos:
        data.append([
            p.nombre_producto,
            p.id_categoria.nombre_categoria if p.id_categoria else "-",
            str(p.stock or 0),
            f"${int(p.precio or 0):,}",
            f"{p.id_usuario.id_usuario.nombre} {p.id_usuario.id_usuario.apellido}" if p.id_usuario else "-",
        ])

    t = Table(data, colWidths=[130, 100, 60, 80, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1d4820')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8e2')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f8faf7')]),
        ('ALIGN', (2, 0), (3, -1), 'CENTER'),
    ]))
    elementos.append(t)

    doc.build(elementos)
    return response


def reporte_pedidos_admin_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas_agrolink.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    elementos = []

    # Header
    elementos.append(Paragraph("AGROLINK - Reporte de Ventas", styles['Title']))
    elementos.append(Spacer(1, 8))
    elementos.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elementos.append(Spacer(1, 16))

    # Resumen
    hoy = datetime.now()
    total_pedidos = Compra.objects.count()
    total_ventas = Compra.objects.aggregate(total=Sum('total'))['total'] or 0
    pedidos_mes = Compra.objects.filter(
        fecha_hora_compra__year=hoy.year, fecha_hora_compra__month=hoy.month
    ).count()
    ventas_mes = Compra.objects.filter(
        fecha_hora_compra__year=hoy.year, fecha_hora_compra__month=hoy.month
    ).aggregate(total=Sum('total'))['total'] or 0

    elementos.append(Paragraph("Resumen", styles['Heading2']))
    data_resumen = [
        ["Indicador", "Valor"],
        ["Total Pedidos", str(total_pedidos)],
        ["Ingresos Totales", f"${int(total_ventas):,}"],
        ["Pedidos del Mes", str(pedidos_mes)],
        ["Ventas del Mes", f"${int(ventas_mes):,}"],
    ]
    t = Table(data_resumen, colWidths=[250, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2f6b31')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8e2')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8faf7')),
    ]))
    elementos.append(t)
    elementos.append(Spacer(1, 20))

    # Pedidos
    elementos.append(Paragraph("Listado de Pedidos", styles['Heading2']))
    elementos.append(Spacer(1, 8))

    compras = Compra.objects.select_related('id_cliente__id_usuario').all()
    data = [["#", "Cliente", "Fecha", "Subtotal", "Total"]]
    for c in compras:
        data.append([
            str(c.id_compra),
            f"{c.id_cliente.id_usuario.nombre} {c.id_cliente.id_usuario.apellido}" if c.id_cliente else "-",
            c.fecha_hora_compra.strftime('%d/%m/%Y') if c.fecha_hora_compra else "-",
            f"${int(c.subtotal or 0):,}",
            f"${int(c.total or 0):,}",
        ])

    t = Table(data, colWidths=[50, 140, 80, 100, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1d4820')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8e2')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f8faf7')]),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
    ]))
    elementos.append(t)

    doc.build(elementos)
    return response


def reporte_envios_admin_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_envios_agrolink.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    elementos = []

    # Header
    elementos.append(Paragraph("AGROLINK - Reporte de Envíos", styles['Title']))
    elementos.append(Spacer(1, 8))
    elementos.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elementos.append(Spacer(1, 16))

    # Resumen
    total_envios = Envio.objects.count()
    envios_activos = Envio.objects.filter(estado_envio="En_Transito").count()
    envios_entregados = Envio.objects.filter(estado_envio="Entregado").count()
    envios_pendientes = Envio.objects.filter(estado_envio="Asignado").count()
    costo_total = Envio.objects.aggregate(total=Sum('costo_total'))['total'] or 0

    elementos.append(Paragraph("Resumen", styles['Heading2']))
    data_resumen = [
        ["Indicador", "Valor"],
        ["Total Envíos", str(total_envios)],
        ["En tránsito", str(envios_activos)],
        ["Entregados", str(envios_entregados)],
        ["Pendientes", str(envios_pendientes)],
        ["Costo Total Acumulado", f"${int(costo_total):,}"],
    ]
    t = Table(data_resumen, colWidths=[250, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2f6b31')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8e2')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8faf7')),
    ]))
    elementos.append(t)
    elementos.append(Spacer(1, 20))

    # Envíos
    elementos.append(Paragraph("Listado de Envíos", styles['Heading2']))
    elementos.append(Spacer(1, 8))

    envios = Envio.objects.select_related(
        'id_transportista__id_usuario', 'id_compra'
    ).all()
    data = [["#Envío", "Transportista", "Estado", "Distancia (km)", "Costo"]]
    for e in envios:
        data.append([
            f"ENV-{e.id_envio}",
            f"{e.id_transportista.id_usuario.nombre} {e.id_transportista.id_usuario.apellido}" if e.id_transportista else "No asignado",
            e.estado_envio or "-",
            str(e.distancia_km or 0),
            f"${int(e.costo_total or 0):,}",
        ])

    t = Table(data, colWidths=[80, 150, 90, 90, 90])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1d4820')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8e2')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f8faf7')]),
        ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
    ]))
    elementos.append(t)

    doc.build(elementos)
    return response