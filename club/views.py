import pickle
import json
from django.shortcuts import render, get_object_or_404
from .models import Host, Season, Team, Player, Position, Match, Performance
from club.worker import Worker

# Create your views here.
def home(request):
    return render(request,'club/home.html')

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
    context = {'player': player, 'performance':performance}
    return render(request, 'club/player.html', context)
