import json

data = {
            "theme": "reddit",
            "hotkeys": [],
            "addProcessData": [],
            "defaultFont": "Bahnschrift",
            "warnNoSound": False,
            "useGIF": False
        }
        
with open("../config.json", "w") as jsonFile:
    json.dump(data, jsonFile)
    print("[EMERGENCY LOG] Dumped all data. Loaded JSON data to defaults.")
    exit(0)