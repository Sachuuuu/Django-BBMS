from urllib.request import Request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from .models import Games, Teams, Coach, Player, teamRecords, userRecords
from django.core import serializers
import json
from django.db.models import Avg
from django.contrib.auth import authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login



# Create your views here.
@login_required
def scoreboard(request):
    games = serializers.serialize("json",Games.objects.all())
    return HttpResponse(games, content_type="application/json")

@login_required
def viewmyteam(request):
    if not Coach.objects.filter(name=request.user):
        return HttpResponseForbidden()
    
    teamId = Coach.objects.filter(name=request.user)[0].coaching_team_id
    players = serializers.serialize('json', Player.objects.filter(team_id=teamId))
    games_team_1 = 0 if Games.objects.filter(team_1 = teamId).aggregate(Avg('team_1_score')).get('team_1_score__avg') == None else Games.objects.filter(team_1 = teamId).aggregate(Avg('team_1_score')).get('team_1_score__avg')
    games_team_2 = 0 if Games.objects.filter(team_2 = teamId).aggregate(Avg('team_2_score')).get('team_2_score__avg') == None else Games.objects.filter(team_2 = teamId).aggregate(Avg('team_2_score')).get('team_2_score__avg')
    avg_score = (games_team_1+games_team_2)/2.0
    players = []
    for p in Player.objects.filter(team_id=teamId):
        temp = {
            'id':p.id,
            'name':p.name,
            'height':p.height,
            'match_count':p.number_of_matches,
            'total_score':p.total_score,
            'avg':p.average,
            'team_id':p.team_id.id
        } 
        players.append(temp)
    resp = {
        "Average score":avg_score,
        "Players":players
    } 
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type="application/json")

@login_required
def viewalldetails(request):
    teams_data = []
    team_players =[]
    teams = Teams.objects.all()
    
    for team in teams:
        teamId = team.id
        games_team_1 = 0 if Games.objects.filter(team_1 = teamId).aggregate(Avg('team_1_score')).get('team_1_score__avg') == None else Games.objects.filter(team_1 = teamId).aggregate(Avg('team_1_score')).get('team_1_score__avg')
        games_team_2 = 0 if Games.objects.filter(team_2 = teamId).aggregate(Avg('team_2_score')).get('team_2_score__avg') == None else Games.objects.filter(team_2 = teamId).aggregate(Avg('team_2_score')).get('team_2_score__avg')
        temp_avg = (games_team_1 + games_team_2)/2.0
        temp_json = {
            'team':teamId,
            'average_score':temp_avg
        }
        teams_data.append(temp_json)

        for p in Player.objects.filter(team_id=teamId):
            temp = {
                'name':p.name,
                'height':p.height,
                'match_count':p.number_of_matches,
                'total_score':p.total_score,
                'avg':p.average,
                'team_id':p.team_id.id
            } 
            team_players.append(temp)

    resp = {
        'team_avg_scores' : teams_data,
        'players' : team_players
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type="application/json")

@csrf_exempt
def login(request):
    uname = request.POST['uname']
    pword = request.POST['password']
    resp ={}
    user = authenticate(request,username=uname, password=pword)
    if user is not None:
        auth_login(request,user)
        resp ={'mesage' : f'Hello {request.user}'}
    else:
        resp ={'mesage' : 'Username or password is incorrect'}
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type="application/json")

@login_required
def logout_now(request):
    logout(request)
    context = {'message' : 'Logget out'}
    context = json.dumps(context)
    return HttpResponse(context, content_type="application/json")

@login_required
@csrf_exempt
def view_user_records(request):
    datalist = []
    if str(request.user) != 'admin':
        return HttpResponseForbidden()
    if request.method == 'POST':
        name = request.POST['username']
        user_recs = userRecords.objects.filter(user=name)
        for i in user_recs:
            temp = {
                'key':i.pk,
                'login':str(i.login_time),
                'logout':str(i.logout_time)
            }
            datalist.append(temp)
        records = {'login_stats':datalist}
    else:
        allusers = userRecords.objects.all().order_by('user')
        for i in allusers:
            temp = {
                'username':str(i.user),
                'login':str(i.login_time),
                'logout':str(i.logout_time)
            }
            datalist.append(temp)
        records = {'login_stats':datalist}

    records = json.dumps(records)
    return HttpResponse(records, content_type="application/json")

@login_required
def bestplayers(request):
    if not Coach.objects.filter(name=request.user):
        return HttpResponseForbidden()
    teamId = Coach.objects.filter(name=request.user)[0].coaching_team_id
    team_score = 0 if teamRecords.objects.filter(team=teamId)[0].total_score == None else teamRecords.objects.filter(team=teamId)[0].total_score
    players = Player.objects.filter(team_id=teamId)
    player_list = []
    for p in players:
        if (p.total_score/team_score)*100 >= 90:
            temp = {
                'name':p.name,
                'height':p.height,
                'match_count':p.number_of_matches,
                'total_score':p.total_score,
                'avg':p.average,
                'team_id':p.team_id.id
            }
            player_list.append(temp)
    resp = {
        'players' : player_list
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type="application/json")