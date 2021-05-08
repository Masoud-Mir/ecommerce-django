from django.db import models

# Create your models here.
from account.models import User
from products.models import Product


class Order(models.Model):
    payment_price = models.DecimalField(max_digits=20, decimal_places=0, verbose_name='مبلغ کل', blank=True, null=True)
    is_paid = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    owner = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='تاریخ پرداخت')

    def get_total_price(self):
        amount = 0
        for order in self.orderdetail_set.all():
            amount += order.get_detail_total_price()
        return amount

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید کابران'

    def __str__(self):
        return self.owner.username


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    size = models.CharField(max_length=15, verbose_name='سایز', blank=True, null=True)
    color = models.CharField(max_length=15, verbose_name='رنگ', blank=True, null=True)
    unit_price = models.DecimalField(max_digits=20, decimal_places=0, verbose_name='مبلغ', blank=True, null=True)
    amount = models.IntegerField(verbose_name='تعداد', default=1)

    class Meta:
        verbose_name = 'جزییات محصول'
        verbose_name_plural = 'جزییات محصولات'

    def __str__(self):
        return self.product.title

    def get_detail_total_price(self):
        return self.amount * self.unit_price
