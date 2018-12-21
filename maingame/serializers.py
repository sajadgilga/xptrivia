from rest_framework import serializers

from maingame.models import Profile, Battle_Group


class record_serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('coins', 'gem', 'level')


class friend_serializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ('username',)


class profile_serializer(serializers.ModelSerializer):
    friends = friend_serializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('name', 'avatar',
                  'level', 'experience',
                  'flag', 'coins', 'gem',
                  'win_strike', 'average_score',
                  'game_number', 'won_number', 'friends',)


class group_serializer(serializers.ModelSerializer):
    class Meta:
        model = Battle_Group
        fields = ('category', 'winner', 'loser')
