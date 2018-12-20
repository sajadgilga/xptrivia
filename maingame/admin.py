from django.contrib import admin

# Register your models here.
from maingame.models import Profile, Question, Answer


@admin.register(Profile)
class profile_admin(admin.ModelAdmin):
    # list_display = ('user',)
    list_display = ('user', 'name',
                    'flag', 'level',
                    'gem', 'coins',
                    'game_number', 'won_number',
                    'win_strike', 'avatar')
    search_fields = ('user', 'name', )

@admin.register(Question)
class Question_admin(admin.ModelAdmin):
    list_display = ('question_text',
                    'question_animation',)
    search_fields = ('question_text',
                     'question_animation',)

@admin.register(Answer)
class Answer_admin(admin.ModelAdmin):
    # list_display = ('answer',)
    list_display = ('question',
                    'answer',)
    search_fields = ('question',
                     'answer',)