import json

current_resource_map = [
    "resources", "resources/audio", "resources/font", "resources/icon"
]

with open("tic-tac-toe/resources/source.json", "w") as file:
    json.dump(current_resource_map, file, indent=2)
