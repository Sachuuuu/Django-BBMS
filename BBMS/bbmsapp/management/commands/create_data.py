from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from bbmsapp.models import Coach, Teams, Games, Player, Coach, userRecords, teamRecords
from faker import Faker
from django.contrib.auth.models import User
import random
from django.db.models import Sum

class Command(BaseCommand):

    def team(self,fake_data):
        for _ in range(16):
            try:
                team = Teams(team_name=fake_data.slug())
            except ObjectDoesNotExist:
                raise CommandError('Teams model not found')
            team.save()
            self.stdout.write(self.style.SUCCESS('Successfully inserted Team : "%s" ' % (team.team_name)))
   
    def qualifiers(self,fake_data):
        teams = Teams.objects.all()
        self.generate_game_data(fake_data, 'Q' , teams)
    
    def super_8(self,fake_data):
        teams = Games.objects.filter(round='Q')
        self.generate_game_data(fake_data, 'S8' , teams)

    def semifinals(self,fake_data):
        teams = Games.objects.filter(round='S8')
        self.generate_game_data(fake_data, 'SF' , teams)

    def finals(self,fake_data):
        teams = Games.objects.filter(round='SF')
        self.generate_game_data(fake_data, 'F' , teams)
    
    def generate_game_data(self, fake_data, roundType, teams):
        team_1_list = teams[0::2]
        team_2_list = teams[1::2]

        for i in range(len(team_1_list)):
            team_1_score = fake_data.random_int(min=1, max=50, step=1)
            team_2_score = fake_data.random_int(min=1, max=50, step=1)
            winning_team = ''
            team_1_id = ''
            team_2_id = ''

            if team_1_score == team_2_score:
                #Every time team_2 will toss the coin 3 times
                for _ in range(3):
                    i = i + random.randint(0,1)
                if i >= 2:
                    winning_team = team_1_list[i]
                else:
                    winning_team = team_2_list[i]

            if team_1_score > team_2_score:
                winning_team = team_1_list[i]
            else:
                winning_team = team_2_list[i]

            if roundType == 'Q' :
                team_1_id = team_1_list[i].id
                team_2_id = team_2_list[i].id
                winning_team = winning_team
            else:
                team_1_id = team_1_list[i].winning_team.id
                team_2_id = team_2_list[i].winning_team.id
                winning_team = winning_team.winning_team
            try:
                game = Games(game_date=fake_data.date_time_this_year(before_now=True, after_now=False, tzinfo=None), team_1_id=team_1_id, team_1_score=team_1_score, team_2_id=team_2_id, team_2_score=team_2_score, winning_team=winning_team, round=roundType )
            except ObjectDoesNotExist:
                raise CommandError('Game model not found')
            game.save()
            self.stdout.write(self.style.SUCCESS('%s Game %s Vs %s =>  winner : %s ' % (roundType, team_1_id, team_2_id, winning_team)))

    def players(self, fake_data):
        teams = Teams.objects.all()
        for team in teams:
            teamRec = teamRecords.objects.filter(team=team)
            total_score = teamRec[0].total_score
            temp_score = 0
            for i in range(10):
                name = fake_data.slug()
                height = fake_data.random_int(min = 150, max = 250, step = 1)
                match_count = fake_data.random_int(min = 1, max = 15, step = 1)
                temp_score = fake_data.random_int(min = 0, max = 50, step = 1)
                if total_score - temp_score < 0:
                    score = 0
                else:
                    score = temp_score
                    total_score = total_score - temp_score
                avg_score = round(score/match_count , 2)
                try:
                    player = Player(name=name, height=height, number_of_matches=match_count, total_score=score, average=avg_score, team_id=team)
                except ObjectDoesNotExist:
                    raise CommandError('Player model not found')
                player.save()
                self.stdout.write(self.style.SUCCESS('Player %s : Height %s : Team ID %s ' % (name, height, team.id)))

    def coach(self, fake_data):
        teams = Teams.objects.all()
        for team in teams:
            name = fake_data.slug()
            try:
                coach = Coach(name=name, coaching_team=team)
            except ObjectDoesNotExist:
                raise CommandError('Player model not found')
            coach.save()
            self.stdout.write(self.style.SUCCESS('Coach %s :  Team ID %s ' % (name, team.id)))

    def create_users(self,fake_data):
        coach = Coach.objects.all()
        players = Player.objects.all()
        userlist = []
        password = 'testpass'

        for c in coach: userlist.append(c.name)
        for p in players: userlist.append(p.name)
        for u in userlist:
            try:
                user = User.objects.create_user(username=u, email=fake_data.safe_email(), password=password)
            except ObjectDoesNotExist:
                raise CommandError('User model not found')
            user.save()
            self.stdout.write(self.style.SUCCESS('User Added : "%s"' % user.username))

    def create_user_stats(self, fake_data):
        users = User.objects.all()
        for user in users:
            for i in range(random.randint(1,15)):
                try:
                    user_stat = userRecords(user_id=user.id,login_time=fake_data.date_time_this_month(before_now=True, after_now=False, tzinfo=None),logout_time=fake_data.date_time_this_month(before_now=False, after_now=True, tzinfo=None))
                except ObjectDoesNotExist:
                    raise CommandError('userRecod model not found')
                user_stat.save()
                self.stdout.write(self.style.SUCCESS('Login record added  %s ' % user.username))
    
    def create_team_stats(self,fake_data):
        teams = Teams.objects.all()
        for team in teams:
            teamId = team
            games_team_1 = 0 if Games.objects.filter(team_1 = teamId).aggregate(Sum('team_1_score')).get('team_1_score__sum') == None else Games.objects.filter(team_1 = teamId).aggregate(Sum('team_1_score')).get('team_1_score__sum')
            games_team_2 = 0 if Games.objects.filter(team_2 = teamId).aggregate(Sum('team_2_score')).get('team_2_score__sum') == None else Games.objects.filter(team_2 = teamId).aggregate(Sum('team_2_score')).get('team_2_score__sum')

            total = games_team_1 + games_team_2
            try:
                team_stat = teamRecords(team=teamId,total_score=total)
            except ObjectDoesNotExist:
                raise CommandError('teamRecord object not found')
            team_stat.save()
            self.stdout.write(self.style.SUCCESS('Team record added  %s ' % teamId))
    
    def handle(self, *args, **options):
        fake = Faker()
        self.team(fake)
        self.qualifiers(fake)
        self.super_8(fake)
        self.semifinals(fake)
        self.finals(fake)
        self.create_team_stats(fake)
        self.players(fake)
        self.coach(fake)
        self.create_users(fake)
        self.create_user_stats(fake)