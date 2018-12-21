from django.conf.urls.static import static
from django.urls import path

from XP import settings
from maingame.views import *

urlpatterns = [
    path('record/', user_record),
    path('profile/', profile),
    path('enter_battle/', enter_battle),
    path('buy/', buy_from_shop)
] + static(settings.STATIC_URL, document_root= settings.STATICFILES_DIRS)