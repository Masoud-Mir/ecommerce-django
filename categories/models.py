from django.db import models

# Create your models here.


class Categories(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    slug = models.CharField(max_length=50, verbose_name='آدرس')
    image = models.ImageField(upload_to='categories', verbose_name='تصویر دسته بندی', blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title
