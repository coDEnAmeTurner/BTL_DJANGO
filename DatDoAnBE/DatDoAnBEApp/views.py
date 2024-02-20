import json

from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth, TruncDay, ExtractQuarter, ExtractYear, ExtractMonth
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, generics, parsers, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from . import perms
from .models import User, UserType, Shop, Dish, Menu, Order, Comment, Rating
from .serializers import *


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('create_shop'):
            return [perms.CreateShopPermission()]

        if self.action.__eq__('validate_shop'):
            return [perms.ValidateShopPermission()]

        if self.action.__eq__('post_menu'):
            return [perms.BaseShopPermission()]

        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='shop')
    def create_shop(self, request, pk):
        shop = Shop.objects.create(
            diaDiem=request.data.get('diaDiem'),
            tienVanChuyen=request.data.get('tienVanChuyen'),
            user=request.user
        )
        return Response(ShopSerializer(shop).data, status=status.HTTP_201_CREATED)

    @action(methods=['patch'], detail=True, url_path='validate-shop')
    def validate_shop(self, request, pk):
        user = self.get_object()
        if user.userType == UserType.SHOP:
            user.shop.isValid = True
            user.shop.save()
            return Response(ShopSerializer(user.shop).data, status=status.HTTP_200_OK)
        else:
            return Response(data={
                'error': 'this is not a shop'
            }, status=status.HTTP_400_BAD_REQUEST)


class DishViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action.__eq__('create'):
            return [perms.BaseShopPermission()]

        if self.action.__eq__('update_buoi') or self.action.__eq__('update-trangthai'):
            return [perms.UpdateDishPermission()]

        if self.action.__eq__('comment_dish') or self.action.__eq__('rate_dish'):
            return [perms.CommentDishPermission()]

        return super().get_permissions()

    def get_queryset(self):
        dishes = self.queryset
        ten = self.request.query_params.get('ten')
        tienFrom = self.request.query_params.get('tienFrom')
        tienTo = self.request.query_params.get('tienTo')
        buoi = self.request.query_params.get('buoi')
        isAvai = self.request.query_params.get('isAvai')
        if ten:
            dishes = dishes.filter(ten__icontains=ten)
        if tienFrom and tienTo:
            dishes = dishes.filter(tienVanChuyen__lte=tienTo, tienVanChuyen__gte=tienFrom)
        if buoi:
            dishes = dishes.filter(buoi=buoi)
        if isAvai:
            dishes = dishes.filter(isAvailable=isAvai)

        return dishes

    @action(methods=['patch'], detail=True, url_path='update-buoi')
    def update_buoi(self, request, pk):
        dish = self.get_object()
        dish.buoi = request.data.get('buoi')
        dish.save()

        return Response(DishSerializer(dish).data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True, url_path='update-trangthai')
    def update_trangthai(self, request, pk):
        dish = self.get_object()
        dish.isAvailable = request.data.get('isAvailable')
        dish.save()

        return Response(DishSerializer(dish).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='comment-dish')
    def comment_dish(self, request, pk):
        comment = Comment.objects.create(
            content=request.data.get('content'),
            dish=self.get_object()
        )

        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='rate-dish')
    def rate_dish(self, request, pk):
        rating = Rating.objects.create(
            rating=request.data.get('rating'),
            dish=self.get_object()
        )

        return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)


class MenuViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [perms.BaseShopPermission]


class OrderViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action.__eq__('create'):
            return [perms.CreateOrderPermission()]

        if self.action.__eq__('validate_order'):
            return [perms.ValidateOrderPermission()]

        if self.action.__eq__('retrieve'):
            return [perms.RetrieveOrderPermission()]

        if self.action.__eq__('shop_make_stats'):
            return [perms.BaseShopPermission()]

        return [permissions.AllowAny()]

    @action(methods=['patch'], detail=True, url_path='validate-order')
    def validate_order(self, request, pk):
        order = self.get_object()
        if order.dish.count() != 0:
            order.isValid = True
            order.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        else:
            order.delete()
            return Response(data={'action': 'the order was invalid and has just been deleted'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, url_path='shop-make-stats')
    def shop_make_stats(self, request):
        doanhThuTheoMonth = Dish.objects.filter(userShop=7) \
            .annotate(doanhThu=Count('orders__id') * F('tienThucAn'), month=ExtractMonth('orders__ngayOrder')) \
            .values('month', 'ten', 'doanhThu') \
            .order_by('month')

        doanhThuTheoQuy = Dish.objects.filter(userShop=7) \
            .annotate(doanhThu=Count('orders__id') * F('tienThucAn'), quy=ExtractQuarter('orders__ngayOrder')) \
            .values('quy', 'ten', 'doanhThu') \
            .order_by('quy')

        doanhThuTheoNam = Dish.objects.filter(userShop=7) \
            .annotate(doanhThu=Count('orders__id') * F('tienThucAn'), nam=ExtractYear('orders__ngayOrder')) \
            .values('nam', 'ten', 'doanhThu') \
            .order_by('nam')

        return Response(data={
            'doanhThuTheoThang': doanhThuTheoMonth,
            'doanhThuTheoQuy': doanhThuTheoQuy,
            'doanhThuTheoNam': doanhThuTheoNam

        })

    @action(methods=['get'], detail=False, url_path='superuser-make-stats')
    def superuser_make_stats(self, request):
        tanSuatTheoThang = Dish.objects.all().annotate(
            tanSuat=Count('orders__id'),
            thang=ExtractMonth('orders__ngayOrder'),
            cuaHang=F('orders__userShop__user__username'),
        ).values('thang', 'cuaHang', 'ten', 'tanSuat')

        tanSuatTheoQuy = Dish.objects.all().annotate(
            tanSuat=Count('orders__id'),
            quy=ExtractQuarter('orders__ngayOrder'),
            cuaHang=F('orders__userShop__user__username'),
        ).values('quy', 'cuaHang', 'ten', 'tanSuat')

        tanSuatTheoNam = Dish.objects.all().annotate(
            tanSuat=Count('orders__id'),
            nam=ExtractYear('orders__ngayOrder'),
            cuaHang=F('orders__userShop__user__username'),
        ).values('nam', 'cuaHang', 'ten', 'tanSuat')

        tongTienMoiMonTheoThang = Dish.objects.all().annotate(
            tongTien=Count('orders__id') * F('tienThucAn'),
            thang=ExtractMonth('orders__ngayOrder'),
            cuaHang=F('orders__userShop__user__username'),
        ).values('thang', 'cuaHang', 'ten', 'tongTien')

        tongTienMoiMonTheoQuy = Dish.objects.all().annotate(
            tongTien=Count('orders__id') * F('tienThucAn'),
            quy=ExtractQuarter('orders__ngayOrder'),
            cuaHang=F('orders__userShop__user__username'),
        ).values('quy', 'cuaHang', 'ten', 'tongTien')

        tongTienMoiMonTheoNam = Dish.objects.all().annotate(
            tongTien=Count('orders__id') * F('tienThucAn'),
            nam=ExtractYear('orders__ngayOrder'),
            cuaHang=F('orders__userShop__user__username'),
        ).values('nam', 'cuaHang', 'ten', 'tongTien')

        return Response(data={
            'tanSuatTheoThang': tanSuatTheoThang,
            'tanSuatTheoQuy': tanSuatTheoQuy,
            'tanSuatTheoNam': tanSuatTheoNam,
            'tongTienMoiMonTheoThang': tongTienMoiMonTheoThang,
            'tongTienMoiMonTheoQuy': tongTienMoiMonTheoQuy,
            'tongTienMoiMonTheoNam': tongTienMoiMonTheoNam,

        })


class CommentViewSet(viewsets.ViewSet, generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action.__eq__('comment_a_comment'):
            return [perms.CommentDishPermission()]

        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='comment-a-comment')
    def comment_a_comment(self, request, pk):
        comment = Comment.objects.create(
            content=request.data.get('content'),
            dish=self.get_object().dish,
            parentComment=self.get_object()
        )

        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
