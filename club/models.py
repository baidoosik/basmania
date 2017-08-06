from django.utils import timezone
from django.db import models

"""
# host : 주최 혹은 대회
- name / CharField : 이름
- description / TextField : 설명
- profile_image / URLField : 사진url
- start_date / DateTimeField / 개최일자
"""
class Host(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    profile_image = models.URLField(blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

"""
# season : 대회차수
- host_id / ForeignKey / 주최 아이디
- season / IntegerField / 회차
- location / CharField / 장소
- start_date / DateTimeField / 개최일자
"""
class Season(models.Model):
    host_id = models.ForeignKey(Host)
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

"""
# team : 팀
- name / CharField :이름
- profile_image / URLField : 사진url
- description / TextField : 설명
- start_date : DateTimeField : 창단일시
- type / CharField : 타입 (대학교 university, 아마추어: amateur)
"""
class Team(models.Model):
    name = models.CharField(max_length=200)
    profile_image = models.URLField(blank=True, null=True)
    description = models.TextField()
    start_date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=50, choices=(('ama', 'amateur'), ('uni', 'university')))

    def __str__(self):
        return self.name

"""
# join_team : 대회참가팀
- season_id / ForeignKey : 대회차수아이디
- team_id / ForeignKey : 팀아이디
"""
class Jointeam(models.Model):
    season_id = models.ForeignKey(Season)
    team_id = models.ForeignKey(Team)

    def __str__(self):
        return str(self.season_id) + ': ' + str(self.team_id.name)

    class Meta:
        unique_together = ('season_id', 'team_id')

"""
# position : 포지션정보
- name / CharField :포지션
"""
class Position(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

"""
# player : 선수
- name / CharField : 이름
- team_id / ForeignKey :팀 아이디
- position_id / ForeignKey : 포지션 아이디
- height / IntegerField : 키
- profile_image / URLField : 사진url
"""
class Player(models.Model):
    name = models.CharField(max_length=200)
    team_id = models.ForeignKey(Team)
    position_id = models.ForeignKey(Position)
    height = models.IntegerField(default=0)
    profile_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

"""
# match : 경기
- season_id / ForeignKey : 대회차수아이디
- team1_id / ForeignKey: 팀1 아이디
- team2_id / ForeignKey: 팀2 아이디
- team1_point / IntegerField : 팀1 포인트
- team2_point / IntegerField : 팀2 포인트
- date / DateTimeField : 일자
- winner / ForeignKey / 승리팀 아이디
"""
class Match(models.Model):
    season_id = models.ForeignKey(Season)
    team1_id = models.ForeignKey(Team, related_name='team1_id')
    team2_id = models.ForeignKey(Team, related_name='team2_id')
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    date = models.CharField(max_length=100)
    winner_id = models.ForeignKey(Team, related_name='winner_id')

    def __str__(self):
        return str(self.season_id) + ': ' + str(self.team1_id) + ' vs ' + str(self.team2_id)


"""
# performance : 경기퍼포먼스
- match_id / ForeignKey : 경기아이디
- player_id / ForeignKey :선수아이디
- position_id / ForeignKey :포지션아이디
- total_point / IntegerField : 총득점
- 2point / IntegerField : 2점
- 3point / IntegerField : 3점
- free_throw_point / IntegerField :자유투
- rebound / IntegerField : 리바운드
- foul / IntegerField : 파울
- play_time / IntegerField : 출전시간(분)
"""
class Performance(models.Model):
    match_id = models.ForeignKey(Match)
    player_id = models.ForeignKey(Player)
    position_id = models.ForeignKey(Position)
    total_point = models.IntegerField(default=0)
    point_2 = models.IntegerField(default=0)
    point_3 = models.IntegerField(default=0)
    free_throw = models.IntegerField(default=0)
    rebound = models.IntegerField(default=0)
    foul = models.IntegerField(default=0)
    assist = models.IntegerField(default=0)
    play_time = models.IntegerField(default=0)

    def __str__(self):
        return str(self.match_id) + ': ' + str(self.player_id) + ' 의 스탯'

    class Meta:
        unique_together = ('match_id', 'player_id')

"""
# trans : 이적기록
- player_id / ForeignKey :선수아이디
- from_team_id / ForeignKey :프롬팀 아이디
- to_team_id / ForeignKey : 투팀 아이디
- position_id / ForeignKey : 포지션 아아디
- date / DateTimeField :일자
"""
class Trans(models.Model):
    player_id = models.ForeignKey(Player)
    from_team_id = models.ForeignKey(Team, related_name='from_team_id')
    to_team_id = models.ForeignKey(Team, related_name='to_team_id')
    position_id = models.ForeignKey(Position)
    date = models.DateTimeField(timezone.now)

    def __str__(self):
        str(self.player_id) + ' 의 ' + str(self.from_team_id) + ' 로 부터 ' + str(self.to_team_id) + ' 로 이적'

