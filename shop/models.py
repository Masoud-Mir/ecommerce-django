from django.db import models

# Create your models here.


class Slider(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    description = models.TextField(max_length=500, verbose_name='توضیحات')
    image = models.ImageField(upload_to='slider', verbose_name='عکس')

    class Meta:
        verbose_name = 'اسلایدر صفحه اصلی'
        verbose_name_plural = 'اسلایدر صفحه اصلی'

    def __str__(self):
        return self.title
