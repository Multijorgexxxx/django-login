from django import forms
from .models import tareas


class tareasForm(forms.ModelForm):
    
    class Meta:
        model = tareas
        fields = ("titulo","descripcion","es_importante")
