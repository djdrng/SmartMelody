from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotify_api import SpotifyAPIHandler, SpotifySongMetadata
from mapping import apply_filter

app = FastAPI()

# Add origins and middleware for CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/get-recommendations')
async def get_recommendations(mood: str, vocals: bool, limit: int = 1):
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
