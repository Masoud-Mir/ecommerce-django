"""TanTan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from account.views import Login, signup, activate, ResetPass
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    # PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    LogoutView
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('login', Login.as_view(), name='login'),
                  path('logout', LogoutView.as_view(), name='logout'),
                  path('signup', signup, name='signup'),
                  path('order/', include('order.urls')),
                  path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
                  path('', include('shop.urls')),
                  path('products/', include('products.urls')),
                  path('password_change/', PasswordChangeView.as_view(), name='password_change'),
                  path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

                  path('password_reset/', ResetPass.as_view(), name='password_reset'),
                  path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
                  path('comment/', include('comment.urls')),
                  path('profile/', include('account.urls')),
                  path('ratings/', include('star_ratings.urls', namespace='ratings')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
