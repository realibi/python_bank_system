from django.db import models


# Create your models here.
# image = models.ImageField(upload_to='club_images', blank=True, null=True)

class Customer(models.Model):
    customer_login = models.CharField(max_length=25, default="")
    customer_password = models.CharField(max_length=25, default="")
    customer_name = models.CharField(max_length=25)
    customer_surname = models.CharField(max_length=25)


class Service_type(models.Model):
    service_type_name = models.CharField(max_length=50)


class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    number = models.IntegerField(default=0)


class Deposits(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField()
    balance = models.IntegerField(default=0)


class Service(models.Model):
    service_name = models.CharField(max_length=50)
    service_desc = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    service_type = models.ForeignKey(Service_type, on_delete=models.CASCADE)


class Account_type(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    desc = models.CharField(max_length=255)


class Transfer(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='%(class)ssender_account')
    amount = models.IntegerField(default=0)
    transaction_type = models.BooleanField()
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='%(class)sreceiver_account')
    transaction_date = models.DateTimeField(auto_now_add=True)
