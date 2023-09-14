from django.shortcuts import render

# Create your views here.
def acerca_de(request):
    return render(request, 'about/acerca_de.html')