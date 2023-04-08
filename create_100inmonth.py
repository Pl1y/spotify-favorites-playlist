import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Authentication

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-top-read user-library-read playlist-modify-public",
    cache_path=".spotifycache"
))

# Retrieve up to 100 top tracks (in batches of 50)
limit = 50
offset = 0
top_tracks = []
while offset < 50:
    results = sp.current_user_top_tracks(limit=limit, offset=offset, time_range="short_term")
    for i, track in enumerate(results['items']):
        artists = ", ".join([artist['name'] for artist in track['artists']])
        print(f"{offset+i+1:03}. {artists} - {track['name']}")
    top_tracks.extend(results['items'])
    offset += limit

# If exists, modify that playlist instead of creating new

playlist_name = "Most listened to"
playlist_exists = False
playlists = sp.user_playlists(sp.current_user()['id'])
for playlist in playlists['items']:
    if playlist['name'] == playlist_name:
        playlist_id = playlist['id']
        playlist_exists = True
        break

# Use the spotipy library to create a new playlist with the name "Most listened to" if it doesn't exist.
if not playlist_exists:
    playlist = sp.user_playlist_create(sp.current_user()['id'], playlist_name)
    playlist_id = playlist['id']

# Use the spotipy library to replace all tracks in the existing playlist with the top 100 songs.
track_ids = [track['id'] for track in top_tracks]
sp.playlist_replace_items(playlist_id, track_ids)