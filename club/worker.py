class Worker:
    def __init__(self, Host, Season, Team, Player, Position, Match, Performance):
        self.Host = Host
        self.Season = Season
        self.Team = Team
        self.Player = Player
        self.Position = Position
        self.Match = Match
        self.Performance = Performance

    def test(self):
        return 1

    HOST_KEYWORD = ['KUSF', '서울시민리그', 'U리그']

    def get_host(self, name):
        host_keyword = None
        for keyword in self.HOST_KEYWORD:
            if keyword in name:
                host_keyword = keyword

        if (host_keyword is None):
            return False

        host = self.Host.objects.filter(name=host_keyword).first()
        if (host is None):
            host = self.Host(name=host_keyword, description=host_keyword)
            host.save()
        return host


    def get_season(self, name):
        host = self.get_host(name)
        if (host is False):
            return False

        season = self.Season.objects.filter(name=name).first()
        if (season is None):
            season = self.Season(name=name, host_id=host)
            season.save()
        return season


    def get_team(self, team_name):
        team = self.Team.objects.filter(name=team_name).first()
        if (team is None):
            team_type = 'ama'
            if '대학교' in team_name:
                team_type = 'uni'
            team = self.Team(name=team_name, type=team_type, description=team_name)
            team.save()
        return team


    def get_player(self, team, player_name, profile_image=None):
        player = self.Player.objects.filter(name=player_name, team_id=team).first()
        if (player is None):
            position = self.Position.objects.all().first()
            player = self.Player(name=player_name, team_id=team, position_id=position, profile_image=profile_image)
            player.save()
        return player


    def insert_player(self, insert_data):
        result = []
        for player_data in insert_data:
            team = self.get_team(self.strip(player_data['team']))
            player = self.get_player(team, self.strip(player_data['name']), self.strip(player_data['profile_image']))
            result.append({'team': team, 'player': player})
        return result


    def insert_match(self, insert_data):
        result = []
        failure = []
        for match_data in insert_data:
            season = self.get_season(self.strip(match_data['host']))
            if (season is False):
                failure.append(match_data)
                continue
            team1 = self.get_team(self.strip(match_data['team1_name']))
            team2 = self.get_team(self.strip(match_data['team2_name']))
            match = self.Match.objects.filter(season_id=season, team1_id=team1, team2_id=team2).first()
            if (match is None):
                winner = team1
                if (self.convert_to_int(match_data['team2_score']) > self.convert_to_int(match_data['team2_score'])):
                    winner = team2
                match = self.Match(season_id=season, team1_id=team1, team2_id=team2, team1_score=self.convert_to_int(match_data['team1_score']),
                                   team2_score=self.convert_to_int(match_data['team2_score']), date=self.strip(match_data['date']), winner_id=winner)
                match.save()
            perf_result = self.insert_performance(match, match_data['performance'])
            result.append({'season': season, 'team1': team1, 'team2': team2, 'match': match, 'performance':perf_result})

        if (len(failure) > 0):
            # print('failure!')
            # print(failure)
            pass
        return result


    def insert_performance(self, match, insert_data):
        result = []
        failure = []
        for perf_data in insert_data:
            team = self.get_team(self.strip(perf_data['team']))
            player = self.get_player(team, self.strip(perf_data['name']))
            performance = self.Performance.objects.filter(match_id=match, player_id=player).first()
            if (performance is None):

                total_point = self.convert_to_int(perf_data['point'])
                rebound = self.convert_to_int(perf_data['rebound'])
                foul = self.convert_to_int(perf_data['foul'])
                assist = self.convert_to_int(perf_data['assist'])
                performance = self.Performance(match_id=match, player_id=player, position_id=player.position_id, total_point=total_point,
                                               rebound=rebound, foul=foul, assist=assist)
                performance.save()
            result.append({'team':team, 'player':player, 'performance':performance})

        if (len(failure) > 0):
            print('failure!')
            print(failure)
        return result

    def convert_to_int(self, data):
        try:
            return int(data)
        except:
            return 0

    def strip(self, data):
        if (isinstance(data, str)):
            return data.strip()
        else:
            return data


# ------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    PROJECT_NAME = 'basmania'
    APP_NAME = 'club'
    FILE_MAP = {'player_list': 'player_list', 'match_list': 'match_list'}

    import os, sys, importlib
    import django
    import pickle

    sys.path.append('../')
    os.environ['DJANGO_SETTINGS_MODULE'] = PROJECT_NAME + '.settings'
    django.setup()

    myapp = importlib.import_module(APP_NAME)
    Host = myapp.models.Host
    Season = myapp.models.Season
    Team = myapp.models.Team
    Player = myapp.models.Player
    Position = myapp.models.Position
    Match = myapp.models.Match
    Performance = myapp.models.Performance


    worker = Worker(Host, Season, Team, Player, Position, Match, Performance)

    with open('../uleague.pickle', 'rb') as f:
        insert_data = pickle.load(f)

    data = [insert_data[0]]
    #print(data)

    result = worker.insert_match(data)
    print(result)
