from django.urls import path
from django.conf.urls import url, include

from . import views

app_name= "main"
urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('transfer/', views.money_transfer, name='money_transfer'),
    path('payments/', views.service_payment, name='service_payment'),
]