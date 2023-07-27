import os

import pandas as pd
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from tabulate import tabulate

load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri="https://coreyfoster.dev",
    )
)

target_playlist_id = "5M3NezYCxblkic3gdkUXRy"


def get_playlist_tracks(playlist_id, fields):
    results = sp.playlist_items(playlist_id, fields)
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    return tracks


def get_track_by_id(track_list, track_id):
    for item in track_list:
        if item["track"]["id"] == track_id:
            return item["track"]
    return None


tracks = get_playlist_tracks(
    target_playlist_id,
    fields="items(track.id, track.name, track.artists), next",
)
del tracks[0]

track_ids = [item["track"]["id"] for item in tracks]

features = sp.audio_features(track_ids)

table_data = []
table_data.append(["Walls", 128, 64])

for track, feature in zip(tracks, features):
    tempo = feature["tempo"] if feature["tempo"] < 130 else 0
    half_tempo = feature["tempo"] / 2 if feature["tempo"] / 2 > 46 else 0
    table_data.append([track["track"]["name"], round(tempo), round(half_tempo)])

df = pd.DataFrame(table_data, columns=["name", "tempo", "half_tempo"])

print(
    tabulate(
        df.replace(0, ""),
        headers="keys",
        showindex=False,
    )
)
