from django.contrib import admin
from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken

from authentication.serializers import CustomJWTSerializer
from authentication.views import *

urlpatterns = [
    path('login/', Login_view.as_view()),
    # path('logout/', logout_),
    # path('signup/', signup_),
]