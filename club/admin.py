from django.contrib import admin
from .models import Team,Host,Season,Jointeam,Player,Match,Performance

# Register your models here.
@admin.register(Team)
class TeamModeladmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_display_links = ['id','name']


@admin.register(Host)
class HostModeladmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_display_links = ['id','name']


@admin.register(Season)
class SeasonModeladmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_display_links = ['id','name']


@admin.register(Jointeam)
class JointeamModeladmin(admin.ModelAdmin):
    list_display = ['id','season_id']
    list_display_links = ['id','season_id']


@admin.register(Player)
class PlayerModeladmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_display_links = ['id','name']
    list_filter = ['name']


@admin.register(Match)
class TeamModeladmin(admin.ModelAdmin):
    list_display = ['id','season_id']
    list_display_links = ['id']

@admin.register(Performance)
class PerformanceModeladmin(admin.ModelAdmin):
    list_display = ['id','player_id']
    list_display_links = ['id']
    list_filter = ['player_id']
