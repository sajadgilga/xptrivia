from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class profile(models.Model):
    user = models.OneToOneField(to='User', on_delete=models.CASCADE)
    picture = models.ImageField(blank=True, default='', upload_to='')  # TODO: default and  upload_to
    name = models.CharField(max_length=64, default='')
    flag = models.ImageField(default='')  # TODO: default
    win_strike = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)
    game_number = models.IntegerField(default=0)
    won_number = models.IntegerField(default=0)
    diamonds = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)
    friends = models.ManyToManyField(to='profile')
