import os
import sys
import json
import requests
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# load local credentials from .env file
from dotenv import load_dotenv
load_dotenv()

# Set up Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.environ['SPOTIFY_CLIENT_ID'],
    client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
    redirect_uri=os.environ['SPOTIFY_REDIRECT_URI'],
    scope='playlist-read-private user-library-read'))

# Get the "Current favourites" playlist ID from Spotify
playlist_name = "Current favourites"
results = sp.current_user_playlists()
playlist_id = None
for item in results['items']:
    if item['name'] == playlist_name:
        playlist_id = item['id']
        break
if playlist_id is None:
    print(f"Playlist '{playlist_name}' not found on Spotify")
    sys.exit(1)

# Get the track IDs from the playlist
track_ids = []
results = sp.playlist_items(playlist_id)
for item in results['items']:
    track_ids.append(item['track']['id'])

# Set up YouTube Music authentication
creds, project = google.auth.default(scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
if not creds or not creds.valid:
    flow = google.auth.transport.requests.Request().from_command_line()
    creds = google.oauth2.credentials.Credentials.from_authorized_user_info(info=flow.run_console().get("token"))
youtube = build('youtube', 'v3', credentials=creds)

# Search for each track on YouTube Music and add them to a new playlist
playlist_name = "Current favourites"
existing_playlists = youtube.playlists().list(part='snippet', mine=True).execute()
existing_playlist_id = None
for item in existing_playlists['items']:
    if item['snippet']['title'] == playlist_name:
        existing_playlist_id = item['id']
        break
if existing_playlist_id is None:
    new_playlist = youtube.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": playlist_name,
            "description": "A playlist of my current favourite songs"
          },
          "status": {
            "privacyStatus": "public"
          }
        }
    ).execute()
    existing_playlist_id = new_playlist['id']
else:
    youtube.playlists().update(
        part='snippet',
        body={
            'id': existing_playlist_id,
            'snippet': {
                'title': playlist_name,
                'description': "A playlist of my current favourite songs"
            }
        }
    ).execute()

for track_id in track_ids:
    # Search for the track on YouTube Music
    search_response = youtube.search().list(
        q=f"{sp.track(track_id)['name']} {sp.track(track_id)['artists'][0]['name']}",
        part='id',
        type='video'
    ).execute()

    # Check if the track was found
    video_id = None
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            break
    if video_id is None:
        print(f"Could not find YouTube video for Spotify track ID {track_id}")
        continue

    # Add the video to the playlist
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={
              "snippet": {
                "playlistId": existing_playlist_id,
                "position": 0,
                "resourceId": {
                  "kind": "youtube#video",
                  "videoId": video_id
                }
              }
            }
        ).execute()
        print(f"Added YouTube video for Spotify track ID {track_id}")
    except HttpError as e:
        print(f"Error adding YouTube video for Spotify track ID {track_id}: {e}")
        continue

print("All tracks added to YouTube Music playlist successfully!")
