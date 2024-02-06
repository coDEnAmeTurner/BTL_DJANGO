from django.contrib.auth.models import AbstractUser
from django.db import models
from enum import Enum
from django_enumfield import enum


class LoaiThanhToan(Enum):
    PAYPAL = 1
    STRIPE = 2
    MOMO = 3
    ZALOPAY = 4
    CASH = 5

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='%Y/%m', null=False)
    ten = models.CharField(max_length=100)
    email = models.CharField()
    sdt = models.CharField()

    def __str__(self):
        return self.ten + ' ' + self.email + ' ' + self.sdt


class Shop(User):
    diaDiem = models.CharField()
    isValid = models.BooleanField(default=False)
    user = models.ManyToManyField(User, related_name='user')
    tienVanChuyen = models.IntegerField(null=False)


class BaseModel(models.Model):
    ten = models.CharField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __self__(self):
        return self.ten


class Menu(BaseModel):
    shop = models.ForeignKey(Shop, models.SET_NULL, related_name='shop')


class Dish(BaseModel):
    shop = models.ForeignKey(Shop, models.SET_NULL, related_name='shop')
    menu = models.ManyToManyField(Menu, related_name='menu')


class Order(models.Model):
    #tienThanhToan =
    ten = models.CharField(default='Hoa Don')
    isValid = models.BooleanField(default=False)
    loaiThanhToan = enum.EnumField(LoaiThanhToan, default=LoaiThanhToan.CASH)
    ngayOrder = models.DateTimeField(auto_now=True)
    dish = models.ManyToManyField(Dish, related_name='dish')

    def tinhTienThanhToan(self):
        #chua viet
        pass