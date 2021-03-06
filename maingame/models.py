from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Profile(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    avatar = models.IntegerField(default=2)  # TODO: default and  upload_to
    name = models.CharField(max_length=64, default='A')
    flag = models.CharField(default='Iran', max_length=16)
    win_strike = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    experience = models.BigIntegerField(default=0)
    average_score = models.FloatField(default=0)
    game_number = models.IntegerField(default=0)
    won_number = models.IntegerField(default=0)
    gem = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)
    friends = models.ManyToManyField(to='self')


class Question(models.Model):
    question_text = models.CharField(max_length=512, default='')
    question_animation = models.FileField(upload_to='', blank=True, default='')  # TODO: upload_to, default, blank


class Answer(models.Model):
    answer = models.CharField(max_length=64)
    question = models.ForeignKey(to='Question', on_delete=models.CASCADE, related_name='answers')
    is_valid = models.BooleanField(default=False)


class Battle_Group(models.Model):
    # TODO: needs to add real category
    CATEGORY_CHOICE = (
        (1, 'dices'),
        (2, 'animal'),
        (3, 'something'),
    )
    participants = models.ManyToManyField(to='Profile')
    category = models.IntegerField(choices=CATEGORY_CHOICE, default=1)
    isEmpty = models.BooleanField(default=True)
    winner = models.ForeignKey(to='Profile', on_delete=models.CASCADE, related_name='won_game', default=1)
    loser = models.ForeignKey(to='Profile', on_delete=models.CASCADE, related_name='lost_game', default=1)
