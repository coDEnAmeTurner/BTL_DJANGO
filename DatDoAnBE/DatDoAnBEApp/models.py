from django.contrib.auth.models import AbstractUser
from django.db import models
from enum import Enum


# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='%Y/%m', null=False)
    sdt = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.username + ' ' + self.email + ' ' + self.sdt


class Shop(User):
    diaDiem = models.CharField(max_length=255)
    isValid = models.BooleanField(default=False)
    user = models.ManyToManyField(User, related_name='shops')
    tienVanChuyen = models.FloatField(null=False)


class BaseModel(models.Model):
    ten = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __self__(self):
        return self.ten


class Menu(BaseModel):
    shop = models.ForeignKey(Shop, models.CASCADE, related_name='menus')


class Dish(BaseModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='dishes')
    menu = models.ManyToManyField(Menu, related_name='dishes')
    tienThucAn = models.FloatField(null=True)
    isAvailable = models.BooleanField(default=True)

    class Buoi(models.TextChoices):
        SANG = 'SANG'
        TRUA = 'TRUA'
        CHIEU = 'CHIEU'

    buoi = models.CharField(max_length=5, choices=Buoi, default=Buoi.SANG)
    chuThich = models.TextField()


class Order(models.Model):
    ten = models.CharField(max_length=50, default='Hoa Don')
    isValid = models.BooleanField(default=False)

    class LoaiThanhToan(models.TextChoices):
        PAYPAL = 'PAYPAL'
        STRIPE = 'STRIPE'
        MOMO = 'MOMO'
        ZALOPAY = 'ZALOPAY'
        CASH = 'CASH'

    loaiThanhToan = models.CharField(max_length=7, choices=LoaiThanhToan, default=LoaiThanhToan.CASH)
    ngayOrder = models.DateTimeField(auto_now=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders')
