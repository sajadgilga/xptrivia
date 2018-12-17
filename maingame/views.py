from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

# Create your views here.
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from maingame.models import Profile
from maingame.serializers import record_serializer, profile_serializer


@api_view(["GET", "POST"])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def user_record(request):
    """
    get user from request and returns its main record

    :param request:
    :return: serialized record in json format
    """
    try:
        user_profile = Profile.objects.get(user=request.user)
        serialized_record = record_serializer(user_profile)
        return Response(serialized_record.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return HttpResponse('There is no profile for this specific user.\nBe sure to send the right token',
                            status=status.HTTP_404_NOT_FOUND)
    except:
        return HttpResponse('Problem in backend',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def profile(request):
    """
    gets user from request and returns its profile

    :param request:
    :return: serialized profile details in json format
    """
    try:
        user_profile = Profile.objects.get(user=request.user)
        serialized_profile = profile_serializer(user_profile)
        return Response(serialized_profile.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return HttpResponse('There is no profile for this specific user.\nBe sure to send the right token',
                            status=status.HTTP_404_NOT_FOUND)
    except:
        return HttpResponse('Problem in backend',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def enter_battle(request):
    pass
