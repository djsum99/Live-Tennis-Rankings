from Player import Player
from Tournament import Tournament
import json

with open('rankings.json', 'r') as rankings_file:
    rankings_data = rankings_file.read()

rankings = json.loads(rankings_data)

def sort_rankings():
    rankings.sort(key=lambda p: p["points"], reverse=True)
    with open('rankings.json', 'w') as rankings_file:
        json.dump(rankings, rankings_file)

def add_players(tournament):
    for player in tournament.bracket.keys():
        for p in rankings:
            if p["name"]==player:
                break
        else:
            newPlayer = {"name": player, "points": 0}
            rankings.append(newPlayer)

#method for updating rankings after a match
