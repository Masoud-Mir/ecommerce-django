from django.db import models
from django.db.models import Q
from django.urls import reverse

from categories.models import Categories
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from star_ratings.models import Rating
from colorfield.fields import ColorField


# Create your models here.

class ProductsManager(models.Manager):

    def search(self, query):
        lookup = (
            Q(title__icontains=query) |
            Q(description__icontains=query)|
            Q(category__title__icontains=query)
        )
        return self.get_queryset().filter(lookup, active=True).distinct()

    def get_products_by_category(self, category_name):
        return self.get_queryset().filter(category__slug__iexact=category_name, active=True)


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آی پی')


class Color(models.Model):
    title = models.CharField(max_length=15, verbose_name='عنوان')

    COLOR_CHOICES = [
        ("#FFFFFF", "white"),
        ("#000000", "black"),
        ("#0000FF", "blue"),
        ("#FF0000", "red"),
        ("#FFFF00", "yellow"),
        ("#00FF00", "green"),
    ]
    code = ColorField(default='#FF0000', choices=COLOR_CHOICES, verbose_name='رنگ')

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=15, verbose_name='عنوان')

    SIZE_CHOICES = [
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
        ("XXXL", "XXXL"),
    ]
    code = models.CharField(max_length=10, choices=SIZE_CHOICES, verbose_name='سایز')

    class Meta:
        verbose_name = 'سایز بندی'
        verbose_name_plural = 'سایز بندی ها'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    description = models.TextField(max_length=500, verbose_name='توضیحات')
    price = models.DecimalField(max_digits=20, decimal_places=0, verbose_name='قیمت')
    image = models.ImageField(upload_to='products', verbose_name='عکس')
    active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    time_stamp = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت')
    category = models.ManyToManyField(Categories, verbose_name='دسته بندی')
    comments = GenericRelation(Comment, verbose_name='دیدگاه')
    hits = models.ManyToManyField(IPAddress, blank=True, related_name='hits', verbose_name='بازدیدها')
    ratings = GenericRelation(Rating, related_query_name='ratings', verbose_name='امتیازات')
    color = models.ManyToManyField(Color, blank=True, related_name='color', verbose_name='رنگ بندی ها')
    size = models.ManyToManyField(Size, blank=True, related_name='size', verbose_name='سایز بندی ها')

    objects = ProductsManager()

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:product-detail', args=[self.id])


class ProductGallery(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    image = models.ImageField(upload_to='products', verbose_name='عکس')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')

    class Meta:
        verbose_name = 'گالری محصول'
        verbose_name_plural = 'گالری محصولات'

    def __str__(self):
        return self.title



