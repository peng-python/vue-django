from django.shortcuts import render
from rest_framework import mixins,viewsets,filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import GoodsSerializer,CategorySerializer,IndexCategorySerializer,BannerSerializer
from .models import Goods,GoodsCategory,Banner
from .filters import GoodsFilter

# Create your views here.


# class GoodsPagination(PageNumberPagination):
#     page_size = 12
#     page_size_query_param = 'page_size'
#     page_query_param = "page"
#     max_page_size = 100
class GoodPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    # 商品列表页，包括分页，搜索，过滤和排序
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        isinstance = self.get_object()
        isinstance.click_num += 1
        isinstance.save()
        serializer = self.get_serializer(isinstance)
        return Response(serializer.data)


class CategoryViewset(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    # 获取商品类目
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer


class IndexCategoryViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    # 首页商品分类数据
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['生鲜食品', '酒水饮料'])
    serializer_class = IndexCategorySerializer