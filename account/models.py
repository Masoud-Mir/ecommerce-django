from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    address = models.TextField(verbose_name='آدرس')
    phone = models.CharField(max_length=15, verbose_name='تلفن')

    class Meta:
        verbose_name = 'حساب کاربری'
        verbose_name_plural = 'حساب های کاربری'

    def __str__(self):
        return self.username
