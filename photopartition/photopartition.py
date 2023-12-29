from os import listdir, makedirs
from os.path import expanduser, join, isfile, basename, isdir, dirname
from typing import List
import datetime
import subprocess
from PIL import Image
from PIL.ExifTags import TAGS
import shutil

import filetype

input_dir = expanduser("~/Documents/personal/Pictures")
output_dir = expanduser("~/Documents/personal/Pictures_temp")


class DateNotFoundException(Exception):
    pass


def get_photo_partition_taken(filepath: str) -> int:
    """Gets the date taken for a photo through a shell."""
    cmd = "mdls '%s'" % filepath
    output = subprocess.check_output(cmd, shell=True)
    lines = output.decode("utf-8").split("\n")
    for l in lines:
        if "kMDItemContentCreationDate" in l:
            datetime_str = l.split("= ")[1]
            if not datetime_str:
                image = Image.open(items)
                exif = {
                    TAGS[k]: v
                    for k, v in image._getexif().items()
                    if k in TAGS
                }
                datetime_str = exif['DateTimeOriginal']
            date = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S +0000")
            return date.year
    raise DateNotFoundException("No EXIF date taken found for file %s" % filepath)


def _destination_path(filepath: str) -> str:
    return f"{output_dir}/{get_photo_partition_taken(filepath=filepath)}/{basename(filepath)}"


def _get_file_name_from_folder(directory_name: str) -> List:
    return [join(directory_name, file) for file in listdir(directory_name) if
            isfile(join(directory_name, file))]


def _get_media_file_path(file_names: List) -> List:
    return [item for item in file_names if
            filetype.guess(item) is not None and filetype.guess(item).mime.split('/')[0] in ['image', 'audio', 'video']]


media = _get_media_file_path(file_names=_get_file_name_from_folder(directory_name=input_dir))

count = 0
for items in media:
    if not isdir(dirname(_destination_path(filepath=items))):
        makedirs(dirname(_destination_path(filepath=items)))
    shutil.copy2(items, _destination_path(filepath=items))
    count += 1
print(f"Number of files copied: {count}")
