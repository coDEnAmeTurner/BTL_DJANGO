# Generated by Django 5.0.1 on 2024-02-12 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DatDoAnBEApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='userType',
            field=models.CharField(choices=[('GENERAL', 'General'), ('SHOP', 'Shop')], default='GENERAL', max_length=7),
        ),
    ]
