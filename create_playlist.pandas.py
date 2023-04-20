import json
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri="https://coreyfoster.dev",
        scope="user-library-read playlist-modify-private",
    )
)

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

target_playlist_id = "0s0vBSB1C4QvKcqiUVxbmk"

added = []

# Use append() to add all the tracks from all the playlists to the added list
for playlist_id in playlist_ids:
    playlist_items = sp.playlist_items(playlist_id)
    track_ids = [
        item["track"]["id"] for item in playlist_items["items"] if item["track"]["id"]
    ]
    added += track_ids

# Convert the added list to a pandas DataFrame to remove duplicates while maintaining order
added_df = pd.DataFrame({"track_id": added})
added_df.drop_duplicates(inplace=True)

# Convert the tracks in the target playlist to a pandas DataFrame
target_items = sp.playlist_items(target_playlist_id, fields="items(track.id)")["items"]
target_df = pd.DataFrame({"track_id": [item["track"]["id"] for item in target_items]})

# Use pandas' merge() method to find the tracks that are not already in the target playlist
tracks_to_add_df = added_df.merge(target_df, how="left", indicator=True)
tracks_to_add = tracks_to_add_df.loc[
    tracks_to_add_df["_merge"] == "left_only", "track_id"
].tolist()

# Use sp.current_user() to get the user ID
user_id = sp.current_user()["id"]

# Use a batched approach to add tracks to the target playlist
while tracks_to_add:
    sp.playlist_add_items(target_playlist_id, tracks_to_add[:100])
    tracks_to_add = tracks_to_add[100:]
