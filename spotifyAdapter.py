from apis.spotify import Spotify
from exceptions import spotify_exceptions
import requests


class SpotifyAdapter:
    def __init__(self, client_id, api_token):
        self.auth = {
            "client_id": client_id,
            "token": api_token
        }
        self.api = Spotify(self.auth)

    # Given a name and a description, creates a Spotify playlist and returns its ID
    def create_playlist(self, playlist_name, playlist_description):
        try:
            return self.api.create_playlist(playlist_name, playlist_description)
        except spotify_exceptions.CreatePlaylistError:
            raise

    # given a dictionary {song:"", artist:""} & Spotify playlist ID, adds the songs to the palylist.
    def add_songs_to_playlist(self, songs, playlist_id):
        try:
            return self.api.add_songs_to_playlist(songs, playlist_id)
        except spotify_exceptions.AddSongsToPlaylistError:
            raise

    def add_uris_to_playlist(self, uris, playlist_id):
        try:
            self.api.add_uris_to_playlist(uris, playlist_id)
        except requests.exceptions.HTTPError:
            raise

    def playlists(self):
        try:
            return self.api.playlists()
        except spotify_exceptions.SearchPlaylistsError:
            raise

    def playlist_songs_uri(self, playlist):
        try:
            return self.api.playlist_songs_uri(playlist)
        except spotify_exceptions.RetrieveSongsFromPlaylist:
            raise

    def get_songs_uris(self, songs):
        try:
            return self.api.get_songs_uri(songs)
        except requests.exceptions.HTTPError:
            raise
        except IndexError:
            raise
