from spotify_api import SpotifyAPIHandler, SpotifySongMetadata
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from config import MODEL_FILENAME
from utils import read_json
import matplotlib.pyplot as plt

if __name__ == '__main__':
  handler = SpotifyAPIHandler(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
  
  tagname = 'happy'

  # Shaka Surf
  happy1 = "2o3VdzVj1qRGJpLI5y2qMj"

  # Love like a river
  happy2 = "5GzllvwuJMnljMJRHME784"

  # The Inner Pattern
  sad1 = "77yA6alNN6ToGYpWT4OvTw"

  songs = [ happy1, happy2, sad1 ]

  for song in songs:
    timbre = [ [] for i in range(12) ]
    analysis = handler.get_audio_analysis(song)
    x = range(len(analysis['segments']))
    for segment in analysis['segments']:
      segment_timbre = segment['timbre']
      for i in range(12):
        timbre[i].append(segment_timbre[i])

    for i in range(12):
      plt.plot(x, timbre[i])
      print(len(timbre[i]))
    
    plt.show()

      
