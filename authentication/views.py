import json

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

# from rest_framework.utils import json
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login_(request):
    user_info = json.loads(request.body)
    user = authenticate(request, username=user_info['username'], password=user_info['password'])
    token, _ = Token.objects.get_or_create(user=user)
    return HttpResponse(content=token.key, status=status.HTTP_200_OK)


def social_authenticate(request):
    pass


def signup_(request):
    pass


@api_view(["GET"])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def logout_(request):
    pass
