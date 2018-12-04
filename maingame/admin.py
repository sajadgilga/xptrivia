from django.contrib import admin

# Register your models here.
from maingame.models import profile, Question, Answer


@admin.register(profile)
class profile_admin(admin.ModelAdmin):
    list_display = ('user', 'name',
                    'flag', 'level',
                    'diamonds', 'coins',
                    'game_number', 'won_number',
                    'win_strike', 'picture')
    search_fields = ('user', 'name', )

@admin.register(Question)
class Question_admin(admin.ModelAdmin):
    list_display = ('question_text', 'question_animation',)
    search_fields = ('question_text', 'question_animation',)

@admin.register(Answer)
class Answer_admin(admin.ModelAdmin):
    list_display = ('question', 'answer',)
    search_fields = ('question', 'answer',)