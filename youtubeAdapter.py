from apis.youtube import Youtube
from exceptions import youtube_exceptions


class YoutubeAdapter:
    def __init__(self, api_key):
        auth = {
            "api_key": api_key
        }
        self.api = Youtube(auth)

    def get_videos_from_playlist(self, playlist):
        try:
            return self.api.get_videos_from_playlist(playlist)
        except youtube_exceptions.EmptyPlaylist:
            raise
        except youtube_exceptions.YoutubeError:
            raise
