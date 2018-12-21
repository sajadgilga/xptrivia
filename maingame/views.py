import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

# Create your views here.
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from maingame.models import Profile, Battle_Group
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
    category_type = json.loads(request.body)['category']

    group = Battle_Group.objects.filter(category__exact=category_type).last()
    user_prof = Profile.objects.get(user=request.user)

    if group is not None and group.isEmpty:
        group.participants.add(user_prof)
        group.isEmpty = False
        group.save()
        participants = group.participants.all()
        opponent = participants[0]
        if opponent == user_prof:
            opponent = participants[1]
        return Response({'opponent': opponent.user.username}, status=status.HTTP_200_OK)
    else:
        group = Battle_Group.objects.create(winner=user_prof)
        group.participants.add(user_prof)
        group.category = category_type
        group.save()
        while True:
            group = Battle_Group.objects.get(pk=group.pk)
            if not group.isEmpty:
                participants = group.participants.all()
                opponent = participants[0]
                if opponent == user_prof:
                    opponent = participants[1]
                return Response({'opponent': opponent.user.username}, status=status.HTTP_200_OK)


@api_view(["GET", ])
@authentication_classes([JSONWebTokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def buy_from_shop(request):
    info = json.loads(request.body)
    user_prof = Profile.objects.get(user=request.user)
    cost = info['cost']
    if user_prof.coins < cost:
        return Response({'result': 'not enough coins to buy this item'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    user_prof.coins -= cost
    return Response({'result': 'successfully bought'}, status=status.HTTP_200_OK)
