from django.shortcuts import render
from rest_framework import viewsets,mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShopCartSerializer,ShopCartDetailSerializer,OrderSerializer,OrderDetailSerializer
from .models import ShoppingCart,OrderInfo,OrderGoods

# Create your views here.


class ShoppingCartViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSerializer
    lookup_field = 'goods_id' #查询商品的id

    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer


    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user) #返回当前用户的购物车列表


class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order