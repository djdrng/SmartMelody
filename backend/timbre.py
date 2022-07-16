from spotify_api import SpotifyAPIHandler, SpotifySongMetadata
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from config import MODEL_FILENAME
from utils import read_json

if __name__ == '__main__':
  handler = SpotifyAPIHandler(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
  
  tagname = 'happy'
  model_data = read_json(MODEL_FILENAME)
  model = model_data.get(tagname)
  if model is not None:
    for track in model['seed_tracks'].split(','):
      aa = handler.get_audio_analysis(track)['segments']
