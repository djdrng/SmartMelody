import numpy as np
from scipy.stats import t, sem
from utils import read_json, save_json
from spotify_api import SpotifyAPIHandler
from spotify_metadata import SpotifySongMetadata
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from config import TAGS_OF_INTEREST, TRAINING_FILENAME, MODEL_FILENAME

def t_confidence_intervals(data: list[float], alpha: float = 0.95) -> tuple[float, float]:
    """
    Given data in an iterable, this returns the Student's t confidence intervals.
    Set alpha to adjust the targeted coverage probability.
    """

    return t.interval(
        alpha=alpha,
        df=len(data) - 1,
        loc=np.mean(data),
        scale=sem(data)
    )

def generate_metadata(features_data: dict[str, list[float]]) -> dict[str, float]:
    """
    Generates metadata by computing confidence intervals for every tag.

    Examples
    --------
    >>> features_data = {'valence': [0.1, 0.1, 0.05, 0.02, 0.8, 0.3]}
    >>> generate_metadata(features_data)
    {
        "max_valence": 0.5396757326423229
    }
    """

    # create empty metadata object
    metadata = SpotifySongMetadata()

    for tagname in TAGS_OF_INTEREST:
        # get confidence intervals
        low, high = t_confidence_intervals(features_data[tagname])
        low = max(low, 0.0)
        high = min(high, 1.0)

        if high < 0.5:
            # if the upper limit is less than 50%
            # then the upper limit should be the maximum
            metadata.set('max_' + tagname, high)
        elif low > 0.5:
            # if the lower limit is more than 50%
            # then the lower limit should be the minimum
            metadata.set('min_' + tagname, low)
        else:
            if (0.5 - low) < (high - 0.5):
                # if the lower limit is closer to 50% than the upper limit
                # then the lower limit should be the minimum
                metadata.set('min_' + tagname, low)
            else:
                # if the upper limit is closer to 50% than the lower limit
                # then the upper limit should be the maximum
                metadata.set('max_' + tagname, high)

    return metadata

def train() -> None:
    """
    Read track IDs from training.json,
    generate metadata using confidence intervals,
    and save metadata to model.json.
    This must be run everytime training.json is edited
    (or when there are major changes to the training source code).
    """

    handler = SpotifyAPIHandler(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)

    training_data = read_json(TRAINING_FILENAME)
    model_data = read_json(MODEL_FILENAME)

    for tagname, track_ids in training_data.items():
        features_data = handler.get_multiple_audio_features(track_ids)
        metadata = generate_metadata(features_data)
        metadata.set('seed_tracks', track_ids)

        model_data[tagname] = metadata.dict()

    save_json(model_data, MODEL_FILENAME)

if __name__ == '__main__':
    train()
