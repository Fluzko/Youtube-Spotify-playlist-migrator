import youtube_dl
import re
from exceptions import extractor_exceptions


class VideoInfoExtractor:
    def __init__(self, spotify):
        self.extractor = youtube_dl.YoutubeDL({"verbose": False, "quiet": True}).extract_info
        self.spt = spotify

    def get_songs_name_author(self, videos):
        songs_info = []

        for video in videos:
            extracted_video = self.extractor(video.get("youtube_url"), download=False)
            song_name = extracted_video.get("track")
            artist = extracted_video.get("artist")

            # If YoutubeDL extraction does not fails, then add the song to playlist
            if artist is not None and song_name is not None:
                songs_info.append({"artist": artist, "song_name": song_name})
            # Try own extraction
            else:
                try:
                    songs_info.append(self.__video_title_extractor__(video.get("video_title")))
                except extractor_exceptions.FailedExtraction:
                    print("{} No se pudo encontrar el autor | cancion".format(video.get("video_title")))

        return self.__beutify_parsed_songs__(songs_info)

    # Tries to extract song & artist name by the video title itself
    def __video_title_extractor__(self, video_title):
        video_title = self.__beutify__(video_title)
        for separator in ['-', '|']:
            try:
                return self.__extract_by_separator__(separator, video_title)
            except extractor_exceptions.FailedExtraction:
                pass

        raise extractor_exceptions.FailedExtraction

    # Por lo general viene "artista separador nombre cancion", entonces probas ir contra spotify a ver si lo encuentra
    def __extract_by_separator__(self, separator, video_title):
        splited_title = video_title.split(separator)
        if not len(splited_title):
            raise extractor_exceptions.FailedExtraction
        try:
            self.spt.get_song_uri(splited_title[0], splited_title[1])
            return {"artist": splited_title[0], "song_name": splited_title[1]}
        except:
            pass
        try:
            self.spt.get_song_uri(splited_title[1], splited_title[0])
            return {"artist": splited_title[1], "song_name": splited_title[0]}
        except:
            raise extractor_exceptions.FailedExtraction

    def __beutify__(self, text):
        # Removes text within () & []
        text = self.__delete_regex__("[\(\[].*?[\)\]]", text)
        # Removes "- Radio edit"
        text = self.__delete_phrase__("- Radio Edit", text)
        # Removes "Videoclip"
        text = self.__delete_phrase__("Videoclip", text)
        text = self.__delete_phrase__("videoclip", text)
        text = self.__delete_phrase__("VIDEOCLIP", text)

        return text

    # Given song dict {artist, song_name} parses eliminates unnecessary info (text)
    def __beutify_parsed_songs__(self, songs_info):
        for song_info in songs_info:
            song_info["artist"] = self.__beutify__(song_info["artist"])
            song_info["song_name"] = self.__beutify__(song_info["song_name"])

        return songs_info

    @staticmethod
    def __delete_regex__(regex, text):
        return re.sub(regex, "", text)

    @staticmethod
    def __delete_phrase__(phrase, text):
        return text.replace(phrase, "")
