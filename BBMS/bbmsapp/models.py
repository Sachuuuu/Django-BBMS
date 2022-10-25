from audioop import reverse
from email.policy import default
from random import choices
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
class Teams(models.Model):
    team_name = models.TextField(max_length=50)

    def __str__(self):
        return str(self.team_name)

class Games(models.Model):
    game_rounds = [('Q','Qualifiers'), ('S8','Super 8'), ('SF','Semi-Final'), ('F','Finals')]
    game_date = models.DateField()
    team_1 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='team_1')
    team_1_score = models.IntegerField()
    team_2 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='team_2')
    team_2_score = models.IntegerField()
    winning_team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='winner')
    round = models.CharField(max_length=5,choices=game_rounds,default='Qualifiers')

    def __str__(self):
        return 'Game : %s' % (self.id)

class Player(models.Model):
    name = models.TextField(max_length = 100)
    height = models.IntegerField()
    number_of_matches = models.IntegerField()
    total_score = models.IntegerField()
    average = models.FloatField()
    team_id = models.ForeignKey(Teams,  on_delete=models.CASCADE, related_name='team_id')

    def __str__(self):
        return 'Player : %s' % (self.id)

class Coach(models.Model):
    name = models.TextField(max_length = 100)
    coaching_team = models.ForeignKey(Teams,  on_delete=models.CASCADE, related_name='coaching_team_id')

    def __str__(self):
        return 'Coach : %s' % (self.id)

class userRecords(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField()

    def __str__(self):
        return 'Record : %s' % (self.id)

class teamRecords(models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    total_score = models.IntegerField()

    def __str__(self):
        return 'Team Record : %s' % (self.id)

