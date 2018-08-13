import json

# data = {}
# data["email"] = "anthonydu77120@hotmail.fr"
# data["password"] = "bc0a239cd4875a933da879c7990033808ecf4863"
# new_player = {}
# new_player["Antho"] = data
#
# with open('bdd_players.json', 'w') as outfile:
#     json.dump(new_player, outfile)


with open('bdd_players.json') as json_file:
    data = json.load(json_file)
    print data["Antho"]
