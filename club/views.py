from django.shortcuts import render
from .models import Team,Player,Match,Performance
# Create your views here.

def home(request):
    teams = Team.objects.all()
    team_count = teams.count()
    player= Player.objects.all()
    player_count=player.count()
    match_count = Match.objects.all().count()

    q = request.GET.get('q', '')

    if q:
        player= player.filter(name__icontains=q)

        return render(request,'club/home.html',{
            'team_count':team_count,
            'player_count':player_count,
            'match_count':match_count,
            'players':player,
        })
    else:
        return render(request,'club/home.html',{
            'team_count':team_count,
            'player_count':player_count,
            'match_count':match_count,
            'teams': teams,
        })


