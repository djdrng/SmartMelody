import imp
from pathlib import Path

TRAINING_FILENAME = Path(__file__).parent / 'training.json'

MODEL_FILENAME = Path(__file__).parent / 'model.json'

TAGS_OF_INTEREST = [
    'acousticness',
    'danceability',
    'energy',
    'instrumentalness',
    'speechiness',
    'valence',
]