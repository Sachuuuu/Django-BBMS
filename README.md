# Django-BBMS

You were hired by a basketball league to develop a management system to monitor games
statistics and rankings of a recent tournament.
A total of 16 teams played in the first qualifying round, 8 moved to the next round, and so forth
until one team was crowned as champion.
Each team consists of a coach and 10 players. not all players participate in every
game.
There are 3 types of users in the system - the league admin, a coach, and a player.
● All 3 types of users can login to the site and logout. Upon login they will view the
scoreboard, which will display all games and final scores, and will reflect how the
competition progressed and who won.

● A coach may select his team in order to view a list of the players on it, and the
average score of the team. When one of the players in the list is selected, his
personal details will be presented, including - player’s name, height, average score,
and the number of games he participated in.

● A coach can filter players to see only the ones whose average score is in the 90
percentile across the team.

● The league admin may view all teams details - their average scores, their list of
players, and players details.

● The admin can also view the statistics of the site’s usage - number of times each
user logged into the system, the total amount of time each user spent on the site,
and who is currently online. (i.e. logged into the site)

# Follow below steps to setup
1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py createsuperuser [set username = admin, pasxword = admin]
4. python manage.py create_data
5. python manage.py  runserver

Run step 1 and 2 if the db.sqlite3 file is deleted or if you apply any changes to the db


## Use following curls to test

### Login
change username and password for other users. Other usernames can be found in the admin panel(http://127.0.0.1:8000/admin) and password for all the other users is 'testpass'.
```
curl -X POST \
  http://127.0.0.1:8000/bbms/login/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -H 'postman-token: 7beff464-e350-d5fd-f19d-da2bfdde855d' \
  -F password=admin \
  -F uname=admin
  ```

### Logout

```
curl -X GET \
  http://127.0.0.1:8000/bbms/logout/ \
  -H 'cache-control: no-cache' \
  -H 'postman-token: d0df389d-d966-3522-e3f1-c5cbfda1dd7d'
```

### View full Score card

```
curl -X GET \
  http://127.0.0.1:8000/bbms/ \
  -H 'cache-control: no-cache' \
  -H 'postman-token: 2b41c9b7-ffe0-f5d6-d27b-ee763962be60'
```

### View team stat as a coach

```
curl -X GET \
  http://127.0.0.1:8000/bbms/myteam \
  -H 'cache-control: no-cache' \
  -H 'postman-token: 40e4f4e2-82cb-38f9-60de-6056eae5b8c1'
```

### View best players of the team (90%)

```
curl -X GET \
  http://127.0.0.1:8000/bbms/bestplayers \
  -H 'cache-control: no-cache' \
  -H 'postman-token: f8cdd871-680c-d9d3-328b-502ebac91e77'
```

### Admin checking all user stats(login and logout)

```
curl -X GET \
  http://127.0.0.1:8000/bbms/userstats \
  -H 'cache-control: no-cache' \
  -H 'postman-token: 4db0c1c5-9d8a-a9f4-1615-7ced1a61245d'
```

### Admin checking a specific user's stats(login and logout)

```
curl -X POST \
  http://127.0.0.1:8000/bbms/userstats/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -H 'postman-token: 2e468b49-be5f-a410-45bc-9366c702a018' \
  -F username=2
  ```
