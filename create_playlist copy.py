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

# Get the track lists for the playlists to combine
playlist_ids = [
    "1JImXt0g0hJ3G0yvybq5z7",
    "3gzbBkya5JNhTAGlVVLjfu",
    "22OADYRXrL7dCvaMkcaNaC",
    "3Bp1geLqOhoin3JF2hJ64V",
    "60J9PzImS49dH53t30Ims8",
    "12FK3XEGCjrjlMbjCflMoX",
    "4vHkEa8ephYlz1aD4pYZBS",
    "0Cy5HsV6mzpupJxUa7uIeX",
    "3iZIe4kFYYFOWvfqrCBTxT",
    "0hbIUT0Z6No3GTtn68gmTX",
    "3ZSn3dFWZCcSLEfCskAicz",
    "4aJwfcWD8n3P95r8urTI0Y",
    "6g1oOfwJkDX1dJrHk5NVxw",
    "1ZYNE0t05VIJxe0tefxa14",
    "7eCRFhabEBRwntSj76xqPK",
    "4Ev52zZNxOAPHM2EJCNSIe",
    "5d0ojZ2SV83ul1zj4whNi0",
    "169ivcGKn9np7UOCx59Fp1",
    "0gQlzxtS5tQKB4lNenNa2X",
    "2esoB0vZ3PYIJY6FLEhd4d",
    "3cJHbnUCZfHsJRGkuKLCrj",
    "531zfbrCuxn0R8VT1vnbp0",
    "0CheXSHkJqYs4hDZ1k8sf6",
    "3ulvO93lvSoLxtswlIoY7C",
    "2gMws6dCWRibxcNbO5clJM",
    "4OdrjOHV0bqCGG0kNWm71Z",
    "1S3LQ63eH6VT2Mthd69l5g",
    "7ymNNvG25VWT1ThIQ0MOj3",
]
tracks = []
for playlist_id in playlist_ids:
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    playlist_response = requests.get(playlist_url, headers=headers)
    playlist_data = playlist_response.json()
    tracks.extend([track["track"]["id"] for track in playlist_data["items"]])

# Create a new playlist and add the tracks
user_id = "1264913076"
playlist_name = "combined_playlist"
playlist_desc = "This is a playlist combining multiple playlists"
create_playlist_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
create_playlist_response = requests.post(
    create_playlist_url,
    headers=headers,
    json={"name": playlist_name, "description": playlist_desc, "public": False},
)
print(create_playlist_response.json())
playlist_id = create_playlist_response.json()["id"]
add_tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
add_tracks_response = requests.post(
    add_tracks_url,
    headers=headers,
    json={"uris": [f"spotify:track:{track}" for track in tracks]},
)
