import requests
import time
from datetime import timedelta

COLLEGE_URL = 'https://api-secure.sports.yahoo.com/v1/editorial/s/scoreboard?lang=en-US&region=US&tz=America%2FIndiana%2FIndianapolis&ysp_redesign=1&ysp_platform=desktop&leagues=ncaab&count=20&date=current&top25=1&ysp_enable_last_update=1'
NBA_URL = 'https://api-secure.sports.yahoo.com/v1/editorial/s/scoreboard?lang=en-US&region=US&tz=America%2FIndiana%2FIndianapolis&ysp_redesign=1&ysp_platform=desktop&leagues=nba&trending=1&count=20&ysp_enable_last_update=1'

NBA_AVERAGES = { "Bucks": 117.8, "Mavericks": 117.0, "Rockets": 116.4, "Clippers": 116.0, "Pelicans": 115.8, "Trail Blazers": 114.6, "Wizards": 114.4, "Spurs": 114.1, "Suns": 113.6, "Lakers": 113.3, "Timberwolves": 113.3, "Grizzlies": 112.8, "Celtics": 112.8, "Raptors": 112.3, "Hawks": 111.8, "Heat": 111.6, "Nets": 111.5, "Jazz": 111.5, "Nuggets": 110.5, "76ers": 110.2, "Kings": 110.1, "Thunder": 109.8, "Pacers": 109.0, "Magic": 107.3, "Pistons": 107.2, "Cavaliers": 106.9, "Bulls": 106.8, "Warriors": 106.3, "Knicks": 105.8, "Hornets": 102.9 }
COLLEGE_AVERAGES = {}

NBA_TOTAL_TIME = 48
NBA_PERIOD_TIME = 12

COLLEGE_TOTAL_TIME = 40
COLLEGE_PERIOD_TIME = 20

def parse_nba_time(display_time, current_period):
  if display_time == "Half":
    seconds = (NBA_TOTAL_TIME / 2) * 60
    return (seconds, seconds)

  if display_time.split(' ')[1] == "OT":
    return (0,0)

  if display_time.split(' ')[0] == "End":
    seconds_elapsed = (current_period * NBA_PERIOD_TIME) * 60

    return (seconds_elapsed, (NBA_TOTAL_TIME * 60) - seconds_elapsed)

  clock = display_time.split(' ')[0]
  current_period_minutes_remaining = int(clock.split(':')[0]) if clock.split(':')[0] != '' else 0
  current_period_seconds_remaining = int(float(clock.split(':')[1])) + (current_period_minutes_remaining * 60)

  current_period_seconds_elapsed = (NBA_PERIOD_TIME * 60) - current_period_seconds_remaining
  finished_period_seconds_elapsed = ((current_period - 1) * NBA_PERIOD_TIME) * 60
  total_seconds_elapsed = current_period_seconds_elapsed + finished_period_seconds_elapsed

  return (total_seconds_elapsed, (NBA_TOTAL_TIME * 60) - total_seconds_elapsed)

def parse_college_time(display_time, current_period):
  if display_time == "Half":
    seconds = (COLLEGE_TOTAL_TIME / 2) * 60
    return (seconds, seconds)

  if display_time.split(' ')[1] == "OT":
    return (0,0)
  
  if display_time.split(' ')[0] == "End":
    total_secons_elapsed = (display_time.split(' ')[1].split('rd')[0] * COLLEGE_PERIOD_TIME) * 60
    
    return (total_seconds_elapsed, (COLLEGE_TOTAL_TIME * 60) - total_seconds_elapsed)

  clock = display_time.split(' ')[0]
  current_period_minutes_remaining = int(clock.split(':')[0]) if clock.split(':')[0] != '' else 0
  current_period_seconds_remaining = int(clock.split(':')[1]) + (current_period_minutes_remaining * 60)

  current_period_seconds_elapsed = (COLLEGE_PERIOD_TIME * 60) - current_period_seconds_remaining
  finished_period_seconds_elapsed = ((current_period - 1) * COLLEGE_PERIOD_TIME) * 60
  total_seconds_elapsed = current_period_seconds_elapsed + finished_period_seconds_elapsed

  return (total_seconds_elapsed, (COLLEGE_TOTAL_TIME * 60) - total_seconds_elapsed)

while True:
  print("------------------ LATEST RESULTS ------------------\n")
  # college_results = requests.get(COLLEGE_URL).json()
  nba_results = requests.get(NBA_URL).json()

  # college_games = college_results["service"]["scoreboard"]["games"]
  # college_teams = nba_results["service"]["scoreboard"]["teams"]

  nba_games = nba_results["service"]["scoreboard"]["games"]
  nba_teams = nba_results["service"]["scoreboard"]["teams"]
  # all_teams = {**college_teams, **nba_teams}
  all_teams = nba_teams

  for league in ["nba"]:
    games = college_games if league == "college" else nba_games
    for k,v in games.items():
      if v["status_type"] == "status.type.in_progress":
        current_period = int(v["current_period_id"])
        away_points = int(v["total_away_points"])
        home_points = int(v["total_home_points"])
        total_points = away_points + home_points
        display_time = v["status_display_name"]

        home_team_id = v["home_team_id"]
        away_team_id = v["away_team_id"]

        home_team_name = all_teams[home_team_id]["last_name"]
        away_team_name = all_teams[away_team_id]["last_name"]

        if league == "college":
          time_elapsed, time_remaining = parse_college_time(display_time, current_period)

        if league == "nba":
          time_elapsed, time_remaining = parse_nba_time(display_time, current_period)

        averages = NBA_AVERAGES if league == "nba" else COLLEGE_AVERAGES
        home_team_average_points = averages[home_team_name]
        away_team_average_points = averages[away_team_name]
        total_average_points = home_team_average_points + away_team_average_points

        total_minutes_played = NBA_TOTAL_TIME if league == "nba" else COLLEGE_TOTAL_TIME
        average_points_per_minute = total_minutes_played / total_average_points

        current_average_points_per_minute = total_points / (time_elapsed / 60)

        projected_points = ((time_remaining / 60) * current_average_points_per_minute) + total_points

        team_display = away_team_name + " @ " + home_team_name
        spaces = 25 - len(team_display)

        print(away_team_name + " @ " + home_team_name + spaces * " ", "time remaining: " + str(timedelta(seconds=time_remaining)), "| TOTAL POINTS: " + str(total_points), "| average points: " + str(round(total_average_points)), "| projected points: " + str(round(projected_points)), "| point diff (HIGHER = TAKE UNDER): " + str(round(total_average_points - projected_points)) + "\n")

  print("\n")
  time.sleep(10)