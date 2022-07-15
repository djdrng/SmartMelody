import itertools
import requests
import json
import random
# from spotipy import Spotify
# from spotipy.oauth2 import SpotifyOAuth


class SpotifySongMetadata:
    def __init__(self) -> None:
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

    def set(self, attr: str, value: any) -> None:
        """
        Set attribute value
        """
        if attr in self.seed_attrs:
            # seed attributes should be comma separated strings
            # this converts list of strings to comma separated string
            if not isinstance(value, str):
                value = ','.join(value)
        elif attr in self.numerical_attrs:
            if not self.numerical_attrs[attr](value):
                raise ValueError(
                    f'Invalid value {value} for attribute "{attr}"'
                )
        else:
            raise ValueError(f'Invalid attribute "{attr}"')

        self.metadata[attr] = value

    def set_from_dict(self, metadata_dict: dict) -> None:
        """
        Set attributes from dictionary.
        """
        for attr, value in metadata_dict.items():
            self.set(attr, value)

    # get value of attribute
    # returns None if attribute hasn't been set
    def get(self, attr: str) -> any:
        """
        Get value of attribute.
        Returns None if attribute hasn't been set.
        """

        if attr not in self.seed_attrs and attr not in self.numerical_attrs:
            raise ValueError(f'Invalid attribute "{attr}"')

        return self.metadata.get(attr)

    def randomize_seeds(self, limit=5) -> None:
        """
        Randomly sample from the seed values
        and get rid of the rest of them.
        This is for executing before getting a song recommendation.
        Spotify requires that there are at most 5 seed values.
        """

        for attr in self.seed_attrs:
            value = self.metadata.get(attr)

            if value is not None:
                # convert comma separated string to list fof strings
                value = value.strip().split(',')
                # choose a sample of seed values
                seed_subset = random.sample(value, min(limit, len(value)))
                # convert list of strings back to comma separated string
                value = ','.join(seed_subset)

                self.metadata[attr] = value

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
        self.AUTH_URL = 'https://accounts.spotify.com/authorize/'
        self.TOKEN_URL = 'https://accounts.spotify.com/api/token/'
        self.BASE_URL = 'https://api.spotify.com/v1/'
        self.AUDIO_FEATURES_URL = self.BASE_URL + 'audio-features/'
        self.RECOMMENDATIONS_URL = self.BASE_URL + 'recommendations/'

        self.authenticate_client()

    def http_get(self, url: str, *args: tuple[any, ...], **kwargs: dict[str, any]) -> any:
        """
        HTTP GET Request
        """

        return requests.get(url, headers=self.headers, *args, **kwargs)

    def http_post(self, url: str, *args: tuple[any, ...], **kwargs: dict[str, any]) -> any:
        """
        HTTP POST Request
        """

        return requests.post(url, headers=self.headers, *args, **kwargs)


    def authenticate_client(self) -> None:
        """
        Authenticate client using client credentials flow.
        This must be done before sending HTTP requests.
        """

        auth_response = self.http_post(
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

    # commenting this out for now since we're not using oauth yet:
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

        response = self.http_get(self.RECOMMENDATIONS_URL, params=params)
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

        response = self.http_get(self.AUDIO_FEATURES_URL + track_id)

        return response.json()

    def get_multiple_audio_features(self, track_ids: list[str]):
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
        response = self.http_get(self.AUDIO_FEATURES_URL, params=params)

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
