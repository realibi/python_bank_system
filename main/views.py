from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer, Account

# Create your views here.
def index(request):
    return render(request, "registration.html", {
        
    })

def registration(request):
    if request.method == 'POST':
        login = request.POST.get("login", None)
        password = request.POST.get("password", None)
        name = request.POST.get("name", None)
        surname = request.POST.get("surname", None)

        if not password or not login or not name or not surname:
            return HttpResponse("reg data not given")

        customer = Customer(customer_login=login, customer_password=password, customer_name=name, customer_surname=surname)
        account = Account(customer=customer, balance=0, number=123)
        customer.save()
        account.save()

        return HttpResponse("registered successfully")
        
    else:
        return HttpResponse("handling get")