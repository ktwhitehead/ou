NBA_AVERAGES = { "Nets": 121.4, "Bucks": 120.1, "Jazz": 116.0, "Pelicans": 115.5, "Clippers": 115.3, "Nuggets": 115.2, "Warriors": 114.7, "Bulls": 114.7, "Wizards": 114.5, "Trail Blazers": 114.2, "Kings": 114.0, "76ers": 113.9, "Hawks": 113.5, "Suns": 113.2, "Pacers": 113.2, "Raptors": 112.9, "Mavericks": 111.9, "Hornets": 111.6, "Lakers": 111.2, "Celtics": 110.9, "Spurs": 110.7, "Grizzlies": 110.4, "Rockets": 108.7, "Timberwolves": 108.2, "Pistons": 108.0, "Heat": 107.7, "Thunder": 107.0, "Magic": 104.8, "Knicks": 104.7, "Cavaliers": 104.3 }
NBA_TOTAL_TIME = 48
NBA_PERIOD_TIME = 12

class Parser:
  def parse_nba_time(self, display_time, current_period):
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

  def parse(self, game_stats, nba_games, nba_teams):
    current_period = int(game_stats["current_period_id"])
    display_time = game_stats["status_display_name"]
    away_points = int(game_stats["total_away_points"])
    home_points = int(game_stats["total_home_points"])
    total_points = away_points + home_points

    home_team_id = game_stats["home_team_id"]
    away_team_id = game_stats["away_team_id"]
    home_team_name = nba_teams[home_team_id]["last_name"]
    away_team_name = nba_teams[away_team_id]["last_name"]
    game_display = away_team_name + " @ " + home_team_name

    time_elapsed, time_remaining = self.parse_nba_time(display_time, current_period)

    home_team_average_points = NBA_AVERAGES[home_team_name]
    away_team_average_points = NBA_AVERAGES[away_team_name]
    total_average_points = home_team_average_points + away_team_average_points

    average_points_per_minute = total_points / (time_elapsed / 60)
    projected_points = ((time_remaining / 60) * average_points_per_minute) + total_points

    data = { "game": game_display, "total_points": total_points, "projected_points": projected_points, "time_elapsed": time_elapsed, "average_points": total_average_points }
    return data
