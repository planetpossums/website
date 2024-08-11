import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

with open('config.json', 'r') as config_file:
    config = json.load(config_file)


spotify_credentials = config.get("spotify", {})

cid = spotify_credentials.get("client_id")
secret = spotify_credentials.get("client_secret")

os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

username = ""
client_credentials_manager = SpotifyClientCredentials(client_id = cid, client_secret = secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
scope = 'user-top-read'
token = util.prompt_for_user_token(username, scope, client_secret = secret, client_id = cid, show_dialog = True)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)

if token:
    print("Fetching top 50 data...")
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_top_tracks(limit = 50, offset = 0, time_range = 'medium_term')
    for song in range(50):
        results_list = []
        results_list.append(results)
        with open('top50_data.json', 'w', encoding = 'utf-8') as f:
            json.dump(results_list, f, ensure_ascii = False, indent = 4)


else:
    print("Can't get token for", username)

