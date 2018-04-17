from rest_framework import serializers
import time

from goods.serializers import GoodsSerializer
from .models import ShoppingCart,OrderGoods,OrderInfo
from goods.models import Goods


class ShopCartDetailSerializer(serializers.ModelSerializer): # 购物车详情
    goods = GoodsSerializer(many=False, read_only=True)
    class Meta:
        model = ShoppingCart
        fields = ('goods', 'nums')


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(required=True, label='数量', min_value=1,
                                    error_messages={
                                        'min_value':'商品数量不能小于1',
                                        'required':'请选择购买数量'
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all()) # 返回对应goods的主键

    def create(self, validated_data):
        # 获得对应的用户名，商品数量和对应的商品
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = ShoppingCart.objects.filter(user=user, goods=goods) #查询该用户对应的该商品是否在购物车中

        if existed:  # 如果在购物车中
            existed = existed[0]
            existed.nums += nums # 则在原来的数量上+1
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data) # 创建该购物车

        return existed

    def update(self, instance, validated_data):
        # 修改商品的数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer): # 订单商品
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer): #订单详情
    goods = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # 获取到当前用户
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)

    def generate_order_sn(self): #订单号
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime('%Y%m%dH%M%S'),
                                                       userid=self.context['request'].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'