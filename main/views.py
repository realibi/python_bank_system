from django.shortcuts import render, redirect, reverse
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


def login(request):
    if request.method == "POST":
        login = request.POST.get("login", None)
        password = request.POST.get("password", None)
        try:
            customer = Customer.objects.get(customer_login=login, customer_password=password)
            print("trying to find customer")
            if customer:
                print("customer not null")
                account = Account.objects.filter(customer=customer)[0]
                request.session["user_id"] = account.id
                request.session["user_number"] = account.number
                return redirect(reverse('main:index'))
        except:
            print("something went wrong")
            return render(request, "login.html", {})
    else:
        return render(request, "login.html", {})


def money_transfer(request):
    print("money transfer is starting")
    if request.method == "POST":
        current_account_id = int(request.session["user_id"])
        print(current_account_id)
        receiver_number = request.POST.get("receiver_number", None)
        amount = int(request.POST.get("amount", None))
        try:
            sender_account = Account.objects.get(id=current_account_id)
            receiver_account = Account.objects.get(number=receiver_number)
            if receiver_account:
                if sender_account.balance >= amount:
                    sender_account.balance = sender_account.balance - amount
                    print(sender_account.balance)
                    sender_account.save()

                    print("receiver_account found!")
                    receiver_account.balance = receiver_account.balance + amount
                    
                
                    receiver_account.save()
                    return redirect(reverse('main:index'))
        except:
            print("something went wrong")
            return render(request, "login.html", {})
    else:
        return render(request, "transfer.html", {})


def service_payment(request):
    print("service payment is starting")
    if request.method == "POST":
        current_account_id = int(request.session["user_id"])
        amount = int(request.POST.get("amount", None))
        try:
            sender_account = Account.objects.get(pk=current_account_id)
            print(sender_account)
            
            if sender_account.balance >= amount:
                sender_account.balance = sender_account.balance - amount
                print(sender_account.balance)
                sender_account.save()
        
                return redirect(reverse('main:index'))
        except:
            print("something went wrong")
            return render(request, "login.html", {})
    else:
        return render(request, "payments.html", {})