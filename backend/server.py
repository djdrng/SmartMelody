from fastapi import FastAPI
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotify_api import SpotifyAPIHandler, SpotifySongMetadata
from mapping import apply_filter

app = FastAPI()

@app.get('/get-recommendations')
def get_recommendations(mood: str, limit: int = 1):
    handler = SpotifyAPIHandler(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )

    metadata = SpotifySongMetadata()
    apply_filter(mood, metadata)
    track_ids = handler.get_recommendations(metadata, limit=limit)

    return track_ids
