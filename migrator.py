from youtubeAdapter import YoutubeAdapter
from spotifyAdapter import SpotifyAdapter
from services.videoInfoExtractor import VideoInfoExtractor
import config


class Migrator:
    def __init__(self):
        self.yt = YoutubeAdapter(config.youtube_api_key)
        self.spt = SpotifyAdapter(config.spotify_client_ID, config.spotify_client_secret)
        self.xtrc = VideoInfoExtractor()
        self.user_spotify_playlists = self.spt.playlists()

    def migrate(self):
        for playlist in config.playlists:
            print("------------- Youtube API -------------")
            print("Tomando videos de la playlist...")
            videos = self.yt.get_videos_from_playlist(playlist.get("id"))
            print("------------- Youtube DL -------------")
            print("Extrayendo autor y cancion de los videos...")
            songs = self.xtrc.get_songs_name_author(videos)
            print("------------- Spotify API -------------")
            print("Creando playlist...")
            playlist_id = self.__playlist_id__(playlist)
            print("Agregando canciones a la playlist...")
            self.spt.add_songs_to_playlist(songs, playlist_id)
            print('\n\n')

    # Given playlist info dict {name,id}, creates it on spotify it does not exists, otherwise returns back its id.
    def __playlist_id__(self, playlist_info):
        user_spotify_playlists_names = [playlist.get("name") for playlist in self.user_spotify_playlists]
        # If playlist exists on spotify
        if playlist_info.get("name") in user_spotify_playlists_names:
            playlist_id = [playlist["id"]
                           for playlist
                           in self.user_spotify_playlists
                           if playlist["name"] is playlist.get("name")][0]
            print("Ya existe una playlist con ese nombre, reutilizandola...")
        # If playlist doesn't exist
        else:
            playlist_id = self.spt.create_playlist(
                playlist_info.get("name"),
                "playlist de {} migrada de yt".format(playlist_info.get("name"))
            )
            print("La playlist no existe, creando una nueva...")

        return playlist_id


# TODO
#  mejorar responsabilidades
#  handle de exceptions,
#  handle yt playlist viene vacia
#  handle temas repetidos en playlist ya creada
#  handle temas repetidos en yt