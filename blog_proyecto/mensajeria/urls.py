from django.urls import path
from . import views

urlpatterns = [
    # URL para la lista de conversaciones
    path('lista-conversaciones/', views.lista_conversaciones, name='lista_conversaciones'),

    # URL para ver una conversación específica
    path('ver-conversacion/<int:conversacion_id>/', views.ver_conversacion, name='ver_conversacion'),
]