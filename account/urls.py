from django.urls import path
from .views import profile, edit_profile

app_name = 'account'
urlpatterns = [
    path('', profile, name='profile'),
    path('edit/', edit_profile, name='edit_profile'),
]
