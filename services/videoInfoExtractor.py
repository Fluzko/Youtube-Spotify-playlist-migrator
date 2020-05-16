import youtube_dl
import re


class VideoInfoExtractor:
    def __init__(self):
        self.extractor = youtube_dl.YoutubeDL({"verbose": False, "quiet": True}).extract_info

    def get_songs_name_author(self, videos):
        songs_info = []

        for video in videos:
            extracted_video = self.extractor(video.get("youtube_url"), download=False)
            song_name = extracted_video.get("track")
            artist = extracted_video.get("artist")

            # If extraction does not fails, then add the song to playlist
            if artist is not None and song_name is not None:
                songs_info.append({"artist": artist, "song_name": song_name})
            else:
                print("{} No se pudo encontrar el autor | cancion".format(video.get("video_title")))

        return self.__beutify__(songs_info)

    # Given song dict {artist, song_name} parses eliminates unnecessary info (text)
    def __beutify__(self, songs_info):
        for song_info in songs_info:
            # Removes text within () & []
            song_info = self.__delete_regex_song_info("[\(\[].*?[\)\]]", song_info)
            # Removes "- Radio edit"
            song_info = self.__delete_phrase__("- Radio Edit", song_info)

        return songs_info

    @staticmethod
    def __delete_regex_song_info(regex, song_info):
        song_info["song_name"] = re.sub(regex, "", song_info["song_name"])
        song_info["artist"] = re.sub(regex, "", song_info["artist"])
        return song_info

    @staticmethod
    def __delete_phrase__(phrase, song_info):
        song_info["song_name"] = song_info["song_name"].replace(phrase, "")
        song_info["artist"] = song_info["artist"].replace(phrase, "")
        return song_info
