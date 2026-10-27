from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db.models import Q
from django.shortcuts import render 

from .models import Shop, Category, Product
from .serializers import ShopSerializer, CategorySerializer, ProductSerializer
from .pagination import ShopPagination
from .permissions import IsOwnerOrReadOnly
from .filters import ProductFilter

SHOP_TAG = ['Магазины и Товары (Shop)']


@extend_schema_view(
    list=extend_schema(tags=SHOP_TAG, summary='Список магазинов'),
    retrieve=extend_schema(tags=SHOP_TAG, summary='Детали магазина по ID'),
    create=extend_schema(tags=SHOP_TAG, summary='Создать магазин (требуется авторизация)'),
    update=extend_schema(tags=SHOP_TAG, summary='Полностью обновить магазин (только владелец)'),
    partial_update=extend_schema(tags=SHOP_TAG, summary='Частично обновить магазин (только владелец)'),
    destroy=extend_schema(tags=SHOP_TAG, summary='Удалить магазин (только владелец)'),
)
class ShopViewSets(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    pagination_class = ShopPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'color']
    search_fields = ['name', 'color']
    ordering_fields = ['name', 'id']
    ordering = ['id']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(tags=SHOP_TAG, summary='Список категорий товаров'),
    retrieve=extend_schema(tags=SHOP_TAG, summary='Детали категории по ID'),
    create=extend_schema(tags=SHOP_TAG, summary='Создать новую категорию'),
    update=extend_schema(tags=SHOP_TAG, summary='Полностью обновить категорию'),
    partial_update=extend_schema(tags=SHOP_TAG, summary='Частично обновить категорию'),
    destroy=extend_schema(tags=SHOP_TAG, summary='Удалить категорию'),
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = ShopPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'id']
    ordering = ['id']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]


@extend_schema_view(
    list=extend_schema(tags=SHOP_TAG, summary='Каталог товаров (пагинация, поиск, фильтры)'),
    retrieve=extend_schema(tags=SHOP_TAG, summary='Детали товара по ID'),
    create=extend_schema(tags=SHOP_TAG, summary='Создать новый товар'),
    update=extend_schema(tags=SHOP_TAG, summary='Полностью обновить товар'),
    partial_update=extend_schema(tags=SHOP_TAG, summary='Частично обновить товар'),
    destroy=extend_schema(tags=SHOP_TAG, summary='Удалить товар'),
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('shop', 'category').all()
    serializer_class = ProductSerializer
    pagination_class = ShopPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'category__name', 'shop__name']
    ordering_fields = ['price', 'stock', 'title', 'id']
    ordering = ['id']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

