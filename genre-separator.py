#!/usr/bin/env python3
import os
import argparse

from shutil import copyfile

from FileTools import AudioFile
from FileTools import Crawler

def parse_args ():
    ap = argparse.ArgumentParser(
        description=("Genera Separator is a tool for seperating a "
                     "collection of music files into folders based on the "
                     "musical ID3 genre tags in MP3 and AIFF files."))
    ap.add_argument("-c",
                             "--config",
                             dest="config",
                             metavar="config",
                             help="ini configuration file.")
    ap.add_argument("-d",
                             "--dest-path",
                             dest="dest_path",
                             metavar="dest_path",
                             required=True,
                             help="Path of root directory to copy files to.")
    ap.add_argument("-s",
                             "--source-path",
                             dest="source_path",
                             metavar="source_path",
                             required=True,
                             help="Path to crawl for audio files.")
    return ap.parse_args()


def main(args):

    # Crawl the source path and build AudioFile objects
    file_paths = Crawler.Crawler(args.source_path).paths
    unknown_path = os.path.join(args.dest_path, "UNKNOWN")
    if not os.path.isdir(os.path.dirname(unknown_path)):
        print(f"Creating directory for unknown ID3 tags: {os.path.dirname}")
        os.mkdir(os.path.dirname(unknown_path))
    for p in file_paths:
        dest_path = None
        audio_file = AudioFile.AudioFile(p)
        try:
            # Needed to keep from creating extra directories if the genre contains '/'
            audio_file.genre = audio_file.genre.replace('/', '&')
            print(f"{audio_file.path}: {audio_file.genre}: {audio_file.tags}")
            if not audio_file.tags:
                dest_path = os.path.join(args.dest_path, "UNKNOWN") +\
                            "/" + os.path.basename(p)
            else:
                dest_path = os.path.join(args.dest_path) + "/" + \
                    audio_file.genre + "/" + os.path.basename(p)
        except Exception as e:
            print(f"EXCEPTION: {e.__str__()}")
            dest_path = os.path.join(args.dest_path, "UNKNOWN") + \
                        "/" + os.path.basename(p)

        print("==========================================")
        print("source: %s" % p)
        print("dest: %s" % dest_path)
        print("genre: %s" % audio_file.genre)# create Genre directory
        if not os.path.isdir(os.path.dirname(dest_path)):
            print("Creating directory: %s" % os.path.dirname(dest_path))
            os.mkdir(os.path.dirname(dest_path))

        # Now copy file
        if os.path.isfile(dest_path):
            print("WARN: File already exists!")
        else:
            print("Copying %s to %s" % (p, dest_path))
            copyfile(p, dest_path)

    return 0


if __name__ == "__main__":
    # Change to BASH return codes:
    # 0   -> True
    # 1   -> False
    # > 1 -> That value
    val = main(parse_args())
    if val == 'False' or val == '0':
        exit(1)
    elif val == 'True' or val == '1':
        exit(0)
    else:
        exit(int(val))