from django import forms
from .models import EntradaBlog
class EntradaBlogForm(forms.ModelForm):
    class Meta:
        model = EntradaBlog
        fields = ['titulo', 'subtitulo', 'cuerpo', 'imagen', 'categoria']