from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login, name='login'),
    path('logout/',views.logout_now, name='logout'),
    path('', views.scoreboard, name='scoreboard'),
    path('myteam/', views.viewmyteam, name="viewMtTeam"), #view players of a team buy coach
    path('bestplayers/',views.bestplayers, name='bestplayers'), #view
    path('viewalldetails/',views.viewalldetails, name='viewalldetails'),
    path('userstats/',views.view_user_records, name='viewalldetails')
]
