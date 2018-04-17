from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.serializers import GoodsSerializer
from .models import UserFav,UserLeavingMessage,UserAddress


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # 获取到当前用户

    class Meta:
        model = UserFav
        validators = [UniqueTogetherValidator(
            queryset=UserFav.objects.all(),
            fields=('user', 'goods'),
            message='已经收藏'
        )]  # 验证用户是否已经收藏，三个参数分别是明确验证唯一性的集合，即在收藏表，序列化类中存在的字段，如果验证失败后的提示

        fields = ('user', 'goods', 'id')


class LeavingMessageSerializer(serializers.ModelSerializer):  # 用户留言
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'message_type', 'subject', 'message', 'file', 'id', 'add_time')


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ('id', 'user', 'province', 'city', 'district', 'address',
                  'signer_name', 'add_time', 'signer_mobile')