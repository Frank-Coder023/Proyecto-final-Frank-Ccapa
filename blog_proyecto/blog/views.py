from django.shortcuts import render,redirect, get_object_or_404
from .models import EntradaBlog
from .forms import EntradaBlogForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def inicio(request):
    # Tu lógica para la página de inicio aquí
    return render(request, "blog/inicio.html")

def lista_entradas(request):
    entradas = EntradaBlog.objects.all()
    return render(request, 'blog/lista_entradas.html', {'entradas': entradas})

def detalle_entrada(request, entrada_id):
    entrada = get_object_or_404(EntradaBlog, pk=entrada_id)
    return render(request, 'blog/detalle_entrada.html', {'entrada': entrada})


@login_required
def crear_entrada_blog(request):
    mensaje = ""
    
    if request.method == 'POST':
        form = EntradaBlogForm(request.POST, request.FILES)
        if form.is_valid():
            info = form.cleaned_data
            titulo = info["titulo"]
            subtitulo = info["subtitulo"]
            cuerpo = info["cuerpo"]
            categoria = info["categoria"]
            
            # Agrega el campo de imagen al formulario y guárdalo en el modelo
            imagen = request.FILES.get('imagen')

            nueva_entrada = EntradaBlog(
                titulo=titulo,
                subtitulo=subtitulo,
                cuerpo=cuerpo,
                categoria=categoria,
                autor=request.user,  # Asignar al usuario actual como autor
                imagen=imagen  # Guardar la imagen en la entrada de blog
            )
            nueva_entrada.save()
            mensaje = "Entrada de blog creada"
        else:
            mensaje = "Datos inválidos"

    # Obtener todas las entradas de blog después de crear una nueva
    entradas_blog = EntradaBlog.objects.all()
    formulario_entrada = EntradaBlogForm()

    return render(
        request,
        "blog/crear_entrada_blog.html",
        {"mensaje": mensaje, "formulario": formulario_entrada, "entradas_blog": entradas_blog},
    )

@login_required
def editar_entrada_blog(request, pk):
    mensaje = ""
    entrada = get_object_or_404(EntradaBlog, pk=pk)
    
    # Verificar si el usuario actual es el autor de la entrada
    usuario_es_autor = entrada.autor == request.user  # Comprueba si el usuario es el autor

    if not usuario_es_autor:
        # Si el usuario no es el autor, puedes redirigirlo o mostrar un mensaje de error
        mensaje = "No tienes permiso para editar esta entrada."

    if request.method == 'POST' and usuario_es_autor:
        form = EntradaBlogForm(request.POST, request.FILES, instance=entrada)
        if form.is_valid():
            info = form.cleaned_data  # Obtener datos limpios del formulario
            entrada.titulo = info["titulo"]
            entrada.subtitulo = info["subtitulo"]
            entrada.cuerpo = info["cuerpo"]
            entrada.categoria = info["categoria"]
            
            # Actualizar la imagen si se proporciona una nueva
            if 'imagen' in request.FILES:
                entrada.imagen = request.FILES['imagen']
            
            entrada.save()
            mensaje = "Entrada de blog editada correctamente"
        else:
            mensaje = "Datos inválidos"

    formulario_entrada = EntradaBlogForm(instance=entrada)

    return render(
        request,
        "blog/editar_entrada_blog.html",
        {"mensaje": mensaje, "formulario": formulario_entrada, "entrada": entrada, "usuario_es_autor": usuario_es_autor}
    )

@login_required
def eliminar_entrada_blog(request, pk):
    entrada = get_object_or_404(EntradaBlog, pk=pk)

    # Verificar si el usuario actual es el autor de la entrada
    if entrada.autor != request.user:
        # Si el usuario no es el autor, puedes redirigirlo o mostrar un mensaje de error
        mensaje = "No tienes permiso para eliminar esta entrada."
        return render(
            request,
            "blog/eliminar_entrada_blog.html",
            {"mensaje": mensaje, "entrada": entrada}
        )

    if request.method == 'POST':
        entrada.delete()
        return redirect('lista_entradas')  # Redirige a la lista de entradas después de la eliminación

    return render(
        request,
        "blog/eliminar_entrada_blog.html",
        {"entrada": entrada}
    )