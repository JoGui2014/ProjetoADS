from django import forms
from .models import Arquivo
from django.db import models

class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ['arquivo']