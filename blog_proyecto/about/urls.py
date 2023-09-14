from django.urls import path
from . import views

urlpatterns = [
    path('acerca_de/', views.acerca_de, name='acerca_de'),
]