from django.urls import path

from .views import add_to_cart, cart, remove_order_detail

app_name = 'order'
urlpatterns = [
    path('', add_to_cart, name='add_to_cart'),
    path('cart', cart, name='cart'),
    path('remove_order_item/<int:detail_id>', remove_order_detail, name='remove_order_item'),
]
