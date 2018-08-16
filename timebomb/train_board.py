# import json
#
# data = {}
# data["email"] = "anthonydu77120@hotmail.fr"
# data["password"] = "bc0a239cd4875a933da879c7990033808ecf4863"
# new_player = {}
# new_player["Antho"] = data
#
# with open('bdd_players.json', 'w') as outfile:
#     json.dump(new_player, outfile)
#
#
# with open('bdd_players.json', 'r') as json_file:
#     data = json.load(json_file)
#     print data["Antho"]

import re

# verify_expression = re.compile(r"^[a-zA-Z0-9.-_\S]+@[a-zA-Z0-9.-\S]+\.([a-zA-Z]{2,3})$")
verify_expression = re.compile(r"^[\w\S\._-]+@[\w\S\.-]+\.([a-zA-Z]{2,3})$")

print re.match(verify_expression, "ara")

