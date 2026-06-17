from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Servicio, Maquinas, Certificados
from usuarios.models import Asesor, Usuario
from envios.models import Envio
from calificaciones.models import Calificacion
from django.db.models import Avg, Count
from productos.models import Producto


@login_required
def asesor_servicios(request):

    # Validar existencia de usuario extendido
    if not hasattr(request.user, 'usuario'):
        return redirect('login_view')

    usuario = request.user.usuario

    # Validar rol
    if usuario.rol.upper().strip() != 'ASESOR':
        return redirect('mostrar_productos')

    asesor, _ = Asesor.objects.get_or_create(id_usuario=usuario)

    if request.method == 'POST':

        # =========================
        # 🗑️ ELIMINAR
        # =========================
        if request.POST.get("eliminar_id"):

            try:
                servicio = Servicio.objects.get(
                    id_servicio=request.POST.get("eliminar_id"),
                    id_asesor=asesor
                )

                servicio.delete()

                messages.success(
                    request,
                    "Servicio eliminado correctamente"
                )

            except Servicio.DoesNotExist:

                messages.error(
                    request,
                    "El servicio no existe"
                )

        # =========================
        # ✏️ EDITAR
        # =========================
        elif request.POST.get("id_servicio"):

            try:
                servicio = Servicio.objects.get(
                    id_servicio=request.POST.get("id_servicio"),
                    id_asesor=asesor
                )

                servicio.categoria = request.POST.get("categoria")
                servicio.descripcion = request.POST.get("descripcion")
                servicio.estado = request.POST.get("estado")

                servicio.save()

                messages.success(
                    request,
                    "Servicio actualizado correctamente"
                )

            except Servicio.DoesNotExist:

                messages.error(
                    request,
                    "No se pudo editar el servicio"
                )

        # =========================
        # ➕ CREAR
        # =========================
        else:

            Servicio.objects.create(
                id_asesor=asesor,
                categoria=request.POST.get('categoria'),
                descripcion=request.POST.get('descripcion'),
                estado=request.POST.get('estado')
            )

            # Crear certificados asociados al asesor
            tipos_cert = request.POST.getlist('tipo_certificado[]')
            descripciones_cert = request.POST.getlist('descripcion_cert[]')
            fechas_cert = request.POST.getlist('fecha_expedicion[]')

            for tipo, desc, fecha in zip(tipos_cert, descripciones_cert, fechas_cert):
                if tipo.strip() and desc.strip() and fecha.strip():
                    Certificados.objects.create(
                        id_usuario=asesor,
                        tipo_certificado=tipo.strip(),
                        descripcion_cert=desc.strip(),
                        fecha_expedicion=fecha
                    )

            messages.success(
                request,
                "Servicio publicado correctamente"
            )

        return redirect('asesor_servicios')

    servicios = Servicio.objects.filter(id_asesor=asesor)
    certificados = Certificados.objects.filter(id_usuario=asesor)

    return render(request, 'servicios/asesor.html', {
        'servicios': servicios,
        'certificados': certificados,
    })


@login_required
def maquinas_asesor(request):

    # Validar existencia de usuario extendido
    if not hasattr(request.user, 'usuario'):
        return redirect('login_view')

    usuario = request.user.usuario

    # Validar rol
    if usuario.rol.upper().strip() != 'ASESOR':
        return redirect('mostrar_productos')

    asesor, _ = Asesor.objects.get_or_create(id_usuario=usuario)

    # =========================
    # ➕ CREAR MÁQUINA
    # =========================
    if request.method == 'POST':

        Maquinas.objects.create(
            id_asesor=asesor,
            tipo_maquina=request.POST.get('tipo_maquina'),
            modelo=request.POST.get('modelo'),
            documento_propiedad=request.POST.get('documento_propiedad'),
            registro_rnma=request.POST.get('registro_rnma'),
            tarjeta_registro_maquinaria=request.POST.get(
                'tarjeta_registro_maquinaria'
            )
        )

        messages.success(
            request,
            "Máquina registrada correctamente"
        )

        return redirect('maquinas_asesor')

    maquinas = Maquinas.objects.filter(id_asesor=asesor)

    return render(request, 'servicios/mis_maquinas.html', {
        'maquinas': maquinas
    })


def detalles_servicios(request, id):

    servicio = get_object_or_404(
        Servicio,
        id_servicio=id
    )

    return render(
        request,
        'servicios/servicios_publicados/servicio_publicado.html',
        {
            'servicio': servicio
        }
    )


def lista_servicios(request):

    servicios = Servicio.objects.filter(
        estado__iexact='activo'
    )

    total_usuarios = Usuario.objects.count()
    total_productos = Producto.objects.count()
    total_entregados = Envio.objects.filter(estado_envio__iexact='entregado').count()
    total_envios = Envio.objects.count()
    porcentaje_entregas = round((total_entregados / total_envios) * 100, 1) if total_envios > 0 else 0
    calificacion_promedio = Calificacion.objects.aggregate(avg=Avg('puntaje_producto'))['avg'] or 0

    return render(
        request,
        'servicios/servicios_publicados/base_servicios.html',
        {
            'servicios': servicios,
            'total_usuarios': total_usuarios,
            'total_productos': total_productos,
            'total_entregados': total_entregados,
            'porcentaje_entregas': porcentaje_entregas,
            'calificacion_promedio': calificacion_promedio,
        }
    )


# ==========================================
# PERFIL ASESOR
# ==========================================

@login_required
def perfil_asesor(request):

    if not hasattr(request.user, 'usuario'):
        return redirect('login_view')

    usuario = request.user.usuario

    # Validar rol
    if usuario.rol.upper().strip() != 'ASESOR':
        return redirect('mostrar_productos')

    asesor = get_object_or_404(
        Asesor,
        id_usuario=usuario
    )

    context = {
        'asesor': asesor,
        'es_dueno': True,
        'url_volver': 'asesor_servicios',
    }

    return render(
        request,
        'perfil_asesor.html',
        context
    )


@login_required
def editar_perfil_asesor(request):

    if request.method == "POST":

        try:

            usuario = request.user.usuario

            asesor = Asesor.objects.get(
                id_usuario=usuario
            )

            correo = request.POST.get("correo")
            cedula = request.POST.get("cedula")

            # =====================================
            # VALIDAR CORREO O CÉDULA DUPLICADA
            # =====================================

            existe = Usuario.objects.filter(
                Q(correo=correo) |
                Q(cedula=cedula)
            ).exclude(
                id_usuario=usuario.id_usuario
            ).exists()

            if existe:

                messages.error(
                    request,
                    "❌ Correo o cédula ya en uso"
                )

                return redirect('perfil_asesor')

            # =====================================
            # DATOS USUARIO
            # =====================================

            usuario.nombre = request.POST.get("nombre")
            usuario.apellido = request.POST.get("apellido")
            usuario.correo = correo
            usuario.telefono = request.POST.get("telefono")
            usuario.ciudad = request.POST.get("ciudad")
            usuario.cedula = cedula

            if 'foto_perfil' in request.FILES:
                usuario.foto_perfil = request.FILES['foto_perfil']

            # =====================================
            # DATOS ASESOR
            # =====================================

            asesor.tipo_asesoria = request.POST.get(
                "tipo_asesoria"
            )

            usuario.save()
            asesor.save()

            messages.success(
                request,
                "✅ Perfil actualizado correctamente"
            )

        except Exception as e:

            print("ERROR EDITAR PERFIL ASESOR:", e)

            messages.error(
                request,
                "❌ Error al actualizar el perfil"
            )

    return redirect('perfil_asesor')