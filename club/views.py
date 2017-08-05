from django.shortcuts import render
from .models import Team,Player,Match
# Create your views here.
def home(request):
    team_count = Team.objects.all().count()
    player_count = Player.objects.all().count()
    match_count = Match.objects.all().count()

    return render(request,'club/home.html',{
        'team_count':team_count,
        'player_count':player_count,
        'match_count':match_count,
    })

