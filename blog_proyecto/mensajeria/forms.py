from django import forms
from .models import Mensaje

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido']  # Define los campos que se mostrarán en el formulario
from django import forms

class CrearConversacionForm(forms.Form):
    # Puedes agregar campos adicionales si es necesario, pero por lo general,
    # solo necesitas el nombre de usuario del destinatario.
    destinatario = forms.CharField(max_length=150)