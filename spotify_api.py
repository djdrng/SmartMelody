import itertools
import requests
import json
# from spotipy import Spotify
# from spotipy.oauth2 import SpotifyOAuth


class SpotifySongMetadata:
    def __init__(self):
        # dictionary for holding metadata parameters
        self.metadata = {}

        # seed parameters
        # these are required parameters for recommendations
        self.seed_attrs = [
            'seed_artists',
            'seed_genres',
            'seed_tracks',
        ]

        valid_fraction = lambda x: x >= 0.0 and x <= 1.0
        # prefixes for numerical parameters
        prefixes = [
            'target',
            'min',
            'max',
        ]
        # numerical parameter validators
        # dictionary, where key is name of the prefix-less attribute
        # and value is a function that validates the value of the attribute
        numerical_attr_validators = {
            'acousticness': valid_fraction,
            'danceability': valid_fraction,
            'energy': valid_fraction,
            'instrumentalness': valid_fraction,
            'liveness': valid_fraction,
            'loudness': lambda x: x <= 0,
            'mode': lambda x: x in (0, 1),
            'speechiness': valid_fraction,
            'valence': valid_fraction,
        }

        # add prefixes to all numerical attributes
        self.numerical_attrs = {
            f'{i[0]}_{i[1]}': numerical_attr_validators[i[1]]
            for i in itertools.product(prefixes, numerical_attr_validators)
        }

    # set attribute value
    def set(self, attr: str, value: any):
        if attr in self.seed_attrs:
            # seed attributes should be comma separated strings
            # this converts list of strings to comma separated string
            value = ','.join(value)
        elif attr in self.numerical_attrs:
            if not self.numerical_attrs[attr](value):
                raise ValueError(
                    f'Invalid value {value} for attribute "{attr}"'
                )
        else:
            raise ValueError(f'Invalid attribute "{attr}"')

        self.metadata[attr] = value

    # get value of attribute
    # returns None if attribute hasn't been set
    def get(self, attr: str):
        if attr not in self.seed_attrs and attr not in self.numerical_attrs:
            raise ValueError(f'Invalid attribute "{attr}"')

        return self.metadata.get(attr)

    # get metadata dictionary
    def dict(self) -> dict:
        return self.metadata

    # get metadata iterator for dictionary conversion
    def __iter__(self) -> any:
        for attr in self.metadata:
            yield (attr, self.metadata[attr])

    # convert and return metadata dictionary to string
    def __str__(self) -> str:
        return str(self.metadata)

    # convert and return metadata dictionary to pretty formatted string
    def __repr__(self) -> str:
        return json.dumps(self.metadata, sort_keys=True, indent=4)

class SpotifyAPIHandler:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        # credentials
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        # HTTP headers
        self.headers = {}

        # Spotify API urls
        self.AUTH_URL = 'https://accounts.spotify.com/authorize'
        self.TOKEN_URL = 'https://accounts.spotify.com/api/token'
        self.BASE_URL = 'https://api.spotify.com/v1/'
        self.RECOMMENDATIONS_URL = self.BASE_URL + 'recommendations/'
  
    # HTTP Operations
    def http_post(self, url: str, *args: tuple[any, ...], **kwargs: dict[any, any]) -> any:
        return requests.post(url, headers=self.headers, *args, **kwargs)

    def http_get(self, url: str, *args: tuple[any, ...], **kwargs: dict[any, any]) -> any:
        return requests.get(url, headers=self.headers, *args, **kwargs)

    # authentical client using client credentials flow
    def authenticate_client(self) -> None:
        auth_response = requests.post(
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

    # commenting this out for now since we're not using oauth yet
    # def oauth_user(self):
    #     oauth = SpotifyOAuth(
    #         client_id=self.client_id,
    #         client_secret=self.client_secret,
    #         redirect_uri=self.redirect_uri,
    #         scope="user-library-read,user-modify-playback-state"
    #     )

    #     self.spotipy = Spotify(auth_manager=oauth)

    # def start_user_playback(self, track_uri: str):
    #     self.spotipy.start_playback(uris=track_uri)

    def get_recommendations(self, metadata: dict[str, any], limit=1):
        params = dict(dict(metadata), limit=limit)
        response = self.http_get(self.RECOMMENDATIONS_URL, params=params)
        track_ids = [track['id'] for track in response.json().get('tracks', [])]

        return track_ids
