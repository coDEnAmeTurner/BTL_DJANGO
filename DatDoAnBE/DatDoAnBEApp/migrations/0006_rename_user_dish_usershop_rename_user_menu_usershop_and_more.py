# Generated by Django 5.0.1 on 2024-02-12 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DatDoAnBEApp', '0005_order_dish'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dish',
            old_name='user',
            new_name='userShop',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='user',
            new_name='userShop',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='user',
            new_name='userShop',
        ),
    ]