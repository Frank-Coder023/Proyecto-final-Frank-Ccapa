from django.shortcuts import render, redirect, get_object_or_404
from .models import Conversacion, Mensaje
from .forms import MensajeForm

from django.contrib.auth.decorators import login_required

def lista_conversaciones(request):
    conversaciones = Conversacion.objects.filter(participantes=request.user)
    return render(request, 'mensajeria/lista_conversaciones.html', {'conversaciones': conversaciones})


@login_required
def ver_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, id=conversacion_id, participantes=request.user)
    mensajes = Mensaje.objects.filter(conversacion=conversacion)

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
