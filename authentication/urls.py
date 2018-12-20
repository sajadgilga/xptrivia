from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from authentication.views import *

urlpatterns = [
    path('login/', Login_view.as_view(), name='login'),
    path('hello/', handshake)
]