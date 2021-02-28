import requests
import asyncio
import time
import json

from .parser import Parser
from .stats import Stats

NBA_URL = 'https://api-secure.sports.yahoo.com/v1/editorial/s/scoreboard?lang=en-US&region=US&tz=America%2FIndiana%2FIndianapolis&ysp_redesign=1&ysp_platform=desktop&leagues=nba&trending=1&count=20&ysp_enable_last_update=1'

test_data = {
  "service": {
    "xml:lang": "en-US",
    "scoreboard": {
      "games": {
        "nba.g.2021022815": {
          "gameid": "nba.g.2021022815",
          "global_gameid": "nba.g.2292301",
          "start_time": "Sun, 28 Feb 2021 20:30:00 +0000",
          "is_time_tba": "false",
          "season_phase_id": "season.phase.season",
          "game_type": "Regular Season",
          "home_team_id": "nba.t.15",
          "away_team_id": "nba.t.12",
          "status_display_name": "10:23 1st",
          "status_description": "Pregame",
          "status_type": "status.type.in_progress",
          "total_away_points": 15,
          "current_period_id": 1,
          "total_home_points": 20,
          "teams": [
            "dataIslandPaths",
            "nba.g.2021022815",
            "teams"
          ]
        }
      },
      "teams": {
        "nba.t.15": {
          "team_id": "nba.t.15",
          "display_name": "Miami",
          "first_name": "Miami",
          "last_name": "Heat",
          "full_name": "Miami Heat",
          "abbr": "MIA"
        },
        "nba.t.12": {
          "team_id": "nba.t.1",
          "display_name": "Jazz",
          "first_name": "Utah",
          "last_name": "Jazz",
          "full_name": "Utah Jazz",
          "abbr": "UTA"
        }
      }
    }
  }
}

class Crawler:
  def __init__(self, socket):
    self.is_crawling = False
    self.parser = Parser()
    self.stats = Stats()
    self.socket = socket

  def start(self):
    self.is_crawling = True
    while self.is_crawling:
      nba_results = requests.get(NBA_URL).json()
      nba_games = nba_results["service"]["scoreboard"]["games"]
      nba_teams = nba_results["service"]["scoreboard"]["teams"]

      for k,v in nba_games.items():
        if v["status_type"] == "status.type.in_progress":
          stats = self.parser.parse(v, nba_games, nba_teams)
          game_update = self.stats.update(stats)

          if game_update:
            asyncio.run(self.socket.send_message(json.dumps(game_update)))
      time.sleep(10)

  def stop(self):
    self.is_crawling = False
