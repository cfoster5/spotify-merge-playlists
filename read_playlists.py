import requests
import json

# Set up authentication and get access token
client_id = ""
client_secret = ""
auth_url = "https://accounts.spotify.com/api/token"
auth_response = requests.post(
    auth_url,
    {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    },
)
access_token = auth_response.json()["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}

# Get a list of playlists associated with your account
playlist_url = "https://api.spotify.com/v1/me/playlists"
playlist_response = requests.get(playlist_url, headers=headers)
playlist_data = playlist_response.json()

# Print the IDs of each playlist
for playlist in playlist_data["items"]:
    print(playlist["id"])
