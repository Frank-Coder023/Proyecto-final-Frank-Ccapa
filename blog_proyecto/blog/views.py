from django.shortcuts import render,redirect, get_object_or_404
from .models import EntradaBlog
from .forms import EntradaBlogForm
from django.contrib.auth.decorators import login_required



# IMPORTANTE: MENSAJES
from mensajeria.models import Conversacion


# Create your views here.
def inicio(request):
    return render(request, "blog/inicio.html")

def lista_entradas(request):
    entradas = EntradaBlog.objects.all()
    return render(request, 'blog/lista_entradas.html', {'entradas': entradas})

#Nueva version para poder detallar las entradas de los blogs
@login_required
def detalle_entrada(request, entrada_id):
    entrada = get_object_or_404(EntradaBlog, pk=entrada_id)
    
    # Verificar si ya existe una conversación entre el autor y el usuario actual
    conversacion = Conversacion.objects.filter(
        usuario_1=entrada.autor,
        usuario_2=request.user
    ).first()

    contexto = {
        'entrada': entrada,
        'conversacion': conversacion,
    }

    return render(request, 'blog/detalle_entrada.html', contexto)

# Codigo anterior solo lista las entradas mas no ayuda cuando se genera una conversacion entre 2 usuarios
def detalle_entrada2(request, entrada_id):
    entrada = get_object_or_404(EntradaBlog, pk=entrada_id)
    return render(request, 'blog/detalle_entrada.html', {'entrada': entrada})


# Nueva version para crear entradas de blog
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
            imagen = request.FILES.get('imagen')

            # Crea la entrada de blog sin asociar una conversación
            nueva_entrada = EntradaBlog(
                titulo=titulo,
                subtitulo=subtitulo,
                cuerpo=cuerpo,
                categoria=categoria,
                autor=request.user,
                imagen=imagen,
            )
            nueva_entrada.save()
            conversacion, creado = Conversacion.objects.get_or_create(usuario_1=request.user, usuario_2=request.user) # Asociamos la conversación a la entrada de blog
            nueva_entrada.conversacion = conversacion
            nueva_entrada.save()

            mensaje = "Entrada de blog creada y conversación iniciada"
        else:
            mensaje = "Datos inválidos"

    # Obtener todas las entradas de blog después de crear una nueva esto se vera mejor en la view
    entradas_blog = EntradaBlog.objects.all()
    formulario_entrada = EntradaBlogForm()

    return render(
        request,
        "blog/crear_entrada_blog.html",
        {"mensaje": mensaje, "formulario": formulario_entrada, "entradas_blog": entradas_blog},
    )

#Version anterior para crear una entrada de blog no esta enlazada con mensajeria 
@login_required
def crear_entrada_blog2(request):
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
                imagen=imagen  # Guardara la imagen en la entrada de blog
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
    usuario_es_autor = entrada.autor == request.user  # Comprueba si el usuario es el autor que creo el blog o posteo

    if not usuario_es_autor:
        # Si el usuario no es el autor, le mostrara un mensaje
        mensaje = "No tienes permiso para editar esta entrada."

    if request.method == 'POST' and usuario_es_autor:
        form = EntradaBlogForm(request.POST, request.FILES, instance=entrada)
        if form.is_valid():
            info = form.cleaned_data  # Obtener datos limpios del formulario
            entrada.titulo = info["titulo"]
            entrada.subtitulo = info["subtitulo"]
            entrada.cuerpo = info["cuerpo"]
            entrada.categoria = info["categoria"]
            
            # Actualiza la imagen si se proporciona una nueva
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
        # Si el usuario no es el autor, mostrara un mensaje de error
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

#view que ayuudara a que se pueda iniciar una conversaicion entre un usuario y otro 
@login_required
def iniciar_conversacion(request, entrada_id):
    entrada = get_object_or_404(EntradaBlog, pk=entrada_id)
    usuario_autor = entrada.autor
    usuario_actual = request.user

    # Verificar si ya existe una conversación entre el autor y el usuario actual
    conversacion = Conversacion.objects.filter(
        usuario_1=usuario_autor,
        usuario_2=usuario_actual
    ).first()

    if conversacion is None:
        # Si no existe una conversación, crea una nueva
        conversacion = Conversacion(usuario_1=usuario_autor, usuario_2=usuario_actual)
        conversacion.save()

    # Redirige al usuario a la vista de ver_conversacion que esta en mensajeria
    return redirect('ver_conversacion', conversacion_id=conversacion.id)
