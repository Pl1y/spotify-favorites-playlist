import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Set up authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-library-read playlist-modify-public",
    cache_path=".spotifycache"
))

# Retrieve up to 200 saved tracks (in batches of 50)
limit = 50
offset = 0
saved_tracks = []
while offset < 200:
    results = sp.current_user_saved_tracks(limit=limit, offset=offset, market='from_token')
    for i, track in enumerate(results['items']):
        artists = ", ".join([artist['name'] for artist in track['track']['artists']])
        print(f"{offset+i+1:03}. {artists} - {track['track']['name']}")
    saved_tracks.extend(results['items'])
    offset += limit

# Create or modify "Current favourites" playlist
playlist_name = "Current favourites"
existing_playlists = sp.current_user_playlists(limit=50, offset=0)

playlist_id = None
for playlist in existing_playlists['items']:
    if playlist['name'] == playlist_name:
        playlist_id = playlist['id']
        sp.user_playlist_replace_tracks(user=sp.current_user()['id'], playlist_id=playlist_id, tracks=[])
        break

if not playlist_id:
    playlist = sp.user_playlist_create(user=sp.current_user()['id'], name=playlist_name)
    playlist_id = playlist['id']

# Add tracks to playlist in batches of 100 or fewer
track_uris = [item['track']['uri'] for item in saved_tracks]
for i in range(0, len(track_uris), 100):
    sp.user_playlist_add_tracks(user=sp.current_user()['id'], playlist_id=playlist_id, tracks=track_uris[i:i+100])
