# Generated by Django 3.2 on 2021-05-21 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_customer_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_login',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_password',
            field=models.CharField(default='', max_length=25),
        ),
    ]
