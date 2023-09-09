from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    nombre = forms.CharField(max_length=50, required=True)
    apellidos = forms.CharField(max_length=50, required=True)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)
    imagen_de_perfil = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "nombre", "apellidos", "descripcion", "imagen_de_perfil"]
        help_texts = {campo: "" for campo in fields}

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nombre', 'apellidos', 'descripcion', 'imagen_de_perfil']
