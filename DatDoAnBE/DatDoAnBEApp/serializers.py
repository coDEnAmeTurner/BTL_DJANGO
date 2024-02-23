from rest_framework.serializers import ModelSerializer

from .models import User, Shop, Dish, Menu, Order, Comment, Rating, Category


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'userType', 'avatar']


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'tongTien': {
                'read_only': True
            },
            'ngayOrder': {
                'read_only': True
            },
            'isValid': {
                'read_only': True
            },
            'userConsumer': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        user = self.context['request'].user
        data = validated_data.copy()
        order = Order(loaiThanhToan=data['loaiThanhToan'], userShop=data['userShop'])
        order.userConsumer = user
        order.save()
        list = data['dish']
        userShopDishes = Dish.objects.filter(userShop=order.userShop.pk)
        for inst in list:
            if inst in userShopDishes and inst.isAvailable:
                order.dish.add(inst)

        order.tongTien = order.tinhTongTien()
        order.save()

        return order


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs={
            'shopUser': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        cat = Category(**validated_data)
        cat.shopUser = self.context['request'].user
        cat.save()
        return cat


class DishSerializer(ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'
        extra_kwargs = {
            'userShop': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        user = self.context['request'].user
        data = validated_data.copy()
        dish = Dish(**data, userShop=user)
        dish.save()

        return dish


class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
        extra_kwargs = {
            'userShop': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        user = self.context['request'].user
        data = validated_data.copy()
        menu = Menu(ten=data['ten'], userShop=user)
        menu.save()
        list = data['dish']
        for id in list:
            menu.dish.add(id)

        return menu


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


