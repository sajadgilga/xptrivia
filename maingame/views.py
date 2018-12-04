from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated


@api_view(["GET", "POST"])
@csrf_protect
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated,])
def get_profile(request):
    return HttpResponse('ok', status=status.HTTP_200_OK)
