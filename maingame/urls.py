from django.contrib import admin
from django.urls import path

from maingame.views import *

urlpatterns = [
    path('ex/', get_profile),
]