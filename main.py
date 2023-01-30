import requests
from bs4 import BeautifulSoup
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/"
SPOTIPY_CLIENT_ID = "YOUR SPOTIFY ID HERE"
SPOTIFY_KEY = "YOUR SPOTIFY KEY HERE"

date = input("what year you would like to travel to in YYY-MM-DD format: ")
# date = "2022-11-26"
response = requests.get(f"{URL}/{date}/")
soup = BeautifulSoup(response.text, 'html.parser')

songs = soup.select("h3#title-of-a-story.c-title.a-no-trucate")
songs = [song.getText().replace("\n", "").replace("\t", "") for song in songs]

authors = soup.select("span.c-label.a-no-trucate")
authors = [author.getText().replace("\n", "").replace("\t", "") for author in authors]

# pprint(songs)
# pprint(authors)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIFY_KEY,
        redirect_uri="http://example.com",
        scope="playlist-modify-private"))

user_data = sp.me()
user_id = user_data["id"]
# print(songs[0])
# print(authors[0])
songs_uri = []

for song in songs:
    song_result = spotipy.Spotify.search(self=sp, q=f"track:{song} year:{date.split('-')[0]}", type="track")
    # pprint(song_result)
    try:
        song_uri = song_result["tracks"]["items"][0]["uri"]
        songs_uri.append(song_uri)
    except IndexError:
        print("There is no such song in the spotify, song skipped.")
# pprint(songs_uri)

playlist_dict = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False,
                                        description=f"the 100 most popular song at date: {date}")
print(playlist_dict)
sp.playlist_add_items(playlist_id=playlist_dict["id"], items=songs_uri)

# sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_dict["id"], tracks=songs_uri)
