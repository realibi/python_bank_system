from django.urls import path
from django.conf.urls import url, include

from . import views

app_name= "main"
urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registration, name='registration'),
]
#