from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    imagen_de_perfil = models.ImageField(upload_to='perfiles/', default='perfiles/avatarpordefecto.png')

    # Otros campos como redes sociales, etc.

    def __str__(self):
        return self.usuario.username