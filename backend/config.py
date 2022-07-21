from pathlib import Path

# file that has training data
TRAINING_FILENAME = Path(__file__).parent / 'training.json'

# file that has current model data
MODEL_FILENAME = Path(__file__).parent / 'model.json'

# tags that are explored when training
TAGS_OF_INTEREST = [
    'acousticness',
    'danceability',
    'energy',
    'instrumentalness',
    'speechiness',
    'valence',
]
