from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class EntradaBlog(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200)
    cuerpo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='imagenes_blog/')
    categoria = models.CharField(max_length=100)
    
    def __str__(self):
        return self.titulo