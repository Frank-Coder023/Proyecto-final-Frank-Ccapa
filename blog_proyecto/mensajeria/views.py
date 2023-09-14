from django.shortcuts import render, redirect, get_object_or_404
from .models import Conversacion, Mensaje
from .forms import MensajeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CrearConversacionForm

@login_required
def listar_conversaciones_autor(request):
    conversaciones = Conversacion.objects.filter(usuario_1=request.user) | Conversacion.objects.filter(usuario_2=request.user)
    return render(request, 'mensajeria/listar_conversaciones_autor.html', {'conversaciones': conversaciones})

@login_required
def ver_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, id=conversacion_id)
    
    if request.user not in [conversacion.usuario_1, conversacion.usuario_2]: # Verificar si el usuario actual está involucrado en la conversación
        return redirect('lista_conversaciones_autor')  # Redirige si no está involucrado
    
    mensajes = Mensaje.objects.filter(conversacion=conversacion).order_by('fecha_envio')
    # Marcar mensajes como vistos y guardarlos en la base de datos
    for mensaje in mensajes:
        if mensaje.remitente != request.user and not mensaje.visto:
            mensaje.visto = True
            mensaje.save()
    
    # Se envia un nuevo mensaje con lo siguiente
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.conversacion = conversacion
            mensaje.remitente = request.user
            mensaje.save()
            return redirect('ver_conversacion', conversacion_id=conversacion_id)
    else:
        form = MensajeForm()

    return render(request, 'mensajeria/ver_conversacion.html', {'conversacion': conversacion, 'mensajes': mensajes, 'form': form})

@login_required
def crear_conversacion(request, username):
    # Encuentra al usuario destinatario (el autor del blog)
    destinatario = User.objects.get(username=username)
    
    # Verifica si ya existe una conversación entre el usuario actual y el destinatario
    conversacion_existente = Conversacion.objects.filter(
        usuario_1=request.user,
        usuario_2=destinatario
    ).first()
    
    if conversacion_existente:
        # Si ya existe una conversación, redirige a la vista de ver_conversacion
        return redirect('ver_conversacion', conversacion_id=conversacion_existente.id)
    else:
        # Si no existe una conversación, crea una nueva conversación
        nueva_conversacion = Conversacion(usuario_1=request.user, usuario_2=destinatario)
        nueva_conversacion.save()
        # Redirige a la vista de ver_conversacion para la nueva conversación
        return redirect('ver_conversacion', conversacion_id=nueva_conversacion.id)


@login_required
def eliminar_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, id=conversacion_id)

    # Verificar si el usuario actual está involucrado en la conversación
    if request.user not in [conversacion.usuario_1, conversacion.usuario_2]:
        return redirect('listar_conversaciones_autor')  # Redirige si no está involucrado

    if request.method == 'POST':
        conversacion.delete()
        return redirect('listar_conversaciones_autor')

    return render(request, 'mensajeria/eliminar_conversacion.html', {'conversacion': conversacion})