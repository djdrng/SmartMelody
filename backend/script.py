from spotify_api import SpotifyAPIHandler, SpotifySongMetadata
from mapping import apply_filter
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


if __name__ == '__main__':
    handler = SpotifyAPIHandler(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)

    spotify_track_url = 'https://open.spotify.com/track'

    metadata = SpotifySongMetadata()
    apply_filter('happy', metadata)
    track_ids = handler.get_recommendations(metadata, limit=3)
    for id in track_ids:
        print(f'Happy:\n{spotify_track_url}/{id}')
