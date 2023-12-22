import json
from box import ConfigBox

def load_json(file):
    with open(path) as f:
        content = json.load(f)
    return ConfigBox(content)

def save_json(file, content):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)