import json

with open('rankings.json', 'r') as rankings_file:
    rankings_data = rankings_file.read()
rankings = json.loads(rankings_data)

with open('players.json', 'r') as players_file:
    players_data = players_file.read()
players = json.loads(players_data)

def sort_rankings():
    global rankings
    rankings.sort(key=lambda p: p["points"], reverse=True)

def save_rankings():
    with open('rankings.json', 'w') as rankings_file:
        json.dump(rankings, rankings_file)

def save_players():
    with open('players.json', 'w') as players_file:
        json.dump(players, players_file)

def update_player(name, tournamentName, tournamentPoints):
    print("HEYY")
    global players
    global rankings
    players[name]["tournaments"][tournamentName] = tournamentPoints
    for i in range(len(rankings)):
        if rankings[i]["name"]==name:
            rankings[i]["points"] += tournamentPoints
            break
    save_players()
    save_rankings()

def clear_rankings():
    global rankings
    rankings = []
    save_rankings()

def clear_players():
    global players
    players = {}
    save_players()

#method for updating rankings after a match
