import os
import base64
import requests

# Get the contents of the .spotifycache file and encode it in base64
with open('.spotifycache', 'rb') as f:
    spotify_cache_bytes = f.read()
    spotify_cache_base64 = base64.b64encode(
        spotify_cache_bytes).decode('utf-8')

# Update the SPOTIPY_CACHE secret using the GitHub API
headers = {
    'Authorization': f'token {os.environ["GH_TOKEN"]}',
    'Accept': 'application/vnd.github.v3+json'
}
data = {
    'encrypted_value': spotify_cache_base64,
    'key_id': None
}
url = f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/actions/secrets/SPOTIFY_CACHE'
response = requests.patch(url, headers=headers, json=data)

if response.status_code == 204:
    print('Secret updated successfully!')
else:
    print(f'Error updating secret: {response.status_code} - {response.text}')
