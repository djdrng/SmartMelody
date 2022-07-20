import json

def read_json(filename: str) -> dict:
    """
    Read json file.
    """

    with open(filename, 'r') as f:
        data = json.load(f)

    return data

def save_json(data: dict, filename: str) -> None:
    """
    Save dictionary to JSON file.
    """

    with open(filename, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
