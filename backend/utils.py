import json

def read_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    return data

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
