#from django.forms import ModelForm
from logging import PlaceHolder
from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["titel", "description", "important"]
        widgets = {
            "titel": forms.TextInput(attrs={'class':'form-control', "placeholder":"Escriba un titulo"}),
            "description": forms.Textarea(attrs={'class':'form-control', "placeholder":"Escriba una descripcion"}),
            "important": forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }