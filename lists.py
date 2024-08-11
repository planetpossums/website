import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

with open('config.json', 'r') as config_file:
    config = json.load(config_file)


spotify_credentials = config.get("spotify", {})

cid = spotify_credentials.get("client_id")
secret = spotify_credentials.get("client_secret")

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

with open('top50_data.json', encoding="utf8") as f:
    data = json.load(f)



list_of_results = data[0]["items"]
list_of_artist_names = []
list_of_artist_uri = []
list_of_song_names = []
list_of_song_uri = []
list_of_popularity = []
list_of_albums = []

for result in list_of_results:
    result["album"]
    this_artists_name = result["artists"][0]["name"]
    list_of_artist_names.append(this_artists_name)
    this_artists_uri = result["artists"][0]["uri"]
    list_of_artist_uri.append(this_artists_uri)
    list_of_songs = result["name"]
    list_of_song_names.append(list_of_songs)
    song_uri = result["uri"]
    list_of_song_uri.append(song_uri)
    song_popularity = result["popularity"]
    list_of_popularity.append(song_popularity)
    this_album = result["album"]["name"]
    list_of_albums.append(this_album)

all_songs = pd.DataFrame(
    {'artist': list_of_artist_names,
     'artist_uri': list_of_artist_uri,
     'song': list_of_song_names,
     'song_uri': list_of_song_uri,
     'popularity': list_of_popularity,
     'album': list_of_albums
     })

all_songs_saved = all_songs.to_csv('top50_songs_typ.csv')

col_list = all_songs.song_uri.values.tolist()

def getTrackFeatures(id):
    features = sp.audio_features(id)
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']
    valence = features[0]['valence']
    mode = features[0]['mode']

    track = [acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature, valence, mode]
    return track

tracks = []
for i in range(len(col_list)):
    track = getTrackFeatures(col_list[i])
    tracks.append(track)

analysis_df = pd.DataFrame(tracks, columns=['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness','speechiness', 'tempo', 'time_signature', 'valence', 'mode'])
track_analysis = analysis_df.to_csv('track_analysis_typ.csv')

complete_table = pd.concat([all_songs, analysis_df], axis=1)

print(complete_table)