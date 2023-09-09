from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Conversacion(models.Model):
    participantes = models.ManyToManyField(User, related_name='conversaciones')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ", ".join([str(user) for user in self.participantes.all()])

class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    remitente = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    visto = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.remitente}: {self.contenido}"