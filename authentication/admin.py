from django.contrib import admin

# Register your models here.
from authentication.models import profile


@admin.register(profile)
class profile_admin(admin.ModelAdmin):
    list_display = ('user', 'name',
                    'flag', 'level',
                    'diamonds', 'coins',
                    'game_number', 'won_number',
                    'win_strike', 'picture')
    search_fields = ('user', 'name', )