from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# Create your views here.
from django.utils import timezone

from order.forms import ShoppingCartForm
from order.models import Order, OrderDetail
from products.models import Product


@login_required
def add_to_cart(request):
    cart_form = ShoppingCartForm(request.POST or None)
    current_user_id = request.user.id

    if cart_form.is_valid():
        order = Order.objects.filter(owner_id=current_user_id, is_paid=False).first()

        if order is None:
            order = Order.objects.create(owner_id=current_user_id, is_paid=False)

        product_id = cart_form.cleaned_data.get('product_id')
        amount = cart_form.cleaned_data.get('amount')
        color = cart_form.cleaned_data.get('color')[0]
        size = cart_form.cleaned_data.get('size')[0]
        print(color)
        if amount < 0:
            amount = 1
        product = Product.objects.filter(id=product_id).first()
        if order.orderdetail_set.filter(product_id=product_id).exists():
            order.orderdetail_set.filter(product_id=product_id).update(product_id=product_id, amount=amount,
                                                                       unit_price=product.price, color=color, size=size
                                                                       )
        else:
            order.orderdetail_set.create(product_id=product_id, amount=amount, unit_price=product.price,
                                         color=color, size=size
                                         )

    return redirect('order:cart')


@login_required(login_url='/login')
def remove_order_detail(request, detail_id):
    detail_id = detail_id
    order_item = get_object_or_404(OrderDetail, id=detail_id)
    if order_item is not None:
        order_item.delete()
        redirect("order:cart")

    return redirect("order:cart")


def cart(request):
    context = {
        'order': None,
        'order_detail': None
    }
    open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()

    if open_order is not None:
        context['order'] = open_order
        context['order_detail'] = open_order.orderdetail_set.all()

    return render(request, 'blog/cart.html', context)
