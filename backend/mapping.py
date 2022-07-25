from utils import read_json
from config import TRAINING_FILENAME, MODEL_FILENAME
from spotify_metadata import SpotifySongMetadata


def apply_filter(tagname: str, metadata: SpotifySongMetadata):
    """
    Apply filter to metadata object using tag name.
    Data in model.json is used to get the appropriate filter values.

    Examples
    --------
    >>> metadata = SpotifySongMetadata()
    >>> apply_filter('happy', metadata)
    >>> metadata
    {
        "max_acousticness": 0.4727109413285636,
        "max_speechiness": 0.09848461298097062,
        "min_danceability": 0.6631031309083332,
        "min_energy": 0.5359383016452571,
        "min_instrumentalness": 0.5748781296386368,
        "min_valence": 0.47506271484973367,
        "seed_tracks": "2o3VdzVj1qRGJpLI5y2qMj,5GzllvwuJMnljMJRHME784"
    }
    """

    model_data = read_json(MODEL_FILENAME)
    model = model_data.get(tagname)
    if model is not None:
        metadata.set_from_dict(model)

def get_moods():
    training_data = read_json(TRAINING_FILENAME)
    moods = list(set([mood.replace('_vocal', '').replace('_instrumental', '') for mood in training_data.keys()]))

    return moods
