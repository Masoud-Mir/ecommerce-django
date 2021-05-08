from django.urls import path
from .views import (home,
                    HeaderPartialView,
                    FooterPartialView,
                    )

app_name = 'shop'
urlpatterns = [
    path('', home, name='home'),
    path('header/', HeaderPartialView.as_view(), name='header'),
    path('footer/', FooterPartialView.as_view(), name='footer'),
]
