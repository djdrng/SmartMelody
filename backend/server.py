from fastapi import FastAPI, Query
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotify_api import SpotifyAPIHandler, SpotifySongMetadata
from mapping import apply_filter

app = FastAPI()

@app.get(
    '/get-tracks',
    summary='Get track information from Spotify track IDs',
    response_description='List of track information',
)
async def get_tracks(
    track_ids: list[str] = Query(..., description='List of Spotify track IDs',
)) -> dict[any]:
    handler = SpotifyAPIHandler(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )

    track_infos = handler.get_multiple_tracks(track_ids)

    return track_infos

@app.get(
    '/get-recommendations',
    summary='Get track recommendation based on mood',
    response_description='List of recommended tracks',
)
async def get_recommendations(
    mood: str = Query(..., description='Specific mood ("happy", "sad", etc.)'),
    vocals: bool = Query(..., description='If true, recommends tracks with vocals, otherwise recommends instrumental tracks'),
    limit: int = Query(default=1, description='Number of tracks to recommend'),
) -> list[str]:
    handler = SpotifyAPIHandler(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )

    tag = mood + '_' + 'instrumental'
    if vocals:
        tag = mood + '_' + 'vocal'

    metadata = SpotifySongMetadata()
    apply_filter(tag, metadata)
    track_ids = handler.get_recommendations(metadata, limit=limit)

    return track_ids
