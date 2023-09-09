from django.urls import path
from .views import *
app_name = 'usuarios'  # Define un espacio de nombres para la aplicación 'usuarios'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name='logout'),
    path('<str:username>/editar/', editar_perfil, name='editar_perfil'),
    path('accounts/<str:username>/', ver_perfil, name='ver_perfil'),
    path('eliminar_cuenta/', confirm_delete_account, name='confirmar_eliminar_cuenta'),
]