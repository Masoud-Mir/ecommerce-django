from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from products.models import Product
from categories.models import Categories
from django.db.models import Count


# Create your views here.
from shop.models import Slider


def home(request):
    product = Product.objects.all()
    slider = Slider.objects.all()
    categories = Categories.objects.filter(parent__isnull=True)
    most_visited = Product.objects.annotate(count=Count('hits')).order_by('-count')[:8]
    best_ratings = Product.objects.filter(ratings__isnull=False).order_by('-ratings__average')

    context = {
        'object_list': product,
        'slider': slider,
        'categories': categories,
        'most_visited': most_visited,
        'best_ratings': best_ratings,
    }
    return render(request, 'blog/index.html', context)


class HeaderPartialView(TemplateView):
    template_name = 'blog/partials/header_partial_view.html'


class FooterPartialView(TemplateView):
    template_name = 'blog/partials/footer_partial_view.html'




