from django.urls import path
from . import views

urlpatterns = [
    path('convertView/', views.convert_button_clicked, name='convert'),
]