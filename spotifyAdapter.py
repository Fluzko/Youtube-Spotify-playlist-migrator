from apis.spotify import Spotify


class SpotifyAdapter:
    def __init__(self, client_id, api_token):
        self.auth = {
            "client_id": client_id,
            "token": api_token
        }
        self.api = Spotify(self.auth)

    # Given a name and a description, creates a Spotify playlist and returns its ID
    def create_playlist(self, playlist_name, playlist_description):
        return self.api.create_playlist(playlist_name, playlist_description)

    # given a dictionary {song:"", artist:""} & Spotify playlist ID, adds the songs to the palylist.
    def add_songs_to_playlist(self, songs, playlist_id):
        return self.api.add_songs_to_playlist(songs, playlist_id)

    def playlists(self):
        return self.api.playlists()
