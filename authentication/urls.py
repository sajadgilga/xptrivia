from django.contrib import admin
from django.urls import path

from authentication.views import *

urlpatterns = [
    path('login/', login_),
    path('logout/', logout_),
    path('signup/', signup_),
]