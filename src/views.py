from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.urls import reverse
from django.core.checks import messages
from AppGUI import AppGUI
from django.shortcuts import render
from .models import ArquivoForm

app_name = 'calendar'

def convertView(request):
    if request.method == 'POST':
        form = ArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['arquivo']
            app = appGUI()
            app.convert_button_clicked(uploaded_file)
    else:
        form = ArquivoForm()
    return render(request, 'homePage.html', {'form': form})