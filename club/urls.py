from django.conf.urls import url,include
from . import views
urlpatterns=[
    url(r'^$',views.home,name='home'),
    url(r'^data/insert$',views.insert,name='insert'),
    url(r'^player//insert$',views.insert,name='insert'),
    url(r'^player/(?P<player_id>\d+)$', views.player, name='player'),
    url(r'^team/detail/(?P<pk>\d+)/$',views.team_detail,name='team_detail'),

]