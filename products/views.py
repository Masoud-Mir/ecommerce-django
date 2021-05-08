from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.views.generic import (
    ListView,
    DetailView, TemplateView,
)

from order.forms import ShoppingCartForm
from .models import Product, ProductGallery, IPAddress
from categories.models import Categories
from django.db.models import Count
import itertools


# Create your views here.


def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def product_detail(request, *args, **kwargs):
    cart_form = ShoppingCartForm(request.POST or None)
    product_id = kwargs['productId']
    product = Product.objects.filter(id=product_id).first()
    gallery_list = ProductGallery.objects.filter(product_id=product_id)
    grouped_gallery = list(my_grouper(3, gallery_list))
    related_products = Product.objects.get_queryset().filter(category__product=product).distinct()
    grouped_related_products = list(my_grouper(4, related_products))

    if product is None or not product.active:
        raise Http404('محصول مورد نظر یافت نشد')

    cart_form = ShoppingCartForm(request.POST or None, initial={'product_id': product_id})

    ip_address = request.user.ip_address
    if ip_address not in product.hits.all():
        product.hits.add(ip_address)

    context = {
        'object': product,
        'cart': cart_form,
        'galleries': grouped_gallery,
        'related_products': grouped_related_products,
        'cart_form': cart_form,
    }

    return render(request, 'blog/product-details.html', context=context)


class Search(ListView):
    template_name = 'blog/shop-list.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            qs = Product.objects.search(query)
            return qs

        return Product.objects.filter(active=True)


def products_categories_partial(request):
    categories = Categories.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'blog/partials/products_categories_partial.html', context)


class CategoriesListView(ListView):
    template_name = 'blog/categories.html'
    paginate_by = 6

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        category = Categories.objects.filter(slug__iexact=category_name).first()

        if category is None:
            raise Http404('صفحه ی مورد نظر یافت نشد')

        category_products = Product.objects.get_products_by_category(category_name)

        return category_products

    def get_context_data(self, **kwargs):
        category_name = self.kwargs['category_name']
        category = Categories.objects.filter(slug__iexact=category_name).first()
        sub_category = Categories.objects.filter(parent__slug__iexact=category_name)
        print(sub_category)

        context = super(CategoriesListView, self).get_context_data(**kwargs)
        context['category'] = category
        context['sub_category'] = sub_category

        return context


class ProductsListView(ListView):
    template_name = 'blog/product-list.html'
    queryset = Product.objects.filter(active=True)
    paginate_by = 6


# def main_page(self, request):
#     product = Product.objects.all()
#     most_visited = Product.objects.annotate(count=Count('hits')).order_by('count')
#     context = {
#         'most_visited': most_visited,
#         'product': product,
#     }
#     print(most_visited)
#     return render(request, 'blog/index.html', context)
