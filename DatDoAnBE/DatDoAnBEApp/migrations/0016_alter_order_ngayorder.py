# Generated by Django 5.0.1 on 2024-02-20 08:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DatDoAnBEApp', '0015_order_tongtien_order_userconsumer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ngayOrder',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]