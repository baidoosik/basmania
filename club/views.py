import pickle
import json
from django.shortcuts import render, get_object_or_404
from .models import Host, Season, Team, Player, Position, Match, Performance
from club.worker import Worker

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


def insert(request):
    # with open('match_list.pickle', 'wb') as f:
    #     pickle.dump(match_list, f)

    with open('uleague.pickle', 'rb') as f:
        insert_data = pickle.load(f)

    with open('uleague.json',  mode='w', encoding='utf-8') as f:
        json.dump(insert_data, f, indent=2)

    worker = Worker(Host, Season, Team, Player, Position, Match, Performance)
    result = worker.insert_match(insert_data)
    context = {'result': result, 'data': insert_data}
    return render(request, 'club/insert.html', context)

def player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    performance = []
    if (player) :
        performance = Performance.objects.filter(player_id=player).all()
        average_point=0
        average_rebound = 0
        average_assist = 0
        average_foul = 0
        for each_performance in performance:
            average_point = average_point + each_performance.total_point
            average_rebound = average_rebound + each_performance.rebound
            average_assist = average_assist + each_performance.assist
            average_foul =  average_foul + each_performance.foul

        average_point=average_point/performance.count()
        average_rebound = average_rebound/performance.count()
        average_assist = average_assist/performance.count()
        average_foul = average_foul/performance.count()

    context = {
        'player': player,
        'performance':performance,
        'average_point':average_point,
        'average_rebound':average_rebound,
        'average_assist':average_assist,
        'average_foul':average_foul,
    }
    return render(request, 'club/player.html', context)
