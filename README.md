# spotify-favorites-playlist
Python scripts that create/update a few Spotify playlists automatically (personal project)

## Actions:

## Scripts currently in repo:
- `create_100inmonth.py` - Create (or modify if exists) a playlist called "Most listened to" with your 50 most listened to songs in the last 30 days
- `create_200liked.py` - Create a playlist called "Current favorites" with your 200 latest in your Liked songs

## Usage

1. Clone the repository
2. Create an app at https://developers.spotify.com and note the client ID and secret
3. Create a GitHub token that can read and write the cloned repository's secrets
4. Set the following environment variables:
    - SPOTIPY_CLIENT_ID: Spotify client ID that you copied in step 2
    - SPOTIPY_CLIENT_SECRET: Spotify client secret that you copied in step 2
    - GH_TOKEN: GitHub token that you copied in step 3
5. Clone the repo and run one of the scripts (create_100inmonth.py or create_200liked.py) to authenticate and create a .spotifycache file
6. Run the updatesecrets.py file to set the GH_TOKEN secret

### Planned features:
- have a GUI app that
  - authenticates you to GitHub and makes it easy to setup the app
  - authenticates you to Spotify for the first time instead of needing to manually clone the repo / run scripts
  - makes you able to choose when you want to run the script (modifies the workflow)
  - makes you able to choose which scripts you want / don't want to run (separate workflows)
- more scripts (for example daily stats via Telegram or backups of playlists / songs)
