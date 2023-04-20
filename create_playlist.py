import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id="",
        client_secret="",
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

# Old code is below; working but could be better
added = []

for playlist_id in playlist_ids:
    playlist_items = sp.playlist_items(playlist_id)
    # print(json.dumps(playlist_items["items"], indent=4))
    for item in playlist_items["items"]:
        # print(json.dumps(item["track"]["id"], indent=4))
        if item["track"]["id"] and item["track"]["id"] not in added:
            added.append(item["track"]["id"])
            sp.user_playlist_add_tracks(
                sp.me()["id"], target_playlist_id, [item["track"]["id"]]
            )

####

# Below is "optimized code" from ChatGPT; Much quicker but tracks are in randomized order
# Use a set to store the added tracks
# added = set()

# # Use set.update() to add all the tracks from all the playlists to the added set
# for playlist_id in playlist_ids:
#     playlist_items = sp.playlist_items(playlist_id)
#     track_ids = [
#         item["track"]["id"] for item in playlist_items["items"] if item["track"]["id"]
#     ]
#     added.update(track_ids)

# # Use set.difference() to find the tracks that are not already in the target playlist
# tracks_to_add = list(
#     added.difference(
#         set(sp.playlist_items(target_playlist_id, fields="items(track.id)")["items"])
#     )
# )

# # Use sp.current_user() to get the user ID
# user_id = sp.current_user()["id"]

# # Use a batched approach to add tracks to the target playlist
# while tracks_to_add:
#     sp.playlist_add_items(target_playlist_id, tracks_to_add[:100])
#     tracks_to_add = tracks_to_add[100:]
