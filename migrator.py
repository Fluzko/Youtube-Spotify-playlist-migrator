from youtubeAdapter import YoutubeAdapter
from spotifyAdapter import SpotifyAdapter
from services.videoInfoExtractor import VideoInfoExtractor
from exceptions import youtube_exceptions, spotify_exceptions
import config
import sys
import requests.exceptions as exceptions


class Migrator:
    def __init__(self):
        self.yt = YoutubeAdapter(config.youtube_api_key)
        self.spt = SpotifyAdapter(config.spotify_client_ID, config.spotify_client_secret)
        self.xtrc = VideoInfoExtractor()
        self.user_spotify_playlists = []

    def migrate(self):
        try:
            self.user_spotify_playlists = self.spt.playlists()
        except spotify_exceptions.SearchPlaylistsError:
            print("No se pudo traer las playlists del usuario, abortando...")
            sys.exit()

        for playlist in config.playlists:
            try:
                videos = self.get_videos_from_playlist(playlist)
                songs = self.extract_song_and_author(videos)
                playlist_id = self.create_spotify_playlist(playlist)
                self.add_songs_to_playlist(songs, playlist_id)

            except youtube_exceptions.EmptyPlaylist:
                print("La playlist esta vacia")
            except spotify_exceptions.CreatePlaylistError:
                print("No se pudo crear la playlist")
            except spotify_exceptions.AddSongsToPlaylistError:
                print("No se pudo agregar las canciones a la playlist")

            print('\n\n')

    def get_videos_from_playlist(self, playlist):
        print("------------- Youtube API -------------")
        print("Tomando videos de la playlist...")
        try:
            return self.yt.get_videos_from_playlist(playlist.get("id"))
        except youtube_exceptions.YoutubeError:
            print("Ocurrio un error con la API de youtube")
            sys.exit()
        except youtube_exceptions.EmptyPlaylist:
            raise

    def extract_song_and_author(self, videos):
        print("------------- Youtube DL -------------")
        print("Extrayendo autor y cancion de los videos...")
        return self.xtrc.get_songs_name_author(videos)

    def create_spotify_playlist(self, playlist):
        print("------------- Spotify API -------------")
        print("Creando playlist...")
        try:
            return self.__playlist_id__(playlist)
        except spotify_exceptions.CreatePlaylistError:
            raise

    def add_songs_to_playlist(self, songs, playlist_id):
        try:
            print("Agregando canciones a la playlist...")
            playlist_songs_uris = self.spt.playlist_songs_uri(playlist_id)
            songs_uris = self.spt.get_songs_uris(songs)
            uris_to_add = [uri for uri in songs_uris if uri not in playlist_songs_uris]
            if len(uris_to_add) and uris_to_add is not [None]:
                self.spt.add_uris_to_playlist(uris_to_add, playlist_id)
        except spotify_exceptions.RetrieveSongsFromPlaylist:
            print("Spotify error, aborting...")
            sys.exit()
        except exceptions.HTTPError:
            print("Spotify error, aborting...")
            sys.exit()
        except IndexError:
            print("Spotify error, aborting...")
            sys.exit()
        except spotify_exceptions.AddSongsToPlaylistError:
            raise

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
            try:
                playlist_id = self.spt.create_playlist(
                    playlist_info.get("name"),
                    "playlist de {} migrada de yt".format(playlist_info.get("name"))
                )
                print("La playlist no existe, creando una nueva...")
            except spotify_exceptions.CreatePlaylistError:
                raise

        return playlist_id


# TODO
#  handle temas repetidos en playlist ya creada
#  handle temas repetidos en yt
#  inyeccion de dependencias migrator
# Pythonic list comprhension, inyeccion de dependencias, patron adapter,propagar exceptions, exceptions custom
