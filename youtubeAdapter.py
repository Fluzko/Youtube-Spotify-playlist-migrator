from apis.youtube import Youtube


class YoutubeAdapter:
    def __init__(self, api_key):
        auth = {
            "api_key": api_key
        }
        self.api = Youtube(auth)

    def get_videos_from_playlist(self, playlist):
        return self.api.get_videos_from_playlist(playlist)
