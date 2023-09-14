from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroUsuarioForm
from .models import Perfil
from .forms import EditarPerfilForm
from django.contrib.auth.decorators import login_required 

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            info = form.cleaned_data
            username = info["username"]
            password = info["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')  # Cambia 'inicio' por la URL de tu página de inicio
            else:
                return render(request, "usuarios/login.html", {"form": form, "mensaje": "Credenciales inválidas"})
        else:
            return render(request, "usuarios/login.html", {"form": form, "mensaje": "Datos inválidos"})
    else:
        form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form})

def signup(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            # Crea el usuario
            user = form.save()
            
            # Crea el perfil asociado
            nombre = form.cleaned_data['nombre']
            apellidos = form.cleaned_data['apellidos']
            descripcion = form.cleaned_data['descripcion']
            imagen_de_perfil = form.cleaned_data['imagen_de_perfil']
            
            perfil = Perfil(usuario=user, nombre=nombre, apellidos=apellidos, descripcion=descripcion, imagen_de_perfil=imagen_de_perfil)
            perfil.save()
            
            # Inicia sesión al usuario recién registrado
            login(request, user)
            
            return redirect('inicio')  # Cambia 'inicio' por la URL de tu página de inicio
        else:
            return render(request, "usuarios/register.html", {"form": form, "mensaje": "Datos inválidos"})
    else:
        form = RegistroUsuarioForm()
    return render(request, "usuarios/register.html", {"form": form})

@login_required
def logout_request(request):
    logout(request)
    return redirect('inicio')  # Cambia 'inicio' por la URL de tu página de inicio

@login_required
def confirm_delete_account(request):
    if request.method == 'POST':
        perfil = request.user.perfil
        if perfil.imagen_de_perfil.name != 'perfiles/avatarpordefecto.png':
            perfil.imagen_de_perfil.delete()
        # Si el usuario confirma la eliminación de la cuenta, procede con la eliminación.
        request.user.delete()
        return redirect('inicio')  # O cualquier otra página que desees después de la eliminación.
    
    return render(request, 'usuarios/confirm_delete_account.html')

@login_required
def ver_perfil(request, username):
    perfil = get_object_or_404(Perfil, usuario__username=username)
    return render(request, "usuarios/ver_perfil.html", {"perfil": perfil})

@login_required
def editar_perfil(request, username):
    perfil = get_object_or_404(Perfil, usuario__username=username)

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil)

        if form.is_valid():
            form.save()
            return render(request, 'usuarios/ver_perfil.html', {'perfil': perfil})  
        
    else:
        form = EditarPerfilForm(instance=perfil)

    return render(request, 'usuarios/editar_perfil.html', {'form': form, 'perfil': perfil})
