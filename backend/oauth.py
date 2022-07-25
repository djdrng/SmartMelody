from spotify_api import SpotifyAPIHandler, SpotifySongMetadata
from mapping import apply_filter
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from utils import read_json
from config import MODEL_FILENAME


if __name__ == '__main__':
    handler = SpotifyAPIHandler(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
    login_url = handler.login_user()

    # Now visit login URL
    print('LOGIN_URL:', login_url)

    # manually set access token and token expiry from response
    handler.headers['Authorization'] = input('ACCESS TOKEN FROM RESPONSE')
    handler.token_expiry = float(input('TOKEN EXPIRY FROM RESPONSE'))

    print(handler.headers)

    # Play a song!
    handler.playback_track(['spotify:track:2o3VdzVj1qRGJpLI5y2qMj'])


