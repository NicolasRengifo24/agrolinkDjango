# 🔹 PANEL DEL ASESO
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q 

from .models import Servicio, Maquinas
from usuarios.models import Asesor

@login_required
def asesor_servicios(request):

    if not hasattr(request.user, 'usuario'):
        return redirect('login_view')

    usuario = request.user.usuario

    if usuario.rol.upper().strip() != 'ASESOR':
        return redirect('servicios_cliente')

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
                messages.success(request, "✅ Servicio eliminado correctamente")
            except Servicio.DoesNotExist:
                messages.error(request, "❌ El servicio no existe")

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

                messages.success(request, "✏️ Servicio actualizado correctamente")

            except Servicio.DoesNotExist:
                messages.error(request, "❌ No se pudo editar el servicio")

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
            messages.success(request, "📢 Servicio publicado correctamente")

        return redirect('asesor_servicios')

    servicios = Servicio.objects.filter(id_asesor=asesor)

    return render(request, 'servicios/asesor.html', {
        'servicios': servicios
    })
    

@login_required
def maquinas_asesor(request):

    if not hasattr(request.user, 'usuario'):
        return redirect('login_view')

    usuario = request.user.usuario

    if usuario.rol.upper().strip() != 'ASESOR':
        return redirect('servicios_cliente')

    asesor, _ = Asesor.objects.get_or_create(id_usuario=usuario)

    # CREAR
    if request.method == 'POST':
        Maquinas.objects.create(
            id_asesor=asesor,
            tipo_maquina=request.POST.get('tipo_maquina'),
            modelo=request.POST.get('modelo'),
            documento_propiedad=request.POST.get('documento_propiedad'),
            registro_rnma=request.POST.get('registro_rnma'),
            tarjeta_registro_maquinaria=request.POST.get('tarjeta_registro_maquinaria')
        )
        return redirect('maquinas_asesor')

    maquinas = Maquinas.objects.filter(id_asesor=asesor)

    return render(request, 'servicios/mis_maquinas.html', {
        'maquinas': maquinas
    })    
    
    


def detalles_servicios(request, id):
    servicio = get_object_or_404(Servicio, id_servicio=id)

    return render(request, 'servicios/servicios_publicados/servicio_publicado.html', {
        'servicio': servicio
    })

    
def lista_servicios(request):
    servicios = Servicio.objects.filter(estado='ACTIVO')

    return render(request, 'servicios/servicios_publicados/base_servicios.html', {
    'servicios': servicios
})
    
    
# Perfil asesor 

@login_required
def perfil_asesor(request):
    usuario = request.user.usuario

    # 🔒 Validar rol
    if usuario.rol.upper() != 'ASESOR':
        return redirect('mostrar_productos')  # o donde quieras

    asesor = Asesor.objects.get(id_usuario=usuario)

    context = {
        'asesor': asesor,
        'es_dueno': True,
        'url_volver': 'asesor_servicios',  # ajusta si tienes otra vista
    }

    return render(request, 'perfil_asesor.html', context)
    

    from django.db.models import Q

@login_required
def editar_perfil_asesor(request):
    if request.method == "POST":
        try:
            usuario = request.user.usuario
            asesor = Asesor.objects.get(id_usuario=usuario)

            correo = request.POST.get("correo")
            cedula = request.POST.get("cedula")

            # 🔥 VALIDACIÓN UNIQUE
            if usuario.objects.filter(
                Q(correo=correo) | Q(cedula=cedula)
            ).exclude(id_usuario=usuario.id_usuario).exists():

                messages.error(request, "Correo o cédula ya en uso")
                return redirect('perfil_asesor')

            # Datos usuario
            usuario.nombre = request.POST.get("nombre")
            usuario.apellido = request.POST.get("apellido")
            usuario.correo = correo
            usuario.telefono = request.POST.get("telefono")
            usuario.ciudad = request.POST.get("ciudad")
            usuario.cedula = cedula

            # Datos asesor
            asesor.tipo_asesoria = request.POST.get("tipo_asesoria")

            usuario.save()
            asesor.save()

            messages.success(request, "Perfil actualizado correctamente")

        except Exception as e:
            print("ERROR:", e)
            messages.error(request, "Error al actualizar")

    return redirect('perfil_asesor')