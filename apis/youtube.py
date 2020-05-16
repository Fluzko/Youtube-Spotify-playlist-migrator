import google_auth_oauthlib.flow
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import os
import requests


class Youtube:
    def __init__(self, auth):
        self.api_key = auth["api_key"]
        # self.client = self.__youtube_client__()

    def __youtube_client__(self):
        pass
        # """ Log Into Youtube, Copied from Youtube Data API """
        # # Disable OAuthlib's HTTPS verification when running locally.
        # # *DO NOT* leave this option enabled in production.
        # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        #
        # api_service_name = "youtube"
        # api_version = "v3"
        # client_secrets_file = "client_secret.json"
        #
        # # Get credentials and create an API client
        # scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        #     client_secrets_file, scopes)
        # credentials = flow.run_console()
        #
        # # from the Youtube DATA API
        # youtube_client = googleapiclient.discovery.build(
        #     api_service_name, api_version, credentials=credentials)
        #
        # return youtube_client

    def get_videos_from_playlist(self, auth,playlist):
        # r = self.client.playlistItems().list(
        #     playlistId=playlist,
        #     part="snippet,contentDetails,statistics",
        #     maxResults=50,
        # ).execute()

        r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?"
                         "playlistId={}&"
                         "part=snippet&"
                         "maxResults=50&"
                         "alt=json&"
                         "key={}".format(playlist, self.api_key)).json()

        if r.get("error"):
            print(r["error"])
            # r["error"]["code"]
            # r["error"]["message"]

        videos = []
        for item in r["items"]:
            video_title = item["snippet"]["title"]
            yt_url = "https://www.youtube.com/watch?v={}".format(item["snippet"]["resourceId"]["videoId"])
            videos.append({"video_title": video_title, "youtube_url": yt_url})

        return videos

    def get_playlist_name(self, playlist):
        # r = self.client()
        pass
