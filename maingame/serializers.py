from rest_framework import serializers

from maingame.models import Profile


class record_serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user',)
        # fields = ('coins', 'gem', 'avatar', 'level')


class profile_serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user',)
        # fields = ('avatar', 'flag',
        #           'level', 'experience',
        #           'friends', 'coins',
        #           'gem', 'name',
        #           'win_strike', 'average_score',
        #           'game_number', 'won_number')
