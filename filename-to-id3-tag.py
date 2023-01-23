#!/usr/bin/env python3
import os
import argparse
from pprint import pprint

import mutagen.id3

from FileTools import AudioFile
from FileTools import Crawler



# Tags are labeled differently depending on if the file is MP3 or AIFF
# We use this mapping when setting these values on an MP3/AIFF file below
MP3_TAGS = {
    "artist": "artist",
    "title": "title",
    "bpm": "bpm",
    "key": "key",
    "genre": "genre",
}

AIFF_TAGS ={
    "artist": "TPE1",
    "title": "TIT2",
    "bpm": "TBPM",
    "key": "",
    "genre": "TCON",
}


def parse_args():
    ap = argparse.ArgumentParser(
        description=(
            "Set ID3 tags on an MP3 or AIFF file via the common naming scheme. "
            "<KEY> - <BPM> - <ARTIST> - <TRACK_NAME> (<MIX_NAME>).<FILE_EXTENSION> "
            "I.E 9A - 117.00 - Polo (AR) - Through Concrete (Original Mix).aiff"
        )
    )

    ap.add_argument(
        "-c",
        "--config",
        dest="config",
        metavar="config",
        help="ini configuration file.")

    ap.add_argument(
        "-s",
        "--source-path",
        dest="source_path",
        metavar="source_path",
        required=True,
        help="Path to crawl for audio files.")

    return ap.parse_args()


def get_id3_from_name(audio_file: AudioFile.AudioFile) -> dict:
    # See https://github.com/quodlibet/mutagen/blob/master/mutagen/easyid3.py#L470
    file_name = os.path.basename(audio_file.path)
    split_name = file_name.split(" - ")
    return {
        "key": split_name[0],
        "bpm": split_name[1],
        "artist": split_name[2],
        "title": split_name[3].split('.')[0],
        "description": f"{split_name[0]} - {split_name[1]}"
    }

def set_id3_tags(audio_file: AudioFile.AudioFile, track_info: dict) -> bool:
    print(f"Missing artist: {audio_file.path}")
    print(f"Audio Info: ", end="")
    pprint(track_info)
    return True



def main(args):
    
    # Crawl the source path and build AudioFile objects
    file_paths = Crawler.Crawler(args.source_path).paths
    for path in file_paths:
        audio_file = AudioFile.AudioFile(path)

        # Skip files that are not MP3 or AIFF
        if not audio_file.file_type:
            continue

        # MP3 Files
        elif (audio_file.file_type == AudioFile.TYPE_MP3):
            continue
            pprint(audio_file.tags.keys())
            track_info = get_id3_from_name(audio_file)
            set_id3_tags(audio_file, track_info)

        # AIFF Files
        elif audio_file.file_type == AudioFile.TYPE_AIFF:
            tagData = audio_file.mutagen_file.get('GEOB:Key')
            mutagen.id3.GEOB
            pprint(tagData)

            #for k in audio_file.tags.keys():
            #    print(f"{k}: {audio_file.tags[k]}")
            exit(0)

    return True


if __name__ == "__main__":
    exit(main(parse_args()))


""" AIFF NOTES:
COMM::eng: 5A - 125.00
GEOB:Key: GEOB(encoding=<Encoding.LATIN1: 0>, mime='application/json', filename='', desc='Key', data=b'eyJhbGdvcml0aG0iOjk0LCJrZXkiOiI1QSIsInNvdXJjZSI6Im1peGVkaW5rZXkifQ==\n')

Data is a base
"""


"""

        if not audio_file.genre or not audio_file.file_type:
            id3_info = get_id3_from_name(audio_file)

            #pprint(id3_info)

            print(f"Missing ID3: {audio_file.path}")

        pprint(audio_file.tags)
"""