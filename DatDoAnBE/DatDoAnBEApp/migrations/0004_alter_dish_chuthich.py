# Generated by Django 5.0.1 on 2024-02-12 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DatDoAnBEApp', '0003_remove_dish_shop_remove_menu_shop_remove_order_shop_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='chuThich',
            field=models.TextField(blank=True),
        ),
    ]