import requests
import json
import sys
from exceptions import spotify_exceptions


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
        params = {
            "limit": 50
        }
        endpoint = self.__endpoint__("/me/playlists")
        try:
            r = requests.get(endpoint, headers=self.headers, params=params)
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
            raise spotify_exceptions.SearchPlaylistsError

    # Given a name and a description, creates a Spotify playlist and returns its ID
    def create_playlist(self, playlist_name, playlist_description):
        body = {
            "name": playlist_name,
            "public": True,
            "collaborative": False,
            "description": playlist_description
        }

        endpoint = self.__endpoint__("/users/{}/playlists".format(self.user_id))
        try:
            r = requests.post(endpoint, headers=self.headers, data=json.dumps(body))
            r.raise_for_status()
            return r.json()["id"]
        except requests.exceptions.HTTPError:
            raise spotify_exceptions.CreatePlaylistError

    def add_uris_to_playlist(self, uris, playlist_id):
        query_uris = ",".join(filter(None, uris))

        params = {
            "uris": query_uris
        }
        endpoint = self.__endpoint__("/playlists/{}/tracks".format(playlist_id))

        try:
            r = requests.post(endpoint, headers=self.headers, params=params)
            r.raise_for_status()

            return r.json()

        except requests.exceptions.HTTPError:
            raise spotify_exceptions.AddSongsToPlaylistError

    # given a dictionary {song:"", artist:""} & Spotify playlist ID, adds the songs to the palylist.
    def add_songs_to_playlist(self, songs, playlist_id):
        try:
            uris = self.get_songs_uri(songs)
            self.add_uris_to_playlist(uris, playlist_id)
        except requests.exceptions.HTTPError:
            raise
        except IndexError:
            raise

    def get_songs_uri(self, songs):
        try:
            return [self.get_song_uri(song["artist"], song["song_name"]) for song in songs]
        except requests.exceptions.HTTPError:
            raise
        except IndexError:
            raise

    # given author & song name, returns back the spotify internal URI for that song.
    def get_song_uri(self, artist, song_name):
        endpoint = self.__endpoint__("/search?"
                                     "query=track%3A{}+artist%3A{}&"
                                     "type=track&"
                                     "offset=0&"
                                     "limit=1".format(song_name, artist).replace(" ", "%20"))
        try:
            r = requests.get(endpoint, headers=self.headers)
            r.raise_for_status()

            r_json = r.json()
            songs = r_json.get("tracks").get("items")
            # get only the first song
            uri = songs[0].get("uri")

            return uri

        except requests.exceptions.HTTPError as e:
            print("no se encontro la uri de {}".format(song_name))

        except IndexError as e:
            print("no se encontro la uri de {}".format(song_name))

    # Given a palylist, resturns a list of all the uris of its songs, if no song, empty list is returned
    def playlist_songs_uri(self, playlist):
        endpoint = self.__endpoint__('/playlists/{}/tracks'.format(playlist))
        params = {
            "market": "AR",
            "fields": "items(track(uri))",
        }
        try:
            r = requests.get(endpoint, headers=self.headers, params=params)
            r.raise_for_status()

            # No songs at the playlist
            if not len(r.json().get("items")):
                return []

            return [song["track"]["uri"] for song in r.json()["items"]]

        except requests.exceptions.HTTPError:
            raise spotify_exceptions.RetrieveSongsFromPlaylist

    # builds the final endpoint
    def __endpoint__(self, url):
        return "{}{}".format(self.base_endpoint, url)
