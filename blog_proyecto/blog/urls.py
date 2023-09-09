from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Establece la vista de inicio como la URL raíz
    path('lista_entradas/', views.lista_entradas, name='lista_entradas'),
    path('entrada/<int:entrada_id>/', views.detalle_entrada, name='detalle_entrada'),
    path('crear_entrada/', views.crear_entrada_blog, name='crear_entrada'),
    path('editar_entrada/<int:pk>/', views.editar_entrada_blog, name='editar_entrada'),
    path('eliminar_entrada/<int:pk>/', views.eliminar_entrada_blog, name='eliminar_entrada'),

]