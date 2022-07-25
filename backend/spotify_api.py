from multiprocessing.sharedctypes import Value
import requests
import string
from secrets import choice
from urllib.parse import urlencode
from spotify_metadata import SpotifySongMetadata
import base64
from datetime import date, datetime

class SpotifyAPIHandler:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        # credentials
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        # HTTP headers
        self.headers = {}

        # Spotify API urls
        self.AUTH_URL = 'https://accounts.spotify.com/authorize/'
        self.TOKEN_URL = 'https://accounts.spotify.com/api/token/'
        self.BASE_URL = 'https://api.spotify.com/v1/'
        self.TRACK_URL = self.BASE_URL + 'tracks/'
        self.AUDIO_FEATURES_URL = self.BASE_URL + 'audio-features/'
        self.AUDIO_ANALYSIS_URL = self.BASE_URL + 'audio-analysis/'
        self.RECOMMENDATIONS_URL = self.BASE_URL + 'recommendations/'
        self.PLAYBACK_URL = self.BASE_URL + 'me/player/'
        self.PLAY_URL = self.PLAYBACK_URL + 'play/'

        self.authenticate_client()

    def __http_get(self, url: str, *args: tuple[any, ...], **kwargs: dict[str, any]) -> any:
        """
        HTTP GET Request
        """
        headers = self.headers
        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            kwargs.pop('headers')
        return requests.get(url, headers=headers, *args, **kwargs)

    def __http_post(self, url: str, *args: tuple[any, ...], **kwargs: dict[str, any]) -> any:
        """
        HTTP POST Request
        """
        headers = self.headers
        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            kwargs.pop('headers')
        return requests.post(url, headers=headers, *args, **kwargs)

    def __http_put(self, url: str, *args: tuple[any, ...], **kwargs: dict[str, any]) -> any:
        """
        HTTP PUT Request
        """
        headers = self.headers
        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            kwargs.pop('headers')
        return requests.put(url, headers=headers, *args, **kwargs)
    
    def validate_tokens(self) -> None:
        """
        Validate that the current authorization token is still valid.
        If it is invalid, call refresh_tokens to request a new token.
        """
        if self.token_expiry < datetime.now().timestamp():
            self.refresh_tokens()
    
    def authenticate_client(self) -> None:
        """
        Authenticate client using client credentials flow.
        This must be done before sending HTTP requests.
        """

        auth_response = self.__http_post(
            self.TOKEN_URL,
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            },
        )

        # save the access token
        auth_response_data = auth_response.json()
        access_token = auth_response_data['access_token']

        # authorization header
        self.headers['Authorization'] = f'Bearer {access_token}'
    
    def login_user(self) -> any:
        """
        Generate a URL to send user to Spotify authentication page.
        Once this link is visited, it should redirect the user to REDIRECT_URI, set in credentials.py
        """

        if 'Authorization' not in self.headers:
            raise ValueError('Not authenticated, run self.authenticate_client() first')

        self.state = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(16)) 

        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'state': self.state,
            'scope': 'user-modify-playback-state',
            'show_dialog': True
        } 
        return f'{self.AUTH_URL}?{urlencode(params)}'
    
    def authenticate_user(self, code: str, redirect_state: str) -> None:
        """
        Setup access token for the user that is logged in

        Parameters:
            code (str): The access code returned from the login request
            redirect_state (str): The state returned from the redirect.
            If it doesn't match self.state, will deny request.
        """

        if self.state != redirect_state:
            raise ValueError('Mismatched redirect_state variable, please perform login steps again.')

        params = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        data = f'{self.client_id}:{self.client_secret}'
        headers = {
            'Authorization': f'Basic {base64.urlsafe_b64encode(data.encode()).decode()}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = self.__http_post(self.TOKEN_URL, headers=headers, params=urlencode(params))

        if response.status_code != 200:
            raise ValueError('Issue requesting access token for user. Please rerun login-user()')

        # save the access token and the expires_in time
        response_data = response.json()
        access_token = response_data['access_token']
        expires_in = response_data['expires_in']

        # set authorization header and time of expiry
        self.headers['Authorization'] = f'Bearer {access_token}'
        self.token_expiry = datetime.now().timestamp() + expires_in
        self.refresh_token = response_data['refresh_token']

    def refresh_tokens(self) -> None:
        """
        Refresh the user access tokens. Will reset self.headers and self.token_expiry
        """
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        data = f'{self.client_id}:{self.client_secret}'
        headers = {
            'Authorization': f'Basic {base64.urlsafe_b64encode(data.encode()).decode()}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = self.__http_post(self.TOKEN_URL, headers=headers, params=urlencode(params))

        if response.status_code != 200:
            raise ValueError('Issue requesting access token for user. Please rerun login-user()')

        # save the access token and the expires_in time
        response_data = response.json()
        access_token = response_data['access_token']
        expires_in = response_data['expires_in']

        # set authorization header and time of expiry
        self.headers['Authorization'] = f'Bearer {access_token}'
        self.token_expiry = datetime.now().timestamp() + expires_in

    def get_track(self, track_id: str) -> dict:
        """
        Get track information from track ID.

        Examples
        --------
        >>> handler = SpotifyAPIHandler(...)
        >>> track_info = handler.get_track('7e4G3lltabdGTRQonrKYaY')
        >>> track_info
        {
            "album": {
                "album_type": "single",
                "artists": [...],
                "available_markets": [...],
                "external_urls": {
                    "spotify": "https://open.spotify.com/album/4KElxuVixn25l3SOguxB8Z"
                },
                "href": "https://api.spotify.com/v1/albums/4KElxuVixn25l3SOguxB8Z",
                "id": "4KElxuVixn25l3SOguxB8Z",
                "images": [...],
                "name": "Lullaby of Woe (From \"The Witcher 3\")",
                "release_date": "2018-02-15",
                "release_date_precision": "day",
                "total_tracks": 1,
                "type": "album",
                "uri": "spotify:album:4KElxuVixn25l3SOguxB8Z"
            },
            "artists": [...],
            "available_markets": [],
            "disc_number": 1,
            "duration_ms": 150019,
            "explicit": false,
            "external_ids": {
                "isrc": "QZ22B1901514"
            },
            "external_urls": {
                "spotify": "https://open.spotify.com/track/7e4G3lltabdGTRQonrKYaY"
            },
            "href": "https://api.spotify.com/v1/tracks/7e4G3lltabdGTRQonrKYaY",
            "id": "7e4G3lltabdGTRQonrKYaY",
            "is_local": false,
            "name": "Lullaby of Woe (From \"The Witcher 3\")",
            "popularity": 0,
            "preview_url": null,
            "track_number": 1,
            "type": "track",
            "uri": "spotify:track:7e4G3lltabdGTRQonrKYaY"
        }
        """

        if 'Authorization' not in self.headers:
            raise ValueError('Not authenticated, run self.authenticate_client() first')

        response = self.__http_get(self.TRACK_URL + track_id)

        return response.json()

    def get_multiple_tracks(self, track_ids: list[str]) -> list[dict]:
        """
        Get track information from multiple track IDs.
        This is equivalent to looping for track IDs
        and calling self.get_track().
        This is a separate method because Spotify has a separate endpoint
        used for obtaining information for multiple songs at once.

        Examples
        --------
        >>> handler = SpotifyAPIHandler(...)
        >>> track_infos = handler.get_track(['7e4G3lltabdGTRQonrKYaY', '3mMWlBGocBwsS1Q0o9wvlc'])
        >>> track_infos
        [
            {
                "album": {...},
                "artists": [...],
                ...
            },
            {
                "album": {...},
                "artists": [...],
                ...
            }
        ]
        """

        if 'Authorization' not in self.headers:
            raise ValueError('Not authenticated, run self.authenticate_client() first')

        params = {'ids': ','.join(track_ids)}
        response = self.__http_get(self.TRACK_URL, params=params)

        return response.json()['tracks']

    def get_recommendations(self, metadata: SpotifySongMetadata, limit :int = 1) -> list[str]:
        """
        Get track recommendations based on metadata object.

        Examples
        --------
        >>> metadata = SpotifySongMetadata()
        >>> metadata.set('seed_tracks', ['77yA6alNN6ToGYpWT4OvTw', '7mcKLkGSybFIhaL1Q1HXrY'])
        >>> metadata.set('min_instrumentalness', 0.8)
        >>> metadata.set('max_valence', 0.1)
        >>> handler = SpotifyAPIHandler(...)
        >>> recommended_track_ids = handler.get_recommendations(metadata, limit=3)
        >>> recommended_track_ids
        ['3G4yDdFmz6G8roJ4Rohpue', '4l3SOyz1WG7TLFvcIKcJ6Y', '5tdIOmrUt4TGqi2DiFQ2M4']
        """

        if 'Authorization' not in self.headers:
            raise ValueError('Not authenticated, run self.authenticate_client() first')

        # randomize seeds
        # this must be done to make sure only 5 seeds are sent in the request
        metadata.randomize_seeds()
        # convert metadata to dictionary of request parameters
        params = dict(metadata.dict(), limit=limit)

        response = self.__http_get(self.RECOMMENDATIONS_URL, params=params)
        # get track IDs from response
        track_ids = [track['id'] for track in response.json().get('tracks', [])]

        return track_ids

    def get_audio_features(self, track_id: str) -> dict:
        """
        Get audio features of a song by track ID.

        Examples
        --------
        >>> handler = SpotifyAPIHandler(...)
        >>> handler.get_audio_features('3G4yDdFmz6G8roJ4Rohpue')
        {
            "acousticness": 0.0462,
            "danceability": 0.328,
            "energy": 0.42,
            "valence": 0.0365,
            ...
        }
        """

        if 'Authorization' not in self.headers:
            raise ValueError('Not authenticated, run self.authenticate_client() first')

        response = self.__http_get(self.AUDIO_FEATURES_URL + track_id)

        return response.json()

    def get_multiple_audio_features(self, track_ids: list[str]) -> dict:
        """
        Get audio features of multiple songs by track IDs.
        This is equivalent to looping for track IDs
        and calling self.get_audio_features().
        This is a separate method because Spotify has a separate endpoint
        used for obtaining audio features for multiple songs at once.

        Examples
        --------
        >>> handler = SpotifyAPIHandler(...)
        >>> handler.get_multiple_audio_features(['3G4yDdFmz6G8roJ4Rohpue', '4l3SOyz1WG7TLFvcIKcJ6Y'])
        {
            "acousticness": [0.0462, 0.00269],
            "danceability": [0.328, 0.586],
            "energy": [0.42, 0.75],
            "valence": [0.0365, 0.0978],
            ...
        }
        """

        if 'Authorization' not in self.headers:
            raise ValueError('Not authenticated, run self.authenticate_client() first')

        # great comma separated string of IDs
        params = {'ids': ','.join(track_ids)}
        response = self.__http_get(self.AUDIO_FEATURES_URL, params=params)

        # set up dictionary of audio features
        features_data = {}
        for features in response.json()['audio_features']:
            if features is None:
                continue

            for k, v in features.items():
                try:
                    features_data[k].append(v)
                except KeyError:
                    features_data[k] = [v]

        return features_data

    def get_audio_analysis(self, track_id: str) -> dict:
        """
        Get audio analysis of a song by track ID.

        Examples
        --------
        >>> handler = SpotifyAPIHandler(...)
        >>> handler.get_audio_analysis('3G4yDdFmz6G8roJ4Rohpue')
        {
            "acousticness": 0.0462,
            "danceability": 0.328,
            "energy": 0.42,
            "valence": 0.0365,
            ...
        }
        """

        if 'Authorization' not in self.headers:
            raise ValueError('Not authenticated, run self.authenticate_client() first')

        response = self.__http_get(self.AUDIO_ANALYSIS_URL + track_id)

        return response.json()

    def playback_track(self, track_ids: list[str], context_uri: str = None) -> None:
        """
        Starts audio playback on the user's spotify account.

        Parameters:
            track_ids (list(str)): The list of track uri's to playback

        Optional Parameters:
            context_uri (str): The album, playlist or genre seed to continue additional playback
        
        Returns:
            None
        """

        if 'Authorization' not in self.headers:
            raise ValueError('Not authenticated, run self.authenticate_client() first')
        
        self.validate_tokens()

        params = {
            'context_uri': context_uri,
            'uris': track_ids
        }

        response = self.__http_put(self.PLAY_URL, params=params)

        if response.status_code == 403:
            raise ValueError('Premium Account not detected, run self.login_user() and follow login URL')
        
        print(response.json())
