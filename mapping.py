def happy(metadata):
    metadata.set('seed_genres', ('jazz', 'happy', 'chill'))
    metadata.set('seed_tracks', ('2o3VdzVj1qRGJpLI5y2qMj', '5GzllvwuJMnljMJRHME784'))
    metadata.set('min_instrumentalness', 0.8)
    metadata.set('max_speechiness', 0.2)
    metadata.set('max_energy', 0.5)
    metadata.set('min_valence', 0.7)

def sad(metadata):
    metadata.set('seed_genres', ('ambient', 'sad', 'chill'))
    metadata.set('seed_tracks', ('77yA6alNN6ToGYpWT4OvTw', '0Xms02B4yBtKxUodh8xoTg'))
    metadata.set('min_instrumentalness', 0.8)
    metadata.set('max_speechiness', 0.2)
    metadata.set('max_energy', 0.3)
    metadata.set('max_valence', 0.1)

def horror(metadata):
    metadata.set('seed_tracks', ('4JC8tCwjzDSjgLsKFtJOPk', '7mcKLkGSybFIhaL1Q1HXrY'))
    metadata.set('min_instrumentalness', 0.8)
    metadata.set('max_speechiness', 0.2)
    metadata.set('max_acousticness', 0.1)
    metadata.set('min_energy', 0.6)
    metadata.set('max_valence', 0.1)
