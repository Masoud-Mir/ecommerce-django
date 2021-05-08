from django.urls import path
from .views import (
    ProductsListView,
    product_detail,
    Search,
    products_categories_partial,
    CategoriesListView,
)

app_name = 'products'
urlpatterns = [
    path('', ProductsListView.as_view(), name='product-list'),
    path('<int:productId>', product_detail, name='product-detail'),
    path('category/<str:category_name>', CategoriesListView.as_view(), name='product-category'),
    path('products_categories_partial', products_categories_partial, name='products_categories_partial'),
    path('search', Search.as_view(), name='search'),
]
