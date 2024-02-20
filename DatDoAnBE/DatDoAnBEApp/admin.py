from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission, ContentType, Group


class DishAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ten', 'userShop', 'tienThucAn', 'isAvailable', 'buoi', 'chuThich']


class MenuAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ten', 'userShop']


class ShopAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user']


class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ngayOrder', 'userShop', 'userConsumer']
    readonly_fields = ['ngayOrder']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'dish', 'parentComment']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['pk', 'rating', 'dish']


# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Permission)
admin.site.register(ContentType)
