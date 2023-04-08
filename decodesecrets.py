import base64
import os

# Get the contents of the SPOTIFY_CACHE secret and decode it from base64
spotify_cache_encoded = os.environ['SPOTIPY_CACHE']
spotify_cache_decoded = base64.b64decode(spotify_cache_encoded)

# Write the decoded contents to a file
with open('.spotifycache', 'wb') as f:
    f.write(spotify_cache_decoded)