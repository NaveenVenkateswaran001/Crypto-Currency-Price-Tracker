# Generated by Django 5.1 on 2024-08-30 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Crypto_app', '0007_coindetails_price_change_1h_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coindetails',
            name='price_change_1h',
        ),
        migrations.RemoveField(
            model_name='coindetails',
            name='price_change_24h',
        ),
    ]
