# Generated by Django 3.2 on 2021-05-21 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210521_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='customer_id',
        ),
    ]
