from spotify_api import SpotifyAPIHandler, SpotifySongMetadata
from mapping import apply_filter
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from utils import read_json
from config import MODEL_FILENAME


if __name__ == '__main__':
    handler = SpotifyAPIHandler(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
    spotify_track_url = 'https://open.spotify.com/track'
    tags = read_json(MODEL_FILENAME).keys()

    for tag in tags:
        metadata = SpotifySongMetadata()
        apply_filter(tag, metadata)
        track_ids = handler.get_recommendations(metadata, limit=1)
        for id in track_ids:
            print(f'{tag}:\n{spotify_track_url}/{id}')
