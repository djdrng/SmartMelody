import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# These are for Devinn's Test Project for now, we will need to update later
CLIENT_ID = 'e6bb4aa58081446ab6938f38bcce50f3'
CLIENT_SECRET = 'a2fc514be5be4be7ab9e33a433e1dc2a'
REDIRECT_URI = 'http://localhost:8080'

class SpotifySongMetadata:
  def __init__(self):
    self._genres = []
    self._limit = 0
    self._acousticness = (0, 0, 0)
    self._danceability = (0, 0, 0)
    self._energy = (0, 0, 0)
    self._instrumentalness = (0, 0, 0)
    self._liveness = (0, 0, 0)
    self._loudness = (0, 0, 0)
    self._mode = (0, 0, 0)
    self._speechiness = (0, 0, 0)
    self._valence = (0, 0, 0)

  # Define Property Getters
  @property
  def genres(self) -> list[str]:
    return self._genres
  
  @property
  def limit(self) -> int:
    return self._limit

  @property
  def acousticness(self) -> tuple[float]:
    return self._acousticness

  @property
  def danceability(self) -> tuple[float]:
    return self._danceability

  @property
  def energy(self) -> tuple[float]:
    return self._energy

  @property
  def instrumentalness(self) -> tuple[float]:
    return self._instrumentalness

  @property
  def liveness(self) -> tuple[float]:
    return self._liveness

  @property
  def loudness(self) -> tuple[float]:
    return self._loudness

  @property
  def mode(self) -> tuple[float]:
    return self._mode

  @property
  def speechiness(self) -> tuple[float]:
    return self._speechiness

  @property
  def valence(self) -> tuple[float]:
    return self._valence
  
  # Define Property Setters
  @genres.setter
  def genres(self, new_genres: list[str]) -> None:
    self._genres = new_genres

  @limit.setter
  def limit(self, new_limit: int) -> None:
    self._limit = new_limit

  @acousticness.setter
  def acousticness(self, new_acousticness: tuple[float]) -> None:
    self._acousticness = new_acousticness

  @danceability.setter
  def danceability(self, new_danceability: tuple[float]) -> None:
    self._danceability = new_danceability

  @energy.setter
  def energy(self, new_energy: tuple[float]) -> None:
    self._energy = new_energy

  @instrumentalness.setter
  def instrumentalness(self, new_instrumentalness: tuple[float]) -> None:
    self._instrumentalness = new_instrumentalness

  @liveness.setter
  def liveness(self, new_liveness: tuple[float]) -> None:
    self._liveness = new_liveness

  @loudness.setter
  def loudness(self, new_loudness: tuple[float]) -> None:
    self._loudness = new_loudness

  @mode.setter
  def mode(self, new_mode: tuple[float]) -> None:
    self._mode = new_mode

  @speechiness.setter
  def speechiness(self, new_speechiness: tuple[float]) -> None:
    self._speechiness = new_speechiness

  @valence.setter
  def valence(self, new_valence: tuple[float]) -> None:
    self._valence = new_valence

class SpotifyAPIHandler:
  def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
    self._client_id = client_id
    self._client_secret = client_secret
    self._redirect_uri = redirect_uri


    # URLS
    self._auth_url = 'https://accounts.spotify.com/authorize'
    self._token_url = 'https://accounts.spotify.com/api/token'
    self._base_url = 'https://api.spotify.com/v1/'
  
  # HTTP Operations
  def post_request(self, url: str, args: any) -> any:
    return requests.post(url, args)

  def get_request(self, url: str, request: str, headers: dict[any, any]) -> any:
    return requests.get(url + request, headers=headers)

  def add_access_token_to_header(self) -> None:
    auth_response = self.post_request(self._token_url, {
      'grant_type': 'client_credentials',
      'client_id': self._client_id,
      'client_secret': self._client_secret,
    })

    # save the access token
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    self._headers = {
      'Authorization': f'Bearer {access_token}'
    }

  def get_tracks_from_metadata(self, metadata: SpotifySongMetadata):
    r = self.get_request(self._base_url, 'recommendations', headers=self._headers.update(metadata))
    tracks = r.json()['tracks']
    return tracks

  def get_song_recommendation_for_user(self, metadata: SpotifySongMetadata):
    
  
  def prompt_user_authentication(self):
    oauth = SpotifyOAuth(client_id=self._client_id,
                         client_secret=self._client_secret,
                         redirect_uri=self._redirect_uri,
                         scope="user-library-read,user-modify-playback-state")
    self._spotipy = spotipy.Spotify(auth_manager=oauth)

  def start_user_playback(self, track_uri: str):
    self._spotipy.start_playback(uris=track_uri)
    
# acousticness, danceability, energy, instrumentalness, liveness, loudness, mode, speechiness, valence

if (__name__ == '__main__'):
  handler = SpotifyAPIHandler(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
  handler.add_access_token_to_header()

  metadata = SpotifySongMetadata()
  metadata.limit = 1
  metadata.acousticness = (0.0, 0.1, 0.2)
  metadata.danceability = (0.0, 0.1, 0.2)
  metadata.energy = (0.0, 0.1, 0.2)
  metadata.instrumentalness = (0.0, 0.1, 0.2)
  metadata.liveness = (0.0, 0.1, 0.2)
  metadata.loudness = (0.0, 0.1, 0.2)
  metadata.mode = (0.0, 0.1, 0.2)
  metadata.speechiness = (0.0, 0.1, 0.2)
  metadata.valence = (0.0, 0.1, 0.2)

  handler.get_song_from_metadata_ranges(metadata)

  