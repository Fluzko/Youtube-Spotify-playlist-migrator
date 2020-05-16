import secrets
import requests
import json


class Spotify:
    def __init__(self, auth):
        self.user_id = auth["client_id"]
        self.user_secret = auth["token"]
        self.base_endpoint = "https://api.spotify.com/v1"
        self.headers = {
            "Authorization": "Bearer {}".format(self.user_secret),
            "Content-Type": "application/json",
        }

    # Given a user id, returns the playlists
    def playlists(self):
        endpoint = self.__endpoint__("/me/playlists?limit=50")
        try:
            r = requests.get(endpoint, headers=self.headers)
            r.raise_for_status()

            playlists_dict = []
            for playlist in r.json().get("items"):
                playlist_info = {
                    "name": playlist.get("name"),
                    "id": playlist.get("id")
                 }
                playlists_dict.append(playlist_info)

            return playlists_dict

        except requests.exceptions.HTTPError:
            print("\nError buscando playlists")
            # TODO raise?

    # Given a name and a description, creates a Spotify playlist and returns its ID
    def create_playlist(self, playlist_name, playlist_description):
        body = {"name": playlist_name,
                "public": True,
                "collaborative": False,
                "description": playlist_description
                }

        endpoint = self.__endpoint__("/users/{}/playlists".format(self.user_id))
        try:
            r = requests.post(endpoint, headers=self.headers, data=json.dumps(body))

            r.raise_for_status()

            r_json = r.json()
            return r_json["id"]

        except requests.exceptions.HTTPError:
            print("\nno se pudo crear la playlist")
#           TODO raise?

    # given a dictionary {song:"", artist:""} & Spotify playlist ID, adds the songs to the palylist.
    def add_songs_to_playlist(self, songs, playlist_id):
        uris = [self.__get_song_uri__(song["artist"], song["song_name"]) for song in songs]

        query_uris = ",".join(filter(None, uris))

        endpoint = self.__endpoint__("/playlists/{}/tracks?uris={}".format(playlist_id, query_uris))

        try:
            r = requests.post(endpoint, headers=self.headers)
            print(r.json())
            r.raise_for_status()

            return r.json()

        except requests.exceptions.HTTPError:
            print("\nNo se pudo agregar las canciones a la playlist")

    # given author & song name, returns back the spotify internal URI for that song.
    def __get_song_uri__(self, artist, song_name):
        endpoint = self.__endpoint__("/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=1".format(
            song_name,
            artist)).replace(" ", "%20")

        try:
            r = requests.get(endpoint, headers=self.headers)
            r.raise_for_status()

            r_json = r.json()
            songs = r_json.get("tracks").get("items")
            # get only the first song
            uri = songs[0].get("uri")

            return uri

        except requests.exceptions.HTTPError:
            print("no se encontro la uri de {}".format(song_name))
#           TODO raise? o mejor return None y print consola. linea 37
        except IndexError:
            print("no se encontro la uri de {}".format(song_name))

    # builds the final endpoint
    def __endpoint__(self, url):
        return "{}{}".format(self.base_endpoint, url)
