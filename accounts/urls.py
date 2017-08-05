from django.conf.urls import url,include
from django.contrib.auth.views import login,logout
from . import views

urlpatterns=[
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^login/$',login,name='login'),
    url(r'^logout/$',login,name='logout'),
    url(r'^profile/$',views.profile,name='profile'),

]