from django.urls import path

from maingame.views import *

urlpatterns = [
    path('record/', user_record),
    path('profile/', profile),
    path('enter_battle/', enter_battle)
]