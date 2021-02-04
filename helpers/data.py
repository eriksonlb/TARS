import json

def assistent_data():
    try:
        with open("data/assistent_personality.json") as json_file:
            json.load(json_file)
            json_file.close()

    except FileNotFoundError:
        header = 'personality'
        header = header.replace("'", "")
        with open("data/assistent_personality.json", "w") as json_file:
            json.dump(header, json_file)
            json_file.close()
            