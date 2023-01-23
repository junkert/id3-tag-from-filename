import json
import os
import encodings
import codecs
from base64 import b64decode, b64encode

import mutagen.aiff
from mutagen.id3 import GEOB
from mutagen.id3 import ID3
from mutagen.id3 import Encoding
from mutagen.easyid3 import EasyID3
from mutagen.aiff import AIFF



TYPE_NONE = None
TYPE_AIFF = "aiff"
TYPE_MP3 = "mp3"


class AudioFile(object):
    def __init__(self, path):
        self.path = path
        self.file_type = self.set_file_type(self.path)
        self.mutagen_file = self.load_mutagen_file(self.path, self.file_type)
        self.tags = self.get_tags(self.path, self.file_type, self.mutagen_file)
        self.genre = self.get_genre(self.tags, self.file_type)
        self.key = None

    @staticmethod
    def set_file_type(path):
        file_type = None
        if ".aif" in os.path.basename(path) or ".mp3" in os.path.basename(path):
            if ".aif" in os.path.basename(path):
                file_type = TYPE_AIFF
            else:
                file_type = TYPE_MP3
        return file_type

    @staticmethod
    def get_genre(tags, file_type: str):
        genre = None
        try:
            if file_type == TYPE_AIFF:
                genre = tags["TCON"].text[0]
            elif file_type == TYPE_MP3:
                genre = str(tags["genre"][0])
        except (TypeError, KeyError):
            pass
        return genre

    @staticmethod
    def load_mutagen_file(path: str, file_type: str):
        if file_type == TYPE_AIFF:
            return AIFF(path)
        return None

    @staticmethod
    def get_tags(path: str, file_type: str, mutagen_file: mutagen.aiff):
        tags = None
        try:
            if file_type == TYPE_AIFF:
                tags = mutagen_file.tags
            elif ".mp3" in os.path.basename(path):
                tags = EasyID3(path)

        except Exception as e:
            print(e.__str__())
        return tags

    def set_music_key(self, key: str):
        if self.file_type == TYPE_AIFF:
            """
            Keys are more complex with AIFF files. We must first build the GLOB and then set it.
            
            Taken from a file ran through Mixed in Key:
            
            TAG["GEOB:Key"] = GEOB(
                    encoding=<Encoding.LATIN1: 0>,
                    mime="application/json",
                    filename="",
                    desc="Key", 
                    data=b"eyJhbGdvcml0aG0iOjk0LCJrZXkiOiI1QSIsInNvdXJjZSI6Im1peGVkaW5rZXkifQ==\n"
                )
                
            Note that "data" above is base64. Decoded it looks like:
            
            {"algorithm":94,"key":"5A","source":"mixedinkey"}% 
            
            For Encoding see: https://mutagen.readthedocs.io/en/latest/user/id3.html
            """
            decoded_key = {
                "algorithm": 94,
                "key": key,
                "source": "levis-dj-tools",
            }
            json_key = json.dumps(decoded_key, indent = 4)
            b64_encoded_key = b64encode(json_key)
            self.key = mutagen.id3.GEOB(
               encoding=Encoding("LATIN1"),
               mime=u"application/json",
               filename=u"",
               desc=u"Key",
               data=b64_encoded_key
            )

            audio = ID3(self.path)
            for key, value in self.tags:
                audio.setall(key, value)
            audio.setall("", self.key)

            audio.save

        elif self.file_type == TYPE_MP3:
            pass

