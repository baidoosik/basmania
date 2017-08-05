from django.contrib import admin
from .models import Host,Season,Jointeam,Team,Position,Player,Performance,Match,Trans

admin.site.register(Host)
admin.site.register(Season)
admin.site.register(Jointeam)
admin.site.register(Team)
admin.site.register(Position)
admin.site.register(Player)
admin.site.register(Performance)
admin.site.register(Match)
admin.site.register(Trans)