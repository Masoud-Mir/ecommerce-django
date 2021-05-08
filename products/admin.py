from django.contrib import admin

# Register your models here.
from products.models import Product, ProductGallery, IPAddress, Color, Size


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__','active']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery)
admin.site.register(IPAddress)
admin.site.register(Color)
admin.site.register(Size)




