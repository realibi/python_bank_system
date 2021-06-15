import random
from datetime import datetime

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Customer, Account, Transfer, Deposits


# Create your views here.
def index(request):
    return render(request, "index.html", {

    })


def registration(request):
    if request.method == 'POST':
        login = request.POST.get("login", None)
        password = request.POST.get("password", None)
        name = request.POST.get("name", None)
        surname = request.POST.get("surname", None)

        if not password or not login or not name or not surname:
            return HttpResponse("reg data not given")

        customer = Customer(customer_login=login, customer_password=password, customer_name=name,
                            customer_surname=surname)
        n = random.randint(100, 999)

        while Account.objects.filter(number=n).exists():
            n = random.randint(100, 999)

        account = Account(customer=customer, balance=0, number=n)
        customer.save()
        account.save()

        return redirect(reverse('main:login'))

    else:
        return render(request, "registration.html", {})


def myBank(request):
    if request.session.get("user_id") is not None:
        current_account_id = int(request.session.get("user_id"))
        account = Account.objects.get(id=current_account_id)

        deposit_customer = Customer.objects.get(id=current_account_id)

        deposit_objects = Deposits.objects.filter(customer=deposit_customer)
        if len(deposit_objects) == 0:
            deposit_info = "no deposit account"
        else:
            deposit = Deposits.objects.get(customer=deposit_customer)
            deposit_info = str(deposit.balance)

        return render(request, "mybank.html", {"account": account,"deposit_info": deposit_info})
    else:
        return redirect(reverse('main:index'))


def deposits(request):
    if request.session.get("user_id") is not None:

        return render(request, "deposit.html", {})
    else:
        return redirect(reverse('main:index'))


def deposit_money(request):
    if request.method == "POST":
        current_account_id = int(request.session.get("user_id"))
        amount = int(request.POST.get("amount", None))
        date = datetime.now()
        try:
            deposit_account = Account.objects.get(id=current_account_id)
            deposit_customer = Customer.objects.get(id=current_account_id)
            if deposit_account.balance >= amount:
                deposit_objects = Deposits.objects.filter(customer=deposit_customer)
                if len(deposit_objects) == 0:
                    deposit = Deposits(customer=deposit_customer, date=date, balance=amount)
                    deposit.save()
                    deposit_account.balance = deposit_account.balance - amount
                    deposit_account.save()
                    return redirect(reverse('main:mybank'))
                else:
                    print("false")
                    deposit = Deposits.objects.get(customer=deposit_customer)
                    deposit.balance += amount
                    deposit.save()
                    deposit_account.balance = deposit_account.balance - amount
                    deposit_account.save()
                    return redirect(reverse('main:mybank'))
        except:
            print("something went wrong")
            return redirect(reverse('main:mybank'))


def withdraw(request):
    if request.method == "POST":
        current_account_id = int(request.session.get("user_id"))
        amount = int(request.POST.get("amount", None))
        withdraw_date = datetime.now()
    try:

        deposit_customer = Customer.objects.get(id=current_account_id)
        deposit_account = Account.objects.get(id=current_account_id)
        deposit_objects = Deposits.objects.filter(customer=deposit_customer)
        if len(deposit_objects) == 0:
            print("user don't have deposit account")
            return redirect(reverse('main:mybank'))
        else:
            deposit = Deposits.objects.get(customer=deposit_customer)
            deposit.balance = deposit.balance - amount
            deposit.save()
            difference = withdraw_date - deposit.date.replace(tzinfo=None)

            if difference.days >= 30:
                multiplier = difference.days/30
                reward = amount + ((amount/100)*(9*multiplier))
                deposit_account.balance += reward
                deposit_account.save()
            else:
                deposit_account.balance += amount
                deposit_account.save()

            return redirect(reverse('main:mybank'))
    except:
        print("something went wrong")
        return redirect(reverse('main:mybank'))


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
                return redirect(reverse('main:mybank'))
        except:
            print("something went wrong")
            return render(request, "login.html", {})
    else:
        return render(request, "login.html", {})


def logout(request):
    del request.session["user_id"]
    del request.session["user_number"]
    return redirect(reverse('main:index'))


def money_transfer(request):
    print("money transfer is starting")
    if request.method == "POST":
        current_account_id = int(request.session.get("user_id"))
        print(current_account_id)
        receiver_number = request.POST.get("receiver_number", None)
        amount = int(request.POST.get("amount", None))
        try:
            sender_account = Account.objects.get(id=current_account_id)
            receiver_account = Account.objects.get(number=receiver_number)
            if receiver_account:
                if sender_account.balance >= amount:
                    transfer = Transfer(account=sender_account, amount=amount, transaction_type=True,
                                        receiver=receiver_account)
                    print("transfer: ")
                    print(transfer)
                    transfer.save()
                    sender_account.balance = sender_account.balance - amount
                    print(sender_account.balance)
                    sender_account.save()

                    print("receiver_account found!")
                    receiver_account.balance = receiver_account.balance + amount

                    receiver_account.save()
                    return redirect(reverse('main:mybank'))
        except:
            print("something went wrong")
            return redirect(reverse('main:money_transfer'))
    else:
        if request.session.get("user_id") is not None:
            return render(request, "transfer.html", {})
        else:
            return render(request, "login.html", {})


def service_payment(request):
    print("service payment is starting")
    if request.method == "POST":
        current_account_id = int(request.session.get("user_id"))
        amount = int(request.POST.get("amount", None))
        service_name = request.POST.get("service_name", None)
        try:
            sender_account = Account.objects.get(pk=current_account_id)
            print(sender_account)

            if sender_account.balance >= amount:
                sender_account.balance = sender_account.balance - amount
                print(sender_account.balance)
                sender_account.save()

                return redirect(reverse('main:mybank'))
        except:
            print("something went wrong")
            return redirect(reverse('main:mybank'))
    else:
        if request.session.get("user_id") is not None:
            return render(request, "payments.html", {})
        else:
            return render(request, "login.html", {})


def history(request):
    print("history is starting")
    if request.method == "POST":
        print("hello")
    else:
        if request.session.get("user_id") is not None:
            current_account_id = int(request.session.get("user_id"))
            current_user_account = Account.objects.get(id=current_account_id)

            user_transfers = Transfer.objects.filter(account=current_user_account)

            return render(request, "history.html", {"transfers": user_transfers})
        else:
            return render(request, "login.html", {})
