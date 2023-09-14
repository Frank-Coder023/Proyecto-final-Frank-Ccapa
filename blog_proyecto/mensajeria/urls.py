from django.urls import path
from . import views

urlpatterns = [
    # URL para la lista de conversaciones
    #path('lista-conversaciones/', views.lista_conversaciones, name='lista_conversaciones'),

    # URL para ver una conversación específica
    path('conversacion/<int:conversacion_id>/', views.ver_conversacion, name='ver_conversacion'),

    #path('conversaciones/', views.lista_conversaciones, name='lista_conversaciones'),
    path('crear_conversacion/<str:username>/', views.crear_conversacion, name='crear_conversacion'),
    path('listar_conversaciones/', views.listar_conversaciones_autor, name='listar_conversaciones_autor'),
    path('eliminar_conversacion/<int:conversacion_id>/', views.eliminar_conversacion, name='eliminar_conversacion'),
]