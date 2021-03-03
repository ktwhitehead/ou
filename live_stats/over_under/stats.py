import datetime

class Stats:
  def __init__(self):
    self.games = {}

  def update(self, update):
    game = update["game"]
    game_data = self.games.get(game) or self.add_new_game(game, update)
    last_update = [game_data["total_points"], game_data["time_elapsed"], game_data["over_under"]]

    if last_update == [update["total_points"], update["time_elapsed"], update["over_under"]]:
      return None

    game_data["total_points"] = update["total_points"]
    game_data["time_elapsed"] = update["time_elapsed"]
    game_data["average_points"] = update["average_points"]
    game_data["over_under"] = update["over_under"]
    game_data["graph_data"][0]["data"].append({ "x": update["time_elapsed"], "y": update["total_points"] })
    game_data["graph_data"][1]["data"].append({ "x": update["time_elapsed"], "y": update["projected_points"] })
    game_data["graph_data"][2]["data"] = [{ "x": 0, "y": update["average_points"] }, { "x": 2880, "y": update["average_points"] }]
    game_data["graph_data"][3]["data"].append({ "x": update["time_elapsed"], "y": update["over_under"] })
    self.games[game] = game_data

    return { game: self.games[game] }

  def add_new_game(self, game, update):
    self.games[game] = self.stat_def()
    return self.stat_def()

  def stat_def(self):
    obj = {
      "total_points": 0,
      "time_elapsed": 0,
      "total_points": 0,
      "over_under": 0,
      "graph_data": [
        { "id": "Total Points", "data": [] },
        { "id": "Projected Points", "data": [] },
        { "id": "Average Points", "data": [] },
        { "id": "BetMGM Over/Under", "data": [] }
      ]
    }

    return obj
