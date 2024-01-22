from django import forms
from .models import Tarefa
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = '__all__'