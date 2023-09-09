from django.contrib import admin

# Register your models here.
from .models import Conversacion, Mensaje

# Register your models here.
admin.site.register(Conversacion)
admin.site.register(Mensaje)