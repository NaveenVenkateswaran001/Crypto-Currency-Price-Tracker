# Generated by Django 5.1 on 2024-09-08 20:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Crypto_app', '0026_mywallet_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coindetails',
            name='current_price',
        ),
        migrations.RemoveField(
            model_name='coindetails',
            name='total_volume',
        ),
    ]
