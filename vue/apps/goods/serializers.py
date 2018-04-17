from rest_framework import serializers

from goods.models import GoodsCategory,Goods,GoodsImage,Banner,IndexAd,GoodsCategoryBrand


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image', )


class GoodsSerializer(serializers.ModelSerializer): #商品
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer): #轮播图片
    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer): #获取商品类目
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class IndexCategorySerializer(serializers.ModelSerializer): #首页商品类目
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField() #取第一类目下的所有商品
    sub_cat = CategorySerializer2(many=True) #取二级商品类目
    ad_goods = serializers.SerializerMethodField() #获取首页第一类目下的广告

    # def get_ad_goods(self, obj):
    #     goods_json = {}
    #     ad_goods = IndexAd.objects.filter(category_id=obj.id, )
    #     if ad_goods:
    #         good_ins = ad_goods[0].goods
    #         goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
    #     return goods_json
    #
    # def get_goods(self, obj):
    #     all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
    #         category__parent_category__parent_category_id=obj.id))
    #     goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
    #     return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = '__all__'